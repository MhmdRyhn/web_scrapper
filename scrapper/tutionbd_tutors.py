# Author: Mahmood Al Rayhan
# Created on: February 12, 2019

"""
About the Script:
    * This script extracts necessary data from tuition post details
    * Also extracts necessary data of the teachers
"""

from pprint import pprint

import requests
from bs4 import BeautifulSoup


class TuitionDetailsInfo:
    def __init__(self):
        # self.all_tuition_url = all_tuition_url
        self.all_tuition_url = 'http://bdtutors.com/all_tuitions.html'
        self.tuition_detail_links = []
        self.info = {}

    def get_html_text(self, url):
        page = requests.get(url)
        page = page.text
        return page

    def extract_tuition_details_urls(self):
        """
        Extracts the `links` of tuition details pages

        :param all_tuition_url: url of all tuition
        :return: a `list of urls` to tuition details page
        """

        page = self.get_html_text(self.all_tuition_url)
        soup = BeautifulSoup(page, 'html.parser')
        all_button_tag = soup.find_all(name='button', text='View Details ')
        for button in all_button_tag:
            # Finds the immediate parent tag of `button` tag
            anchor_tag = button.parent.get('href')
            if anchor_tag:
                self.tuition_detail_links.append(anchor_tag)
        return self.tuition_detail_links

    def get_kv(self, element, sep):
        k, v = element.split(sep)
        return k.strip(), v.strip()
        # k, v = k.strip(), v.strip()
        # self.info[k.replace(' ', '_')] = v

    def get_single_post_details(self, tuition_post_page):
        # tuition_post_page = self.get_html_text('http://bdtutors.com/' + url)
        soup = BeautifulSoup(tuition_post_page, 'html.parser')
        element = soup.find_all('div', {'class': 'c8'})[0]
        element = element.find_all('div', {'class': 'row'})

        # get tuition ID
        emt = element[0].text
        emt = emt.replace('\r\n\t', '')
        k, v = emt.split('#')
        k, v = k.strip(), v.strip()
        self.info[k.replace(' ', '_')] = v

        emt = element[1].text
        emt = emt.strip().replace('\n', '').replace('\r', ' ')
        # print(emt)
        self.info['description'] = emt

        self.info['details'] = {}

        for i in range(2, 6):
            emts = element[i]
            emts = emts.find_all('div', {'class': 'c6'})
            # pprint(emts)
            emt1, emt2 = emts[0].text, emts[1].text
            # print(emt1, emt2)
            # print('-' * 20)
            k, v = self.get_kv(emt1, ':')
            self.info['details'][k.replace(' ', '_')] = v
            k, v = self.get_kv(emt2, ':')
            self.info['details'][k.replace(' ', '_')] = v
        emt = element[6]
        # print('emt:', emt)
        emt = emt.find_all('div', {'class': 'c6'})[1]
        emt = emt.text
        k, v = self.get_kv(emt, ':')
        self.info['details'][k.replace(' ', '_')] = v

        pprint(self.info)
        return self.info

    def aggregate_pages(self, url_list):
        html_pages = []
        for url in url_list:
            page = self.get_html_text('http://bdtutors.com/' + url)
            html_pages.append(page)
        return html_pages

    def get_tuition_post_details(self):
        tuition_details_link = self.extract_tuition_details_urls()
        pprint(tuition_details_link)
        all_details_page = self.aggregate_pages(tuition_details_link)
        info_list = []
        for page in all_details_page:
            info = self.get_single_post_details(page)
            info_list.append(info)
        return info_list


if __name__ == '__main__':
    info_of_today = TuitionDetailsInfo().get_tuition_post_details()
    # pprint(info_of_today)
    # print(len(info_of_today))
    d = {
        'all_info': info_of_today
    }
    import json

    with open('today.json', 'w') as file:
        json.dump(d, file, indent=4)

"""
http://bdtutors.com/all_tuitions.html

['index.php?cms=tuitiondetails&id=2092019100925',
 'index.php?cms=tuitiondetails&id=2042019054058',
 'index.php?cms=tuitiondetails&id=2032019102130',
 'index.php?cms=tuitiondetails&id=2042019082326',
 'index.php?cms=tuitiondetails&id=2082019081854',
 'index.php?cms=tuitiondetails&id=2032019124159',
 'index.php?cms=tuitiondetails&id=2062019090918',
 'index.php?cms=tuitiondetails&id=2102019102804',
 'index.php?cms=tuitiondetails&id=2092019062206',
 'index.php?cms=tuitiondetails&id=2092019055304',
 'index.php?cms=tuitiondetails&id=1302019090259',
 'index.php?cms=tuitiondetails&id=2052019084653',
 'index.php?cms=tuitiondetails&id=2102019121017',
 'index.php?cms=tuitiondetails&id=2042019053511',
 'index.php?cms=tuitiondetails&id=2032019104835',
 'index.php?cms=tuitiondetails&id=2042019103447',
 'index.php?cms=tuitiondetails&id=2052019120941',
 'index.php?cms=tuitiondetails&id=2102019083410',
 'index.php?cms=tuitiondetails&id=2012019093551']
"""
