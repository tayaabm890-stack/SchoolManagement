
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('academics/', views.academics, name='academics'),
    path('classes/', views.classes, name='classes'),
    path('classes/<int:class_id>/', views.class_detail, name='class_detail'),
    path('teachers/', views.teachers, name='teachers'),

    path('admissions/', views.admissions, name='admissions'),
    path('admission-success/', views.admission_success, name='admission_success'),

    path('gallery/', views.gallery, name='gallery'),
    path('notices/', views.notices, name='notices'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('timetable/', views.timetable_list, name='timetable_list'),
path('timetable/create/', views.create_timetable, name='create_timetable'),

path('tasks/', views.task_list, name='task_list'),
path('tasks/create/', views.create_task, name='create_task'),

path('study-material/', views.study_material_list, name='study_material_list'),
path('study-material/create/', views.create_study_material, name='create_study_material'),
    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'teacher-dashboard/',
        views.teacher_dashboard,
        name='teacher_dashboard'
    ),

    path(
        'student-dashboard/',
        views.student_dashboard,
        name='student_dashboard'
    ),

    path(
        'parent-dashboard/',
        views.parent_dashboard,
        name='parent_dashboard'
    ),

    # ================= STUDENTS =================

    path(
        'students/',
        views.student_list,
        name='student_list'
    ),

    path(
        'students/add/',
        views.add_student,
        name='add_student'
    ),

    path(
        'students/<int:student_id>/',
        views.student_profile,
        name='student_profile'
    ),

    path(
        'students/<int:student_id>/edit/',
        views.edit_student,
        name='edit_student'
    ),

    path(
        'students/<int:student_id>/delete/',
        views.delete_student,
        name='delete_student'
    ),

    # ================= ADMISSIONS =================

    path(
        'admin-dashboard/admission/<int:admission_id>/',
        views.admission_detail,
        name='admission_detail'
    ),

    path(
        'admin-dashboard/admission/<int:admission_id>/<str:status>/',
        views.update_admission_status,
        name='update_admission_status'
    ),
    path(
    'admin-dashboard/admission/<int:admission_id>/delete/',
    views.delete_admission,
    name='delete_admission'
    ),
    # ================= ATTENDANCE =================

    path(
        'attendance/',
        views.attendance_list,
        name='attendance_list'
    ),

    path(
        'attendance/mark/',
        views.mark_attendance,
        name='mark_attendance'
    ),

    path(
        'attendance/report/<int:student_id>/',
        views.attendance_report,
        name='attendance_report'
    ),

    # ================= EXAMS =================

    path(
        'exams/create/',
        views.create_exam,
        name='create_exam'
    ),

    path(
        'exams/',
        views.exam_list,
        name='exam_list'
    ),

    # ================= MARKS =================

    path(
        'marks/enter/',
        views.enter_marks,
        name='enter_marks'
    ),

    path(
        'marks/',
        views.marks_list,
        name='marks_list'
    ),

    # ================= FEES =================

    path(
        'fees/structure/create/',
        views.create_fee_structure,
        name='create_fee_structure'
    ),

    path(
        'fees/structure/',
        views.fee_structure_list,
        name='fee_structure_list'
    ),

    path(
        'fees/payment/create/',
        views.create_fee_payment,
        name='create_fee_payment'
    ),

    path(
        'fees/payments/',
        views.fee_payment_list,
        name='fee_payment_list'
    ),

    path(
        'fees/status/',
        views.fee_status,
        name='fee_status'
    ),

    path(
        'fees/payment/<int:payment_id>/receipt/',
        views.fee_receipt,
        name='fee_receipt'
    ),

    # ================= TIMETABLE =================

    path(
        'timetable/',
        views.timetable_list,
        name='timetable_list'
    ),

    path(
        'timetable/create/',
        views.create_timetable,
        name='create_timetable'
    ),

    # ================= TASKS =================

    path(
        'tasks/',
        views.task_list,
        name='task_list'
    ),

    path(
        'tasks/create/',
        views.create_task,
        name='create_task'
    ),

    # ================= STUDY MATERIAL =================

    path(
        'study-material/',
        views.study_material_list,
        name='study_material_list'
    ),

    path(
        'study-material/create/',
        views.create_study_material,
        name='create_study_material'
    ),

# =========================
# STUDENT PORTAL
# =========================

path(
    'student/attendance/',
    views.student_attendance,
    name='student_attendance'
),

path(
    'student/results/',
    views.student_results,
    name='student_results'
),

path(
    'student/fees/',
    views.student_fees,
    name='student_fees'
),

path(
    'student/timetable/',
    views.student_timetable,
    name='student_timetable'
),

path(
    'student/tasks/',
    views.student_tasks,
    name='student_tasks'
),

path(
    'student/study-material/',
    views.student_study_material,
    name='student_study_material'
),


]
