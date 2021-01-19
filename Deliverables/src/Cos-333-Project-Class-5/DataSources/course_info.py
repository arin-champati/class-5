#!/usr/bin/env python3
from DataSources.MobileApp.req_lib import ReqLib
import pickle

'''
This endpoint takes up to three parameters:
term, subject, search
Term is a required parameter. The other two
parameters work a slightly different way. 
You should only provide one of these two
parameters in order to make a valid query
to this endpoint.
If you provide only the subject parameter,
the endpoint will return all courses 
within that subject for the term. That is, 
if for example you pass in 'COS', all classes
within the COS department will be returned.
Keep in mind that this must be all capital 
letters.
If you provide only the search parameter,
the endpoint will query all courses in the Registrar
and return all courses which match the search query.
For example, a search value of 'intro' would return 
all courses with the string 'intro' in either the
Course Title, Course Description, Professor Name,
or the Course Department Code.
If both the subject and search are provided, then 
the endpoint will return an OR of the two. That is,
a course will be returned if EITHER it matches the 
subject parameter OR the search parameter.


Below is an outline of the structure of this nested dictionary

term: code (term code), suffix, name, cal_name, reg_name, start_date, end_date, subjects
    subjects: code, name, courses
        courses: guid, course_id, catalog_number, title, detail
            detail: start_date, end_date, track, description
            instructors: emplid, first_name, last_name, full_name
            crosslistings: list of dicts {subject, catalog_number}
            classes: list of dicts {class_number, section, status, type_name, capacity, enrollment, schedule}
                schedule: {start_date, end_date, meetings}
                    meetings: [{meeting number, start_time, end_time, days}]

Academic Term is a coded string containing 4 digits.  The value for the current term is ‘1212’.
-          The characters within the first, second and third position ‘121’ represents the calendar year 2021, e.g. it aligns with ending year value for the academic year ‘2020-2021’.  Academic years always begin on July 01; and end on June 30 the following year.
-          The digit in the fourth position ‘2’ represents the semester.  Fall is the second semester within the order
o   1=Summer,
o   2=Fall,
o   3=Winter,
o   4=Spring.

'''
ORDERED_TERM_CODE_LIST = ['1214', '1212', '1204', '1202', '1194', '1192', '1184', '1182', '1174', '1172', '1164'] 

