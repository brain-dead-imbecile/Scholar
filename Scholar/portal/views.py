from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Classroom, PerformanceMonitoring, Message, Attendance
from django.contrib.auth.models import User
from django.db.models import Q

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'portal/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user, role=role)
            login(request, user)
            return redirect('dashboard')
    return render(request, 'portal/signup.html')

@login_required
def dashboard_view(request):
    profile = request.user.userprofile
    if profile.role == 'student':
        return redirect('student_dash')
    else:
        return redirect('teacher_dash')

@login_required
def student_dash(request):
    profile = request.user.userprofile
    courses = Classroom.objects.filter(section=profile.section)
    performances = PerformanceMonitoring.objects.filter(student=request.user)
    attendance = Attendance.objects.filter(student=request.user)
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'portal/student_dashboard.html', {
        'courses': courses,
        'performances': performances,
        'attendance': attendance,
        'messages': messages
    })

@login_required
def teacher_dash(request):
    classrooms = Classroom.objects.filter(teacher=request.user)
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'portal/teacher_dashboard.html', {
        'classrooms': classrooms,
        'messages': messages
    })

@login_required
def classroom_detail(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id, teacher=request.user)
    students = User.objects.filter(userprofile__section=classroom.section, userprofile__role='student')
    return render(request, 'portal/classroom_detail.html', {
        'classroom': classroom,
        'students': students
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        receiver = get_object_or_404(User, id=receiver_id)
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    return redirect('dashboard')

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        classroom_id = request.POST.get('classroom_id')
        student_id = request.POST.get('student_id')
        date = request.POST.get('date')
        status = request.POST.get('status')
        
        classroom = get_object_or_404(Classroom, id=classroom_id, teacher=request.user)
        student = get_object_or_404(User, id=student_id)
        
        Attendance.objects.update_or_create(
            student=student,
            classroom=classroom,
            date=date,
            defaults={'status': status}
        )
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    return redirect('dashboard')

@login_required
def add_grade(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        subject = request.POST.get('subject')
        grade = request.POST.get('grade')
        performance_type = request.POST.get('performance_type', 'others')
        remarks = request.POST.get('remarks', '')
        
        student = get_object_or_404(User, id=student_id)
        PerformanceMonitoring.objects.create(
            student=student,
            subject=subject,
            grade=grade,
            performance_type=performance_type,
            remarks=remarks
        )
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    return redirect('dashboard')

@login_required
def profile_update(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        student_id = request.POST.get('student_id')
        section = request.POST.get('section')
        
        # Split name for User fields
        names = name.split(' ', 1)
        request.user.first_name = names[0]
        if len(names) > 1:
            request.user.last_name = names[1]
        request.user.email = email
        request.user.save()
        
        profile = request.user.userprofile
        profile.student_id = student_id
        profile.section = section
        profile.save()
        
        return redirect('dashboard')
    return redirect('dashboard')

def logout_view(request):
    logout(request)
    return redirect('login')