from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime, timedelta
import jwt

from .serializers import UserSerializer
from .models import User


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CurrentUserRetrieveView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, key='secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class UserLoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload = {
            'id': user.id,
            'exp': int((datetime.now() + timedelta(minutes=60)).timestamp()),
            'iat': int(datetime.now().timestamp()),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "jwt": token
        }

        return response
    

class UserLogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "success"
        }
        return response
