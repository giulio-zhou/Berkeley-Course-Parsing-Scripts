from bs4 import BeautifulSoup
import os
import subprocess
import urllib2

link = 'http://guide.berkeley.edu/courses'
response = urllib2.urlopen(link)
html = response.read()
soup = BeautifulSoup(html)

# Grab the list of course links from the atozindex div element
a_to_z_div = soup.find('div', {'id': 'atozindex'})
with open('class_list.html', 'w') as outfile:
    outfile.write(str(a_to_z_div))

# Call the class list parser on the extracted file
subprocess.call(['python', 'parse_html_class.py', 'class_list.html'])
