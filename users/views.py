from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User



class UserRegisterView(APIView):
    """
    post:
    Register a new user.

    Register a new user by providing a username and password. The user will be created with an inactive status initially.

    ### Request Body

    - `username`: String, required. The username for the new user account.
    - `password`: String, required. The password for the new user account.

    ### Responses

    - `201 Created`: Successfully created the user.
        - `id`: Integer. The unique ID of the newly created user.

    - `400 Bad Request`: The required fields were not provided in the request body or were invalid.
    """
    def post(self, request):
        # Check if required fields are provided
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'error': 'Missing username or password'}, status=400)

        # Create a new user
        user = User.objects.create_user(
            username=request.data['username'],
            password=request.data['password'],
            is_active=False,
        )
        return Response({'id': user.id}, status=201)
