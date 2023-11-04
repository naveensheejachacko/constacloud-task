from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    total_score = serializers.IntegerField()  # Include the total_score field

    class Meta:
        model = Student
        fields = '__all__'
