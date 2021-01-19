import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Database.database import CourseEdges, UnitaryWeights
# from session_maker import Session
from Database.database import Database
import pickle


# def delete_edges(edges, fifth, liked, disliked, db_fifth, db_liked, db_disliked):
#     """
#     This will query the database and it will delete the necessary edges, 
#     update the unitaries, and update the user liked / disliked
#     """

#     # if the inputs are null, initialize them to empty lists so we don't get errors
#     if db_liked is None:
#         db_liked = []
#     elif db_disliked is None:
#         db_disliked = []

#     delete_liked = set(db_liked).difference(liked)
#     delete_disliked = set(db_disliked).difference(disliked)

#     # this is where we delete the edges from the database
#     for course1 in delete_liked:

#         # we have to delete the delete_liked to db_liked edges
#         # and we have to delete the db_liked to delete_liked edges
#         for course2 in db_liked:
#             if course2 in edges[course1]: edges[course1].remove(course2)

#             if course1 in edges[course2]: edges[course2].remove(course1)
        
#         # we have to delete the delete_liked to db_disliked edges
#         for course2 in db_disliked:
#             if course2 in edges[course1]: edges[course1].remove(course2)
    

#     # now remove every liked to delete_disliked edge
#     for course1 in db_liked:
#         for course2 in delete_disliked:
#             if course2 in edges[course1]: edges[course1].remove(course2)


#     # then, for every course to delete, update the unitary and remove it as a liked/disliked for the user
#     for course in delete_liked:
#         db_liked.remove(course)
    
#     for course in delete_disliked:
#         db_disliked.remove(course)
            

# def add_edges(edges, fifth, liked, disliked, db_fifth, db_liked, db_disliked):
#     # if the inputs are null, initialize them to empty lists so we don't get errors
#     if liked is None:
#         liked = []
#     elif disliked is None:
#         disliked = []
#     elif db_liked is None:
#         db_liked = []
#     elif db_disliked is None:
#         db_disliked = []

#     add_liked = set(liked).difference(db_liked)
#     add_disliked = set(disliked).difference(db_disliked)

#     i = 0


#     # for every course to be added we need to create the edges
#     for course1 in add_liked:

#         # # create liked-fifth relationship
#         # # also create fifth-like relationship
#         # if course1 not in edges:
#         #     edges[course1] = []
#         # edges[course1].append(fifth)

#         # if fifth not in edges:
#         #     edges[fifth] = []
#         # edges[fifth].append(course1)

#         # create liked-liked relationship
#         for course2 in liked:
#             if course1 != course2:
#                 if course1 not in edges:
#                     edges[course1] = []

#                 edges[course1].append(course2)
            
#             i+=1
        
#         # create liked-disliked relationship
#         for course2 in disliked:
#             if course1 != course2:
#                 if course1 not in edges:
#                     edges[course1] = []

#                 edges[course1].append(course2)
#             i+=1

            
    
#     # now we need to add db_liked to add_disliked relationships
#     for course1 in db_liked:
#         for course2 in add_disliked:
#             if course1 not in edges:
#                     edges[course1] = []

#             edges[course1].append(course2)
#             i+=1
        
#         for course2 in add_liked:
#             if course1 != course2:
#                 if course1 not in edges:
#                     edges[course1] = []

#                 edges[course1].append(course2)
#             i+=1
    
#     print(i)
                

#     # # also create a fifth-disliked relationship
#     # for course2 in disliked:
#     #     if fifth not in edges:
#     #         edges[fifth] = []

#     #     edges[fifth].append(course1)

    
#     # # add the courses to the database
#     # db_fifth.append(fifth)

#     for course in add_liked:
#         db_liked.append(course)
    
#     for course in add_disliked:
#         db_disliked.append(course)
        
#     return edges

def delete_edges_helper(course_list_type, edges, db_fifth, db_liked, db_disliked):
    """
    course_list_type: {string} either fifth or liked
    runs the for loop of deletion

    deletes edges from course_list_type to the other inputs
    """
    if course_list_type == 'fifth':
        courses = db_fifth
    elif course_list_type == 'liked':
        courses = db_liked
    else:
        courses = db_liked
    
    for course1 in courses:
        # we have to delete the course1 to db_liked edges
        for course2 in db_liked:
            if course2 in edges[course1]: 
                edges[course1].remove(course2)
        
        # we have to delete the course1 to db_fifth edges
        for course2 in db_fifth:
            if course2 in edges[course1]: 
                edges[course1].remove(course2)
        
        # we have to delete the course1 to db_disliked edges
        for course2 in db_disliked:
            if course2 in edges[course1]: 
                edges[course1].remove(course2)
    
    return edges


def delete_edges(edges, db_fifth, db_liked, db_disliked):
    """
    This will query the database and it will delete the necessary edges, 
    update the unitaries, and update the user liked / disliked
    """

    # if the inputs are null, initialize them to empty lists so we don't get errors
    if db_liked is None:
        db_liked = []
    if db_disliked is None:
        db_disliked = []
    if db_fifth is None:
        db_fifth = []
                
    # delete edges from liked courses and fifth courses
    delete_edges_helper('fifth', edges, db_fifth, db_liked, db_disliked)
    delete_edges_helper('liked', edges, db_fifth, db_liked, db_disliked)

    # then, for every course to delete, update the unitary and remove it as a liked/disliked for the user
    for course in db_liked:
        db_liked.remove(course)
    
    for course in db_disliked:
        db_disliked.remove(course)
    
    for course in db_fifth:
        db_fifth.remove(course)
    

