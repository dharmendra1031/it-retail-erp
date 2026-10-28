"""Verify Product schema parity on disposable Django and ASP.NET SQL Server databases."""

import os

import pyodbc


SCHEMAS = (
    (
        "erp_integration",
        "catalog_product",
        {
            "id": ("bigint", None, None, None, False),
            "sku": ("nvarchar", 40, None, None, False),
            "barcode": ("nvarchar", 64, None, None, True),
            "name_en": ("nvarchar", 200, None, None, False),
            "name_ar": ("nvarchar", 200, None, None, False),
            "description_en": ("nvarchar", 1000, None, None, False),
            "description_ar": ("nvarchar", 1000, None, None, False),
            "category_id": ("bigint", None, None, None, False),
            "brand_id": ("bigint", None, None, None, True),
            "unit_id": ("bigint", None, None, None, False),
            "cost_price": ("decimal", None, 18, 3, False),
            "base_price": ("decimal", None, 18, 3, False),
            "min_price": ("decimal", None, 18, 3, False),
            "reorder_level": ("decimal", None, 18, 6, False),
        },
        {"category_id": "catalog_category", "brand_id": "catalog_brand", "unit_id": "catalog_unit"},
    ),
    (
        "erp_net_ci",
        "Products",
        {
            "Id": ("bigint", None, None, None, False),
            "Sku": ("nvarchar", 40, None, None, False),
            "Barcode": ("nvarchar", 64, None, None, True),
            "NameEn": ("nvarchar", 200, None, None, False),
            "NameAr": ("nvarchar", 200, None, None, False),
            "DescriptionEn": ("nvarchar", 1000, None, None, False),
            "DescriptionAr": ("nvarchar", 1000, None, None, False),
            "CategoryId": ("bigint", None, None, None, False),
            "BrandId": ("bigint", None, None, None, True),
            "UnitId": ("bigint", None, None, None, False),
            "CostPrice": ("decimal", None, 18, 3, False),
            "BasePrice": ("decimal", None, 18, 3, False),
            "MinPrice": ("decimal", None, 18, 3, False),
            "ReorderLevel": ("decimal", None, 18, 6, False),
        },
        {"CategoryId": "Categories", "BrandId": "Brands", "UnitId": "Units"},
    ),
)


def verify(database, table, expected_columns, expected_fks):
    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER=127.0.0.1,1433;DATABASE={database};UID=sa;"
        f"PWD={os.environ['DB_PASSWORD']};Encrypt=yes;TrustServerCertificate=yes;"
    )
    with pyodbc.connect(connection_string) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT c.name, t.name, c.max_length, c.precision, c.scale,
                   c.is_nullable, c.is_identity
            FROM sys.columns AS c
            JOIN sys.types AS t ON c.user_type_id = t.user_type_id
            WHERE c.object_id = OBJECT_ID(?)
            """,
            table,
        )
        columns = {row[0].lower(): row[1:] for row in cursor.fetchall()}
        for name, (kind, length, precision, scale, nullable) in expected_columns.items():
            actual = columns.get(name.lower())
            assert actual is not None, f"{database}.{table}.{name} is missing"
            type_matches = actual[0].lower() == kind or (
                kind == "decimal" and actual[0].lower() == "numeric"
            )
            assert type_matches, f"{database}.{name}: expected {kind}, got {actual[0]}"
            if length is not None:
                assert actual[1] == length * 2, f"{database}.{name}: incorrect NVARCHAR length"
            if precision is not None:
                assert (actual[2], actual[3]) == (precision, scale), (
                    f"{database}.{name}: expected DECIMAL({precision},{scale}), got {actual[2:4]}"
                )
            assert bool(actual[4]) == nullable, f"{database}.{name}: nullable mismatch"
        id_column = "Id" if table == "Products" else "id"
        assert columns[id_column.lower()][5] == 1, f"{database}: Product ID is not IDENTITY"

        cursor.execute(
            """
            SELECT i.name, i.is_unique, i.filter_definition, c.name, ic.key_ordinal
            FROM sys.indexes AS i
            JOIN sys.index_columns AS ic
                ON ic.object_id = i.object_id AND ic.index_id = i.index_id
            JOIN sys.columns AS c
                ON c.object_id = ic.object_id AND c.column_id = ic.column_id
            WHERE i.object_id = OBJECT_ID(?) AND ic.key_ordinal > 0
            """,
            table,
        )
        indexes = {}
        for name, unique, filter_definition, column, ordinal in cursor.fetchall():
            entry = indexes.setdefault(name, {"unique": bool(unique), "filter": filter_definition, "keys": []})
            entry["keys"].append((ordinal, column.lower()))

        for field in ("sku", "barcode"):
            matches = [
                index for index in indexes.values()
                if index["unique"] and sorted(index["keys"]) == [(1, field)]
            ]
            assert matches, f"{database}.{table}: missing unique {field} index"
            if field == "barcode":
                assert any(
                    index["filter"] and "is not null" in index["filter"].lower()
                    for index in matches
                ), f"{database}.{table}: nullable barcode must use filtered unique index"

        cursor.execute(
            """
            SELECT pc.name, OBJECT_NAME(fkc.referenced_object_id),
                   fk.delete_referential_action_desc
            FROM sys.foreign_keys AS fk
            JOIN sys.foreign_key_columns AS fkc ON fk.object_id = fkc.constraint_object_id
            JOIN sys.columns AS pc
                ON pc.object_id = fk.parent_object_id AND pc.column_id = fkc.parent_column_id
            WHERE fk.parent_object_id = OBJECT_ID(?)
            """,
            table,
        )
        foreign_keys = {name.lower(): (parent.lower(), action) for name, parent, action in cursor.fetchall()}
        for column, referenced in expected_fks.items():
            assert foreign_keys.get(column.lower()) == (referenced.lower(), "NO_ACTION"), (
                f"{database}.{table}.{column}: missing protected FK to {referenced}"
            )
        print(f"PASS {database}.{table}: BIGINT IDENTITY, Unicode, DECIMAL, nullable barcode, unique indexes, FKs")


if __name__ == "__main__":
    if os.getenv("GITHUB_ACTIONS") != "true" or os.getenv("DB_NAME") != "erp_integration":
        raise SystemExit("Product schema verification runs only against disposable CI SQL Server.")
    for schema in SCHEMAS:
        verify(*schema)
