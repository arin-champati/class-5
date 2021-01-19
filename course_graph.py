#!/usr/bin/env python

#-----------------------------------------------------------------------
# graph.py
# Author: Ethan Seide
#-----------------------------------------------------------------------

from queue import PriorityQueue
from collections import deque
from Database.database import Database, Users, Liked, Disliked, FifthClass
from Database.database import Suggestions, DislikedSuggestions, UnitaryWeights

class CourseGraph:
    
    #--------------------------------------------------------------
    class CourseNode:

        def __init__(self, courseid=None, edges={}, popularity=1):
            self._courseid = courseid
            self._edges = edges   # dict tracking edge and edge weights
            self._popularity = popularity

        #--------------------------------------------------------------
        # ACCESSORS
        #--------------------------------------------------------------

        def getCourseid(self):
            return self._courseid

        def getEdges(self):
            return self._edges

        def getPopularity(self):
            return self._popularity

        #--------------------------------------------------------------
        # MUTATORS
        #--------------------------------------------------------------
        
        def addEdge(self, other, weight=0):
            courseid = other.getCourseid()

            edges = self.getEdges()
            otherid = other.getCourseid()
        
            edges[otherid] = weight


        def addPop(self, weight):
            self._popularity += weight

    #--------------------------------------------------------------
    #--------------------------------------------------------------

    def __init__(self, database, session, max_suggestions=5, max_courses=30, cache_mult=4):
        """
        Create a CourseGraph, fetching unitary weights and edge weights
        from database, creating CourseNodes for each course, and 
        constructing a dict mapping {courseid: CourseNode}
        """

        self._nodes = dict()  # dict with courseid keys, CourseNode vals
        self._max_suggestions = max_suggestions
        self._max_courses = max_courses
        self._cache_mult = cache_mult
        
        db = database

        # Get dict mapping courses to unitary weights
        unitary_dict = db.get_unitary_dict(session)

        # Get dict mapping courses to adjacent courses and weights
        edge_dict = db.get_edges_dict(session)

        # Create CourseNodes
        for courseid in unitary_dict:
            courseNode = CourseGraph.CourseNode(courseid=courseid, edges=dict(), popularity=unitary_dict[courseid])
            self._nodes[courseid] = courseNode


        # Create course edge dict for each CourseNode
        for courseid in edge_dict:
            node = self._nodes[courseid]  # get node of interest
            adj_courses = edge_dict[courseid]  # get inner dict {otherid: edge_weight}
            for otherid in adj_courses:
                other_node = self._nodes[otherid]
                node.addEdge(other_node, adj_courses[otherid])

    #--------------------------------------------------------------
    # MUTATORS
    #--------------------------------------------------------------
    def addNode(self, CourseNode):
        courseid = CourseNode.getCourseid()
        self._nodes[courseid] = CourseNode

    #------------------------------------------------------------------
    # ACCESSORS
    #------------------------------------------------------------------
    def getNode(self, courseid):
        return self._nodes.get(courseid)
    
    #------------------------------------------------------------------
    # SUGGESTIONS
    #------------------------------------------------------------------
        
    def cacheUserSuggestions(self, database, session, netid):
        """
        netid: (list) list of courseids of courses the user
        has indicated they like
        
        output: a list of MAX_SUGGESTIONS suggestions for the user,
        ranked combined unitary and edge-weighted score
        """
        if netid == None:
            return []

        fav_fifth = session.query(FifthClass).filter_by(netid=netid).first()
        liked_classes = session.query(Liked).filter_by(netid=netid).all()
        disliked_classes = session.query(Disliked).filter_by(netid=netid).all()
        disliked_suggestions = session.query(DislikedSuggestions).filter_by(netid=netid).all()
        
        pq = PriorityQueue()  # PriorityQueue tracking top courses by weight    
        UNITARY_FACTOR = 1      #####
        BINARY_FACTOR = 5       #####

        # track liked, disliked, and disliked suggestions
        liked_ids = {}
        for liked in liked_classes:
            if liked != None:
                liked_ids[liked.courseid] = 1
        
        liked_ids[fav_fifth.courseid] = 1
        
        disliked_ids = {}
        for disliked in disliked_classes:
            if disliked != None:
                disliked_ids[disliked.courseid] = 1

        disliked_sugg_ids = {}
        for disliked_sugg in disliked_suggestions:
            if disliked_sugg != None:
                disliked_sugg_ids[disliked_sugg.courseid] = 1
        
        seen_suggestions = {}  # track any suggestions seen twice 

        for liked in liked_classes:
            if liked == None:
                continue

            node = self.getNode(liked.courseid)  # get CourseNode
            if not node:
                return []
            edges = node.getEdges()   # get its Edge dict


            for courseid in edges:
                if not (courseid in liked_ids) and not (courseid in disliked_ids) and not (courseid in disliked_sugg_ids):
                    # add (weight, CourseNode) tuples to PriorityQueue
                    adj_node = self.getNode(courseid)
                    popularity = adj_node.getPopularity()

                    # Calculate scores 
                    score = (BINARY_FACTOR * edges[courseid]) + (UNITARY_FACTOR * popularity)

                    if courseid in seen_suggestions:
                        max_score = max(seen_suggestions[courseid], score)  # update max score
                        seen_suggestions[courseid] = max_score
                    else:
                        seen_suggestions[courseid] = score
            
        # insert all courses into pq    
        for courseid in seen_suggestions:
            score = seen_suggestions[courseid]
            pq.put((-score, courseid))  # flip sign to implement Max Heap
        
        suggestions = []
        scores = []
        length = min(self._max_suggestions * self._cache_mult, pq.qsize())  # can toggle for infinite suggestions!
        for _ in range(length):
            suggestion = pq.get()
            # correct solution:
            score = -suggestion[0]

            # we need to see that it is over zero as we could have bad suggestions in this list
            # negate it so that it is now positive
            if score > 0:
                scores.append(suggestion[0])
                suggestions.append(suggestion[1])
        
                
        # add liked (fifth is in this dict), disliked, disliked suggestions
        # to seen suggestions to that top unitary doesn't return these values
        seen_suggestions.update(liked_ids)
        seen_suggestions.update(disliked_ids)
        seen_suggestions.update(disliked_sugg_ids)

        # if not enough suggestions, get more suggestions by unitary weight
        if len(suggestions) < self._max_suggestions * self._cache_mult:
            k = (self._max_suggestions * 2) - len(suggestions)
            most_popular = database.get_top_unitary(session, k, seen_suggestions)  # get k most popular courses

            if scores:
                min_score = min(scores)
            else:
                min_score = 10
                
            for i, pop in enumerate(most_popular):
                suggestions.append(pop)
                scores.append(min_score - i)
        
        # remove old suggestions
        old_suggestions = session.query(Suggestions).filter_by(netid=netid).all()
        if old_suggestions is not None:
            session.query(Suggestions).filter_by(netid=netid).delete()
        
        
        # add suggestions to Suggestions table (caching twice as many as MAX_SUGGESTIONS)
        i = 1 # rank 1 = best suggestion
        for score, courseid in zip(scores, suggestions):
            suggestion = Suggestions(netid=netid, courseid=courseid, rank=i, score=score)
            session.add(suggestion)
            i += 1
                        
        return suggestions[:self._max_suggestions]
    
    #------------------------------------------------------------------
    # FILTERS
    #------------------------------------------------------------------

    # Retrieves a list of the most popular deptNums (not sure if handling crosslistings correctly)
    def getMostLiked(self, database, session, netid):

        if netid == None:
            return []

        seen_suggestions = {}
        # for liked in liked_classes:
        #     seen_suggestions[liked.courseid] = 1
        # for disliked in disliked_classes:
        #     seen_suggestions[disliked.courseid] = 1
        # for dislikedSugg in disliked_suggestions:
        #     seen_suggestions[dislikedSugg.courseid] = 1

        k = self._max_courses + len(seen_suggestions)
        most_popular_ids = database.get_top_unitary(session, k, seen_suggestions)


        most_popular_deptnums = []
        for courseid in most_popular_ids:
            crosslisting = database.get_crosslistings(session, courseid)
            crosslistingStr = ' / '.join(crosslisting)
            most_popular_deptnums.append(crosslistingStr)

        return most_popular_deptnums[:self._max_courses]
    
    # Retrieves a list of the least popular deptNums (not sure if handling crosslistings correctly)
    def getMostDisliked(self, database, session, netid):

        if netid == None:
            return []

        seen_suggestions = {}

        k = self._max_courses + len(seen_suggestions)
        least_popular_ids = database.get_bottom_unitary(session, k, seen_suggestions)

        least_popular_deptnums = []
        for courseid in least_popular_ids:
            crosslisting = database.get_crosslistings(session, courseid)
            crosslistingStr = ' / '.join(crosslisting)
            least_popular_deptnums.append(crosslistingStr)

        return least_popular_deptnums[:self._max_courses]

    def getFavorites(self, database, session, netid):

        if netid == None:
            return []

        seen_suggestions = {}

        k = self._max_courses + len(seen_suggestions)
        favorite_ids, n = database.get_top_favorites(session, k, seen_suggestions)
        favorite_deptnums = []
        for courseid in favorite_ids:
            crosslisting = database.get_crosslistings(session, courseid)
            crosslistingStr = ' / '.join(crosslisting)
            favorite_deptnums.append(crosslistingStr)

        return favorite_deptnums[:self._max_courses]
    
    def getTopEdgesFrom(self, session, courseid):
        """
        Gets the crosslistings of the top edges from a course
        """
        node = self.getNode(courseid)  # get CourseNode
        if not node:
            return []
        edges = node.getEdges()   # get its Edge dict

        return sorted(edges.keys(), key=lambda k: edges[k], reverse=True)[:5]
        
        
#------------------------------------------------------------------------
    
if __name__ == '__main__':
    # FOR TESTING PURPOSES
    
    from Database.session_maker import Session
    db = Database()

    sess = Session()

    class_5 = CourseGraph(db, sess, max_suggestions=10)

    # suggestions = class_5.getSuggestions([14894]) # 002065 - 333 # 002054 - 226
    userSuggestions = class_5.cacheUserSuggestions(db, sess, 'champati')

    userSuggestions = class_5.getTopEdgesFrom(sess, '002065')

    for suggestion in userSuggestions:
        courses = db.get_crosslistings(sess, suggestion)    
        print(' / '.join(courses))
    
    sess.close()