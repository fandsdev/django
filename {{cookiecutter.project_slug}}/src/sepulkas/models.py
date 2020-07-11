from app.models import TimestampedModel, models


class Sepulka(TimestampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
