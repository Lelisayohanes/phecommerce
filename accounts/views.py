from django.shortcuts import render
from rest_framework.generics import GenericAPIView,RetrieveAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
 
# Create your views here.
class UserRegistrationAPIView(GenericAPIView):
    """description"""
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request,*args,**kwargs):
        serializers = self.get_serializer(data = request.data)
        serializers.is_valid(raise_exception= True)
        user = serializers.save()
        token = RefreshToken.for_user(user)
        data = serializers.data
        data["tokens"] = {"refresh":str(token),
                          "access":str(token.access_token)}
        return Response(data,status=status.HTTP_201_CREATED)
    

class UserLoginAPIView(GenericAPIView):
    """description"""
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request,*args,**kwargs):
        serializers = self.get_serializer(data = request.data)
        serializers.is_valid(raise_exception= True)
        user = serializers.validated_data
        serializers = CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializers.data
        data["tokens"] = {"refresh":str(token),
                          "access":str(token.access_token)}
        return Response(data,status=status.HTTP_200_OK)


class UserLogoutAPIView(GenericAPIView):
    """description"""
    permission_classed = (IsAuthenticated,)

    def post(self, request,*args,**kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserInfoAPIView(RetrieveAPIView):
    """description"""
    permission_classed = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user