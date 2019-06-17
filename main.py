#!/usr/bin/env python3
from mechanize import Browser;  # for making requests
from bs4 import BeautifulSoup;  # for parsing html

"""
@return a list of json courses
@param url: the basename url to the catalog for a course
@param catoid: the catalog id
@param coid_begin: the course id for the first course in the catalog
@param coid_end: the course id for the last course in the catalog
"""
def web_parse(url, catoid, coid_begin, coid_end):
    courses = []
    coid = coid_begin
    bro = Browser();
    while coid <= coid_end:
        # never fail to access the link
        connected = False
        while not connected:
            try:
                bro.follow_link(url+"?catoid="+catoid+"&coid="+coid)
                connected = True
            except:
                print("retrying")
        coid += 1;

def request_course(url, catoid, coid):
    # TODO:


### Main ###
def main():
    catoid = 40
    # page with list of courses
    smuCatalogURL = "https://catalog.smu.edu/content.php?catoid="+catoid+"&navoid=3146"
    ### find the last courses id
    coid_begin = 144004
    bro = Browser();
    # never fail to access the link
    connected = False
    while not connected:
        try:
            bro.follow_link(smuCatalogURL)
            connected = True
        except:
            print("retrying")
    links = list(bro.links())
    # find the link to get to the last page of courses
    for i in range(len(links)-1, 0):
        text = links[i].text
        if(text = "Forward 10"):
            # the link after this one is the link to the last page
    
    
if __name__ == '__main__':
    main()
