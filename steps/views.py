from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import StepRecord
from .serializers import StepRecordSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.db.models import Sum, Avg



class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                "message": "User registered successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )

class StepRecordViewSet(viewsets.ModelViewSet):
    serializer_class = StepRecordSerializer
    permission_classes = [IsAuthenticated]

    queryset = StepRecord.objects.none()

    def get_queryset(self):
        return StepRecord.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        user = self.request.user
        today = now().date()
        existing_record = StepRecord.objects.filter(user=user, date=today).first()

        if existing_record:
            # Update the existing record instead of creating a new one
            existing_record.steps = serializer.validated_data.get("steps", existing_record.steps)
            existing_record.weight = serializer.validated_data.get("weight", existing_record.weight)
            existing_record.save()
        else:
            # If no existing record, create a new one with today's date
            serializer.save(user=user, date=today)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.username  # Include username in response
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LeaderBoardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        currentMonth = datetime.today().month
        leaderboard = StepRecord.objects.filter(date__month = currentMonth).values("user__username").annotate(total_steps=Sum("steps")).order_by("-total_steps")[:10]
        return Response({leaderboard})
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        userserializer = UserSerializer(user)

        userdetails = userserializer.data

        steps = StepRecord.objects.filter(user = user)

        start_date = datetime.today().date() - timedelta(days=7)

        avg_steps_week = steps.filter(date__range=[start_date,datetime.today().date()]).aggregate(avg = Avg('steps'))['avg']

        currentMonth = datetime.today().month

        avg_steps_month = steps.filter(date__month = currentMonth).aggregate(avg = Avg('steps'))['avg']

        records = StepRecordSerializer(steps,many=True)

        totalCalories = sum([record["calories_burned"] for record in records.data])

        totalsteps = sum([record["steps"] for record in records.data])

        return Response({
            "user_details" : userdetails,
            "total_steps"  : totalsteps,
            "total_calories" : totalCalories,
            "Average_steps_week" : avg_steps_week,
            "Average_steps_month" : avg_steps_month,
        }
        )
    
    def put(self, request):
        user = request.user
        username = request.data.get("username")
        email = request.data.get("email")

        if not username or not email:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            user.username = username
            user.email = email
            user.save()
            return Response({"Profile Updated"},status=status.HTTP_200_OK)
        else:
            return Response({"error": "User Does Not Exist"}, status=status.HTTP_400_BAD_REQUEST)
            



        


