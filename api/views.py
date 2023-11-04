from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import StudentForm
from django.contrib.auth import logout
from django.views import View
from django.core.paginator import Paginator
from .models import Student
from django.views.generic.list import ListView
from .models import Student
from django.views.decorators.cache import never_cache
from rest_framework import permissions
from rest_framework import filters
from rest_framework import generics
from django.db.models import F  
from .models import Student
from .serializers import StudentSerializer



def register(request):
    if request.user.is_authenticated:
        return redirect('student_list')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_list')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('student_list')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('student_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})





def logout_view(request):
    logout(request)
    return redirect('login')  


# @login_required
# def add_student(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST, request.FILES)
#         if form.is_valid():
#             student = form.save(commit=False)
#             student.user = request.user
#             student.save()
#             return redirect('student_list')
#     else:
#         form = StudentForm()
#     return render(request, 'add_student.html', {'form': form})



@login_required(login_url='login')
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user  # Assign the current user to the user field
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm(initial={'user': request.user.username})  # Pre-populate the user field with the current username
    return render(request, 'add_student.html', {'form': form})

@login_required(login_url='login')
def student_list(request):
    students = Student.objects.all()
    paginator = Paginator(students, 4)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    return render(request, 'student_list.html', {'students': students})



# http://localhost:8000/api/getstudents/?class=3
class StudentListAPI(generics.ListAPIView):
    serializer_class = StudentSerializer
    filter_backends = (filters.OrderingFilter,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retrieve the class filter from the query parameters
        class_filter = self.request.query_params.get('class')
        queryset = Student.objects.all()

        if class_filter:
            # Filter students by class
            queryset = queryset.filter(class_grade=class_filter)

        # Calculate total score using the Sum function
        queryset = queryset.annotate(
            total_score=(
                F('score1') + F('score2') + F('score3') + F('score4') + F('score5')
            )
        )

        # Order students by total score in descending order
        queryset = queryset.order_by('-total_score')

        return queryset
