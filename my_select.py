from sqlalchemy import  select, and_, desc, func
#from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Mapped, mapped_column

from db import session
from models import Group, Teacher, Student, Subject, Grade

def select_1():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """
    print("SELECT 1")
    print("1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів:")
    statement = (
                    select(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label("average_grade"))
                    .join(Grade.student)
                    .group_by(Student.id)
                    .order_by(desc("average_grade"))
                    .limit(5)
    )
    result = session.execute(statement).all()
    for st_id, st_name, avg_grade in result:
        #print(row)
        print(f"{st_id}\t\t{st_name}\t\t{avg_grade}")
    print("----------------------------------------")


def select_2():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    where g.subject_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """
    print("SELECT 2")
    print("2. Знайти студента із найвищим середнім балом з певного предмета:")
    statement = (
        select(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label("average_grade"))
        .join(Grade.student)
        .where(Grade.subjects_id==1)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .limit(1)
    )
    result = session.execute(statement).all()
    for st_id, st_name, avg_grade in result:
        print(f"{st_id}\t\t{st_name}\t\t{avg_grade}")
    print("----------------------------------------")


def select_3():
    """
    SELECT
        groups.name,
        subjects.name,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    JOIN subjects ON g.subject_id = subjects.id
    JOIN groups ON s.group_id = groups.id
    WHERE subjects.id = 2
    GROUP BY g.subject_id, s.group_id
    ORDER BY s.group_id
    """
    print("SELECT 3")
    print("3. Знайти середній бал у групах з певного предмета (specific):")
    statement = (
        select(Group.name, Subject.name, func.round(func.avg(Grade.grade), 2).label("average_grade"))
        .join(Grade.student)
        .join(Grade.discipline)
        .join(Student.group)
        .where(Subject.id == 2)
        .group_by(Subject.name, Group.id)
        .order_by(Group.id)
    )
    result = session.execute(statement).all()
    print(f"group name\t\tsubject name\t\tavg grade")

    for gr_name, sb_name, avg_grade in result:
        print(f"{gr_name}\t\t{sb_name}\t\t{avg_grade}")
    print("----------------------------------------")

def select_4():
    """
    SELECT
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g;
    """
    print("SELECT 4")
    print("4. Знайти середній бал на потоці (по всій таблиці оцінок):")
    statement = (
        select(func.round(func.avg(Grade.grade), 2).label("average_grade"))
    )
    result = session.execute(statement).scalar()
    print("avg grade:", result)

    print("----------------------------------------")

def select_5():
    """
    SELECT
        teachers.fullname,
        subjects.name
    FROM teachers
    JOIN subjects ON subjects.teacher_id = teachers.id
    WHERE teachers.id = 3;
    """
    print("SELECT 5")
    print("5. Знайти які курси читає певний викладач (specific):")
    statement = (
        select(Teacher.fullname, Subject.name)
        .join(Subject.teacher)
        .where(Teacher.id == 3)
    )
    result = session.execute(statement).all()
    print(f"Teacher name\t\tSubjects")
    for t_name, sb_name in result:
        print(f"{t_name}\t\t{sb_name}")
    print("----------------------------------------")

def select_6():
    """
    SELECT
        g.name,
        s.fullname
    FROM groups g
    JOIN students s ON s.group_id = g.id
    WHERE g.id=1;
    """
    print("SELECT 6")
    print("6. Знайти список студентів у певній групі (specific):")
    statement = (
        select(Group.name, Student.fullname)
        .join(Student.group)
        .where(Group.id == 1)
    )
    result = session.execute(statement).all()
    print(f"Group name\t\tStudent name")
    for gr_name, st_name in result:
        print(f"{gr_name}\t\t{st_name}")
    print("----------------------------------------")

def select_7():
    """
    SELECT
        g.name,
        s.name,
        grades.grade
    FROM groups g
    LEFT JOIN students st ON st.group_id = g.id
    LEFT JOIN grades ON st.id = grades.student_id
    LEFT JOIN subjects s ON s.id = grades.subject_id
    WHERE g.id=1 AND s.id=2;
    """
    print("SELECT 7")
    print("7. Знайти оцінки студентів у окремій групі з певного предмета (specific):")
    statement = (
        select(Group.name, Subject.name, Student.fullname, Grade.grade)
        .join(Grade.student)
        .join(Grade.discipline)
        .join(Student.group)
        .where(and_(Subject.id == 2, Group.id == 1))
    )
    result = session.execute(statement).all()
    print(f"group name\t\tsubject name\t\tstudent name\t\tgrade")

    for gr_name, sb_name, st_name, grade in result:
        print(f"{gr_name}\t\t{sb_name}\t\t{st_name}\t\t{grade}")
    print("----------------------------------------")

