# update_cpno_fk.py

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SIMS.settings')
django.setup()

from manageSystem.models import Course

def update_cpno_fk():
    courses = Course.objects.all()
    for course in courses:
        if course.Cpno:
            try:
                related_course = Course.objects.get(Cno=course.Cpno)
                #print(type(related_course))
                course.Cpno_fk = related_course
                course.save()
                print(f'Successfully updated cpno_fk for course {course.Cno}')
            except Course.DoesNotExist:
                print(f'Related course {course.Cpno} does not exist for course {course.Cno}')

if __name__ == '__main__':
    update_cpno_fk()