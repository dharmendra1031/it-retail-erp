from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DocumentSequence",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("series", models.CharField(max_length=20)),
                ("fiscal_year", models.PositiveSmallIntegerField()),
                ("branch_id", models.BigIntegerField(default=0)),
                ("last_number", models.BigIntegerField(default=0)),
            ],
        ),
        migrations.AddConstraint(
            model_name="documentsequence",
            constraint=models.UniqueConstraint(
                fields=("series", "fiscal_year", "branch_id"),
                name="uq_document_sequence_scope",
            ),
        ),
    ]
