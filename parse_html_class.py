from HTMLParser import HTMLParser
import os
import subprocess
import sys
import urllib2

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    in_link = False
    link = ''
    class_list = []

    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag
        if tag == 'a':
            self.in_link = True
            self.link = attrs[0][1]
    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag
        self.in_link = False
    def handle_data(self, data):
        print "Encountered some data  :", data
        if self.in_link:
            self.class_list.append((data, self.link))

if not os.path.exists('output'): 
    os.mkdir('output')

if (len(sys.argv) < 2):
    print "Please enter the name of the input class page to parse"
    sys.exit()
f = open(sys.argv[1], 'r')
parser = MyHTMLParser()
parser.feed(f.read())
for subject, link in parser.class_list:
    # Links are now relative, so append it to the base address
    link = 'http://guide.berkeley.edu' + link
    response = urllib2.urlopen(link)
    html = response.read()
    course_title = subject[subject.find('(')+1:subject.find(')')]

    # Make sure to sanitize the file names to account for cases such
    # as Malaysian/Indonesian, where the backslash makes a difference
    output_directory = 'output/' + course_title.replace('/', ' ')
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    with open('temp.html', 'w') as outfile:
        outfile.write(html)
    subprocess.call(['python', 'parse_div_class.py', 'temp.html', course_title])
