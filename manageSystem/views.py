from django.shortcuts import render, redirect
from manageSystem import models


# Create your views here.

def index(request):
    return render(request, 'index.html')


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

    if request.method == 'POST':
        course_id = request.POST.get('course_id', '').strip()
        course_name = request.POST.get('course_name', '').strip()
        min_hours = request.POST.get('min_hours', '1').strip()
        max_hours = request.POST.get('max_hours', '99').strip()
        min_credit = request.POST.get('min_credit', '0.0').strip()
        max_credit = request.POST.get('max_credit', '10.0').strip()
        pre_course_filter = request.POST.get('pre_course_filter', '')

        filters = {}
        if course_id:
            filters['Cno__contains'] = course_id
        if course_name:
            filters['Cname__contains'] = course_name
        if min_hours and min_hours != '1':
            filters['Chours__gte'] = min_hours
        if max_hours and max_hours != '99':
            filters['Chours__lte'] = max_hours
        if min_credit and min_credit != '0.0':
            filters['Ccredit__gte'] = min_credit
        if max_credit and max_credit != '10.0':
            filters['Ccredit__lte'] = max_credit
        if pre_course_filter == '1':
            filters['Cpno__isnull'] = False
        elif pre_course_filter == '2':
            filters['Cpno__isnull'] = True

        courses = models.Course.objects.filter(**filters)
        if not courses.exists():
            message = 'No courses found with the given criteria: '
            if course_id:
                message += f'ID contains "{course_id}", '
            if course_name:
                message += f'name contains "{course_name}", '
            if min_hours and min_hours != '1':
                message += f'hours >= "{min_hours}", '
            if max_hours and max_hours != '99':
                message += f'hours <= "{max_hours}", '
            if min_credit and min_credit != '0.0':
                message += f'credit >= "{min_credit}", '
            if max_credit and max_credit != '10.0':
                message += f'credit <= "{max_credit}", '
            if pre_course_filter == '1':
                message += '有先修课程, '
            elif pre_course_filter == '2':
                message += '无先修课程, '
            message = message.rstrip(', ')
        else:
            message = f'{courses.count()} courses found with the given criteria: '
            if course_id:
                message += f'ID contains "{course_id}", '
            if course_name:
                message += f'name contains "{course_name}", '
            if min_hours and min_hours != '1':
                message += f'hours >= "{min_hours}", '
            if max_hours and max_hours != '99':
                message += f'hours <= "{max_hours}", '
            if min_credit and min_credit != '0.0':
                message += f'credit >= "{min_credit}", '
            if max_credit and max_credit != '10.0':
                message += f'credit <= "{max_credit}", '
            if pre_course_filter == '1':
                message += 'has pre-course, '
            elif pre_course_filter == '2':
                message += 'no pre-course, '
            message = message.rstrip(', ')

    return render(request, 'course-table.html', {'courses': courses, 'message': message})
