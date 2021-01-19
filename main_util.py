#!/usr/bin/env python
#-----------------------------------------------------------------------
# helper.py
# Author: Ethan Seide, Arin Champati, Chaz Bethel-Brescia
#-----------------------------------------------------------------------
from cas_client import CASClient
from flask import Flask, make_response, render_template, session, flash
from json import dumps
import sys
import traceback

from DataSources.DataFiles.AreasOfStudy import CODE_TO_MAJOR
import datetime
#-----------------------------------------------------------------------
def authenticate():
        netid = CASClient().authenticate()
        netid = netid.strip().split()[0]
        session['logged_in'] = True
        return netid

def handleError(e, verbose="", client="A server error has occured.", session=None, isJson=False):
        print(verbose, file=sys.stderr)
        print(e, file=sys.stderr)
        traceback.print_exc(file=sys.stdout)
        
        if session is not None:
            session.rollback()

        if isJson:
            jsonStr = dumps([{"Error":client}])
            response = make_response(jsonStr)
            response.headers['Content-Type'] = 'application/json'
            return response

        html = render_template('status.html', status=client)
        return make_response(html)
    
def validate_inputs(liked, disliked, disliked_suggestions, favCourseId, certificates, major, year):
    """
    Takes in the inputted arguments by a user and validates them by
    running a series of tests
    """
    liked_valid = True
    disliked_valid = True
    fav_valid = True
    cert_valid = True
    major_valid = True
    year_valid = True

    # check if the deptnums are valid
    for course in liked:
        if course is None:
            flash('Please enter valid course names in the liked courses section')
            liked_valid = False
            break
    
    # check if the deptnums are valid
    for course in disliked:
        if course is None:
            flash('Please enter valid course names in the disliked courses section')
            disliked_valid = False
            break

    if favCourseId is None:
        flash('Please enter a valid course name in the favorite fifth course section')
        fav_valid = False

    # check if liked and disliked are unique
    for course1 in liked:
        if liked_valid == False:
            break

        for course2 in disliked:
            if course1 == course2:
                flash('Liked and disliked courses must not overlap')
                disliked_valid = False 
                liked_valid = False                       

            if liked_valid == False:
                break
    
    # check if liked is in disliked suggestions unless liked is nonetype
    for course1 in liked:
        if liked_valid == False:
            break
        
        for course2 in disliked_suggestions:
            if course1 and course2:
                if course1 == course2:
                    flash('Liked course cannot also be a disliked suggestion')
                    liked_valid = False   

            if liked_valid == False:
                break
    

    # check if favorite is in disliked unless fav fifth is nonetype
    # also check if favorite fifth is in disliked suggestions 
    if favCourseId:
        for course in disliked:
            if course == favCourseId:
                flash('Favorite fifth course cannot also be a disliked course')
                fav_valid = False 
                disliked_valid = False
                break   

        for course in disliked_suggestions:
            if course:
                if favCourseId == course:
                    flash('Favorite fifth course cannot also be a disliked suggestion')
                    fav_valid = False
                    break

        
    # corner case: we only need to check if the elements are unique if they are not none
    filter_liked = list(filter(None, liked))
    if len(filter_liked) != len(set(filter_liked)):
        flash('Liked courses must be unique')
        liked_valid = False
    
    # corner case: we only need to check if the elements are unique if they are not none
    filter_disliked = list(filter(None, disliked))
    if len(filter_disliked) != len(set(filter_disliked)):
        flash('Disliked courses must be unique')
        disliked_valid = False


    # check if the major is valid
    if not CODE_TO_MAJOR.get(major):
        flash('Please enter a valid major')
        major_valid = False
    

    # check if the certificates are valid
    for cert in certificates:
        if cert is None:
            flash('Please enter valid certificate names')
            cert_valid = False
            break

    # corner case: if all of them are none, we just
    # continue so that the unique error doesn't show up
    filter_certs = list(filter(None, certificates))
    if len(filter_certs) > len(set(filter_certs)):
        flash('Certificates must be unique')
        cert_valid = False

    
    # check if the year is valid
    now = datetime.datetime.now()
    years = [str(now.year + i) for i in range(6)]
    if year not in years:
        flash('Please enter a valid graduation year')
        year_valid = False
    
    return liked_valid, disliked_valid, fav_valid, cert_valid, major_valid, year_valid