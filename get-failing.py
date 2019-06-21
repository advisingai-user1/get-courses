from mechanize import Browser  # for making requests
from bs4 import BeautifulSoup  # for parsing html
from collections import OrderedDict
import json
import re
import io
import codecs

bro = Browser()
bro.set_handle_robots(False)
bro.set_handle_refresh(False)
bro.set_cookiejar(None)


html = bro.open('https://catalog.smu.edu/preview_course_nopop.php'+"?catoid="+'40'+"&coid="+'145376').get_data()

request = BeautifulSoup(html, 'html.parser')


#converting Beautiful Soup Object to a string
html2 = request.prettify()

#removing the unwanted HTML
html2 = re.sub('<meta.*?<h1', '', html2, flags=re.DOTALL)
html2 = re.sub('<a class.*?Mobile Site', '', html2, flags=re.DOTALL)


#inputing in the lost characters 
insrtStr = "<h1 "
breakStr = "id="
indx = html2.index(breakStr)
html2 = html2[:indx] + insrtStr + html2[indx:]

#converting the string back to a BeautifulSoup object
soup = BeautifulSoup(html2, 'html.parser')

#saving course name and long name
courseRaw = soup.select('h1')[0].get_text(strip = True)
#print(courseRaw)
name, longName = courseRaw.split(' - ')[0], courseRaw.split(' - ')[1]


#regex to extract the course description
html2 = re.sub('<span.*?>', '', html2, flags=re.DOTALL)
html2 = re.sub('</span>', '', html2, flags=re.DOTALL)
string1 = '<br/>'
string2 = '</p'

#cleaning up the html 
'''
everything inbetween <br/> (string1) and </p (string2) should be the course description.
'''
html2 = html2.replace("\n", "")
html2 = re.sub('\s+', ' ', html2)
descr = html2[html2.find(string1) : html2.find(string2)]
descr = re.sub("<br/>", '', descr)
descr = re.sub("Prerequisite:", '', descr)
descr = descr.strip()
#print(descr)

#removing all tags
html2 = re.sub('<[^>]+>', '', html2, flags=re.DOTALL)

#saving the hours through regex
html2 = html2.replace("\n", "")
hours = html2.split('Credits:', 1)[1]
hours = hours.strip()
hours = hours.partition(' ')[0]

#saving prerequisites for the class (STILL NEEDS FOR IF THE COURSE HAS MULTIPLE ONES)
prereqs = html2.split('Prerequisite:', 1)[1]
prereqs = prereqs.split('.')[0]
prereqs = prereqs.strip()
print(prereqs)


#converting the string back to a BeautifulSoup object
soup = BeautifulSoup(html2, 'html.parser')

#outputting my html (when I got curious about the process)
with open("failoutput.html", "w", encoding='utf-8') as file:
    file.write(str(html2))
