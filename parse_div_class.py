from bs4 import BeautifulSoup
import codecs
import sys

f = open(sys.argv[1], 'r')
html = f.read()
soup = BeautifulSoup(html)
mydivs = soup.findAll('div', class_='courseblock')
for div in mydivs:
    print('-----------------------------')
    print(str(div))
    div_soup = BeautifulSoup(str(div))
    class_code = div_soup.findAll('span', class_='code')[0].text.replace(u'\xa0', u' ')
    title = div_soup.findAll('span', class_='title')[0].text
    units = div_soup.findAll('span', class_='hours')[0].text
    description = div_soup.findAll('span', class_='descshow')[0]
    description = description.text.split('\n')[-2]
    print('class: {0}, title: {1}, units: {2}'
          .format(class_code, title, units))
    print(description)

    course_sections = div_soup.findAll('div', class_='course-section')
    text_content = {key: None for key in ['rules', 'hours', 'additional']}
    for course_section in course_sections:
        if 'Requirements' in course_section.text:
            text_content['rules'] = course_section
        if 'Hours' in course_section.text:
            text_content['hours'] = course_section
        if 'Additional' in course_section.text:
            text_content['additional'] = course_section
    for course_section, value in text_content.iteritems():
        if value:
            section_content = BeautifulSoup(str(value))
            lines = section_content.findAll('p')
            lines = [line.text for line in lines]
            text_content[course_section] = '\n'.join(lines)
    rules = text_content['rules']
    hours = text_content['hours']
    additional= text_content['additional']
    with codecs.open('output/{0}/{1}'.format(sys.argv[2], class_code), 'w', 'utf-8') as outfile:
        content = [x for x in [class_code, title, units, rules, hours, additional] if x != None]
        outfile.write('\n'.join(content))
