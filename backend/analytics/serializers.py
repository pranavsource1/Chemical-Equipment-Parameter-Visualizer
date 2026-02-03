from rest_framework import serializers
from .models import Dataset, EquipmentData

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'file', 'uploaded_at']

class EquipmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentData
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']
