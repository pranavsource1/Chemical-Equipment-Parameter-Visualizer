from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class Dataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='uploads/', validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Dataset {self.id} - {self.uploaded_at}"

class EquipmentData(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=255)
    flowrate = models.FloatField(null=True, blank=True)
    pressure = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.equipment_name
