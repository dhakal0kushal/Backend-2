import uuid

from django.db import models

from .asset import Asset


class ScanTracker(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING)
    total_scans = models.IntegerField()
    last_scanned = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Total: {self.total_scans}; {self.last_scanned}'
