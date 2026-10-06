from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Sum

from .models import (
    SchoolClass,
    Teacher,
    Admission,
    Notice,
    UserProfile,
    Student,
    Attendance,
    Exam,
    ExamMark,
    Subject,
    FeeStructure,
    FeePayment,
    Timetable,
    Task,
    StudyMaterial
)


# =========================
# HOME
# =========================

def home(request):
    latest_notices = Notice.objects.all().order_by('-created_at')[:3]

    dashboard_url = None
    dashboard_title = None

    if request.user.is_authenticated:

        if request.user.is_superuser:
            dashboard_url = 'admin_dashboard'
            dashboard_title = 'Admin Dashboard'

        else:
            try:
                profile = request.user.profile

                if profile.role == 'Teacher':
                    dashboard_url = 'teacher_dashboard'
                    dashboard_title = 'Teacher Dashboard'

                elif profile.role == 'Student':
                    dashboard_url = 'student_dashboard'
                    dashboard_title = 'Student Dashboard'

                elif profile.role == 'Parent':
                    dashboard_url = 'parent_dashboard'
                    dashboard_title = 'Parent Dashboard'

            except UserProfile.DoesNotExist:
                pass

    return render(
        request,
        'schoolapp/home.html',
        {
            'latest_notices': latest_notices,
            'dashboard_url': dashboard_url,
            'dashboard_title': dashboard_title,
        }
    )


# =========================
# ABOUT
# =========================

def about(request):
    return render(
        request,
        'schoolapp/about.html'
    )


# =========================
# ACADEMICS
# =========================

def academics(request):
    classes = SchoolClass.objects.prefetch_related('subjects')

    return render(
        request,
        'schoolapp/academics.html',
        {
            'classes': classes
        }
    )


# =========================
# CLASSES
# =========================

def classes(request):
    school_classes = SchoolClass.objects.all().order_by(
        'name',
        'section'
    )

    return render(
        request,
        'schoolapp/classes.html',
        {
            'classes': school_classes
        }
    )


# =========================
# CLASS DETAIL
# =========================

def class_detail(request, class_id):
    school_class = get_object_or_404(
        SchoolClass,
        id=class_id
    )

    subjects = school_class.subjects.all()

    return render(
        request,
        'schoolapp/class_detail.html',
        {
            'school_class': school_class,
            'subjects': subjects
        }
    )


# =========================
# TEACHERS
# =========================

def teachers(request):
    teachers = Teacher.objects.all()

    return render(
        request,
        'schoolapp/teachers.html',
        {
            'teachers': teachers
        }
    )


# =========================
# ADMISSIONS
# =========================

