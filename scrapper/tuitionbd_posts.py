# Author: Mahmood Al Rayhan
# Created on: February 12, 2019

"""
About the Script:
    * This script extracts necessary data from tuition post details
"""

import datetime
import json

import requests
from bs4 import BeautifulSoup


class TuitionDetailsInfo:
    def __init__(self):
        self.all_tuition_url = 'http://bdtutors.com/all_tuitions.html'
        self.tuition_detail_links = []

    def get_html_text(self, url):
        """
        Get the HTML text of page of given `url`

        :param url: link of a web page
        :return: HTML text of page
        """
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

    def get_single_post_details(self, tuition_post_page):
        """
        Get relevant information from `tuition_post_page` HTML text
        :param tuition_post_page: HTML text of page
        :return: tuition post information
        """
        info = {}
        soup = BeautifulSoup(tuition_post_page, 'html.parser')
        element = soup.find_all('div', {'class': 'c8'})[0]
        element = element.find_all('div', {'class': 'row'})

        # get tuition ID
        emt = element[0].text
        emt = emt.replace('\r\n\t', '')
        k, v = emt.split('#')
        k, v = k.strip(), v.strip()
        info[k.replace(' ', '_')] = v

        emt = element[1].text
        emt = emt.strip().replace('\n', '').replace('\r', ' ')
        info['description'] = emt

        info['details'] = {}

        for i in range(2, 6):
            emts = element[i]
            emts = emts.find_all('div', {'class': 'c6'})
            emt1, emt2 = emts[0].text, emts[1].text
            k, v = self.get_kv(emt1, ':')
            info['details'][k.replace(' ', '_')] = v
            k, v = self.get_kv(emt2, ':')
            info['details'][k.replace(' ', '_')] = v
        emt = element[6]
        emt = emt.find_all('div', {'class': 'c6'})[1]
        emt = emt.text
        k, v = self.get_kv(emt, ':')
        info['details'][k.replace(' ', '_')] = v

        return info

    def aggregate_pages(self, url_list):
        """
        Aggregate a list of pages from a list of urls
        :param url_list: a list of urls which HTML will be aggregated
        :return: list of HTML page text
        """
        html_pages = []
        for url in url_list:
            page = self.get_html_text('http://bdtutors.com/' + url)
            html_pages.append(page)
        return html_pages

    def get_tuition_post_details(self):
        """
        Aggregates the relevant tuition post info for `current day`
        :return: a dict containing tuition post info for `current day`
        """
        tuition_details_link = self.extract_tuition_details_urls()
        all_details_page = self.aggregate_pages(tuition_details_link)
        info_list = []
        for page in all_details_page:
            info = self.get_single_post_details(page)
            info_list.append(info)
        return {
            'date': str(datetime.datetime.now().date()),
            'all_post': info_list
        }

    def dump_into_json(self):
        data = self.get_tuition_post_details()
        with open('tuition_post_' + str(datetime.datetime.now().date()) + '.json', 'w') as file:
            json.dump(data, file, indent=4)


if __name__ == '__main__':
    TuitionDetailsInfo().dump_into_json()
