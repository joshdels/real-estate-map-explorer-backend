import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.datasets.geometry import sync_lot_geometries
from apps.datasets.models import AppDataset
from apps.datasets.serializers import validate_dataset_payload


class Command(BaseCommand):
    help = "Seed or replace the singleton dataset from an Open Lot Plans data.json file."

    def add_arguments(self, parser):
        parser.add_argument("path", type=Path)

    def handle(self, *args, **options):
        source = options["path"]
        if not source.is_file():
            raise CommandError(f"Dataset file not found: {source}")
        try:
            payload = validate_dataset_payload(json.loads(source.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise CommandError(f"Dataset file is not valid JSON: {error}") from error
        dataset = AppDataset.objects.order_by("pk").first()
        if dataset is None:
            AppDataset.objects.create(payload=payload)
        else:
            dataset.payload = payload
            dataset.save(update_fields=["payload", "updated_at"])
        summary = sync_lot_geometries(payload)
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded dataset from {source} "
                f"({summary['written']} lot geometries written, {summary['removed']} removed)"
            )
        )
