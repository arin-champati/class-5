from DataSources.course_info import getCourseInfoForTerms, saveCourseInfo, ORDERED_TERM_CODE_LIST
import DataSources.convert_csv_data as csv_data
import pickle

"""
saves the data from the csv and from princeton data sources into pickled dicts

course_info:
    'subjects': subjects,
    'crosslistings': crosslistings,
    'courses': courseids,
        'area': None, 
        'title': courseid['title'],
        'descrip': courseid['description'],
        'prereqs': None,
        'term': i.e. Spring 20,
        'popularity': 0

    'professors': professors,
    'course_profs': course_profs,
    'prof_courses': courses_for_professor

user_info:
    'users': users_dict,
        'userid'
            'name': req[0]['displayname'],
            'class_year': '',
            'major': '',
            'email': req[0]['mail']
    'certificates': certificates_dict,
        'userid'
            certificates
    'fifth_classes': fav_fifth_classes_dict,
        'userid'
            fav_fifth_classes
    'liked_classes': liked_classes_dict,
        'userid'
            liked_classes
    'disliked_classes': disliked_classes_dict
        'userid'
            disliked_classes
"""

if __name__ == '__main__':
    # save a pickle file that contains course_info 
    course_info = getCourseInfoForTerms(ORDERED_TERM_CODE_LIST)
    saveCourseInfo(course_info, 'DataSources/DataFiles/course_info.pickle')

    # save a pickle file that contains user_info 
    user_info = csv_data.getUserInfo('DataSources/DataFiles/Data Collection.csv', 'DataSources/DataFiles/course_info.pickle')
    csv_data.saveUserInfo(user_info, 'DataSources/DataFiles/csv_user_info.pickle')



    # FOR TESTING PURPOSES
    # open course_info and print something
    with open('DataSources/DataFiles/course_info.pickle', 'rb') as handle:
        course_info = pickle.load(handle)


    # open user_info and print something
    with open('DataSources/DataFiles/csv_user_info.pickle', 'rb') as handle:
        user_info = pickle.load(handle)
    
    user = 'champati'
    import pprint
    # pprint.pprint(course_info['course_profs'])
    pprint.pprint(course_info['courses']['015739']['department_name'])
    # for course in course_info['courses']:
    #     print(course_info['courses'][course]['term_code'])

