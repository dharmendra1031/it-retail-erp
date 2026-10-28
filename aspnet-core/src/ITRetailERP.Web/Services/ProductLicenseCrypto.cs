using System.Security.Cryptography;
using System.Text;

namespace ITRetailERP.Web.Services;

public sealed class ProductLicenseCrypto(IConfiguration configuration)
{
    private byte[] MasterKey()
    {
        var encoded = configuration["PRODUCT_LICENSE_SECRET"];
        byte[] key;
        try
        {
            key = Convert.FromBase64String(encoded ?? "");
        }
        catch (FormatException)
        {
            throw new InvalidOperationException("PRODUCT_LICENSE_SECRET must be a base64-encoded 32-byte key.");
        }
        if (key.Length != 32)
            throw new InvalidOperationException("PRODUCT_LICENSE_SECRET must be a base64-encoded 32-byte key.");
        return key;
    }

    private byte[] Derive(string purpose) =>
        HMACSHA256.HashData(MasterKey(), Encoding.UTF8.GetBytes(purpose));

    public byte[] Fingerprint(string licenseKey) =>
        HMACSHA256.HashData(Derive("product-license-fingerprint-v1"),
            Encoding.UTF8.GetBytes(new string(licenseKey.Trim().Select(c =>
                c is >= 'a' and <= 'z' ? (char)(c - 32) : c).ToArray())));

    public byte[] Encrypt(string licenseKey)
    {
        var nonce = RandomNumberGenerator.GetBytes(12);
        var plain = Encoding.UTF8.GetBytes(licenseKey.Trim());
        var cipher = new byte[plain.Length];
        var tag = new byte[16];
        using var aes = new AesGcm(Derive("product-license-encryption-v1"), 16);
        aes.Encrypt(nonce, plain, cipher, tag);
        return [.. nonce, .. cipher, .. tag];
    }

    public string Decrypt(byte[] encrypted)
    {
        if (encrypted.Length < 28)
            throw new CryptographicException("Invalid encrypted license key.");
        var plain = new byte[encrypted.Length - 28];
        using var aes = new AesGcm(Derive("product-license-encryption-v1"), 16);
        aes.Decrypt(encrypted.AsSpan(0, 12), encrypted.AsSpan(12, plain.Length),
            encrypted.AsSpan(encrypted.Length - 16), plain);
        return Encoding.UTF8.GetString(plain);
    }
}
