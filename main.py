#!/usr/bin/env python3
from mechanize import Browser;  # for making requests
from bs4 import BeautifulSoup;  # for parsing html

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
        html = request_course(url+"?catoid="+str(catoid)+"&coid="+str(coid))
        course = process_request(html)
        if course:
            courses.append(course)
        coid += 1;
    return courses
        
"""
@returns a course json

"""
def request_course(url):
    bro = Browser();            # again a different one
    connect_nofail(bro,) # connect to a course page


"""
get the course information from the html page

"""
def process_request(html):
    # TODO: beautiful soup probably
    print("TODO")
    

"""
connects to a page. if connection times out, rety indefinitly
@param bro: the mechanize browser object
@param url: the url to connect to 
"""
def connect_nofail(bro, url):
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
    bro = Browser();
    bro.set_handle_robots(False)
    bro.set_handle_refresh(False)
    bro.set_cookiejar(None) 
    connect_nofail(bro, smu_cat_url)
    # find the link to get to the last page of courses
    links = list(bro.links())
    for i in range(len(links)-1, 0, -1):
        text = links[i].text
        if(text == "Forward 10"):
            # the link after this one is the link to the last page
            connect_nofail(bro, links[i+1].url) # we are going to the last page
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
    print(courses);
    
if __name__ == '__main__':
    main()
