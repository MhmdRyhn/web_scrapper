from bs4 import BeautifulSoup
import requests
from pprint import pprint
from selenium import webdriver


class TutorInformation:
    def __init__(self):
        # self.tutor_url = 'http://bdtutors.com/tutor/21925139.html'
        self.tutor_url = 'http://bdtutors.com/tutor/21924544.html'
        # self.tutor_url = 'http://bdtutors.com/tutor/21924549.html'
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

    def get_protected_email(self, cfemail):
        encoded_bytes = bytes.fromhex(cfemail)
        email = bytes(byte ^ encoded_bytes[0] for byte in encoded_bytes[1:]).decode('utf8')
        return email

    def clean_data(self, data):
        return data.replace('\'', '').strip().rstrip()

    def tutor_overview(self, page):
        overview = {}
        soup = BeautifulSoup(page, 'html.parser')

        # Joining Date
        joined = soup.find_all('strong', text='Member Since:')[0]
        overview[joined.text] = self.clean_data(self.nth_next_element(joined, 2))

        div_class_c8 = soup.find_all(name='div', class_='c8')[1]
        necessary = div_class_c8.find_all(name='strong')
        # pprint(necessary)

        # Name, Experience, Qualification, Phone, Email
        for index in [0, 3, 4, 8, 9]:
            tag = necessary[index]
            key = 'Name'
            if index:
                key = self.clean_data(self.nth_next_element(tag, 1))
            if key == 'Email:':
                data = self.nth_next_element(tag, 3)
                cfemail = data.__dict__['attrs'].get('data-cfemail')
                data = self.get_protected_email(cfemail)
            else:
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
        return overview

    def tuition_info(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        expected = soup.find_all('div', class_='style_border_p')[0]
        c3_class = expected.find_all('div', class_='c3')
        c9_class = expected.find_all('div', class_='c9')
        # pprint(c3_class)
        # print('*'*60)
        # pprint(c9_class)

        min_len = min(len(c3_class), len(c9_class))
        info = {}

        for i in range(min_len):
            key = self.clean_data(c3_class[i].text)
            if i < 3:
                value = self.clean_data(c9_class[i].text)
            else:
                checkbox = c9_class[i].find_all('input')
                value = [self.clean_data(self.nth_next_element(k, 1)) for k in checkbox]
            info[key] = value
        return info

    def educational_qualification(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        expected = soup.find_all('div', class_='style_border_sl')

        education = []
        for row in expected:
            school = {}
            whole_row = row.find_all('div', class_='row')
            first_half = whole_row[0]
            second_half = whole_row[1]
            f3 = first_half.find_all('div')
            s3 = second_half.find_all('div')
            # print(s3)

            # print(self.clean_data(f3[0].text))
            # for k in [0, 1, 2]:
            #     print(self.clean_data(f3[k].text))
            #     print('----')

            # a = s3[0].next_element + s3[0].next_element.next_element.next_element
            # print(self.clean_data(a))
            # for k in [1, 2]:
            #     print(self.clean_data(s3[k].text))
            #     print('----')

            school['Exam'] = self.clean_data(f3[0].text)
            school['Subject / Group'] = self.clean_data(f3[1].text)
            school['Institute'] = self.clean_data(f3[2].text)
            school['Result'] = self.clean_data(self.nth_next_element(s3[0], 1)) + \
                               self.clean_data(self.nth_next_element(s3[0], 3))
            school['Passing Year'] = self.clean_data(s3[1].text)
            school['Awards'] = self.clean_data(s3[2].text)

            education.append(school)
        return education

    def tutor_details(self):
        page = self.get_html_text()
        overview = self.tutor_overview(page)
        info = self.tuition_info(page)
        education = self.educational_qualification(page)
        return {
            'tutor_overview': overview,
            'tuition_info': info,
            'education': education
        }


if __name__ == '__main__':
    obj = TutorInformation()
    pprint(obj.tutor_details())
