from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DocumentSequence(models.Model):
    series = models.CharField(max_length=20)
    fiscal_year = models.PositiveSmallIntegerField()
    branch_id = models.BigIntegerField(default=0)
    last_number = models.BigIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("series", "fiscal_year", "branch_id"),
                name="uq_document_sequence_scope",
            )
        ]
