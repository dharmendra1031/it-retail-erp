import re

from django.db import connection, transaction
from django.db.models import F

from .models import DocumentSequence


def next_number(series: str, fiscal_year: int, branch_id: int = 0) -> int:
    series = series.strip().upper()
    if not re.fullmatch(r"[A-Z0-9_-]{1,20}", series):
        raise ValueError("Series must contain 1-20 uppercase letters, digits, _ or -.")
    if not 2000 <= fiscal_year <= 9999 or branch_id < 0:
        raise ValueError("Invalid fiscal year or branch ID.")

    with transaction.atomic():
        if connection.vendor == "microsoft":
            resource = f"erp:sequence:{series}:{fiscal_year}:{branch_id}"
            with connection.cursor() as cursor:
                cursor.execute(
                    "SET NOCOUNT ON; DECLARE @result INT; "
                    "EXEC @result = sp_getapplock @Resource = %s, "
                    "@LockMode = 'Exclusive', @LockOwner = 'Transaction', @LockTimeout = 10000; "
                    "SELECT @result", [resource],
                )
                if cursor.fetchone()[0] < 0:
                    raise RuntimeError("Unable to lock document number series.")

        counter, _ = DocumentSequence.objects.get_or_create(
            series=series,
            fiscal_year=fiscal_year,
            branch_id=branch_id,
        )
        DocumentSequence.objects.filter(pk=counter.pk).update(
            last_number=F("last_number") + 1
        )
        counter.refresh_from_db(fields=["last_number"])
        return counter.last_number
