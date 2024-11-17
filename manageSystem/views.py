from django.shortcuts import render, redirect
from manageSystem import models


# Create your views here.

def index(request):
    return render(request, 'index.html')
from django.shortcuts import render
from manageSystem import models

def student_table(request):
    message = ''
    students = models.Student.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        student_name = request.POST.get('student_name', '').strip()
        student_gender = request.POST.get('student_gender', '').strip()
        student_department = request.POST.get('student_department', '').strip()
        age_min = request.POST.get('min_age', '19').strip()
        age_max = request.POST.get('max_age', '22').strip()

        filters = {}
        if student_id:
            filters['Sno__contains'] = student_id
        if student_name:
            filters['Sname__contains'] = student_name
        if student_gender:
            filters['Ssex'] = student_gender
        if student_department:
            filters['Sdept__contains'] = student_department
        if age_min and age_min != '19':
            filters['Sage__gte'] = age_min
        if age_max and age_max != '22':
            filters['Sage__lte'] = age_max

        students = models.Student.objects.filter(**filters)
        if not students.exists():
            message = 'No students found with the given criteria: '
            if student_id:
                message += f'ID contains "{student_id}", '
            if student_name:
                message += f'name contains "{student_name}", '
            if student_gender:
                message += f'gender is "{student_gender}", '
            if student_department:
                message += f'department contains "{student_department}", '
            if age_min and age_min != '19':
                message += f'age >= "{age_min}", '
            if age_max and age_max != '22':
                message += f'age <= "{age_max}".'
            message = message.rstrip(', ')
        else:
            message = f'{students.count()} students found with the given criteria: '
            if student_id:
                message += f'ID contains "{student_id}", '
            if student_name:
                message += f'name contains "{student_name}", '
            if student_gender:
                message += f'gender is "{student_gender}", '
            if student_department:
                message += f'department contains "{student_department}", '
            if age_min and age_min != '19':
                message += f'age >= "{age_min}", '
            if age_max and age_max != '22':
                message += f'age <= "{age_max}".'
            message = message.rstrip(', ')

    return render(request, 'student-table.html', {'students': students, 'message': message})


def course_table(request):
    message = ''
    courses = models.Course.objects.all()
    return render(request, 'course-table.html', {'courses': courses, 'message': message})