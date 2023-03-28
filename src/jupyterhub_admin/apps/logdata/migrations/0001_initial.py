# Generated by Django 4.1.7 on 2023-03-13 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ParsedAccessLog",
            fields=[
                (
                    "filename",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("status", models.CharField(max_length=255)),
                ("last_line_added", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="LoginLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tenant", models.CharField(max_length=255)),
                ("user", models.CharField(max_length=255)),
                ("date", models.DateField()),
                ("time", models.TimeField()),
            ],
            options={
                "unique_together": {("tenant", "user", "date", "time")},
            },
        ),
        migrations.CreateModel(
            name="FileLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tenant", models.CharField(max_length=255)),
                ("user", models.CharField(max_length=255)),
                ("action", models.CharField(max_length=255)),
                ("filepath", models.TextField()),
                ("filename", models.CharField(max_length=255)),
                ("date", models.DateField()),
                ("time", models.TimeField()),
                ("raw_filepath", models.TextField()),
            ],
            options={
                "unique_together": {
                    (
                        "tenant",
                        "user",
                        "action",
                        "filepath",
                        "filename",
                        "date",
                        "time",
                        "raw_filepath",
                    )
                },
            },
        ),
    ]