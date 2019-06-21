#!/usr/bin/envpip python3
#import pandas as pd
from mechanize import Browser  # for making requests
from bs4 import BeautifulSoup  # for parsing html
from collections import OrderedDict
import json
import re
import io
import codecs

# this is the global browser for this program
bro = Browser()
bro.set_handle_robots(False)
bro.set_handle_refresh(False)
bro.set_cookiejar(None)

"""
Get a list of courses from the catalog
@param url: the basename url to the catalog for a course
@param catoid: the catalog id
@param coid_begin: the course id for the first course in the catalog
@param coid_end: the course id for the last course in the catalog
@return a list of json courses
"""
def web_parse(url, catoid, coid_begin, coid_end):
    courses = []
    coid = coid_begin

    while coid <= coid_end:
        html = bro.open(url+"?catoid="+str(catoid)+"&coid="+str(coid)).get_data()
        print(coid)
        course = process_request(html)

        

        if course != False:
            courses.append(course)
        coid += 1
        

    return courses



"""
get the course information from the html page
@return a course json or false if not a course
"""
def process_request(html):

    #converting html to a Beautiful Soup object
    request = BeautifulSoup(html, 'html.parser')
    header = request.h1.string
    #check if the header has any digits. All courses MUST have digits
    headDig = any(char.isdigit() for char in header)

    if(headDig != True):
        print(header)
        return False
    else:
        #creating course dictionary
        print('saving this one') 
        information = OrderedDict()
        information["name"] = None
        information["hours"] = None
        information["long_name"] = None
        information["description"] = None
        information["min_hours_general"] = None
        information["min_hours_specific"] = []
        information["min_standing"] = None
        information["prereqs_raw"] = []
        information["coreqs_raw"] = []
        information["preco_raw"] = []
        information["prereqs"] = []
        information["coreqs"] = []
        information["preco"] = []
        information["majors"] = []
        information["minors"] = []
        information["sections"] = []



        #converting Beautiful Soup Object to a string
        html2 = request.prettify()

        #removing the unwanted HTML
        html2 = re.sub('<meta.*?<h1', '', html2, flags=re.DOTALL)
        html2 = re.sub('<span.*?Mobile Site', '', html2, flags=re.DOTALL)

        #inputing in the lost characters 
        insrtStr = "<h1 "
        breakStr = "id="
        indx = html2.index(breakStr)
        html2 = html2[:indx] + insrtStr + html2[indx:]

    #regex to extract the course description
        string1 = '<br/>'
        string2 = '<a'
        descr = html2[html2.find(string1) : html2.find(string2)]
        descr = re.sub("<br/>", '', descr)
        descr = re.sub("Prerequisite:", '', descr)
        descr = descr.strip()


        #converting the string back to a BeautifulSoup object
        soup = BeautifulSoup(html2, 'html.parser')
        
        
        #getting course name
        courseRaw = soup.select('h1')[0].get_text(strip = True)
        print(courseRaw)
        name, longName = courseRaw.split(' - ')[0], courseRaw.split(' - ')[1]
        

        #getting hours
        hours = soup.select('em')[1].get_text(strip = True)

        #getting prereq
        preReq = soup.select('a')[0].get_text(strip = True)


        information["name"] = name
        information["hours"] = hours
        information["long_name"] = longName
        information["prereqs"] = preReq
        information["description"] = descr

        return information 

'''
connect to a page. if connection times out, rety indefinitly
@param bro: the mechanize browser object
@param url: the url to connect to 
'''

def connect_nofail(url):
    # never fail to access the link
    connected = False
    while not connected:
        try:
            bro.open(url)
            connected = True
        except:
            print(".", end='',flush=True)

### Main ###
"""
get any user input and get initial information like the last course id

"""
def main():
    catoid = 40
    # page with list of courses: southern methodist university catalog uniform resource locator
    smu_cat_url = "https://catalog.smu.edu/content.php?catoid="+str(catoid)+"&navoid=3146"
    ### find the last courses id
    coid_begin = 144004         # hopefuly this stays the same forever
    coid_end = 0;               # will set later
    
    connect_nofail(smu_cat_url)
    # find the link to get to the last page of courses
    links = list(bro.links())
    for i in range(len(links)-1, 0, -1):
        text = links[i].text
        if(text == "Forward 10"):
            # the link after this one is the link to the last page
            connect_nofail(links[i+1].url) # we are going to the last page
            break
    # now being on the last page of courses, we can start from the back again and find the last course
    links = list(bro.links())
    for i in range(len(links)-1, 0, -1):
        text = links[i].text
        if(text == "1"):         # this is the link right after the last course
            # get the course id of the last course
            text = links[i-1].url # the previous link on the page should be the last course
            url_parts = text.split('=')
            coid_end = int(url_parts[-1]) # the last element is the coid
            break
    # we got the course ids, now we leave the rest of the work to web_parse()
    courses = web_parse("https://catalog.smu.edu/preview_course_nopop.php", catoid, coid_begin, coid_end)
    # I guess we just print them out for now
    print(courses)

if __name__ == '__main__':
    main()
