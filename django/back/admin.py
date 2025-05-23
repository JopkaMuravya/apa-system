from django.contrib import admin
from .models import (
    User, Group, Subject,
    StudentGroup, GroupSubject, TeacherSubject
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('role',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('student', 'group')
    search_fields = ('student__email', 'group__name')
    list_filter = ('group',)


@admin.register(GroupSubject)
class GroupSubjectAdmin(admin.ModelAdmin):
    list_display = ('group', 'subject')
    search_fields = ('group__name', 'subject__name')
    list_filter = ('group', 'subject')


@admin.register(TeacherSubject)
class TeacherSubjectAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'subject')
    search_fields = ('teacher__email', 'subject__name')
    list_filter = ('teacher',)
