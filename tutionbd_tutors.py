# Author: Mahmood Al Rayhan
# Created on: February 12, 2019

"""
About the Script:
    * This script extracts necessary data from tuition post details
    * Also extracts necessary data of the teachers
"""

import requests
from bs4 import BeautifulSoup


def extract_tuition_details_url(all_tuition_url):
    """
    Extracts the `links` of tuition details pages

    :param all_tuition_url: url of all tuition
    :return: a `list of urls` to tuition details page
    """

    tuition_detail_links = []
    page = requests.get(all_tuition_url)
    page = page.text
    soup = BeautifulSoup(page, 'html.parser')
    all_button_tag = soup.find_all(name='button', text='View Details ')
    for button in all_button_tag:
        # Finds the immediate parent tag of `button` tag
        anchor_tag = button.parent.get('href')
        if anchor_tag:
            tuition_detail_links.append(anchor_tag)
    return tuition_detail_links


if __name__ == '__main__':
    from pprint import pprint

    tuition_detail_info_links = extract_tuition_details_url(
        'http://bdtutors.com/all_tuitions.html'
    )
    print(len(tuition_detail_info_links))
    pprint(tuition_detail_info_links)
