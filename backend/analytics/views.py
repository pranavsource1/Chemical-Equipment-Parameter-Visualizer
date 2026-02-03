from rest_framework import views, status, generics, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Avg, Min, Max, Count
from django.contrib.auth.models import User
import pandas as pd
from .models import Dataset, EquipmentData
from .serializers import DatasetSerializer, EquipmentDataSerializer

import re

class RegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            if not username or not password:
                return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create_user(username=username, password=password)
            return Response({'success': 'User created'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UploadDatasetView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_serializer = DatasetSerializer(data=request.data)
        if file_serializer.is_valid():
            # Save with user
            dataset = file_serializer.save(user=request.user)
            
            try:
                # Read CSV
                df = pd.read_csv(dataset.file.path)
                
                equipment_list = []
                
                def extract_number(val):
                    if pd.isna(val):
                        return None
                    # Convert to string and find the first integer or float
                    match = re.search(r"[-+]?\d*\.\d+|\d+", str(val))
                    if match:
                        return float(match.group())
                    return None

                for _, row in df.iterrows():
                    # Handle potential column name variations
                    name = row.get('Equipment Name') or row.get('Equipment_Name') or row.get('name') or row.get('Equipment')
                    etype = row.get('Type') or row.get('Equipment Type') or row.get('type')
                    # simple validation
                    if not name: 
                        continue 

                    equipment_list.append(EquipmentData(
                        dataset=dataset,
                        equipment_name=str(name),
                        equipment_type=str(etype),
                        flowrate=extract_number(row.get('Flowrate')),
                        pressure=extract_number(row.get('Pressure')),
                        temperature=extract_number(row.get('Temperature'))
                    ))
                
                EquipmentData.objects.bulk_create(equipment_list)
                
                # Maintain history limit (Last 5 per user)
                datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
                if datasets.count() > 5:
                    for d in datasets[5:]:
                        d.delete()

                return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                dataset.delete()
                return Response({'error': f'Failed to parse CSV: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SummaryView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, dataset_id):
        try:
            # Filter by user
            dataset = Dataset.objects.get(id=dataset_id, user=request.user)
            data = EquipmentData.objects.filter(dataset=dataset)
            
            stats = {
                'total_count': data.count(),
                'flowrate': data.aggregate(avg=Avg('flowrate'), min=Min('flowrate'), max=Max('flowrate')),
                'pressure': data.aggregate(avg=Avg('pressure'), min=Min('pressure'), max=Max('pressure')),
                'temperature': data.aggregate(avg=Avg('temperature'), min=Min('temperature'), max=Max('temperature')),
                'type_distribution': list(data.values('equipment_type').annotate(count=Count('id')))
            }
            
            raw_data = EquipmentDataSerializer(data, many=True).data
            
            return Response({
                'dataset_id': dataset.id,
                'uploaded_at': dataset.uploaded_at,
                'summary': stats,
                'data': raw_data
            }, status=status.HTTP_200_OK)
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, dataset_id):
        try:
            # Filter by user
            dataset = Dataset.objects.get(id=dataset_id, user=request.user)
            dataset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)

class HistoryView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DatasetSerializer
    
    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user).order_by('-uploaded_at')[:5]
