import os
import django
import random
from datetime import datetime, timedelta
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from back.models import Group, StudentGroup, Subject, TeacherSubject, GroupSubjectTeacher, Grade, TeacherComment

User = get_user_model()


def clear_test_data():
    """Удаляет только тестовые данные"""
    print("Удаляем старые тестовые данные...")
    Grade.objects.all().delete()
    TeacherComment.objects.all().delete()
    StudentGroup.objects.all().delete()
    GroupSubjectTeacher.objects.all().delete()
    TeacherSubject.objects.all().delete()
    User.objects.filter(email__regex=r'^(teacher|student)\d+@example\.com$').delete()
    Group.objects.filter(name__startswith="Группа ").delete()
    Subject.objects.filter(name__startswith="Предмет ").delete()


def create_groups():
    """Создает 10 учебных групп"""
    return [Group.objects.create(name=f"Группа {i}") for i in range(1, 11)]


def create_teachers():
    """Создает 10 преподавателей с корректными паролями"""
    teachers = []
    for i in range(1, 11):
        teacher = User.objects.create_user(  # Используем create_user вместо create!
            email=f"teacher{i}@example.com",
            password='123',  # Пароль устанавливается здесь
            first_name=f"Преподаватель_{i}",
            last_name="Тестовый",
            role="teacher",
            is_active=True
        )
        teachers.append(teacher)
    return teachers


def create_subjects():
    """Создает 20 учебных предметов (каждые 2 преподавателя делят предмет)"""
    return [Subject.objects.create(name=f"Предмет {i}") for i in range(1, 21)]


def assign_teachers_to_subjects(teachers, subjects):
    """Назначает каждому преподавателю 10 случайных предметов"""
    for teacher in teachers:
        # Каждый преподаватель ведет 10 предметов
        for subject in random.sample(subjects, 10):
            TeacherSubject.objects.create(teacher=teacher, subject=subject)


def assign_groups_to_teachers(groups, teachers, subjects):
    """Распределяет группы так, чтобы каждый студент изучал 10 предметов"""
    for group in groups:
        # Для группы выбираем 10 уникальных предметов
        group_subjects = random.sample(subjects, 10)

        for subject in group_subjects:
            # Находим всех преподавателей для этого предмета
            available_teachers = User.objects.filter(
                teacher_subjects__subject=subject
            )

            if available_teachers.exists():
                # Выбираем случайного преподавателя для предмета в группе
                teacher = random.choice(available_teachers)
                GroupSubjectTeacher.objects.create(
                    group=group,
                    subject=subject,
                    teacher=teacher
                )


def create_students(groups):
    """Создает 100 студентов (по 10 на группу)"""
    for i in range(1, 101):
        student = User.objects.create(
            email=f"student{i}@example.com",
            first_name=f"Студент_{i}",
            last_name="Фамилия",
            role="student",
            is_active=True
        )
        student.set_password('123')
        student.save()
        group_index = (i - 1) // 10
        StudentGroup.objects.create(student=student, group=groups[group_index])


def create_grades():
    """Создает по 3 оценки на каждый предмет студента"""
    assignments = ["ДЗ", "Контрольная", "Экзамен"]

    for student in User.objects.filter(role='student'):
        student_group = StudentGroup.objects.get(student=student)
        group_subjects = GroupSubjectTeacher.objects.filter(group=student_group.group)

        for gst in group_subjects:
            for assignment in assignments:
                Grade.objects.create(
                    student=student,
                    subject=gst.subject,
                    group=gst.group,
                    assignment_name=f"{assignment}",
                    value=str(random.randint(2, 5)),
                    created_at=datetime.now() - timedelta(days=random.randint(1, 180))
                )


@transaction.atomic
def create_sample_data():
    """Основная функция создания данных"""
    if input("Создать новые тестовые данные? (y/n): ").lower() != 'y':
        return

    try:
        clear_test_data()

        groups = create_groups()
        teachers = create_teachers()
        subjects = create_subjects()

        assign_teachers_to_subjects(teachers, subjects)
        assign_groups_to_teachers(groups, teachers, subjects)
        create_students(groups)
        create_grades()

        print("\nДанные успешно созданы!")
        print(f"Групп: {Group.objects.count()}")
        print(f"Преподавателей: {User.objects.filter(role='teacher').count()}")
        print(f"Студентов: {User.objects.filter(role='student').count()}")
        print(f"Предметов: {Subject.objects.count()}")
        print(f"Назначений преподавателей: {TeacherSubject.objects.count()} (по 10 на каждого)")
        print(f"Назначений группам: {GroupSubjectTeacher.objects.count()} (по 10 на группу)")
        print(f"Оценок: {Grade.objects.count()} (по 3 на каждый предмет студента)")

    except Exception as e:
        print(f"\nОшибка: {str(e)}")


if __name__ == "__main__":
    create_sample_data()