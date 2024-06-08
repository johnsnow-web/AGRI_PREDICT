# predictions/models.py

from django.db import models

class Prediction(models.Model):
    input_data = models.JSONField()
    rainfall_prediction = models.FloatField()
    advisory = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction at {self.created_at}"
