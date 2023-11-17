
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageSerializer
import cv2
import numpy as np
from deepface import DeepFace
import os

class ImageAnalysisAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            image = serializer.validated_data['image']
            image_data = image.read()
            image_array = np.asarray(bytearray(image_data), dtype=np.uint8)
            image_cv2 = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            result = DeepFace.analyze(image_cv2, actions=["emotion"])       

            return Response({'result': result}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
