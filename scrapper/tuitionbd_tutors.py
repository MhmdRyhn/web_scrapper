from bs4 import BeautifulSoup
import requests
from pprint import pprint
from selenium import webdriver


class TutorInformation:
    def __init__(self):
        # self.tutor_url = 'http://bdtutors.com/tutor/21925139.html'
        self.tutor_url = 'http://bdtutors.com/tutor/21924544.html'
        self.tutor_info_details = {}

    def get_html_text(self):
        """
        Get the HTML text of page of given `url`

        :param url: link of a web page
        :return: HTML text of page
        """
        page = requests.get(self.tutor_url)
        page = page.text
        return page

    def nth_next_element(self, element, n):
        for i in range(n):
            element = element.next_element
        return element

    def clean_data(self, data):
        return data.replace('\'', '').strip().rstrip()

    def tutor_overview(self, page):
        overview = {}
        soup = BeautifulSoup(page, 'html.parser')
        div_class_c8 = soup.find_all(name='div', class_='c8')[1]

        necessary = div_class_c8.find_all(name='strong')
        pprint(necessary)

        # Name, Experience, Qualification, Phone
        for index in [0, 3, 4, 8]:
            tag = necessary[index]
            key = 'Name'
            if index:
                key = self.clean_data(self.nth_next_element(tag, 1))
            data = self.nth_next_element(tag, 2)
            overview[self.clean_data(key)] = self.clean_data(data)

        # Area covered, Subjects
        for index in [5, 7]:
            tag = necessary[index]
            key1 = self.clean_data(self.nth_next_element(tag, 1))
            nxt = 4
            if index == 5:
                nxt = 7
            details = self.nth_next_element(tag, nxt)
            details = list(map(self.clean_data, details.split(',')))
            if index == 5:
                key2 = self.nth_next_element(tag, 4)
                overview[key1] = {}
                overview[key1][key2] = details
            else:
                overview[key1] = details

        # # Name
        # name = necessary[0]
        # # key = self.clean_data(self.nth_next_element(name, 1))
        # name = self.nth_next_element(name, 2)
        # overview[name] = self.clean_data(name)
        #
        # # Experience
        # experience = necessary[3]
        # experience = self.nth_next_element(experience, 2)
        # overview['experience'] = self.clean_data(experience)
        #
        # # Qualification
        # qualification = necessary[4]
        # qualification = self.nth_next_element(qualification, 2)
        # overview['qualification'] = self.clean_data(qualification)
        #
        # # Phone
        # phone = necessary[8]
        # phone = self.nth_next_element(phone, 2)
        # overview['phone'] = self.clean_data(phone)

        # # Area Covered
        # area = necessary[5]
        # key = self.clean_data(self.nth_next_element(area, 1))
        # area_name = self.nth_next_element(area, 4)
        # area_details = self.nth_next_element(area, 7)
        # area_details = list(map(self.clean_data, area_details.split(',')))
        # overview[key] = {}
        # overview[key][area_name] = area_details
        #
        # # Subjects
        # subjects = necessary[7]
        # key = self.clean_data(self.nth_next_element(subjects, 1))
        # subjects = self.nth_next_element(subjects, 4)
        # subjects = list(map(self.clean_data, subjects.split(',')))
        # overview[key] = subjects

        pprint(overview)

    def tutor_details(self):
        page = self.get_html_text()
        self.tutor_overview(page)


if __name__ == '__main__':
    TutorInformation().tutor_details()
