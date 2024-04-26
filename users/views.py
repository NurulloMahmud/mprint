from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User



class UserRegisterView(APIView):
    def post(self, request):
        user = User.objects.create_user(
            username=request.data['username'],
            password=request.data['password'],
            is_active=False,
        )
        return Response({'id': user.id})

