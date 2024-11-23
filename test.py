import os
import django
import random
import logging

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SIMS.settings')
django.setup()

from manageSystem import models

# 配置日志
logging.basicConfig(filename='output.log', level=logging.INFO, format='%(message)s')


def biased_random():
    if random.random() < 0.8:
        return random.randint(61, 100)
    else:
        return random.randint(0, 60)


def insert_random_sc_record(students=None, courses=None, list=None):
    s = len(students)
    c = len(courses)
    student = students[random.randint(0, s - 1)]
    course = courses[random.randint(0, c - 1)]
    grade = biased_random()
    if (student.Sno, course.Cno) in list:
        return


    # 检查课程是否有先修课
    if course.Cpno:
        pre_course = course.Cpno
        pre_grade = biased_random()
        try:
            sc_record = models.SC.objects.get(Sno=student.Sno, Cno=pre_course)
            print(f"Student {student.Sno} has already taken course {pre_course}")
        except models.SC.DoesNotExist:
            models.SC.objects.create(student=student, course=models.Course.objects.get(Cno=pre_course), Grade=pre_grade,
                                     Cno=pre_course, Sno=student.Sno)
            list.append((student.Sno, pre_course))
            print(f"Student {student.Sno} has taken course {pre_course} with grade {pre_grade}")

    models.SC.objects.create(student=student, course=course, Grade=grade,
                             Cno=course.Cno, Sno=student.Sno)
    list.append((student.Sno, course.Cno))
    print(f"Student {student.Sno} has taken course {course.Cno} with grade {grade}")


def add_sc_record(sno, cno, grade):
    try:
        student = models.Student.objects.get(Sno=sno)
        course = models.Course.objects.get(Cno=cno)
        sc_record = models.SC.objects.create(student=student, course=course, Grade=grade)



    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    # students = models.Student.objects.all()
    # courses = models.Course.objects.all()
    # list = []
    # for i in range(5000):
    #     insert_random_sc_record(students, courses, list)