class CourseInfo:
    """
    CourseInfo is a class that has methods that allow us to easily
    get information about a current term (term_code) from the OIT 
    data source
    """
    def __init__(self, term_code, search=' '):
        """
        term_code: {int} the code that corresponds to the query term
        summary: the constructor will set the class's term_info instance
        variable to be a dict of many dicts that contains information about a given term
        """
        # every course will contain a space in its name, description, or professor list
        # so this is why we set search to ' '
        req_lib = ReqLib()

        # returns all courses that match with the search query
        term_info = req_lib.getJSON(
        req_lib.configs.COURSE_COURSES,
        # To return a json version of the return value
        fmt="json",
        term=term_code,
        search=search
        )   
        self.term_info = term_info
    
    def getTermInfo(self):
        return self.term_info
    
    def getSubjectsOffered(self, subjects = {}):
        """
        subject code: subject name
        summary: adds to a subjects dict all of the subjects for this term
        """
        for term in self.term_info["term"]:
            for subject in term["subjects"]:      
                if subject['code'] not in subjects:
                    subjects[subject['code']] =  subject['name']    
        return subjects
    
    def getCrosslistings(self, crosslistings = {}):
        """
        coursid: dept_and_num
        Summary: adds to a crosslistings dict all of the crosslistings for the current term
        """
        for term in self.term_info["term"]:
            for subject in term["subjects"]:    
                for course in subject["courses"]:
                    courseid = course['course_id']
                    dept_and_num = f'{subject["code"]} {course["catalog_number"]}'
                    if courseid not in crosslistings:
                        crosslistings[courseid] = [dept_and_num] 
                    else:
                        if dept_and_num not in crosslistings[courseid]:
                            crosslistings[courseid].append(dept_and_num)

                    for crosslisting in course["crosslistings"]:
                        dept_and_num = f'{crosslisting["subject"]} {crosslisting["catalog_number"]}'

                        if dept_and_num not in crosslistings[courseid]:
                            crosslistings[courseid].append(dept_and_num)
                    
                    # if the course had no crosslistings, add an empty list to the course id mapping
                    if courseid not in crosslistings:
                        crosslistings[courseid] = []

            return crosslistings
    
    def getCourses(self, courses = {}):
        """
        courseid: area, title, description, prereqs, popularity
        courses: courses dict
        summary: adds to a courses dict all the courses in this term
        """
        for term in self.term_info["term"]:
            for subject in term["subjects"]:    
                for course in subject["courses"]:
                    courseid = course['course_id']
                    if courseid not in courses:
                        courses[courseid] = {
                            'area': '', 
                            'title': course['title'],
                            'descrip': course['detail']['description'],
                            'term': term['cal_name'],
                            'term_code': term['code'],
                            'prereqs': '',
                            'department_name': subject['name']
                        }
        return courses

    def getProfessors(self, professors = {}):
        """
        emplid: professor name
        professors: professors dict
        summary: adds to a professors dict all the professors in this term
        """
        for term in self.term_info["term"]:
            for subject in term["subjects"]:    
                for course in subject["courses"]:
                    for instructor in course["instructors"]:
                        emplid = instructor['emplid']
                        if emplid not in professors:
                            professors[emplid] = instructor['full_name']

        return professors

    
    def getCourseProfs(self, course_profs = {}):
        """
        courseid: professors
        summary: adds to a course_profs dict all of the professors for a given course
        in this term
        """
        for term in self.term_info["term"]:
            for subject in term["subjects"]:    
                for course in subject["courses"]:
                    courseid = course['course_id']
                    if courseid not in course_profs:
                        course_profs[courseid] = []

                        # dont allow instructors to be added twice
                        seen_instructors = {} 
                        for instructor in course["instructors"]:
                            if instructor['emplid'] not in seen_instructors:
                                course_profs[courseid].append(instructor['emplid'])

                            seen_instructors[instructor['emplid']] = True

        return course_profs

    def getCoursesForProfessors(self, courses_for_professor = {}):
        """
        professor: courseids
        summary: adds to a courses_for_professor dict all of the classes that
        a professor teaches for the given term
        """

        for term in self.term_info["term"]:
            for subject in term["subjects"]:    
                for course in subject["courses"]:
                    courseid = course['course_id']
                    for instructor in course["instructors"]:
                        emplid = instructor['emplid']

                        if emplid not in courses_for_professor:
                            courses_for_professor[emplid] = [courseid]
                        else:
                            courses_for_professor[emplid].append(courseid)

                    if emplid not in courses_for_professor:
                        courses_for_professor[emplid] = []
        return courses_for_professor

def getCourseInfoForTerms(ordered_term_code_list):
    """
    ordered_term_code_list should be ordered in chronological order,
    meaning that the most recent term will be at index 0
    summary: returns subjects
    """
    subjects = {}
    crosslistings = {}
    courses = {}
    professors = {}
    course_profs = {}
    courses_for_professor = {}

    for term in ORDERED_TERM_CODE_LIST:
        """
        For every term, add to the total information dicts
        """
        course_info = CourseInfo(term)
        subjects = course_info.getSubjectsOffered(subjects)
        crosslistings = course_info.getCrosslistings(crosslistings)
        courses = course_info.getCourses(courses)
        professors = course_info.getProfessors(professors)
        course_profs = course_info.getCourseProfs(course_profs)
        courses_for_professor = course_info.getCoursesForProfessors(courses_for_professor)

    course_info_dict = {
        'subjects': subjects,
        'crosslistings': crosslistings,
        'courses': courses,
        'professors': professors,
        'course_profs': course_profs,
        'prof_courses': courses_for_professor
    }
        
    return course_info_dict

    
def saveCourseInfo(course_info_dict, save_file):
    with open(save_file, 'wb') as handle:
        pickle.dump(course_info_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    # FOR TESTING PURPOSES
    # '002635'
    # ORDERED_TERM_CODE_LIST = [FALL_2020_TERM_CODE, SPRING_2020_TERM_CODE] 
    
    # course_info = getCourseInfoForTerms(ORDERED_TERM_CODE_LIST)
    # saveCourseInfo(course_info, 'course_info.pickle')

    # with open('course_info.pickle', 'rb') as handle:
    #     course_info = pickle.load(handle)
    
    # print(course_info['courses']['006276']['code'])
    # c = CourseInfo('1214', search='common')
    course_info_dict = getCourseInfoForTerms('1214')
    print(course_info_dict['courses'])