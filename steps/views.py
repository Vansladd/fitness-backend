from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import StepRecord , Workouts
from .serializers import StepRecordSerializer, UserSerializer, WorkoutSerializer
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
from django.db.models import Sum, Avg, Count



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

        avg_steps_week = round(steps.filter(date__range=[start_date,datetime.today().date()]).aggregate(avg = Avg('steps'))['avg'],0)

        currentMonth = datetime.today().month

        avg_steps_month = round(steps.filter(date__month = currentMonth).aggregate(avg = Avg('steps'))['avg'],0)

        records = StepRecordSerializer(steps,many=True)

        totalCalories = round(sum([record["calories_burned"] for record in records.data]),0)

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
        avatar = request.data.get("avatar", user.profile.avatar)

        # Ensure both fields are provided
        if not username or not email:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username is taken by another user
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            return Response({"error": "Username is already taken by another user"}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's profile
        user.username = username
        user.email = email
        user.profile.avatar = avatar
        user.save()
        user.profile.save()

        # Return success response with a message
        return Response({"message": "Profile Updated"}, status=status.HTTP_200_OK)
    

class WorkoutLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        workouts = Workouts.objects.filter(user=request.user).order_by('-date')
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = WorkoutSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WorkoutAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        workouts = Workouts.objects.filter(user=user)

        # Optional filtering
        workout_type = request.query_params.get("workout_type")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if workout_type:
            workouts = workouts.filter(workout_type=workout_type)
        if start_date and end_date:
            workouts = workouts.filter(date__range=[start_date, end_date])

        analytics = workouts.aggregate(
            total_workouts=Count("id"),
            total_duration=Sum("duration_minutes"),
            total_calories=Sum("calories_burned"),
            avg_duration=Avg("duration_minutes"),
            avg_calories=Avg("calories_burned")
        )

        return Response(analytics, status=status.HTTP_200_OK)

            



        


