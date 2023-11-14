
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageSerializer
import cv2
from deepface import DeepFace
import os

class ImageAnalysisAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            image = serializer.validated_data['image']

            # Perform analysis using DeepFace
            image_path = image.temporary_file_path()
            image_data = cv2.imread(image_path)
            result = DeepFace.analyze(image_data, actions=["emotion"])            

            return Response({'result': result}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
