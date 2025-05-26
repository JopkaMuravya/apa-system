from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('У пользователя должна быть корпоративная почта')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Админ'),
            ('moderator', 'Модератор'),
            ('teacher', 'Преподаватель'),
            ('student', 'Студент'),
            ('waiting', 'Без роли')
        ],
        default='waiting'
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role})"


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StudentGroup(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='student_groups'
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='group_students'
    )

    class Meta:
        unique_together = ('student', 'group')

    def __str__(self):
        return f"{self.student} в {self.group}"


class GroupSubject(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='group_subjects'
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='subject_groups'
    )

    class Meta:
        unique_together = ('group', 'subject')

    def __str__(self):
        return f"{self.group} изучает {self.subject}"


class TeacherSubject(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_subjects'
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='subject_teachers'
    )

    class Meta:
        unique_together = ('teacher', 'subject')

    def __str__(self):
        return f"{self.teacher} преподает {self.subject}"
    

class GroupSubjectTeacher(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='teaching_assignments'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='group_teaching_assignments'
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='teaching_subjects'
    )

    class Meta:
        unique_together = ('group', 'subject')  

    def __str__(self):
        return f"{self.teacher} ведёт {self.subject} у {self.group}"


class Lesson(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    lesson_date = models.DateField()
    lesson_number = models.IntegerField()

    def __str__(self):
        return f"{self.subject} для {self.group} ({self.lesson_date})"