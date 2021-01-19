import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Database.session_maker import Session
from Database.database import Database

db = Database()

sess = Session()

db.delete_user(sess, 'champati')
sess.commit()
# class_5 = CourseGraph(db, sess, max_suggestions=10)

# # suggestions = class_5.getSuggestions([14894]) # 002065 - 333 # 002054 - 226
# userSuggestions = class_5.getUserSuggestions(db, sess, 'champati')

# userSuggestions = class_5.getTopEdgesFrom(sess, '002065')

# for suggestion in userSuggestions:
#     courses = db.get_crosslistings(sess, suggestion)    
#     print(' / '.join(courses))

sess.close()