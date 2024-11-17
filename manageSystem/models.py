from django.db import models
from django.db.models import F, Q, CheckConstraint
from django.core.validators import MinValueValidator, MaxValueValidator


class Course(models.Model):
    Cno = models.CharField(max_length=4, primary_key=True)
    Cname = models.CharField(max_length=40)
    Cpno = models.CharField(max_length=4, blank=True, null=True)
    Ccredit = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    Chours = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)], default=48)  # New field

    class Meta:
        db_table = 'course'
        constraints = [
            CheckConstraint(check=Q(Ccredit__range=(0, 10)), name='course_chk_1'),
            CheckConstraint(check=(Q(Cpno__isnull=True) | ~Q(Cpno=F('Cno'))), name='course_chk_2'),
            CheckConstraint(check=Q(Chours__range=(1, 99)), name='course_chk_3')  # New constraint
        ]

    def __str__(self):
        return self.Cname

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.Cpno and self.Cpno == self.Cno:
            raise ValidationError("Cpno 不能与 Cno 相同。")

    def get_cpno_name(self):
        if self.Cpno:
            try:
                return Course.objects.get(Cno=self.Cpno).Cname
            except Course.DoesNotExist:
                return ''
        return ''


class Student(models.Model):
    Sno = models.CharField(max_length=11, primary_key=True)
    Sname = models.CharField(max_length=20)
    Ssex = models.CharField(
        max_length=2,
        choices=[
            ('男', '男'),
            ('女', '女')
        ],
        blank=True,
        null=True
    )
    Sage = models.SmallIntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    Sdept = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'student'
        constraints = [
            CheckConstraint(check=Q(Sage__gt=0), name='student_chk_1'),
            CheckConstraint(check=Q(Ssex__in=['男', '女']), name='student_chk_2')
        ]

    def __str__(self):
        return self.Sname


class SC(models.Model):
    Sno = models.CharField(max_length=11)
    Cno = models.CharField(max_length=4)
    Grade = models.SmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])

    student = models.ForeignKey('Student', to_field='Sno', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', to_field='Cno', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sc'
        constraints = [
            CheckConstraint(check=Q(Grade__gte=0, Grade__lte=100), name='sc_chk_1'),
            models.UniqueConstraint(fields=['Sno', 'Cno'], name='uc_student_course')
        ]
        unique_together = (('Sno', 'Cno'),)

    def __str__(self):
        return f'{self.student.Sname} - {self.course.Cname}'
