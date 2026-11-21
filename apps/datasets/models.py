from django.db import models


class AppDataset(models.Model):
    payload = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "application dataset"

    def __str__(self):
        return f"Dataset updated {self.updated_at:%Y-%m-%d %H:%M:%S}"
