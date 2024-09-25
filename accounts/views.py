from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

class UserRegistrationAPIView(GenericAPIView):
    """
    Handles user registration.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.save()
        
        # Generate JWT token for the new user
        token = RefreshToken.for_user(user)
        data = serializers.data
        data["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token)
        }
        
        # Send welcome email
        self.send_welcome_email(user.email, user.username)
        
        return Response(data, status=status.HTTP_201_CREATED)

    def send_welcome_email(self, email, username):
        """
        Sends a welcome email to the user upon registration.
        """
        subject = "Welcome to Our Platform!"
        message = f"Hi {username},\n\nThank you for registering on our platform! We are excited to have you on board."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print(f"Error sending email: {str(e)}")


class UserLoginAPIView(GenericAPIView):
    """
    Handles user login and returns JWT tokens.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.validated_data
        serializers = CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializers.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)


class UserLogoutAPIView(GenericAPIView):
    """
    Handles user logout and token blacklist.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required for logout."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserInfoAPIView(RetrieveAPIView):
    """
    Retrieves the authenticated user's information.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user