def admissions(request):

    if request.method == 'POST':

        student_name = request.POST.get('student_name', '').strip()
        father_name = request.POST.get('father_name', '').strip()

        if len(student_name) > 20:
            return render(
                request,
                'schoolapp/admissions.html',
                {
                    'error': 'Student name must be 20 characters or less.'
                }
            )

        if len(father_name) > 20:
            return render(
                request,
                'schoolapp/admissions.html',
                {
                    'error': 'Father name must be 20 characters or less.'
                }
            )

        Admission.objects.create(
            student_name=student_name,
            father_name=father_name,
            date_of_birth=request.POST.get('date_of_birth'),
            gender=request.POST.get('gender'),
            admission_class=request.POST.get('admission_class'),
            previous_school=request.POST.get('previous_school'),
            parent_phone=request.POST.get('parent_phone'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            previous_result=request.POST.get('previous_result'),
            student_photo=request.FILES.get('student_photo'),
            documents=request.FILES.get('documents'),
        )

        return redirect('admission_success')

    return render(
        request,
        'schoolapp/admissions.html'
    )


# =========================
# ADMISSION SUCCESS
# =========================

def admission_success(request):
    return render(
        request,
        'schoolapp/admission_success.html'
    )


# =========================
# GALLERY
# =========================

def gallery(request):
    return render(
        request,
        'schoolapp/gallery.html'
    )


# =========================
# CONTACT
# =========================

def contact(request):
    return render(
        request,
        'schoolapp/contact.html'
    )


# =========================
# NOTICES
# =========================

def notices(request):
    notices = Notice.objects.all().order_by('-created_at')

    return render(
        request,
        'schoolapp/notices.html',
        {
            'notices': notices
        }
    )


# =========================
# REGISTER
# =========================

def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:

            return render(
                request,
                'schoolapp/register.html',
                {
                    'error': 'Passwords do not match.'
                }
            )

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                'schoolapp/register.html',
                {
                    'error': 'Username already exists.'
                }
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(
        request,
        'schoolapp/register.html'
    )


# =========================
# LOGIN
# =========================

def user_login(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user is None:

            return render(
                request,
                'schoolapp/login.html',
                {
                    'error': 'Invalid username or password.'
                }
            )

        login(request, user)

        return redirect('home')

    return render(
        request,
        'schoolapp/login.html'
    )


# =========================
# LOGOUT
# =========================

def user_logout(request):
    logout(request)
    return redirect('home')


# =========================
# ADMIN DASHBOARD
# =========================

def admin_dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    admissions = Admission.objects.all().order_by('-created_at')

    return render(
        request,
        'schoolapp/admin_dashboard.html',
        {
            'admissions': admissions
        }
    )


# =========================
# TEACHER DASHBOARD
# =========================

def teacher_dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not hasattr(request.user, 'profile'):
        return redirect('home')

    if request.user.profile.role != 'Teacher':
        return redirect('home')

    return render(
        request,
        'schoolapp/teacher_dashboard.html'
    )


# =========================
# STUDENT DASHBOARD
# =========================

def student_dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not hasattr(request.user, 'profile'):
        return redirect('home')

    if request.user.profile.role != 'Student':
        return redirect('home')

    return render(
        request,
        'schoolapp/student_dashboard.html'
    )


# =========================
# PARENT DASHBOARD
# =========================

def parent_dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not hasattr(request.user, 'profile'):
        return redirect('home')

    if request.user.profile.role != 'Parent':
        return redirect('home')

    return render(
        request,
        'schoolapp/parent_dashboard.html'
    )


# =========================
# ADD STUDENT
# =========================

def add_student(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    school_classes = SchoolClass.objects.all().order_by(
        'name',
        'section'
    )

    if request.method == 'POST':

        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        school_class_id = request.POST.get('school_class')
        address = request.POST.get('address')
        photo = request.FILES.get('photo')

        school_class = None

        if school_class_id:
            school_class = get_object_or_404(
                SchoolClass,
                id=school_class_id
            )

        Student.objects.create(
            name=name,
            father_name=father_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            gender=gender,
            school_class=school_class,
            address=address,
            photo=photo
        )

        return redirect('student_list')

    return render(
        request,
        'schoolapp/add_student.html',
        {
            'school_classes': school_classes
        }
    )


# =========================
# STUDENT LIST
# =========================

def student_list(request):

    students = Student.objects.all().order_by(
        '-admission_date'
    )

    return render(
        request,
        'schoolapp/student_list.html',
        {
            'students': students
        }
    )


# =========================
# STUDENT PROFILE
# =========================

def student_profile(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    return render(
        request,
        'schoolapp/student_profile.html',
        {
            'student': student
        }
    )


# =========================
# EDIT STUDENT
# =========================

def edit_student(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == 'POST':

        student.name = request.POST.get('name')
        student.father_name = request.POST.get('father_name')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.gender = request.POST.get('gender')
        student.school_class_id = request.POST.get('school_class')
        student.address = request.POST.get('address')

        if request.FILES.get('photo'):
            student.photo = request.FILES.get('photo')

        student.save()

        return redirect(
            'student_profile',
            student_id=student.id
        )

    school_classes = SchoolClass.objects.all()

    return render(
        request,
        'schoolapp/edit_student.html',
        {
            'student': student,
            'school_classes': school_classes
        }
    )


# =========================
# DELETE STUDENT
# =========================

def delete_student(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == 'POST':

        student.delete()

        return redirect('student_list')

    return render(
        request,
        'schoolapp/delete_student.html',
        {
            'student': student
        }
    )


# =========================
# ADMISSION DETAIL
# =========================

def admission_detail(request, admission_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    admission = get_object_or_404(
        Admission,
        id=admission_id
    )

    return render(
        request,
        'schoolapp/admission_detail.html',
        {
            'admission': admission
        }
    )


# =========================
# ADMISSION STATUS
# =========================

def update_admission_status(
    request,
    admission_id,
    status
):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    admission = get_object_or_404(
        Admission,
        id=admission_id
    )

    if request.method == 'POST':

        if status in ['Approved', 'Rejected']:

            admission.status = status
            admission.save()

    return redirect('admin_dashboard')




@login_required
def delete_admission(request, admission_id):
    # Only the site superuser may delete admission applications.
    if not request.user.is_superuser:
        return redirect('home')

    # Deletion must be submitted through the POST form.
    if request.method == 'POST':
        admission = get_object_or_404(Admission, id=admission_id)
        admission.delete()

    return redirect('admin_dashboard')

# =========================
# CREATE ATTENDANCE
# =========================

def create_attendance(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    students = Student.objects.all().order_by('name')

    if request.method == 'POST':

        student_id = request.POST.get('student')
        date = request.POST.get('date')
        status = request.POST.get('status')

        student = get_object_or_404(
            Student,
            id=student_id
        )

        Attendance.objects.update_or_create(
            student=student,
            date=date,
            defaults={
                'status': status
            }
        )

        return redirect('attendance_list')

    return render(
        request,
        'schoolapp/create_attendance.html',
        {
            'students': students
        }
    )


# =========================
# ATTENDANCE LIST
# =========================

def attendance_list(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    attendance_records = Attendance.objects.select_related(
        'student'
    ).all()

    return render(
        request,
        'schoolapp/attendance_list.html',
        {
            'attendance_records': attendance_records
        }
    )


# =========================
# MARK ATTENDANCE
# =========================

def mark_attendance(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    students = Student.objects.all().order_by('name')

    if request.method == 'POST':

        date = request.POST.get('date')

        for student in students:

            status = request.POST.get(
                f'status_{student.id}'
            )

            if status in ['Present', 'Absent']:

                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={
                        'status': status
                    }
                )

        return redirect('attendance_list')

    return render(
        request,
        'schoolapp/mark_attendance.html',
        {
            'students': students
        }
    )


# =========================
# ATTENDANCE REPORT
# =========================

def attendance_report(request, student_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    student = get_object_or_404(
        Student,
        id=student_id
    )

    attendance_records = Attendance.objects.filter(
        student=student
    ).order_by('-date')

    total_days = attendance_records.count()

    present_days = attendance_records.filter(
        status='Present'
    ).count()

    absent_days = attendance_records.filter(
        status='Absent'
    ).count()

    if total_days > 0:

        percentage = round(
            (present_days / total_days) * 100,
            2
        )

    else:

        percentage = 0

    return render(
        request,
        'schoolapp/attendance_report.html',
        {
            'student': student,
            'attendance_records': attendance_records,
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'percentage': percentage,
        }
    )


# =========================
# CREATE EXAM
# =========================

def create_exam(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    classes = SchoolClass.objects.all().order_by('name')

    if request.method == 'POST':

        name = request.POST.get('name')

        school_class_id = request.POST.get(
            'school_class'
        )

        start_date = request.POST.get(
            'start_date'
        )

        end_date = request.POST.get(
            'end_date'
        )

        description = request.POST.get(
            'description'
        )

        school_class = get_object_or_404(
            SchoolClass,
            id=school_class_id
        )

        Exam.objects.create(
            name=name,
            school_class=school_class,
            start_date=start_date,
            end_date=end_date,
            description=description
        )

        return redirect('exam_list')

    return render(
        request,
        'schoolapp/create_exam.html',
        {
            'classes': classes
        }
    )


# =========================
# EXAM LIST
# =========================

def exam_list(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    exams = Exam.objects.select_related(
        'school_class'
    ).all().order_by('-start_date')

    return render(
        request,
        'schoolapp/exam_list.html',
        {
            'exams': exams
        }
    )


# =========================
# ENTER MARKS
# =========================

def enter_marks(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    exams = Exam.objects.select_related(
        'school_class'
    ).all().order_by('-start_date')

    subjects = Subject.objects.select_related(
        'school_class'
    ).all().order_by('name')

    students = Student.objects.select_related(
        'school_class'
    ).all().order_by('name')

    if request.method == 'POST':

        exam_id = request.POST.get('exam')
        subject_id = request.POST.get('subject')
        student_id = request.POST.get('student')

        total_marks = request.POST.get(
            'total_marks'
        )

        obtained_marks = request.POST.get(
            'obtained_marks'
        )

        exam = get_object_or_404(
            Exam,
            id=exam_id
        )

        subject = get_object_or_404(
            Subject,
            id=subject_id
        )

        student = get_object_or_404(
            Student,
            id=student_id
        )

        if int(obtained_marks) > int(total_marks):

            return render(
                request,
                'schoolapp/enter_marks.html',
                {
                    'exams': exams,
                    'subjects': subjects,
                    'students': students,
                    'error': (
                        'Obtained marks cannot be '
                        'greater than total marks.'
                    )
                }
            )

        ExamMark.objects.update_or_create(
            exam=exam,
            student=student,
            subject=subject,
            defaults={
                'total_marks': total_marks,
                'obtained_marks': obtained_marks
            }
        )

        return redirect('marks_list')

    return render(
        request,
        'schoolapp/enter_marks.html',
        {
            'exams': exams,
            'subjects': subjects,
            'students': students
        }
    )


# =========================
# MARKS LIST
# =========================

def marks_list(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    marks = ExamMark.objects.select_related(
        'exam',
        'student',
        'subject'
    ).all()

    return render(
        request,
        'schoolapp/marks_list.html',
        {
            'marks': marks
        }
    )


# =========================
# CREATE FEE STRUCTURE
# =========================

def create_fee_structure(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    classes = SchoolClass.objects.all().order_by('name')

    if request.method == 'POST':

        school_class_id = request.POST.get(
            'school_class'
        )

        admission_fee = request.POST.get(
            'admission_fee'
        ) or 0

        monthly_fee = request.POST.get(
            'monthly_fee'
        ) or 0

        exam_fee = request.POST.get(
            'exam_fee'
        ) or 0

        other_fee = request.POST.get(
            'other_fee'
        ) or 0

        school_class = get_object_or_404(
            SchoolClass,
            id=school_class_id
        )

        FeeStructure.objects.create(
            school_class=school_class,
            admission_fee=admission_fee,
            monthly_fee=monthly_fee,
            exam_fee=exam_fee,
            other_fee=other_fee
        )

        return redirect('fee_structure_list')

    return render(
        request,
        'schoolapp/create_fee_structure.html',
        {
            'classes': classes
        }
    )


# =========================
# FEE STRUCTURE LIST
# =========================

def fee_structure_list(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    fee_structures = FeeStructure.objects.select_related(
        'school_class'
    ).all().order_by(
        'school_class__name'
    )

    return render(
        request,
        'schoolapp/fee_structure_list.html',
        {
            'fee_structures': fee_structures
        }
    )


# =========================
# CREATE FEE PAYMENT
# =========================

def create_fee_payment(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    students = Student.objects.select_related(
        'school_class'
    ).all().order_by('name')

    fee_structures = FeeStructure.objects.select_related(
        'school_class'
    ).all().order_by(
        'school_class__name'
    )

    if request.method == 'POST':

        student_id = request.POST.get('student')

        fee_structure_id = request.POST.get(
            'fee_structure'
        )

        month = request.POST.get('month')

        amount = request.POST.get('amount')

        payment_date = request.POST.get(
            'payment_date'
        )

        status = request.POST.get('status')

        payment_method = request.POST.get(
            'payment_method'
        )

        notes = request.POST.get('notes')

        student = get_object_or_404(
            Student,
            id=student_id
        )

        fee_structure = None

        if fee_structure_id:

            fee_structure = get_object_or_404(
                FeeStructure,
                id=fee_structure_id
            )

        FeePayment.objects.create(
            student=student,
            fee_structure=fee_structure,
            month=month,
            amount=amount,
            payment_date=payment_date,
            status=status,
            payment_method=payment_method,
            notes=notes
        )

        return redirect('fee_payment_list')

    return render(
        request,
        'schoolapp/create_fee_payment.html',
        {
            'students': students,
            'fee_structures': fee_structures
        }
    )


# =========================
# FEE PAYMENT LIST
# =========================

def fee_payment_list(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    payments = FeePayment.objects.select_related(
        'student',
        'student__school_class',
        'fee_structure'
    ).all().order_by('-payment_date')

    return render(
        request,
        'schoolapp/fee_payment_list.html',
        {
            'payments': payments
        }
    )


# =========================
# FEE STATUS
# =========================

def fee_status(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    total_paid = (
        FeePayment.objects
        .filter(status='Paid')
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    total_pending = (
        FeePayment.objects
        .filter(status='Pending')
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    paid_count = FeePayment.objects.filter(
        status='Paid'
    ).count()

    pending_count = FeePayment.objects.filter(
        status='Pending'
    ).count()

    students = Student.objects.select_related(
        'school_class'
    ).all().order_by('name')

    student_fee_data = []

    for student in students:

        paid_amount = (
            FeePayment.objects
            .filter(
                student=student,
                status='Paid'
            )
            .aggregate(total=Sum('amount'))['total'] or 0
        )

        pending_amount = (
            FeePayment.objects
            .filter(
                student=student,
                status='Pending'
            )
            .aggregate(total=Sum('amount'))['total'] or 0
        )

        student_fee_data.append(
            {
                'student': student,
                'paid_amount': paid_amount,
                'pending_amount': pending_amount,
            }
        )

    return render(
        request,
        'schoolapp/fee_status.html',
        {
            'total_paid': total_paid,
            'total_pending': total_pending,
            'paid_count': paid_count,
            'pending_count': pending_count,
            'student_fee_data': student_fee_data,
        }
    )


# =========================
# FEE RECEIPT
# =========================

def fee_receipt(request, payment_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    payment = get_object_or_404(
        FeePayment.objects.select_related(
            'student',
            'student__school_class',
            'fee_structure'
        ),
        id=payment_id
    )

    return render(
        request,
        'schoolapp/fee_receipt.html',
        {
            'payment': payment
        }
    )


# =========================
# TIMETABLE
# =========================

def timetable_list(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    timetables = Timetable.objects.select_related(
        'school_class',
        'subject',
        'teacher'
    ).all().order_by(
        'school_class__name',
        'day',
        'start_time'
    )

    return render(
        request,
        'schoolapp/timetable_list.html',
        {
            'timetables': timetables
        }
    )


def add_timetable(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    classes = SchoolClass.objects.all().order_by('name')
    subjects = Subject.objects.select_related(
        'school_class'
    ).all().order_by('name')
    teachers = Teacher.objects.all().order_by('name')

    if request.method == 'POST':

        school_class_id = request.POST.get('school_class')
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher')
        day = request.POST.get('day')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        school_class = get_object_or_404(
            SchoolClass,
            id=school_class_id
        )

        subject = get_object_or_404(
            Subject,
            id=subject_id
        )

        teacher = None

        if teacher_id:
            teacher = get_object_or_404(
                Teacher,
                id=teacher_id
            )

        Timetable.objects.create(
            school_class=school_class,
            subject=subject,
            teacher=teacher,
            day=day,
            start_time=start_time,
            end_time=end_time
        )

        return redirect('timetable_list')

    return render(
        request,
        'schoolapp/add_timetable.html',
        {
            'classes': classes,
            'subjects': subjects,
            'teachers': teachers
        }
    )


# =========================
# TASKS
# =========================

def task_list(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    tasks = Task.objects.select_related(
        'school_class',
        'subject'
    ).all().order_by('-due_date')

    return render(
        request,
        'schoolapp/task_list.html',
        {
            'tasks': tasks
        }
    )


def add_task(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    classes = SchoolClass.objects.all().order_by('name')

    subjects = Subject.objects.select_related(
        'school_class'
    ).all().order_by('name')

    if request.method == 'POST':

        title = request.POST.get('title')
        school_class_id = request.POST.get('school_class')
        subject_id = request.POST.get('subject')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        school_class = get_object_or_404(
            SchoolClass,
            id=school_class_id
        )

        subject = None

        if subject_id:
            subject = get_object_or_404(
                Subject,
                id=subject_id
            )

        Task.objects.create(
            title=title,
            school_class=school_class,
            subject=subject,
            description=description,
            due_date=due_date
        )

        return redirect('task_list')

    return render(
        request,
        'schoolapp/add_task.html',
        {
            'classes': classes,
            'subjects': subjects
        }
    )


# =========================
# STUDY MATERIAL
# =========================

def study_material_list(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    materials = StudyMaterial.objects.select_related(
        'school_class',
        'subject'
    ).all().order_by('-created_at')

    return render(
        request,
        'schoolapp/study_material_list.html',
        {
            'materials': materials
        }
    )


def add_study_material(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')

    classes = SchoolClass.objects.all().order_by('name')

    subjects = Subject.objects.select_related(
        'school_class'
    ).all().order_by('name')

    if request.method == 'POST':

        title = request.POST.get('title')
        school_class_id = request.POST.get('school_class')
        subject_id = request.POST.get('subject')
        description = request.POST.get('description')
        file = request.FILES.get('file')

        school_class = get_object_or_404(
            SchoolClass,
            id=school_class_id
        )

        subject = None

        if subject_id:
            subject = get_object_or_404(
                Subject,
                id=subject_id
            )

        StudyMaterial.objects.create(
            title=title,
            school_class=school_class,
            subject=subject,
            description=description,
            file=file
        )

        return redirect('study_material_list')

    return render(
        request,
        'schoolapp/add_study_material.html',
        {
            'classes': classes,
            'subjects': subjects
        }
    )


# =========================
# URL COMPATIBILITY FUNCTIONS
# =========================

# Dashboard aur urls.py mein create_timetable use ho raha hai,
# jabke actual function add_timetable hai.

def create_timetable(request):
    return add_timetable(request)


# Dashboard aur urls.py mein create_task use ho raha hai,
# jabke actual function add_task hai.

def create_task(request):
    return add_task(request)


# Dashboard aur urls.py mein create_study_material use ho raha hai,
# jabke actual function add_study_material hai.

def create_study_material(request):
    return add_study_material(request)

# =========================
# STUDENT PORTAL HELPER
# =========================

def get_logged_in_student(request):
    """
    Logged-in student ko email ke through find karta hai.
    Student record ka email aur User ka email same hona chahiye.
    """

    if not request.user.is_authenticated:
        return None

    if not hasattr(request.user, 'profile'):
        return None

    if request.user.profile.role != 'Student':
        return None

    return Student.objects.select_related(
        'school_class'
    ).filter(
        email=request.user.email
    ).first()


# =========================
# MY ATTENDANCE
# =========================

def student_attendance(request):

    if not request.user.is_authenticated:
        return redirect('login')

    student = get_logged_in_student(request)

    if student is None:
        return render(
            request,
            'schoolapp/student_message.html',
            {
                'title': 'Attendance',
                'message': (
                    'Your student account is not linked with a student record. '
                    'Please make sure your login email matches your student email.'
                )
            }
        )

    attendance_records = Attendance.objects.filter(
        student=student
    ).order_by('-date')

    total_days = attendance_records.count()

    present_days = attendance_records.filter(
        status='Present'
    ).count()

    absent_days = attendance_records.filter(
        status='Absent'
    ).count()

    if total_days > 0:
        percentage = round(
            (present_days / total_days) * 100,
            2
        )
    else:
        percentage = 0

    return render(
        request,
        'schoolapp/student_attendance.html',
        {
            'student': student,
            'attendance_records': attendance_records,
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'percentage': percentage,
        }
    )


# =========================
# MY RESULTS
# =========================

def student_results(request):

    if not request.user.is_authenticated:
        return redirect('login')

    student = get_logged_in_student(request)

    if student is None:
        return render(
            request,
            'schoolapp/student_message.html',
            {
                'title': 'Results',
                'message': (
                    'Your student account is not linked with a student record.'
                )
            }
        )

    marks = ExamMark.objects.select_related(
        'exam',
        'subject'
    ).filter(
        student=student
    ).order_by(
        '-exam__start_date',
        'subject__name'
    )

    total_marks = 0
    obtained_marks = 0

    for mark in marks:
        total_marks += mark.total_marks
        obtained_marks += mark.obtained_marks

    if total_marks > 0:
        percentage = round(
            (obtained_marks / total_marks) * 100,
            2
        )
    else:
        percentage = 0

    if percentage >= 80:
        grade = 'A+'
    elif percentage >= 70:
        grade = 'A'
    elif percentage >= 60:
        grade = 'B'
    elif percentage >= 50:
        grade = 'C'
    elif percentage >= 40:
        grade = 'D'
    else:
        grade = 'F'

    return render(
        request,
        'schoolapp/student_results.html',
        {
            'student': student,
            'marks': marks,
            'total_marks': total_marks,
            'obtained_marks': obtained_marks,
            'percentage': percentage,
            'grade': grade,
        }
    )


# =========================
# MY FEES
# =========================

def student_fees(request):

    if not request.user.is_authenticated:
        return redirect('login')

    student = get_logged_in_student(request)

    if student is None:
        return render(
            request,
            'schoolapp/student_message.html',
            {
                'title': 'Fees',
                'message': (
                    'Your student account is not linked with a student record.'
                )
            }
        )

    payments = FeePayment.objects.select_related(
        'fee_structure'
    ).filter(
        student=student
    ).order_by('-payment_date')

    total_paid = (
        payments
        .filter(status='Paid')
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    total_pending = (
        payments
        .filter(status='Pending')
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    return render(
        request,
        'schoolapp/student_fees.html',
        {
            'student': student,
            'payments': payments,
            'total_paid': total_paid,
            'total_pending': total_pending,
        }
    )


# =========================
# MY TIMETABLE
# =========================

def student_timetable(request):

    if not request.user.is_authenticated:
        return redirect('login')

    student = get_logged_in_student(request)

    if student is None:
        return render(
            request,
            'schoolapp/student_message.html',
            {
                'title': 'Timetable',
                'message': (
                    'Your student account is not linked with a student record.'
                )
            }
        )

    if not student.school_class:
        return render(
            request,
            'schoolapp/student_message.html',
            {
                'title': 'Timetable',
                'message': (
                    'No class has been assigned to your student record yet.'
                )
            }
        )

    timetables = Timetable.objects.select_related(
        'school_class',
        'subject',
        'teacher'
    ).filter(
        school_class=student.school_class
    ).order_by(
        'day',
        'start_time'
    )

    return render(
        request,
        'schoolapp/student_timetable.html',
        {
            'student': student,
            'timetables': timetables,
        }
    )


# =========================
# MY ASSIGNMENTS
# =========================

def student_tasks(request):

    if not request.user.is_authenticated:
        return redirect('login')

    student = get_logged_in_student(request)

    if student is None:
        return render(
            request,
            'schoolapp/student_message.html',
            {
                'title': 'Assignments',
                'message': (
                    'Your student account is not linked with a student record.'
                )
            }
        )

    if not student.school_class:
        return render(
            request,
            'schoolapp/student_message.html',
            {
                'title': 'Assignments',
                'message': (
                    'No class has been assigned to your student record yet.'
                )
            }
        )

    tasks = Task.objects.select_related(
        'school_class',
        'subject',
        
    ).filter(
        school_class=student.school_class
    ).order_by(
        'due_date'
    )

    return render(
        request,
        'schoolapp/student_tasks.html',
        {
            'student': student,
            'tasks': tasks,
        }
    )


# =========================
# MY STUDY MATERIAL
# =========================

def student_study_material(request):

    if not request.user.is_authenticated:
        return redirect('login')

    student = get_logged_in_student(request)

    if student is None:
        return render(
            request,
            'schoolapp/student_message.html',
            {
                'title': 'Study Material',
                'message': (
                    'Your student account is not linked with a student record.'
                )
            }
        )

    if not student.school_class:
        return render(
            request,
            'schoolapp/student_message.html',
            {
                'title': 'Study Material',
                'message': (
                    'No class has been assigned to your student record yet.'
                )
            }
        )

    materials = StudyMaterial.objects.select_related(
        'school_class',
        'subject'
    ).filter(
        school_class=student.school_class
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'schoolapp/student_study_material.html',
        {
            'student': student,
            'materials': materials,
        }
    )

