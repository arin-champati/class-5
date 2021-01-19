from DataSources.course_info import CourseInfo, ORDERED_TERM_CODE_LIST
from DataSources.user_info import UserInfo
from DataSources.DataFiles.AreasOfStudy import CERTIFICATE_TO_CODE
import csv
import pickle

def getInfoFromCSV(csv_name):
    """
    Reads a csv that contains department and numbers
    The columns are as follows:
        name, netid, year, major, certificates, 5th class,
        liked 1, liked 2, ..., liked 5, disliked 1, ..., disliked 5
    """

    users = []
    user_info = []
    certificates = []
    fav_fifth_classes = []
    liked_classes = []
    disliked_classes = []

    with open(csv_name, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            row = list(row)
            users.append(row[1])
            user_info.append([row[0], row[2], row[3]])
            certificates.append(row[4])
            fav_fifth_classes.append([row[5]])
            liked_classes.append(row[6:11])
            disliked_classes.append(row[11:16])

    return users, user_info, certificates, fav_fifth_classes, liked_classes, disliked_classes

def __getCrosslistings(course_info_filename):
    with open(course_info_filename, 'rb') as handle:
        course_info = pickle.load(handle)

    return course_info['crosslistings']

def __representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def convertToCourseIds(classes_list, course_info_filename):
    crosslistings = __getCrosslistings(course_info_filename)
    N = len(classes_list)

    for i in range(N):
        L = len(classes_list[i])
        for courseid in crosslistings:
            class_list = crosslistings[courseid]
            if courseid == '':
                continue
            for course in class_list:
                # for every course in the crosslisting, 
                # check if it matches with any the classes in our 3 lists
                # and replace the necessary items
                for j in range(L):
                    if course in classes_list[i][j]:
                        classes_list[i][j] = courseid
            
        # if there is no course id for this class, make it an empty string
        for j in range(L):
            if not __representsInt(classes_list[i][j]):
                classes_list[i][j] = ''

    return classes_list

def createUsersDict(users, user_info):
    """
    users: list of user ids
    user_info: list of user info
    """
    users_dict = {}
    for user, info in zip(users, user_info):
        user_info = UserInfo.getInfo(user)
        email = user_info['email']
        name = user_info['name']
        users_dict[user] = {'name': name, 'class_year': info[1], 'major': info[2], 'email': email}
    return users_dict

def createCertificatesDict(users, certificates):
    certificates_dict = {}
    for user, certificate in zip(users, certificates):
        certificate = certificate.split(',')
        for i in range(len(certificate)):
            cert = certificate[i]
            cert = cert.lstrip()
            certificate[i] = cert
            if cert in CERTIFICATE_TO_CODE:
                certificate[i] = int(CERTIFICATE_TO_CODE[cert])

        certificates_dict[user] = certificate
    
    return certificates_dict

def createClassDict(users, classes):
    course_dict = {}
    for user, course in zip(users, classes):
        course_dict[user] = course
    
    return course_dict

def getUserInfo(csv_filepath, course_info_filepath):
    users, user_info, certificates, fav_fifth_classes, liked_classes, disliked_classes = getInfoFromCSV(csv_filepath)

    fav_fifth_classes = convertToCourseIds(fav_fifth_classes, course_info_filepath)
    liked_classes = convertToCourseIds(liked_classes, course_info_filepath)
    disliked_classes = convertToCourseIds(disliked_classes, course_info_filepath)

    users_dict = createUsersDict(users, user_info)
    certificates_dict = createCertificatesDict(users, certificates)
    fav_fifth_classes_dict = createClassDict(users, fav_fifth_classes)
    liked_classes_dict = createClassDict(users, liked_classes)
    disliked_classes_dict = createClassDict(users, disliked_classes)

    user_info = {
        'users': users_dict,
        'certificates': certificates_dict,
        'fifth_classes': fav_fifth_classes_dict,
        'liked_classes': liked_classes_dict,
        'disliked_classes': disliked_classes_dict
    }

    return user_info


def saveUserInfo(user_info, save_file):    
    with open(save_file, 'wb') as handle:
        pickle.dump(user_info, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    user_info = getUserInfo('Data Collection.csv', 'DataSources/DataFiles/user_info.pickle')
    saveUserInfo(user_info, 'csv_user_info.pickle')

    with open('csv_user_info.pickle', 'rb') as handle:
        user_info = pickle.load(handle)
    
    user = 'champati'
    print(user_info['users']['champati'])

