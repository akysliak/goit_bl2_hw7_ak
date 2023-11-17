import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from db import session
from models import Group, Teacher, Student, Subject, Grade

NUMBER_STUDENTS_PER_GROUP = 15
NUMBER_GROUPS = 3
NUMBER_TEACHERS = 5
NUMBER_SUBJECTS_PER_TEACHER = 2
NUMBER_GRADES_PER_SUBJECT = 10

fake = Faker('uk-UA')


# to remove current entries from the tables (if any)
def clean_tables():
    for entry in [Group, Teacher, Student, Subject, Grade]:
        els = session.query(entry).all()
        print(els)
        for el in els:
            session.delete(el)
        #session.commit()

def add_groups(number_groups=NUMBER_GROUPS):
    for i in range(1, number_groups+1):
        group = Group(
            id = i,
            name = fake.word().title()
        )
        session.add(group)


def add_teachers(number_teachers=NUMBER_TEACHERS):
    for i in range(1, number_teachers+1):
        teacher = Teacher(
            id = i,
            fullname = fake.name()
        )
        session.add(teacher)


def add_subjects(number_subjects_per_teacher=NUMBER_SUBJECTS_PER_TEACHER,
                              number_teachers=NUMBER_TEACHERS):
    subject_id = 0
    for teacher_id in range(1, number_teachers+1):
        for _ in range(number_subjects_per_teacher):
            subject_id +=1
            subject = Subject(
                id = subject_id,
                name=fake.word().title(),
                teacher_id = teacher_id
            )
            session.add(subject)

def add_students(number_groups=NUMBER_GROUPS, number_students_per_group=NUMBER_STUDENTS_PER_GROUP):
        student_id = 0
        for group_id in range(1, number_groups+1):
            for _ in range(number_students_per_group):
                student_id += 1
                student = Student(
                    id = student_id,
                    fullname = fake.name(),
                    group_id = group_id
                )
                session.add(student)


def add_grades(number_subjects=NUMBER_SUBJECTS_PER_TEACHER*NUMBER_TEACHERS,
                number_students=NUMBER_GROUPS*NUMBER_STUDENTS_PER_GROUP,
                number_grades_per_subject=NUMBER_GRADES_PER_SUBJECT):
    fake_dates = set()
    for _ in range(number_grades_per_subject * 4):
        fake_dates.add(fake.date_this_decade())
    fake_dates = list(fake_dates)
    grade_id = 0
    for subject_id in range(1, number_subjects + 1):
        dates_classes = random.sample(fake_dates, number_grades_per_subject*2)
        for student_id in range(1, number_students+1):
            dates_with_grade = random.sample(dates_classes, number_grades_per_subject)
            for i in range(number_grades_per_subject):
                grade_id += 1
                grade = Grade(
                    id = grade_id,
                    grade=random.randint(0, 100),
                    date_of=dates_with_grade[i], #fake.date_this_decade(),
                    student_id=student_id,
                    subjects_id=subject_id
                )
                session.add(grade)


if __name__ == '__main__':
    try:
        clean_tables()
        session.commit()

        add_groups()
        session.commit()

        add_teachers()
        add_subjects()
        add_students()
        add_grades()
        session.commit()

        #insert_rel()
        #session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()