from django.urls import path
from .views import UploadDatasetView, SummaryView, HistoryView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('upload/', UploadDatasetView.as_view(), name='upload_dataset'),
    path('summary/<int:dataset_id>/', SummaryView.as_view(), name='dataset_summary'),
    path('history/', HistoryView.as_view(), name='history'),
]