def select_8():
    """
    SELECT
        t.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM teachers t
    JOIN subjects s ON s.teacher_id = t.id
    JOIN grades g ON g.subject_id = s.id
    WHERE t.id=2
    GROUP BY t.id;
    """
    print("SELECT 8")
    print("8. Знайти середній бал, який ставить певний викладач зі своїх предметів (specific):")
    statement = (
        select(Teacher.fullname, func.round(func.avg(Grade.grade), 2).label("average_grade"))
        .join(Grade.discipline)
        .join(Subject.teacher)
        .where(Teacher.id == 2)
        .group_by(Teacher.id)
    )
    result = session.execute(statement).all()
    print(f"Teacher name\t\tavg grade")
    for t_name, grade in result:
        print(f"{t_name}\t\t{grade}")
    print("----------------------------------------")

def select_9():
    """
    SELECT DISTINCT
        st.fullname,
        sb.name
    FROM students st
    JOIN grades g ON g.student_id = st.id
    JOIN subjects sb ON g.subject_id = sb.id
    WHERE st.id = 15;
    """
    print("SELECT 9")
    print("9. Знайти список курсів, які відвідує студент (specific):")
    statement = (
        select(Student.fullname, Subject.name)
        .distinct()
        .join(Grade.student)
        .join(Grade.discipline)
        .where(Student.id == 15)
    )
    result = session.execute(statement).all()
    print(f"Student name\t\tsubjects")
    for (st_name, subj) in result:
        print(f"{st_name}\t\t{subj}")
    print("----------------------------------------")


def select_10():
    """
    SELECT DISTINCT
        st.fullname,
        t.fullname,
        sb.name
    FROM students st
    JOIN grades g ON g.student_id = st.id
    JOIN subjects sb ON g.subject_id = sb.id
    JOIN teachers t ON t.id = sb.teacher_id
    WHERE st.id = 15 AND t.id = 2;
    """
    print("SELECT 10")
    print("10. Список курсів, які певному студенту читає певний викладач (specific):")
    statement = (
        select(Student.fullname, Teacher.fullname, Subject.name)
        .distinct()
        .join(Grade.student)
        .join(Grade.discipline)
        .join(Subject.teacher)
        .where(and_(Student.id == 15, Teacher.id == 2))
    )
    result = session.execute(statement).all()
    print(f"Student name\t\tTeacher name\t\tSubject name")

    for st_name, t_name, sb_name in result:
        print(f"{st_name}\t\t{t_name}\t\t{sb_name}")
    print("----------------------------------------")

def select_11():
    """
    SELECT
        t.fullname,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM teachers t
    JOIN subjects sb ON sb.teacher_id = t.id
    JOIN grades g ON g.subject_id = sb.id
    JOIN students s ON g.student_id = s.id
    WHERE t.id = 4 AND s.id = 20;
    """
    print("SELECT 11 (additional)")
    print("11 (additional). Середній бал, який певний викладач ставить певному студентові (specific):")
    statement = (
        select(Teacher.fullname, Student.fullname, func.round(func.avg(Grade.grade), 2).label("average_grade"))
        .join(Grade.discipline)
        .join(Subject.teacher)
        .join(Grade.student)
        .where(and_(Student.id == 20, Teacher.id == 4))
        .group_by(Teacher.fullname, Student.fullname)
    )
    result = session.execute(statement).all()
    print(f"Student name\t\tTeacher name\t\taverage grade")
    for t_name, st_name, avg_grade in result:
        print(f"{t_name}\t\t{st_name}\t\t{avg_grade}")
    print("----------------------------------------")


def select_12():
    print("SELECT 12 (additional)")
    print("12 (additional). Оцінки студентів у певній групі з певного предмета на останньому занятті (specific):")
    subqr = (
        select(Group.id.label("group_id"), Grade.subjects_id.label("subject_id"),
               func.max(Grade.date_of).label("last_grade_date"))
        .join(Grade.student)
        .join(Student.group)
        .where(and_(Group.id == 2, Grade.subjects_id==3))
        .group_by(Group.id, Grade.subjects_id)
        .cte()
    )
    statement = (
        select(Group.name, Subject.name, Student.fullname, Grade.grade, Grade.date_of) # subqr.c.last_grade_date) #,  subqr.c.group_name)
        .join(Grade.student)
        .join(Student.group)
        .join(Grade.discipline)
        .where(and_(Group.id == subqr.c.group_id, Subject.id == subqr.c.subject_id, Grade.date_of==subqr.c.last_grade_date))
    )
    #print(statement)
    result = session.execute(statement).all()
    print(f"Group name\t\tSubject name\t\tStudent name\t\tGrade\t\tGrade date")
    for g_name, s_name, st_name, grade, tgt_date in result:
        print(f"{g_name}\t\t{s_name}\t\t{st_name}\t\t\t{grade}\t\t\t{tgt_date}")
    print("----------------------------------------")


if __name__ == "__main__":
    select_1()
    select_2()
    select_3()
    select_4()
    select_5()
    select_6()
    select_7()
    select_8()
    select_9()
    select_10()
    select_11()
    select_12()