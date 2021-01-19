#!/usr/bin/env python

# -----------------------------------------------------------------------
# database_c5.py
# Author: Chaz Bethel-Brescia & Arin Champati
# -----------------------------------------------------------------------

from os import path, remove
from sys import argv, stderr, exit
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from psycopg2 import connect

from DataSources.DataFiles.AreasOfStudy import MAJOR_TO_CODE, CODE_TO_CERTIFICATE
import pickle

# -----------------------------------------------------------------------
FIFTH_WEIGHT = 1
LIKED_WEIGHT = 1
DISLIKED_WEIGHT = 1

Base = declarative_base()

class Users (Base):
    __tablename__ = 'users'
    netid = Column(String, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    dept = Column(String)
    email = Column(String)


class Certificates (Base):
    __tablename__ = 'certificateids'
    netid = Column(String, primary_key=True)
    certificateid = Column(Integer, primary_key=True)
    order = Column(Integer)


# class CertificateNames (Base):
#     __tablename__ = 'certificatenames'
#     certificateid = Column(String, primary_key=True)
#     certificatename = Column(String)


class FifthClass (Base):
    __tablename__ = 'class5'
    netid = Column(String, primary_key=True)
    courseid = Column(String, primary_key=True)
    order = Column(Integer)


class Liked (Base):
    __tablename__ = 'liked'
    netid = Column(String, primary_key=True)
    courseid = Column(String, primary_key=True)
    order = Column(Integer)


class Disliked (Base):
    __tablename__ = 'disliked'
    netid = Column(String, primary_key=True)
    courseid = Column(String, primary_key=True)
    order = Column(Integer)


class Suggestions (Base):
    __tablename__ = 'suggestions'
    netid = Column(String, primary_key=True)
    courseid = Column(String, primary_key=True)
    score = Column(Integer)
    rank = Column(Integer)


class DislikedSuggestions (Base):
    __tablename__ = 'dis_suggestions'
    netid = Column(String, primary_key=True)
    courseid = Column(String, primary_key=True)


class CourseEdges (Base):
    __tablename__ = 'course_edges'
    courseid1 = Column(String, primary_key=True)
    courseid2 = Column(String, primary_key=True)
    weight = Column(Integer)


# class FifthCourseEdges (Base):
#     __tablename__ = 'fifth_course_edges'
#     edge = Column(String, primary_key=True)
#     courseid1 = Column(String)
#     courseid2 = Column(String)
#     weight = Column(Integer)


class UnitaryWeights(Base):
    __tablename__ = 'unitary_weights'
    courseid = Column(String, primary_key=True)
    weight = Column(Integer)
    num_liked = Column(Integer)
    num_disliked = Column(Integer)
    num_fifth = Column(Integer)


class Crosslistings (Base):
    __tablename__ = 'crosslistings'
    courseid = Column(String, primary_key=True)
    dept_and_num = Column(String, primary_key=True)
    order = Column(Integer)


class CourseDetails (Base):
    __tablename__ = 'course_details'
    courseid = Column(String, primary_key=True)
    description = Column(String)
    title = Column(String)
    term = Column(String)
    term_code = Column(Integer)
    department_name = Column(String)


class CourseProfs (Base):
    __tablename__ = 'courseprofs'
    courseid = Column(String, primary_key=True)
    profid = Column(String, primary_key=True)


class Professors (Base):
    __tablename__ = 'professors'
    profid = Column(String, primary_key=True)
    profname = Column(String)

#--------------------------------------------------------------------

class Database:
    # def __init__(self):
    #     self._engine = None
    #     self._session = None


    # def connect(self):
    #     """
    #     Connects to database, sets and returns database's engine and session
    #     """
    #     if self._engine is None:
    #         connect_stmt = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    #         self._engine = create_engine(connect_stmt)
        
    #     engine = self._engine
    #     Session = sessionmaker(bind=engine)
    #     session = Session()

    #     self._session = session

    #     return engine, session


    # def disconnect(self):
    #     self._session.close()

    # ---------------------------------------------------------------
    # UPDATE a user and propagate the information through the database
    # These are the higher level functions that should be called
    # in clients of this database class
    # ---------------------------------------------------------------
    
    # ---------------------------------------------------------------
    # UPDATE USER TABLES
    # ---------------------------------------------------------------
    def update_user_info(self, session, netid, name, year, dept, email):
        """
        update user information if it exists in the database, otherwise create a new user entry
        """
        user = session.query(Users).filter_by(netid=netid).first()
        # initialize this user into the database if they aren't in it already
        if not user:
            user = Users(netid=netid, name=name, year=year, dept=dept, email=email)
            session.add(user)

        # otherwise update the user information (except for netid)
        else:
            user.name = name
            user.year = year
            user.dept = dept
            user.email = email
            session.flush()


    
    def update_user_certificates(self, session, netid, certificateids):
        """
        update user certificates if it exists in the database, otherwise, delete
        all old information and create new user entries
        """ 
        user_certs = session.query(Certificates).filter_by(netid=netid).all()

        # if there are pre-existing certificates, delete them all
        if user_certs:
            session.query(Certificates).filter_by(netid=netid).delete()
        

        # if the user has no certificates to enter, exit this function
        if not certificateids:
            return

        # repopulate the certificates
        for i, cert_id in enumerate(certificateids):
            if cert_id == '':
                continue
            else: 
                cert = Certificates(netid=netid, certificateid=cert_id, order=i)
                session.add(cert)
            


    def update_user_class_info(self, session, netid, fifth_class, liked_list, disliked_list):
        """
        adds all user class preferences
        """
        self.update_user_fifth_class(session, netid, fifth_class)
        self.update_user_liked_classes(session, netid, liked_list)
        self.update_user_disliked_classes(session, netid, disliked_list)



    # ---------------------------------------------------------------
    # REMOVE USER TABLES
    # ---------------------------------------------------------------

    # May not need this functionality

    # ---------------------------------------------------------------
    # ADD INTO USER TABLES
    # ---------------------------------------------------------------
    # def add_user_info(self, netid, name, year, dept, email):
    #     try:
    #         user = Users(netid=netid, name=name, year=year, dept=dept, email=email)
    #         self._session.add(user)
    #         self._session.commit()
    #     except Exception as e:
    #         print('Error adding user info to database', file=stderr)
    #         return False, e
        
    #     return True, ''
    

    # def add_user_fifth_class(self, netid, fifth_class):
    #     try:
    #         if fifth_class == '':
    #             fifth_class = 0
    #         course = FifthClass(netid=netid, courseid=fifth_class)
    #         self._session.add(course)
    #         self._session.commit()
    #     except Exception as e:
    #         print("Error adding user's favorite fifth class to database'", file=stderr)
    #         return False, e

    #     return True, ''


    # def add_user_liked_class(self, netid, liked_class):
    #     try:
    #         if liked_class == '':
    #             liked_class = 0
    #         course = Liked(netid=netid, courseid=liked_class)
    #         self._session.add(course)
    #         self._session.commit()
    #     except Exception as e:
    #         print("Error adding user's liked class to database'", file=stderr)
    #         return False, e

    #     return True, ''

    
    # def add_user_disliked_class(self, netid, disliked_class):
    #     try: 
    #         if disliked_class == '':
    #             disliked_class = 0
    #         course = Disliked(netid=netid, courseid=disliked_class)
    #         self._session.add(course)
    #         self._session.commit()
    #     except Exception as e:
    #         print("Error adding user's disliked class to database", file=stderr)
    #         return False, e
        
    #     return True, ''


    # ---------------------------------------------------------------
    # COURSE TABLES
    # ---------------------------------------------------------------
    # def update_certids(self, session):
    #     """
    #     Update certificateids in the database
    #     """
    #     cert_names = session.query(CertificateNames).all()

    #     # if there are pre-existing certificatesnames, delete them all
    #     if cert_names:
    #         session.query(CertificateNames).delete()

    #     for cert_id in CODE_TO_CERTIFICATE:
    #         certificateids = CertificateNames(
    #             certificateid=cert_id, certificatename=CODE_TO_CERTIFICATE[cert_id])
    #         session.add(certificateids)


    def update_crosslistings(self, session, crosslistings_dict):
        """
        Update crosslistings in the database
        """
        for courseid in crosslistings_dict:
            cross = session.query(Crosslistings).filter(Crosslistings.courseid==courseid).first()
            # if it already exists, delete it
            if cross:
                cross = session.query(Crosslistings).filter(Crosslistings.courseid==courseid).delete()

            for i, dept_and_num in enumerate(crosslistings_dict[courseid]):
                crosslisting = Crosslistings(courseid=courseid, dept_and_num=str(dept_and_num), order=i)
                session.add(crosslisting)


    def update_course_profs(self, session, courseprofs):
        """
        Update professors for a particular course in the database
        """
        for courseid in courseprofs:
            # if there was a row with these items before, delete it
            courseprof = session.query(CourseProfs).filter_by(courseid=courseid).all()
            if courseprof:
                session.query(CourseProfs).filter_by(courseid=courseid).delete()

            for profid in courseprofs[courseid]:
                courseprof = CourseProfs(courseid=courseid, profid=profid)
                session.add(courseprof)


    def update_professors(self, session, professors):
        """
        Update professors (profid to profname) in the database
        """
        for profid in professors:
            # if there was a row with this item before, delete it
            professor = session.query(Professors).filter_by(profid=profid).one_or_none()
            if professor:
                session.query(Professors).filter_by(profid=profid).delete()

            profname = professors[profid]
            professor = Professors(profid=profid, profname=profname)
            session.add(professor)


    def update_course_details(self, session, courses):
        """
        Update course descriptions and terms in the database
        """
        for courseid in courses:
            descrip = courses[courseid]['descrip']
            term = courses[courseid]['term']
            term_code = courses[courseid]['term_code']
            title = courses[courseid]['title']
            department_name = courses[courseid]['department_name']

            # if there was a row with this item before, delete it
            details = session.query(CourseDetails).filter_by(courseid=courseid).one_or_none()
            if details:
                session.query(CourseDetails).filter_by(courseid=courseid).delete()

            details = CourseDetails(courseid=courseid, description=descrip, term=term, term_code=term_code, title=title, department_name=department_name)
            session.add(details)


    # ---------------------------------------------------------------
    # UPDATE EDGES, WEIGHTS, AND CLASSES
    # ---------------------------------------------------------------
    # def update_user_fifth_class(self, session, netid, courseid):
    #     # if the user has no "fifth class" to enter, exit this function
    #     if not courseid:
    #         return
        
    #     fifth_class = session.query(FifthClass).filter_by(netid=netid).first()

    #     # if there are pre-existing fifth class, delete it
    #     # subtract 1 from fifth class count and liked count
    #     if fifth_class:
    #         self.update_unitary_weight(session, fifth_class.courseid, weight=-1, num_liked=-1, num_disliked=0, num_fifth=-1)

    #         session.query(FifthClass).filter_by(netid=netid).delete()
    #         session.flush()

    #     # repopulate the fifth_class and add one to the fifth class count
    #     if courseid == '':
    #         pass
    #     else:
    #         self.update_unitary_weight(session, courseid, weight=1, num_liked=1, num_disliked=0, num_fifth=1)

    #         course = FifthClass(netid=netid, courseid=courseid)
    #         session.add(course)     

    def update_edges(self, session, netid, entered_fifth, entered_liked, entered_disliked):
        db_fifth = session.query(FifthClass).filter_by(netid=netid).all()
        db_liked = session.query(Liked).filter_by(netid=netid).all()
        db_disliked = session.query(Disliked).filter_by(netid=netid).all()

        self.delete_edges(session, netid, entered_fifth, entered_liked, entered_disliked, db_fifth, db_liked, db_disliked)
        self.add_edges(session, netid, entered_fifth, entered_liked, entered_disliked, db_fifth, db_liked, db_disliked)


    def __delete_edges_helper(self, session, course_type, course_list, db_fifth, db_liked, db_disliked):
        """
        course_type: {str} string name of course type (fifth or liked)
        course_list: {list} list of edges from

        deletes edges from course_list_type to the other inputs
        """

        if course_type == 'fifth':
            liked_weight = FIFTH_WEIGHT
        elif course_type == 'liked':
            liked_weight = LIKED_WEIGHT
        
        fifth_weight = FIFTH_WEIGHT
        disliked_weight = DISLIKED_WEIGHT

        
        for course1 in course_list:
            if course1 == '' or course1 == None:
                    continue

            # update edge for courses-liked relationship
            for course2 in db_liked:
                if course1 == course2:
                    continue
                if course2 == '' or course2 == None:
                    continue

                # decrement relationship
                self.update_edge_weight(session, course1, course2, -liked_weight)
            
            # update edge for courses-fifth relationship
            for course2 in db_fifth:
                if course1 == course2:
                    continue
                if course2 == '' or course2 == None:
                    continue

                # decrement relationship (-2 becuase fifth class is special)
                self.update_edge_weight(session, course1, course2, -fifth_weight)
            
            # update edge for courses-disliked relationship
            for course2 in db_disliked:
                if course1 == course2:
                    continue
                if course2 == '' or course2 == None:
                    continue

                # increment relationship
                self.update_edge_weight(session, course1, course2, disliked_weight)


    def delete_edges(self, session, netid, entered_fifth, entered_liked, entered_disliked, db_fifth, db_liked, db_disliked):
        """
        This will query the database and it will delete the necessary edges, 
        update the unitaries, and update the user liked / disliked / fifth class
        """

        # convert everything to courseid lists
        if db_fifth:
            db_fifth = [course.courseid for course in db_fifth]
        else:
            db_fifth = []
        
        if db_liked:
            db_liked = [course.courseid for course in db_liked]
        else:
            db_liked = []
        
        if db_disliked:
            db_disliked = [course.courseid for course in db_disliked]
        else:
            db_disliked = []
        
        # greedily remove duplicates (between fifth and liked) from liked
        for course in db_fifth:
            if course in db_liked:
                db_liked.remove(course)


        # note: if the entered fifth or liked is none, we need to update edges for the old data
        # delete the edges that are connected to db_fifth and db_liked
        self.__delete_edges_helper(session, 'fifth', db_fifth, db_fifth, db_liked, db_disliked)
        self.__delete_edges_helper(session, 'liked', db_liked, db_fifth, db_liked, db_disliked)


        # now, remove the user's fifth class, liked, and disliked from the database
        if db_fifth:
            session.query(FifthClass).filter_by(netid=netid).delete()

        if db_liked:
            session.query(Liked).filter_by(netid=netid).delete()

        if db_disliked:
            session.query(Disliked).filter_by(netid=netid).delete()

        # for every course in db_fifth, db_liked, and db_disliked, update the unitary
        for course in db_fifth:
            if course and course != '':
                self.update_unitary_weight(session, course, weight=-1, num_liked=-1, num_disliked=0, num_fifth=-1)
        
        for course in db_liked:
            if course and course != '':
                self.update_unitary_weight(session, course, weight=-1, num_liked=-1, num_disliked=0, num_fifth=0)
        
        for course in db_disliked:
            if course and course != '':
                self.update_unitary_weight(session, course, weight=1, num_liked=0, num_disliked=-1, num_fifth=0)
    


    def __add_edges_helper(self, session, course_type, course_list, entered_fifth, entered_liked, entered_disliked):
        """
        course_type: {str} string name of course type (fifth or liked)
        course_list: {list} list of edges from
        runs the for loop of deletion

        deletes edges from course_list_type to the other inputs
        """
        if course_type == 'fifth':
            liked_weight = FIFTH_WEIGHT
        elif course_type == 'liked':
            liked_weight = LIKED_WEIGHT
        
        fifth_weight = FIFTH_WEIGHT
        disliked_weight = DISLIKED_WEIGHT
        
        for course1 in course_list:
            if course1 == '' or course1 == None:
                    continue

            # update edge for courses-liked relationship
            for course2 in entered_liked:
                if course1 == course2:
                    continue
                if course2 == '' or course2 == None:
                    continue

                # increment relationship
                self.update_edge_weight(session, course1, course2, liked_weight)
            
            # update edge for courses-fifth relationship
            for course2 in entered_fifth:
                if course1 == course2:
                    continue
                if course2 == '' or course2 == None:
                    continue

                # increment relationship (2 becuase fifth class is special)
                self.update_edge_weight(session, course1, course2, fifth_weight)
            
            # update edge for courses-disliked relationship
            for course2 in entered_disliked:
                if course1 == course2:
                    continue
                if course2 == '' or course2 == None:
                    continue

                # decrement relationship
                self.update_edge_weight(session, course1, course2, -1)


    def add_edges(self, session, netid, entered_fifth, entered_liked, entered_disliked, db_fifth, db_liked, db_disliked):
        """
        This will query the database and it will add the necessary edges, 
        update the unitaries, and update the user liked / disliked / fifth class

        Entered_liked: list of liked inputted courseids that 
        are meant to be added to the database

        Entered_disliked: list of disliked inputted courseids that 
        are meant to be added to the database

        Entered_fifth: list of inputted fifth class courseids that 
        are meant to be added to the database
        """

        # convert everything to courseid lists
        if db_fifth:
            db_fifth = [course.courseid for course in db_fifth]
        else:
            db_fifth = []
        
        if db_liked:
            db_liked = [course.courseid for course in db_liked]
        else:
            db_liked = []
        
        if db_disliked:
            db_disliked = [course.courseid for course in db_disliked]
        else:
            db_disliked = []

        # IF THE INPUT IS NONE, WE CANNOT UPDATE THE EDGES TO (we will update edges from the existing data) THAT SET OF COURSES
        if not entered_fifth:  
            entered_fifth = []
            entered_fifth_valid = db_fifth
        else:
            entered_fifth_valid = entered_fifth

        if not entered_liked:
            entered_liked = []
            entered_liked_valid = db_liked
        else:
            entered_liked_valid = entered_liked
        
        if not entered_disliked:
            entered_disliked = []
            entered_disliked_valid = db_disliked
        else:
            entered_disliked_valid = entered_disliked
        
        # ADD the user's courses to the database
        # enumerate the lists so we can store them with an order variable
        enumerated_fifth_valid = [(course, i) for i, course in enumerate(entered_fifth_valid)]
        enumerated_liked_valid = [(course, i) for i, course in enumerate(entered_liked_valid)]
        enumerated_disliked_valid = [(course, i) for i, course in enumerate(entered_disliked_valid)]

        for course, order in enumerated_fifth_valid:
            if course and course != '':
                fifth = FifthClass(netid=netid, courseid=course, order=order)
                session.add(fifth)
        
        for course, order in enumerated_liked_valid:
            if course and course != '':
                liked = Liked(netid=netid, courseid=course, order=order)
                session.add(liked)
        
        for course, order in enumerated_disliked_valid:
            if course and course != '':
                disliked = Disliked(netid=netid, courseid=course, order=order)
                session.add(disliked)
        

        # greedily remove duplicates (between fifth and liked) from liked
        for course in entered_fifth_valid:
            if course in entered_liked_valid:
                entered_liked_valid.remove(course)
        
        # add the edges that are connected to entered_fifth and entered_liked
        # note: if there is an invalid fifth or liked list, we need to still update edges from the 
        # existing data to valid entered data
        self.__add_edges_helper(session, 'fifth', entered_fifth_valid, entered_fifth_valid, entered_liked_valid, entered_disliked_valid)
        self.__add_edges_helper(session, 'liked', entered_liked_valid, entered_fifth_valid, entered_liked_valid, entered_disliked_valid)

        # for every course in db_fifth, db_liked, and db_disliked, update the unitary
        for course in entered_fifth_valid:
            if course and course != '':
                self.update_unitary_weight(session, course, weight=1, num_liked=1, num_disliked=0, num_fifth=1)
        
        for course in entered_liked_valid:
            if course and course != '':
                self.update_unitary_weight(session, course, weight=1, num_liked=1, num_disliked=0, num_fifth=0)
        
        for course in entered_disliked_valid:
            if course and course != '':
                self.update_unitary_weight(session, course, weight=-1, num_liked=0, num_disliked=1, num_fifth=0)


    # def update_user_liked_classes(self, session, netid, liked_classes):
    #     """
    #     Update user liked classes if they exist in the database, deleting 
    #     all old information and create new user entries
    #     """
    #     # if the user has no liked classes to enter, exit this function
    #     if not liked_classes:
    #         liked_classes = []
        
    #     liked_classes = [(course, i) for i, course in enumerate(liked_classes)]
    #     old_liked = session.query(Liked).filter_by(netid=netid).all()
    #     disliked = session.query(Disliked).filter_by(netid=netid).all()

    #     # get the courses that need to be deleted from the database
    #     # and get the courses that need to be added in the database
    #     # everything else will remain the same
    #     if not old_liked:  
    #         old_liked = []      # initialize the array if it is None so we can iterate

    #     old_liked = [(course.courseid, course.order) for course in old_liked]
    #     disliked = [(course.courseid, course.order) for course in disliked]

    #     add_liked = set(liked_classes).difference(old_liked)
    #     delete_liked = set(old_liked).difference(liked_classes)


    #     # delete from the database the courses that must be deleted
    #     for course1 in delete_liked:
    #         if course1[0] == '' or course1[0] == None:
    #             continue
    #         session.query(Liked).filter_by(netid=netid, courseid=course1[0]).delete()
    #         self.update_unitary_weight(session, course1[0], weight=-1, num_liked=-1, num_disliked=0, num_fifth=0) 

    #         # decrement the liked-liked edge relationship
    #         for course2 in old_liked:
    #             if course1[0] == course2[0]:
    #                 continue
    #             if course2[0] == '' or course2[0] == None:
    #                 continue

    #             # two way relationship delete
    #             self.update_edge_weight(session, course1[0], course2[0], -1)

    #         # increment the liked-disliked edge relationship
    #         for course2 in disliked:
    #             if course1[0] == course2[0]:
    #                 continue
    #             if course2[0] == '' or course2[0] == None:
    #                 continue

    #             self.update_edge_weight(session, course1[0], course2[0], 1)
        

    #     # add to the database the courses that must be added
    #     for course1 in add_liked:
    #         if course1[0] == '' or course1[0] == None:
    #             continue
    #         course = Liked(netid=netid, courseid=course1[0], order=course1[1])
    #         session.add(course)
    #         self.update_unitary_weight(session, course1[0], weight=1, num_liked=1, num_disliked=0, num_fifth=0) 

    #         # increment the liked-liked edge relationship
    #         for course2 in liked_classes:
    #             if course1[0] == course2[0]:
    #                 continue
    #             if course2[0] == '' or course2[0] == None:
    #                 continue

    #             # add two way relationship
    #             self.update_edge_weight(session, course1[0], course2[0], 1)

    #         for course2 in disliked:
    #             if course1[0] == course2[0]:
    #                 continue
    #             if course2[0] == '' or course2[0] == None:
    #                 continue
    #             self.update_edge_weight(session, course1[0], course2[0], -1)


    # def update_user_disliked_classes(self, session, netid, disliked_classes):
    #     """
    #     Update user disliked courses if they exist in the database, deleting
    #     all old information and create new user entries
    #     """
    #     # if the user has no disliked classes to enter, exit this function
    #     if not disliked_classes:
    #         disliked_classes = []
        
    #     disliked_classes = [(course, i) for i, course in enumerate(disliked_classes)]
    #     old_disliked = session.query(Disliked).filter_by(netid=netid).all()
    #     liked = session.query(Liked).filter_by(netid=netid).all()

    #     # get the courses that need to be deleted from the database
    #     # and get the courses that need to be added in the database
    #     # everything else will remain the same
    #     if not old_disliked:  
    #         old_disliked = []      # initialize the array if it is None so we can iterate

    #     old_disliked = [(course.courseid, course.order) for course in old_disliked]
    #     liked = [(course.courseid, course.order) for course in liked]

    #     add_disliked = set(disliked_classes).difference(old_disliked)
    #     delete_disliked = set(old_disliked).difference(disliked_classes)

    #     # delete from the database the courses that must be deleted
    #     for course1 in delete_disliked:
    #         if course1[0] == '' or course1[0] == None:
    #             continue
    #         session.query(Disliked).filter_by(netid=netid, courseid=course1[0]).delete()
    #         self.update_unitary_weight(session, course1[0], weight=1, num_liked=0, num_disliked=-1, num_fifth=0)

    #         # increment the liked-disliked edge relationship
    #         for course2 in liked:
    #             if course1[0] == course2[0]:
    #                 continue
    #             if course2[0] == '' or course2[0] == None:
    #                 continue

    #             self.update_edge_weight(session, course2[0], course1[0], 1)
            

    #     # add to the database the courses that must be added
    #     for course1 in add_disliked:
    #         if course1[0] == '' or course1[0] == None:
    #             continue
    #         course = Disliked(netid=netid, courseid=course1[0], order=course1[1])
    #         session.add(course)
    #         self.update_unitary_weight(session, course1[0], weight=-1, num_liked=0, num_disliked=1, num_fifth=0) 

    #         # decrement the liked-disliked edge relationship
    #         for course2 in liked:
    #             if course1[0] == course2[0]:
    #                 continue
    #             if course2[0] == '' or course2[0] == None:
    #                 continue
    #             self.update_edge_weight(session, course2[0], course1[0], -1)

    def delete_user(self, session, netid):
        """
        Deletes a user from the database (for testing purposes)
        """
        db_fifth = session.query(FifthClass).filter_by(netid=netid).all()
        db_liked = session.query(Liked).filter_by(netid=netid).all()
        db_disliked = session.query(Disliked).filter_by(netid=netid).all()

        self.delete_edges(session, netid, db_fifth, db_liked, db_disliked, db_fifth, db_liked, db_disliked)
        
        session.query(FifthClass).filter_by(netid=netid).delete()
        session.query(Users).filter_by(netid=netid).delete()
        session.query(Liked).filter_by(netid=netid).delete()
        session.query(Disliked).filter_by(netid=netid).delete()
        session.query(Certificates).filter_by(netid=netid).delete()
        session.query(Suggestions).filter_by(netid=netid).delete()
        session.query(DislikedSuggestions).filter_by(netid=netid).delete()
    

    # ---------------------------------------------------------------
    # MANIPULATE SUGGESTIONS
    # ---------------------------------------------------------------
    # Returns a list of the top k unitary weighted courseIds
    def get_top_unitary(self, session, k, seen_suggestions):
        """
        Fetch the top k most popular courses from the database
        """
        popular_classes = session.query(UnitaryWeights)\
            .order_by(UnitaryWeights.weight.desc(), UnitaryWeights.num_liked.desc()).all()
            
        top_k_list = []
        for i in range(len(popular_classes)):
            if (len(top_k_list) > k):
                break
            course = popular_classes[i]
            if course != None and not (course.courseid in seen_suggestions):
                if course.num_liked > 0:
                    top_k_list.append(course.courseid)

        return top_k_list
    
    # Returns a list of the bottom k unitary weighted courseIds
    def get_bottom_unitary(self, session, k, seen_suggestions):
        """
        Fetch the top k most popular courses from the database
        """
        least_popular_classes = session.query(UnitaryWeights)\
            .order_by(UnitaryWeights.weight.asc(), UnitaryWeights.num_disliked.desc()).all()
                
        bottom_k_list = []
        for i in range(len(least_popular_classes)):
            if (len(bottom_k_list) > k):
                break
            course = least_popular_classes[i]
            if course != None and not (course.courseid in seen_suggestions):
                if course.num_disliked > 0:
                    bottom_k_list.append(course.courseid)

        return bottom_k_list

    # Retrieve a list of the top k most popular 'fifth courses'
    def get_top_favorites(self, session, k, seen_suggestions):
        # Can maybe optimize with a join?
        fifthClasses = session.query(FifthClass).all()
        courseIds = {fifthClass.courseid : 0 for fifthClass in fifthClasses}

        unitaryWeights = session.query(UnitaryWeights)\
            .filter(UnitaryWeights.courseid.in_(courseIds))\
                .order_by(UnitaryWeights.num_fifth.desc(), UnitaryWeights.weight.desc(), UnitaryWeights.num_liked.desc()).all()

        top_k_list = []
        n = min(k, len(unitaryWeights))

        for i in range(n):
            course = unitaryWeights[i]
            if course != None and not (course.courseid in seen_suggestions):
                if course.num_fifth > 0:
                    top_k_list.append(course.courseid)
        
        return top_k_list, len(unitaryWeights)



    
    def update_disliked_suggestions(self, session, netid, disliked_suggestions):
        # remove disliked suggestions
        session.query(DislikedSuggestions).filter_by(netid=netid).delete()

        if not disliked_suggestions or disliked_suggestions == '':
            return

        for courseid in disliked_suggestions:
            # add course to user's disliked suggestions
            disliked_sugg = DislikedSuggestions(netid=netid, courseid=courseid)
            session.add(disliked_sugg)
    

    def refresh_suggestions(self, session, netid, disliked_id):
        """
        Update user's disliked suggestions, and return updated list of liked suggestions.
        Method takes in the courseid of a disliked suggestion, and returns a refreshed
        list of suggested courseids
        """
        # if the user has no disliked suggestions to update, exit this function
        if not disliked_id or disliked_id == '':
            return

        # remove disliked suggestion from suggestions list 
        session.query(Suggestions).filter_by(netid=netid, courseid=disliked_id).delete()

        # add course to user's disliked suggestions
        disliked_sugg = DislikedSuggestions(netid=netid, courseid=disliked_id)
        session.add(disliked_sugg)

        # repopulate suggestions list, adding next-ranked suggested course 
        refreshed_sugg = self.get_suggestions(session, netid)

        return refreshed_sugg


    def remove_disliked_suggestion(self, session, netid, disliked_id):
        """
        Remove a user's disliked suggestion
        """
        # if the user has no disliked suggestions to update, exit this function
        if not disliked_id or disliked_id == '':
            return

        # remove disliked suggestion from suggestions list 
        session.query(DislikedSuggestions).filter_by(netid=netid, courseid=disliked_id).delete()
        


    # ---------------------------------------------------------------
    # MANIPULATE GRAPH ELEMENTS
    # ---------------------------------------------------------------
    def update_unitary_weight(self, session, courseid, weight, num_liked, num_disliked, num_fifth):
        """
        update a unitary weight if it exists, create a new entry otherwise
        """
        unitary = session.query(UnitaryWeights).filter_by(courseid=courseid).first()
        if not unitary:
            unitary = UnitaryWeights(courseid=courseid, weight=weight, num_liked=num_liked, num_disliked=num_disliked, num_fifth=num_fifth)
            session.add(unitary)
        else:
            unitary.weight = UnitaryWeights.weight + weight
            unitary.num_liked = UnitaryWeights.num_liked + num_liked
            unitary.num_disliked = UnitaryWeights.num_disliked + num_disliked
            unitary.num_fifth = UnitaryWeights.num_fifth + num_fifth
            session.flush()
            

    def update_edge_weight(self, session, courseid1, courseid2, weight):
        """
        update a course edge weight if it exists, create a new entry otherwise
        """
        edge = session.query(CourseEdges).filter_by(courseid1=courseid1, courseid2=courseid2).first()
        if not edge:
            edge = CourseEdges(courseid1=courseid1, courseid2=courseid2, weight=weight)
            session.add(edge)
        else:
            edge.weight = CourseEdges.weight + weight
            session.flush()


    # ---------------------------------------------------------------
    # GET from database
    # ---------------------------------------------------------------
    def get_unitary_dict(self, session):
        unitary_dict = {}
        for unitary in session.query(UnitaryWeights).all():
            unitary_dict[unitary.courseid] = unitary.weight

        return unitary_dict

    
    def get_edges_dict(self, session):
        edge_dict = {}
        for edge in session.query(CourseEdges).all():
            if edge.courseid1 not in edge_dict:
                edge_dict[edge.courseid1] = {edge.courseid2: edge.weight}
            else:
                edge_dict[edge.courseid1][edge.courseid2] =  edge.weight

        return edge_dict

    
    # get the top edges from a course
    def get_top_edges_from(self, session, courseid, num_edges):

        # we get the courseid2's from courseedges
        # secondary sort on unitary weights
        edges = session.query(CourseEdges)\
            .join(UnitaryWeights, UnitaryWeights.courseid == CourseEdges.courseid2)\
            .filter(CourseEdges.courseid1==courseid)\
            .order_by(CourseEdges.weight.desc(), UnitaryWeights.weight.desc())\
            .all()
        
        edges = edges[:num_edges]
        
        # return a list of deptnums if the unitary score is over 0
        edges_from = []
        for edge in edges:
            if edge.weight > 0:
                crosslistings = self.get_crosslistings(session, edge.courseid2)
                course_name = ' / '.join(crosslistings)
                edges_from.append(course_name)
        
        return edges_from
 
    # temporary function to return user data for prototype
    def get_user_info(self, session, netid):
        user = session.query(Users).filter_by(netid=netid).one_or_none()
        if user is None:
            return {'name': '', 'year': '', 'dept': '', 'email': ''}

        if user.email:
            email = user.email.lower()
        else:
            email = None

        name, year, dept, email = user.name, user.year, user.dept, email

        return {'name': name, 'year': year, 'dept': dept, 'email': email}
    
    
    def get_certificates(self, session, netid):
        certificate_list = []
        for certificateid in session.query(Certificates.certificateid).filter_by(netid=netid).all():
            certificate_name = CODE_TO_CERTIFICATE.get(certificateid[0])
            certificate_list.append(certificate_name)
        
        return certificate_list
    
    def get_all_course_info(self, session, courseid):
        course_info = {}
        course_details = self.get_course_details(session, courseid)
        course_numbers = self.get_course_numbers(session, courseid)
        course_profs = self.get_course_profs(session, courseid)
        # course_profs = {'hi': 'hi'}

        
        return {'course_details': course_details, 'course_numbers': course_numbers, 'course_profs': course_profs}

    
    def get_course_details(self, session, courseid):
        course_details = {'courseid': '', 'term_code': '', 'term': '', 'description': '', 'title': '', 'department_name': ''}
        if courseid is None:
            return course_details

        details = session.query(CourseDetails).filter_by(courseid=courseid).one_or_none()
        if not details:
            return course_details
        else:
            return {'courseid': courseid, 'term_code': details.term_code, 'term': details.term, 'title': details.title, 'description': details.description, 'department_name': details.department_name}

    
    def get_course_numbers(self, session, courseid):
        course_numbers = {'num_liked': 0, 'num_disliked': 0}
        if not courseid:
            return course_numbers
        
        course_numbers = course_numbers

        unitary = session.query(UnitaryWeights).filter_by(courseid=courseid).one_or_none()
        if unitary:
            return {'num_liked': unitary.num_liked, 'num_fifth': unitary.num_fifth, 'num_disliked': unitary.num_disliked}
        else:
            return course_numbers
    

    def get_course_score(self, session, netid, courseid):
        score = session.query(Suggestions.score).filter(Suggestions.netid==netid, Suggestions.courseid==courseid).first()
        return {'score':score}
    
    def get_course_profs(self, session, courseid):
        if not courseid:
            return []
        
        professors = session.query(CourseProfs.profid).filter_by(courseid=courseid)
        if professors is None:
            return []
            
        
        prof_list = []
        for profid in professors:
            prof = session.query(Professors).filter_by(profid=profid).first()
            prof_list.append(prof.profname)
        
        return prof_list


    def get_fav_fifth(self, session, netid):
        courseid = session.query(FifthClass.courseid).filter_by(netid=netid)
        fav_fifth = ''
        crosslistings = self.get_crosslistings(session, courseid)
        fav_fifth = ' / '.join(crosslistings)
                
        return fav_fifth


    def get_liked(self, session, netid):
        liked_list = []
        for courseid in session.query(Liked.courseid)\
        .filter(Liked.netid==netid)\
        .order_by(Liked.order.asc())\
        .all(): 
            crosslistings = self.get_crosslistings(session, courseid)
            liked_list.append(' / '.join(crosslistings))

        return liked_list
    
    def get_disliked(self, session, netid):
        disliked_list = []
        for courseid in session.query(Disliked.courseid)\
        .filter(Disliked.netid==netid)\
        .order_by(Disliked.order.asc())\
        .all():
            crosslistings = self.get_crosslistings(session, courseid)
            disliked_list.append(' / '.join(crosslistings))

        return disliked_list

    
    def get_disliked_suggestions(self, session, netid):
        disliked_sugg_list = []
        for courseid in session.query(DislikedSuggestions.courseid)\
        .filter(DislikedSuggestions.netid==netid)\
        .all():
            crosslistings = self.get_crosslistings(session, courseid)
            disliked_sugg_list.append(' / '.join(crosslistings))
    
        return disliked_sugg_list
    
    # Returns a list of a user's suggestions as courseIds
    def get_suggestions(self, session, netid):
        suggestions = []
        for suggestion in session.query(Suggestions)\
        .filter_by(netid=netid)\
        .order_by(Suggestions.rank.asc())\
        .all():
            suggestions.append(suggestion.courseid)

        return suggestions

    
    def get_crosslistings(self, session, courseid):
        crosslistings = []
        for course in session.query(Crosslistings)\
            .filter(Crosslistings.courseid == courseid)\
            .order_by(Crosslistings.order.asc())\
            .all():
                crosslistings.append(course.dept_and_num)
        return crosslistings
    

    def get_courseids(self, session):
        courseids = {}
        for course in session.query(Crosslistings):
            courseids[course.courseid] = course.dept_and_num
        
        return courseids


    def get_courseid_from_deptnum(self, session, dept_and_num):
        course = session.query(Crosslistings).filter_by(dept_and_num=dept_and_num).first()
        if not course:
            return None
        return course.courseid


    def get_deptnum_to_courseid(self, session):
        crosslistings = {}
        for course in session.query(Crosslistings):
            crosslistings[course.dept_and_num] = course.courseid
        return crosslistings


    def get_list_of_deptnum(self, session, deptNum):
        courses = session.query(Crosslistings).filter(Crosslistings.dept_and_num.like('%' + deptNum + '%')).all()
        deptNums = []
        for course in courses:
            deptNums.append(course.dept_and_num)
        return deptNums

    # Do not need session
    def get_maj_list(self, maj):
        majs = [major for major in MAJOR_TO_CODE]
        query = []
        maj = maj.lower()

        for major in majs:
            # if major.lower().startswith(maj):
            #     query.append(major)
            
            if maj in major.lower():
                query.append(major)
        
        return query

    # No session needed
    def get_cert_list(self, cert):
        certificates = [CODE_TO_CERTIFICATE[i] for i in CODE_TO_CERTIFICATE]

        query = []
        cert = cert.lower()

        for certificate in certificates:
            # Contains since may start typing 'Comp' for 'Applications of Computing'
            if cert in certificate.lower():
                query.append(certificate)
        
        return query
    
    # ---------------------------------------------------------------
    # REMOVE from database
    # ---------------------------------------------------------------
    def remove_user(self, session, netid):
        """
        Remove one user's information from Database
        """
        session.query(Users).filter(Users.netid == netid)\
            .delete(synchronize_session=False)
        session.query(Certificates).filter(Certificates.netid == netid)\
            .delete(synchronize_session=False)
        session.query(FifthClass).filter(FifthClass.netid == netid)\
            .delete(synchronize_session=False)
        session.query(Liked).filter(Liked.netid == netid)\
            .delete(synchronize_session=False)
        session.query(Disliked).filter(Disliked.netid == netid)\
            .delete(synchronize_session=False)
        session.query(Suggestions).filter(Suggestions.netid == netid)\
            .delete(synchronize_session=False)
        session.query(DislikedSuggestions).filter(DislikedSuggestions.netid == netid)\
            .delete(synchronize_session=False)


#--------------------------------------------------------------------
if __name__ == '__main__':
    # FOR TESTING

    # Connection to database
    db = Database()
    engine, session = db.connect()
    if (session is not None):
        print('connected')

    # open course_info and print something
    with open('DataSources/DataFiles/course_info.pickle', 'rb') as handle:
        course_info = pickle.load(handle)
    
    # open user_info and print something
    with open('DataSources/DataFiles/csv_user_info.pickle', 'rb') as handle:
        user_info = pickle.load(handle)
    
    db.disconnect()