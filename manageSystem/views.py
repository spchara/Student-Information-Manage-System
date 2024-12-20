from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from manageSystem import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from django.http import HttpRequest
from django.db import IntegrityError

from django.conf import settings
from django.http import HttpResponse


def change_setting(request):
    print("change_setting view called")  # 调试语句
    if request.method == 'POST':
        mode = request.POST.get('mode', '')
        print("Mode:" + mode)
        if mode == 'RESTRICT':
            settings.ON_DELETE_BEHAVIOR = 'CASCADE'
            query_params = urlencode({'mode': 'CASCADE', 'status': 'C'})
        else:
            settings.ON_DELETE_BEHAVIOR = 'RESTRICT'
            query_params = urlencode({'mode': 'RESTRICT', 'status': 'C'})

        return HttpResponseRedirect(f"{reverse('delete')}?{query_params}")

# Create your views here.

def index(request):
    return render(request, 'index.html')


from django.core.paginator import Paginator


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

    paginator = Paginator(students, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student-table.html', {'page_obj': page_obj, 'message': message})


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
            filters['Cno__icontains'] = course_id
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


def sc_table(request):
    message = ''
    sc_list = models.SC.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        student_name = request.POST.get('student_name', '').strip()
        course_name = request.POST.get('course_name', '').strip()
        course_id = request.POST.get('course_id', '').strip()
        min_grade = request.POST.get('min_grade', '0').strip()
        max_grade = request.POST.get('max_grade', '100').strip()

        filters = {}
        if student_id:
            filters['Sno__contains'] = student_id
        if student_name:
            filters['student__Sname__contains'] = student_name
        if course_name:
            filters['course__Cname__contains'] = course_name
        if course_id:
            filters['course__Cno__icontains'] = course_id
        if min_grade:
            filters['Grade__gte'] = min_grade
        if max_grade:
            filters['Grade__lte'] = max_grade

        sc_list = models.SC.objects.filter(**filters)
        if not sc_list.exists():
            message = 'No students found with the given criteria: '
            if student_id:
                message += f'ID contains "{student_id}", '
            if student_name:
                message += f'name contains "{student_name}", '
            if course_name:
                message += f'course name contains "{course_name}", '
            if course_id:
                message += f'course ID contains "{course_id}", '
            if min_grade:
                message += f'grade >= "{min_grade}", '
            if max_grade:
                message += f'grade <= "{max_grade}".'
            message = message.rstrip(', ')
        else:
            message = f'{sc_list.count()} students found with the given criteria: '
            if student_id:
                message += f'ID contains "{student_id}", '
            if student_name:
                message += f'name contains "{student_name}", '
            if course_name:
                message += f'course name contains "{course_name}", '
            if course_id:
                message += f'course ID contains "{course_id}", '
            if min_grade:
                message += f'grade >= "{min_grade}", '
            if max_grade:
                message += f'grade <= "{max_grade}".'
            message = message.rstrip(', ')

    paginator = Paginator(sc_list, 100)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sc-table.html', {'page_obj': page_obj, 'message': message})


def delete(request):
    print(settings.ON_DELETE_BEHAVIOR)
    message = ''
    table = 'student'
    mode = settings.ON_DELETE_BEHAVIOR
    if request.method == 'GET':
        table = request.GET.get('table', '')
        status = request.GET.get('status', '')
        if request.GET.get('mode', '') != '':
            mode = request.GET.get('mode', '')
        if status == 'F':
            message = 'Deleted successfully.'
        elif status == 'U':
            message = 'Updated successfully.'
        elif status == 'C':
            message = 'Successfully change delete mode.'
        print("mode:"+mode)
        return render(request, 'delete.html', {'message': message, 'table': table, 'mode': mode})

    if request.method == 'POST':
        table = request.POST.get('table', '')
        d = request.POST.get('delete', '')
        if table == 'student':
            student_id = request.POST.get('student_id', '').strip()
            if student_id:
                student = models.Student.objects.filter(Sno=student_id)
                if student.exists():
                    print("delete:" + d)
                    if d == "True":
                        try:
                            student.delete()
                            query_params = urlencode({'table': table, 'status': 'F'})
                            return HttpResponseRedirect(f"{reverse('delete')}?{query_params}")
                        except IntegrityError:
                            message = 'Cannot delete student because it is referenced by other records.'
                    else:
                        return render(request, 'delete.html', {'message': message, 'table': table, 'students': student})


                else:
                    message = f'No student found with ID: "{student_id}".'
            else:
                message = 'Please enter a student ID.'

        elif table == 'course':
            course_id = request.POST.get('course_id', '').strip()
            if course_id:
                course = models.Course.objects.filter(Cno=course_id)
                if course.exists():

                    if d == "False":
                        return render(request, 'delete.html', {'message': message, 'table': table, 'courses': course})
                    else:
                        try:
                            course.delete()
                            query_params = urlencode({'table': table, 'status': 'F'})
                            return HttpResponseRedirect(f"{reverse('delete')}?{query_params}")
                        except IntegrityError:
                            message = 'Cannot delete course because it is referenced by other records.'

                else:
                    message = f'No course found with ID: "{course_id}".'
            else:
                message = 'Please enter a course ID.'
        elif table == 'sc':
            student_id = request.POST.get('student_id', '').strip()
            course_id = request.POST.get('course_id', '').strip()
            if student_id and course_id:
                sc = models.SC.objects.filter(Sno=student_id, Cno=course_id)
                if sc.exists():

                    if d == "False":
                        return render(request, 'delete.html', {'message': message, 'table': table, 'scs': sc})
                    else:
                        try:
                            sc.delete()
                            query_params = urlencode({'table': table, 'status': 'F'})
                            return HttpResponseRedirect(f"{reverse('delete')}?{query_params}")
                        except IntegrityError:
                            message = 'Cannot delete SC record because it is referenced by other records.'

                else:
                    message = f'No sc record found with student ID: "{student_id}" and course ID: "{course_id}".'
            else:
                message = 'Please enter student ID and course ID.'

    return render(request, 'delete.html', {'message': message, 'table': table,'mode':mode})


def update(request):
    table = 'student'
    message = ''
    if request.method == "POST":
        table = request.POST.get('table', '')
        u = request.POST.get('update', '')
        if table == 'student':
            student_id = request.POST.get('student_id', '').strip()
            if student_id:
                student = models.Student.objects.filter(Sno=student_id)
                if student.exists():
                    student = student.first()

                    if u == "True":
                        student.Sname = request.POST.get('student_name', '').strip()
                        student.Ssex = request.POST.get('student_gender', '').strip()
                        student.Sage = request.POST.get('student_age', '').strip()
                        student.Sdept = request.POST.get('student_department', '').strip()

                        try:
                            student.full_clean()
                            student.save()
                            query_params = urlencode({'table': table, 'status': 'U'})
                            return HttpResponseRedirect(f"{reverse('delete')}?{query_params}")
                        except Exception as e:
                            message = str(e)

                    else:
                        return render(request, 'update.html', {'table': table, 'student': student, 'message': message})
        elif table == 'course':
            course_id = request.POST.get('course_id', '')
            if course_id:
                course = models.Course.objects.filter(Cno=course_id)
                if course.exists():
                    course = course.first()
                    if u == "True":

                        course.Cname = request.POST.get('course_name', '').strip()
                        course.Chours = int(request.POST.get('course_hours', ''))
                        course.Ccredit = float(request.POST.get('course_credit', '').strip())
                        course.Cpno = request.POST.get('pre_course_id', '').strip()
                        course.Cpno_fk = models.Course.objects.filter(Cno=course.Cpno).first()
                        if course.Cpno and not models.Course.objects.filter(Cno=course.Cpno).exists():
                            message = 'Invalid pre-course ID.'
                        else:
                            try:
                                course.full_clean()
                                course.save()
                                query_params = urlencode({'table': table, 'status': 'U'})
                                return HttpResponseRedirect(f"{reverse('delete')}?{query_params}")
                            except Exception as e:
                                message = str(e)

                    else:
                        print(course)
                        return render(request, 'update.html', {'table': table, 'course': course, 'message': message})
        else:
            student_id = request.POST.get('student_id', '').strip()
            course_id = request.POST.get('course_id', '').strip()
            if student_id and course_id:
                sc = models.SC.objects.filter(Sno=student_id, Cno=course_id)
                if sc.exists():
                    sc = sc.first()
                    if u == "True":
                        sc.Grade = int(request.POST.get('new_grade', ''))
                        try:
                            sc.full_clean()
                            sc.save()
                            query_params = urlencode({'table': table, 'status': 'U'})
                            return HttpResponseRedirect(f"{reverse('delete')}?{query_params}")
                        except Exception as e:
                            message = str(e)
                    else:
                        return render(request, 'update.html', {'table': table, 'sc': sc, 'message': message})

    return render(request, 'update.html', {'table': table, 'message': message})


def insert(request):
    table = 'student'
    message = ''
    if request.method == 'GET':
        table = request.GET.get('table', '')
        status = request.GET.get('status', '')
        if status == 'I':
            message = 'Successfully insert.'

        return render(request, 'insert.html', {'message': message, 'table': table})

    if request.method == "POST":
        table = request.POST.get('table', '')
        if table == 'student':
            student_id = request.POST.get('student_id', '').strip()
            student_name = request.POST.get('student_name', '').strip()
            student_gender = request.POST.get('student_gender', '').strip()
            student_age = request.POST.get('student_age', '').strip()
            student_department = request.POST.get('student_department', '').strip()
            print("id:" + student_id)
            print("name:" + student_name)
            print("gender:" + student_gender)
            print("age:" + student_age)
            print("department:" + student_department)
            try:
                models.Student.objects.create(Sno=student_id, Sname=student_name, Ssex=student_gender,
                                              Sage=int(student_age), Sdept=student_department)
                query_params = urlencode({'table': table, 'status': 'I'})
                return HttpResponseRedirect(f"{reverse('insert')}?{query_params}")

            except Exception as e:
                message = str(e)

        elif table == 'course':
            course_name = request.POST.get('course_name', '').strip()
            course_hours = request.POST.get('course_hours', '').strip()
            course_credit = request.POST.get('course_credit', '').strip()
            pre_course_id = request.POST.get('pre_course_id', '').strip()
            print("name:" + course_name)
            print("hours:" + course_hours)
            print("credit:" + course_credit)
            print("pre_course_id:" + pre_course_id)
            if pre_course_id and not models.Course.objects.filter(Cno=pre_course_id).exists():
                message = '先修课程编号不合法'
            elif (not pre_course_id.startswith('C') or not pre_course_id[1:].isdigit() or len(
                    pre_course_id) != 4) and pre_course_id:
                message = '先修课程编号不合法'
            else:
                try:
                    total_courses = models.Course.objects.count()
                    course_id = 'C' + f"{total_courses + 1:03}"
                    print(course_id)
                    models.Course.objects.create(Cno=course_id, Cname=course_name, Chours=int(course_hours),
                                                 Ccredit=float(course_credit), Cpno=pre_course_id,Cpno_fk=models.Course.objects.filter(Cno=pre_course_id).first())
                    query_params = urlencode({'table': table, 'status': 'I'})
                    return HttpResponseRedirect(f"{reverse('insert')}?{query_params}")
                except Exception as e:
                    message = str(e)

        else:
            student_id = request.POST.get('new_student_id', '').strip()
            course_id = request.POST.get('new_course_id', '').strip()
            student = models.Student.objects.filter(Sno=student_id).first()
            course = models.Course.objects.filter(Cno=course_id).first()
            grade = request.POST.get('new_grade', '')
            print("student_id:" + student_id)
            print("course_id:" + course_id)
            print("grade:" + grade)
            # 如果这门课有先修，但是学生没有修先修课程，就不能选这门课
            if course and course.Cpno:
                pre_course = models.SC.objects.filter(Sno=student_id, Cno=course.Cpno)
                if not pre_course:
                    message = '先修课程未修'
            elif not student:
                message = '学生不存在'
            elif not course:
                message = '课程不存在'
            elif not grade.isdigit() or not 0 <= int(grade) <= 100:
                message = '成绩不合法'
            else:
                try:
                    models.SC.objects.create(student=student, course=course,
                                             Grade=int(grade),
                                             Cno=course_id, Sno=student_id)
                    query_params = urlencode({'table': table, 'status': 'I'})
                    return HttpResponseRedirect(f"{reverse('insert')}?{query_params}")
                except Exception as e:
                    message = str(e)

    return render(request, 'insert.html', {'table': table, 'message': message})
