#!/usr/bin/env python

#-----------------------------------------------------------------------
# create_c5.py
# Authors: Arin Champati, Chaz Bethel-Brescia
#-----------------------------------------------------------------------

from os import path, remove
from sys import argv, stderr, exit
from sqlalchemy import create_engine
from Database.session_maker import Session, engine

from Database.database import Database, Base
from Database.database import Users, Certificates, FifthClass
from Database.database import Liked, Disliked, Suggestions, DislikedSuggestions
from Database.database import Crosslistings, UnitaryWeights, CourseProfs, Professors
from Database.database import CourseEdges, CourseDetails
from Database.configs import DB_PASSWORD

import pickle

def view_tables():
    db = Database()
    
    session = Session()  # connects and returns engine and session
    # UNCOMMENT THIS IF YOU WANT TO VIEW WHAT IS ALREADY IN THE TABLES
    for user in session.query(Users).all():
        print(user.netid, user.name, user.year, user.dept, user.email)
        session.close()
    
    session = Session()
    for user in session.query(Certificates).all():
        print(user.netid, user.certificateid)
        session.close()
    
    session = Session()
    for user in session.query(FifthClass).all():
        print(user.netid, user.courseid)
        session.close()

    session = Session()
    for user in session.query(Liked).all():
        print(user.netid, user.courseid, user.order)
        session.close()
    
    session = Session()
    for user in session.query(Disliked).all():
        print(user.netid, user.courseid, user.order)    
        session.close()

    session = Session()
    for course in session.query(Crosslistings).all():
        print(course.courseid, course.dept_and_num) 
        session.close()

    session = Session()
    for course in session.query(UnitaryWeights).all():
        print(course.courseid, course.weight, course.num_liked, course.num_disliked, course.num_fifth)
        session.close()
    
    session = Session()
    for edge in session.query(CourseEdges).all():
        print(edge.courseid1, edge.courseid2, edge.weight)
        session.close()
    
    session = Session()
    for detail in session.query(CourseDetails).all()[100:200]:
        print(detail.term_code, detail.term, detail.description)
        session.close()
    
    session = Session()
    for course in session.query(CourseProfs).all():
        print(course.courseid, course.profid)
        session.close()
    
    session = Session()
    for prof in session.query(Professors).all():
        print(prof.profid, prof.profname)
        session.close()


def count_tables():
    db = Database()

    session = Session()
    print('Num Users:',len(session.query(Users).all()))
    print('Num Certificates:',len(session.query(Certificates).all()))
    print('Num Fifth Classes:', len(session.query(FifthClass).all()))
    print('Num Liked:', len(session.query(Liked).all()))
    print('Num Disliked:', len(session.query(Disliked).all()))
    print('Num Courses:', len(session.query(CourseDetails).all()))
    print('Num Crosslistings:', len(session.query(Crosslistings).all()))
    print('Num Unitary:', len(session.query(UnitaryWeights).all()))
    print('Num Edges:', len(session.query(CourseEdges).all()))
    print('Num Profs:', len(session.query(Professors).all()))
    session.close()


def authenticate():
    password = input("Please enter the password: ")
    
    if password != DB_PASSWORD:
        print('Incorrect Password', file=stderr)
        exit(1)

#-----------------------------------------------------------------------
# INITIALIZE USER TABLES
#-----------------------------------------------------------------------
def __populate_users_table(db, user_info):
    session = Session()

    Users.__table__.drop(engine)
    Users.__table__.create(engine)

    for userid in user_info['users']:
        user_data = user_info['users'].get(userid)
        db.update_user_info(session, userid, user_data.get('name'), user_data.get('class_year'), user_data.get('major'), user_data.get('email'))
    session.commit()
    session.close()


def __populate_certicates_table(db, user_info):
    session = Session()

    Certificates.__table__.drop(engine)
    Certificates.__table__.create(engine)

    for userid in user_info['certificates']:
        certificates = user_info['certificates'].get(userid)
        db.update_user_certificates(session, userid, certificates)
    session.commit()
    session.close()

def __populate_course_preference_tables(db, user_info):
    session = Session()

    Liked.__table__.drop(engine)
    Disliked.__table__.drop(engine)
    CourseEdges.__table__.drop(engine)
    UnitaryWeights.__table__.drop(engine)
    FifthClass.__table__.drop(engine)

    Liked.__table__.create(engine)
    Disliked.__table__.create(engine)
    CourseEdges.__table__.create(engine)
    UnitaryWeights.__table__.create(engine)
    FifthClass.__table__.create(engine)

    preferences = zip(user_info['fifth_classes'], user_info['liked_classes'], user_info['disliked_classes'])
    for userid, _, _ in preferences:
        liked = user_info['liked_classes'].get(userid)
        disliked = user_info['disliked_classes'].get(userid)
        fifth = user_info['fifth_classes'].get(userid)

        db.update_edges(session, userid, fifth, liked, disliked)

    session.commit()
    session.close()


#-----------------------------------------------------------------------
# INITIALIZE COURSE TABLES
#-----------------------------------------------------------------------
def __populate_crosslistings_table(db, course_info):
    session = Session()

    Crosslistings.__table__.drop(engine)
    Crosslistings.__table__.create(engine)

    db.update_crosslistings(session, course_info['crosslistings'])
    session.commit()
    session.close()


def __populate_coursedetails_table(db, course_info):
    session = Session()

    CourseDetails.__table__.drop(engine)
    CourseDetails.__table__.create(engine)

    # if there are pre-existing professors, delete them all
    details = session.query(CourseDetails).all()
    if details:
        session.query(CourseDetails).delete()

    db.update_course_details(session, course_info['courses'])
    session.commit()
    session.close()


def __populate_professor_table(db, course_info):
    session = Session()

    Professors.__table__.drop(engine)
    Professors.__table__.create(engine)

    db.update_professors(session, course_info['professors'])
    session.commit()
    session.close()

def __populate_course_profs_table(db, course_info):
    session = Session()

    CourseProfs.__table__.drop(engine)
    CourseProfs.__table__.create(engine)

    db.update_course_profs(session, course_info['course_profs'])
    session.commit()
    session.close()
    
#-----------------------------------------------------------------------
# INITIALIZE ALL TABLES
#-----------------------------------------------------------------------
def create_tables(user_info, course_info):
    authenticate()
    
    db = Database()

    __populate_users_table(db, user_info)
    print('populated user table')

    __populate_certicates_table(db, user_info)
    print('populated certificates table')

    __populate_course_preference_tables(db, user_info)
    print('populated course preferences tables')

    __populate_crosslistings_table(db, course_info)
    print('populated crosslistings table')

    __populate_coursedetails_table(db, course_info)
    print('populated coursedetails table')

    __populate_professor_table(db, course_info)
    print('populated professor table')

    __populate_course_profs_table(db, course_info)
    print('populated course profs table')


def initialize_database():
    # import user info as pickled datafile
    with open('DataSources/DataFiles/csv_user_info.pickle', 'rb') as handle:
        user_info = pickle.load(handle)
    
    with open('DataSources/DataFiles/course_info.pickle', 'rb') as handle:
        course_info = pickle.load(handle)

    create_tables(user_info, course_info)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    # CREATE DATABASE
    # initialize_database()

    # VIEW DATABASE
    # view_tables()

    # COUNT FIELDS IN DATABASE TABLES
    count_tables()

    # from sqlalchemy import text

    # sql = text("SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'd1glk585fbq096' AND pid <> pg_backend_pid();")
    # result = engine.execute(sql)
