import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Database.session_maker import Session, engine
from Database.database import Database, CourseEdges, FifthClass, Liked, Disliked, UnitaryWeights
import pickle
import traceback

db = Database()
session = Session()


entered_fifth = []
entered_fifth.append(db.get_courseid_from_deptnum(session, 'MUS 213'))

entered_liked = []
entered_liked.append(db.get_courseid_from_deptnum(session, 'MUS 213'))
entered_liked.append(db.get_courseid_from_deptnum(session, 'COS 226'))
entered_liked.append(db.get_courseid_from_deptnum(session, 'COS 333'))

entered_disliked = []
entered_disliked.append(db.get_courseid_from_deptnum(session, 'PHY 104'))
entered_disliked.append(db.get_courseid_from_deptnum(session, 'PHY 205'))

# try:
#     # Liked.__table__.drop(engine)
#     # Disliked.__table__.drop(engine)
#     # CourseEdges.__table__.drop(engine)
#     # UnitaryWeights.__table__.drop(engine)
#     # FifthClass.__table__.drop(engine)

#     # Liked.__table__.create(engine)
#     # Disliked.__table__.create(engine)
#     # CourseEdges.__table__.create(engine)
#     # UnitaryWeights.__table__.create(engine)
#     # FifthClass.__table__.create(engine)

#     db.update_edges(session, 'testing', entered_fifth, entered_liked, entered_disliked)
#     session.commit()
            
# except Exception as e:
#     print(e)
#     session.rollback()
#     traceback.print_exc()

# finally:
#     session.close()

def view_edges(course_list):
    for course1 in course_list:
        cross1 = db.get_crosslistings(session, course1)
        print(cross1)
        courses = session.query(CourseEdges).filter_by(courseid1=course1).all()

        unitary = session.query(UnitaryWeights).filter_by(courseid=course1).first()
        print(unitary.weight, unitary.num_liked, unitary.num_disliked, unitary.num_fifth)

        for course2 in courses:
            cross2 = db.get_crosslistings(session, course2.courseid2)
            print(f'{cross1} -> {cross2} : {course2.weight}')



try:

    courseid = db.get_courseid_from_deptnum(session, 'COS 226')
    view_edges([courseid])
    unitary = session.query(UnitaryWeights).filter_by(courseid=courseid).first()
    print(unitary.weight, unitary.num_liked, unitary.num_disliked, unitary.num_fifth)
            
except Exception as e:
    print(e)
    session.rollback()
    traceback.print_exc()

finally:
    session.close()


# print()
# print('FIFTH')
# view_edges(entered_fifth)

# print()
# print('LIKED')
# view_edges(entered_liked)

# print()
# print('DISLIKED')
# view_edges(entered_disliked)
# print()
        


# db.update_user_info(session, 'testing', 'TEST', 2022, 'COS', 'testing@princeton.edu')
# db.delete_edges(session, 'testing')
# db.add_edges(session, 'testing', [])

# fifth_before = db.get_fav_fifth(session,'testing')
# liked_before = db.get_liked(session,'testing')
# disliked_before = db.get_disliked(session,'testing')

# print('BEFORE')
# print('CROSSLISTINGS')
# print(fifth_before)
# print(liked_before)
# print(disliked_before)



# cross = db.get_crosslistings(session, '001391')
# print(cross)

# courses = session.query(CourseEdges).filter_by(courseid1=courseid).all()
# for course in courses:
#     cross1 = db.get_crosslistings(session, course.courseid1)
#     cross2 = db.get_crosslistings(session, course.courseid2)
#     print(f'{cross1} -----> {cross2} : {course.weight}')

# courses = session.query(UnitaryWeights).filter_by(courseid=courseid).all()
# for course in courses:
#     print(course.courseid, course.weight, course.num_liked, course.num_disliked, course.num_fifth)
