namespace ITRetailERP.Web.Security;

public static class PermissionCatalog
{
    private static readonly Dictionary<string, string[]> Actions = new()
    {
        ["companies"] = ["view", "add", "edit", "delete"],
        ["roles"] = ["view", "add", "edit", "delete"],
        ["users"] = ["view", "add", "edit", "delete"],
        ["branches"] = ["view", "add", "edit", "delete"],
        ["warehouses"] = ["view", "add", "edit", "delete"],
        ["quotations"] = ["view", "add", "edit", "delete", "print", "export", "approve", "cancel", "post", "reverse"],
        ["sales"] = ["view", "add", "edit", "delete", "print", "export", "approve", "cancel", "post", "reverse"],
        ["purchases"] = ["view", "add", "edit", "delete", "print", "export", "approve", "cancel", "post", "reverse"],
        ["inventory"] = ["view", "add", "edit", "delete", "print", "export", "approve", "cancel", "post", "reverse"],
        ["services"] = ["view", "add", "edit", "delete", "print", "export", "approve", "cancel", "post", "reverse"],
        ["reports"] = ["view", "print", "export"],
    };

    public static IReadOnlyList<PermissionItem> Items { get; } = Actions
        .SelectMany(module => module.Value.Select(action =>
            new PermissionItem($"{module.Key}.{action}", $"{ToTitle(module.Key)} - {ToTitle(action)}")))
        .ToArray();

    public static IReadOnlySet<string> Codes { get; } =
        Items.Select(item => item.Code).ToHashSet(StringComparer.Ordinal);

    private static string ToTitle(string name) =>
        char.ToUpperInvariant(name[0]) + name[1..];
}

public sealed record PermissionItem(string Code, string Name);
