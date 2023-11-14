
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedImage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
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
            emotion = result[0]["dominant_emotion"]

            # Update the image with the detected emotion
            cv2.putText(image_data, emotion, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

             # Save the updated image in the media directory using Django's File class
            processed_image_path = os.path.join('media', image.name)
            processed_image_content = cv2.imencode('.jpg', image_data)[1].tostring()
            processed_image = ContentFile(processed_image_content)

            with default_storage.open(processed_image_path, 'wb') as destination:
                destination.write(processed_image.read())
            

            return Response({'result': emotion,'processed_image_path': processed_image_path}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
