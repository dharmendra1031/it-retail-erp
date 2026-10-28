import base64
import binascii
import hashlib
import hmac
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from django.core.exceptions import ImproperlyConfigured


def _master_key():
    try:
        key = base64.b64decode(os.getenv("PRODUCT_LICENSE_SECRET", ""), validate=True)
    except (ValueError, binascii.Error) as error:
        raise ImproperlyConfigured(
            "PRODUCT_LICENSE_SECRET must be a base64-encoded 32-byte key."
        ) from error
    if len(key) != 32:
        raise ImproperlyConfigured("PRODUCT_LICENSE_SECRET must be a base64-encoded 32-byte key.")
    return key


def _derive(purpose):
    return hmac.new(_master_key(), purpose.encode("utf-8"), hashlib.sha256).digest()


def fingerprint(license_key):
    normalized = license_key.strip().translate(
        str.maketrans("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    ).encode("utf-8")
    return hmac.new(_derive("product-license-fingerprint-v1"), normalized,
                    hashlib.sha256).digest()


def encrypt(license_key):
    nonce = os.urandom(12)
    encrypted = AESGCM(_derive("product-license-encryption-v1")).encrypt(
        nonce, license_key.strip().encode("utf-8"), None
    )
    return nonce + encrypted


def decrypt(encrypted):
    data = bytes(encrypted)
    if len(data) < 28:
        raise ValueError("Invalid encrypted license key.")
    return AESGCM(_derive("product-license-encryption-v1")).decrypt(
        data[:12], data[12:], None
    ).decode("utf-8")
