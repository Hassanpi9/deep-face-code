# urls.py
from django.urls import path
from .views import ImageAnalysisAPIView

urlpatterns = [
    path('analyze-image/', ImageAnalysisAPIView.as_view(), name='analyze-image'),
]