def add_edges_helper(course_list_type, edges, fifth, liked, disliked):
    """
    course_list_type: {string} either fifth or liked
    runs the for loop of deletion

    adds edges from course_list_type to the other inputs
    """
    if course_list_type == 'fifth':
        courses = fifth
        weight = 2
    elif course_list_type == 'liked':
        courses = liked
        weight = 1
    else:
        courses = disliked
        weight = 1


    for course1 in courses:
        # create courses-liked relationship
        for course2 in liked:
            if course1 == course2:
                continue
            if course1 not in edges:
                edges[course1] = []

            edges[course1].append(course2)
        
        # create courses-fifth relationship
        for course2 in fifth:
            if course1 == course2:
                continue
            if course1 not in edges:
                edges[course1] = []

            edges[course1].append(course2)
        
        # create courses-disliked relationship
        for course2 in disliked:
            if course1 == course2:
                continue
            if course1 not in edges:
                edges[course1] = []

            edges[course1].append(course2)       


def add_edges(edges, fifth, liked, disliked, db_fifth, db_liked, db_disliked):
    # if the inputs are null, initialize them to empty lists so we don't get errors
    if liked is None:
        liked = []
    if disliked is None:
        disliked = []
    if fifth is None:
        fifth = []

    
    # create edges from fifth and liked
    add_edges_helper('fifth', edges, fifth, liked, disliked)
    add_edges_helper('liked', edges, fifth, liked, disliked)


    # add the courses to the database
    for course in fifth:
        db_fifth.append(course)

    for course in liked:
        db_liked.append(course)
    
    for course in disliked:
        db_disliked.append(course)    
    

def print_edges(edges):
    for course1, course2 in edges.items():
        for course in course2:
            print(f'{course1} -> {course}')


print('#ROUND 1')
fifth = [10]
db_fifth = []

liked = [2,3,4,5]
db_liked = []

disliked = [6,9]
db_disliked = []

edges = {}
delete_edges(edges, db_fifth, db_liked, db_disliked)
add_edges(edges, fifth, liked, disliked)

print_edges(edges)

print(db_liked)
print(db_disliked)

print()
print('#ROUND 2')
fifth = [10]
liked = [1,2,3]
disliked = [7,8,9]

delete_edges(edges, db_fifth, db_liked, db_disliked)
add_edges(edges, fifth, liked, disliked)

print_edges(edges)
print(db_liked)
print(db_disliked)

# print()
# print('#ROUND 3')
# liked = [3,5,9]
# disliked = [13,2,12]

# delete_edges(edges, db_fifth, db_liked, db_disliked)
# add_edges(edges, fifth, liked, disliked)


# print_edges(edges)
# print(db_liked)
# print(db_disliked)

# print()
# print('#ROUND 4')
# liked = [3,1,8]
# disliked = [13,2,12]

# delete_edges(edges, fifth, liked, disliked, db_fifth, db_liked, db_disliked)
# add_edges(edges, fifth, liked, disliked, db_fifth, db_liked, db_disliked)


# print_edges(edges)
# print(db_liked)
# print(db_disliked)


"""
edges:
    
    before                  after
                            
                            1-2
                            1-3
                            1-7
                            1-8
                            1-9
    
    2-3                     2-1
    2-4                     2-3
    2-5                     2-7
    2-6                     2-8
    2-9                     2-9
    
    3-2                     3-1
    3-4                     3-2
    3-5                     3-7
    3-6                     3-8
    3-9                     3-9

    4-2                    
    4-3                     
    4-5
    4-6
    4-9
    
    5-2
    5-3
    5-4
    5-6
    5-9

"""







# db = Database()
# session = Session()



# # crosslisting = database.get_crosslistings(session, courseid)
# # crosslistingStr = ' / '.join(crosslisting)
# # print(score, edges[courseid], crosslistingStr)
# courseid = db.get_courseid_from_deptnum(session, 'LAO 201')

# # cross = db.get_crosslistings(session, '001391')
# # print(cross)

# courses = session.query(CourseEdges).filter_by(courseid1=courseid).all()
# for course in courses:
#     cross1 = db.get_crosslistings(session, course.courseid1)
#     cross2 = db.get_crosslistings(session, course.courseid2)
#     print(f'{cross1} -----> {cross2} : {course.weight}')

# courses = session.query(UnitaryWeights).filter_by(courseid=courseid).all()
# for course in courses:
#     print(course.courseid, course.weight, course.num_liked, course.num_disliked, course.num_fifth)

# session.close()

"""
                            BEFORE                      LIKE                    DISLIKE                   
LAO 218 - LAO 201           None
LAO 218 - LAO 210           None
LAO 218 - AAS 230           None
LAO 218 - AAS 211           None
Unitary                     None

LAO 201 - LAO 218           None
LAO 201 - LAO 210           None
LAO 201 - AAS 230           None
LAO 201 - AAS 211           None
Unitary                     None

LAO 210 - LAO 218           None
LAO 210 - LAO 201           None
LAO 210 - AAS 230           None
LAO 210 - AAS 211           None
Unitary                     None


LAO 201: 015428
LAO 210: 006397
LAO 218: 015741
AAS 211: 008485
AAS 230: 013693

"""