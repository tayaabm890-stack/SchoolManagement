
from django.contrib import admin


from .models import (
    SchoolClass,
    Subject,
    Teacher,
    Admission,
    Notice,
    UserProfile,
    Student
)




@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'section',
    )

    search_fields = (
        'name',
        'section',
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'school_class',
    )

    list_filter = (
        'school_class',
    )

    search_fields = (
        'name',
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'subject',
        'assigned_class',
        'assigned_subject',
        'qualification',
        'phone',
        'email',
    )

    list_filter = (
        'assigned_class',
        'assigned_subject',
    )

    search_fields = (
        'name',
        'subject',
        'qualification',
    )


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):

    list_display = (
        'student_name',
        'father_name',
        'admission_class',
        'gender',
        'parent_phone',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'gender',
        'admission_class',
    )

    search_fields = (
        'student_name',
        'father_name',
        'parent_phone',
        'email',
    )

    list_editable = (
        'status',
    )

    readonly_fields = (
        'created_at',
    )


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
    )

    readonly_fields = (
        'created_at',
    )

    ordering = (
        '-created_at',
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'role',
    )

    list_filter = (
        'role',
    )

    search_fields = (
        'user__username',
        'user__email',
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'father_name',
        'school_class',
        'gender',
        'phone',
        'admission_date',
    )

    list_filter = (
        'gender',
        'school_class',
    )

    search_fields = (
        'name',
        'father_name',
        'phone',
        'email',
    )

    readonly_fields = (
        'admission_date',
    )

