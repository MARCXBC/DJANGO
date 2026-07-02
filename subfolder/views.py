from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.conf import settings

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from django.core.mail import send_mail, EmailMultiAlternatives
import random

from .models import User
from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer

@api_view(['POST'])
def hello(request):
    email = request.data.get('email')
    password = request.data.get('password')

    users = [
        {'email': 'a@b.com', 'password': '12345'},
        {'email': 'c@d.com', 'password': 'pass123'},
        {'email': 'e@f.com', 'password': 'pass456'},
    ]

    for user in users:
        if user['email'] == email and user['password'] == password:
            return Response({'message': 'Authentication successful.'})
    
    return Response({'error': 'Invalid credentials.'})
        
@api_view(['POST'])
def mail_user(request):
    first_name = request.data.get("first_name")
    email = request.data.get("email")

    otp = ""
    for i in range(5):
        otp += str(random.randrange(0, 9))
    print(otp)

    html_content = render_to_string("email/verification.html", {
        "first_name": first_name,
        "otp": otp,
    })

    striphtml = strip_tags(html_content)

    mail = EmailMultiAlternatives(
        subject="Your OTP Verification code",
        body=striphtml,
        from_email="marcusatoyebirash@gmail.com",
        to=[email]
    )

    mail.attach_alternative(html_content,"text/html")
    mail.send()

    return Response({"message": "Email sent successfully"})

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        otp = ""
        for i in range(6):
            otp += str(random.randrange(0, 10))

        user.otp = otp
        user.is_active = False
        user.save()

        html_content = render_to_string(
            "email/verification.html", {
                "first_name": user.first_name,
                "otp": otp
            }
        )

        plain_text = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject="Verify Your Email Here With Ezitech042",
            body=plain_text,
            from_email= settings.EMAIL_HOST_USER,
            to=[user.email]
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

        return Response({"message": "Registration successful. Check your email for the OTP please with marcustheking", "user_id": user.id}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_user(request):
    email = request.data.get("email")
    otp = request.data.get("otp")

    user = User.objects.filter(email=email).first()

    if user is None:
         return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if user.otp != otp :
         return Response({"message": "invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
    
    user.is_verified = True
    user.is_active = True
    user.otp = ""
    user.save()

    return Response({"message": "Signup successful"}, status=status.HTTP_200_OK)

# FIX 1: Linked the CSRF Exemption bypass rule to your lecturer's real login view endpoint function
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
     email = request.data.get("email")
     password = request.data.get("password")

     user = authenticate(
          email=email,
          password=password
     )   

     if user is None:
         return Response({"message": "Invalid Email or Password"}, status=status.HTTP_400_BAD_REQUEST)
    
     if not user.is_verified:
         return Response({"message": "Verify your email first"}, status=status.HTTP_400_BAD_REQUEST)
     
     refresh = RefreshToken.for_user(user)

     return Response({
          "refresh": str(refresh),
          "access": str(refresh.access_token)
     })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
         
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    serializer = UserSerializer(
        instance = request.user,
        data = request.data,
        partial = True
    )

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User update"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, id):
    try:
         user = User.objects.get(id=id)
         user.is_deleted = True
         user.is_active = False
         user.save()
         return Response({"message":"User deleted"})
    except User.DoesNotExist:
         return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def reset_password(request):
     serializer = ChangePasswordSerializer(data=request.data)

     if serializer.is_valid():
          old_password = serializer.validated_data["old_password"]
          new_password = serializer.validated_data["new_password"]

          if not request.user.check_password(old_password):
               return Response({"message": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
          
          request.user.set_password(new_password)
          request.user.save()
          return Response({"message": "Password changed successfully"})
     
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# FIX 2: Eradicated the unclosed, broken fallback layout block from your view file footer
