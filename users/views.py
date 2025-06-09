from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SecureCipherUser
from .serializers import SecureCipherUserSerializer

class RegisterUserView(APIView):
    def post(self, request):
        serializer = SecureCipherUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PingView(APIView):
    def get(self, request):
        return Response({"message": "DRF is working ✅"})
