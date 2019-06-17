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
    while coid <= coid_end:
        
        coid += 1;

def request_course(url, catoid, coid):
    # TODO:


### Main ###
def main():
    catoid = 40
    # page with list of courses
    smuCatalogURL = "https://catalog.smu.edu/content.php?catoid="+catoid+"&navoid=3146"
    ### find the first and last courses
    bro = Browser();
    connected = False
    while not connected:
        try:
            bro.follow_link(smuCatalogURL)
            connected = True
        except:
            print("retrying")
    
    
    
    
if __name__ == '__main__':
    main()
