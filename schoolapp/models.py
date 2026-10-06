
from django.core.serializers import python
from django.db import models
from django.contrib.auth.models import User


# =========================
# SCHOOL CLASS
# =========================

class SchoolClass(models.Model):

    name = models.CharField(max_length=20)

    section = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.section}"


# =========================
# SUBJECT
# =========================

class Subject(models.Model):

    name = models.CharField(max_length=20)

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='subjects'
    )

    def __str__(self):
        return f"{self.name} - {self.school_class}"


# =========================
# TEACHER
# =========================

class Teacher(models.Model):

    name = models.CharField(max_length=20)

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=12,
        blank=True
    )

    qualification = models.CharField(
        max_length=20
    )

    experience = models.CharField(
        max_length=20,
        blank=True
    )

    subject = models.CharField(
        max_length=20
    )

    bio = models.TextField(
        blank=True
    )

    photo = models.ImageField(
        upload_to='teachers/',
        blank=True,
        null=True
    )

    assigned_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='class_teachers'
    )

    assigned_subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subject_teachers'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# =========================
# ADMISSION
# =========================

class Admission(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    student_name = models.CharField(
        max_length=150
    )

    father_name = models.CharField(
        max_length=150
    )

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    admission_class = models.CharField(
        max_length=20
    )

    previous_school = models.CharField(
        max_length=200,
        blank=True
    )

    parent_phone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField()

    previous_result = models.CharField(
        max_length=100,
        blank=True
    )

    student_photo = models.ImageField(
        upload_to='admission_photos/',
        blank=True,
        null=True
    )

    documents = models.FileField(
        upload_to='admission_documents/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.student_name


# =========================
# NOTICE
# =========================

class Notice(models.Model):

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =========================
# USER PROFILE / ROLES
# =========================

class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
        ('Parent', 'Parent'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Student'
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# STUDENT
class Student(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    name = models.CharField(max_length=150)

    father_name = models.CharField(max_length=150)

    email = models.EmailField(blank=True)

    phone = models.CharField(max_length=20)

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )

    address = models.TextField()

    photo = models.ImageField(
        upload_to='students/',
        blank=True,
        null=True
    )

    admission_date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# =========================
# ATTENDANCE
# =========================

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Present'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

        constraints = [
            models.UniqueConstraint(
                fields=['student', 'date'],
                name='unique_student_attendance_per_date'
            )
        ]

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"


class Exam(models.Model):
    name = models.CharField(max_length=150)

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='exams'
    )

    start_date = models.DateField()

    end_date = models.DateField()

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.school_class}"



class ExamMark(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='marks'
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='exam_marks'
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='exam_marks'
    )

    total_marks = models.PositiveIntegerField()

    obtained_marks = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['student__name']

        constraints = [
            models.UniqueConstraint(
                fields=['exam', 'student', 'subject'],
                name='unique_exam_student_subject'
            )
        ]

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.exam.name}"


class FeeStructure(models.Model):

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='fee_structures'
    )

    admission_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    monthly_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    exam_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    other_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def total_fee(self):
        return (
            self.admission_fee
            + self.monthly_fee
            + self.exam_fee
            + self.other_fee
        )

    def __str__(self):
        return f"{self.school_class} Fee Structure"


class FeePayment(models.Model):

    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Bank', 'Bank'),
        ('Online', 'Online'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='fee_payments'
    )

    fee_structure = models.ForeignKey(
        FeeStructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )

    month = models.CharField(
        max_length=20
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Paid'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='Cash'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.name} - {self.month} - {self.status}"


# =========================
# TIMETABLE
# =========================

class Timetable(models.Model):

    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='timetables'
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='timetables'
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='timetables'
    )

    day = models.CharField(
        max_length=20,
        choices=DAY_CHOICES
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.school_class} - {self.subject} - {self.day}"


# =========================
# TASKS
# =========================

class Task(models.Model):

    title = models.CharField(
        max_length=200
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )

    description = models.TextField(
        blank=True
    )

    due_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =========================
# STUDY MATERIAL
# =========================

class StudyMaterial(models.Model):

    title = models.CharField(
        max_length=200
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='study_materials'
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='study_materials'
    )

    description = models.TextField(
        blank=True
    )

    file = models.FileField(
        upload_to='study_material/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

