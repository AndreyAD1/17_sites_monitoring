import argparse
import requests
import whois
from urllib.parse import urlsplit
from datetime import datetime


def get_console_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file_path',
        default='url_list.txt',
        help='Enter the path of file containing url list.'
    )
    arguments = parser.parse_args()
    return arguments


def get_url_list_for_checking(path):
    with open(path, 'r', encoding='utf-8') as file_with_urls:
        file_content = file_with_urls.read()
    url_list = file_content.split()
    return url_list


def get_response_status(url):
    try:
        response = requests.get(url)
        return response.status_code
    except requests.exceptions.MissingSchema:
        return 'Invalid URL'
    except requests.exceptions.ConnectionError:
        return None


def get_domain_name(link):
    splitted_link = urlsplit(link)
    domain_name = splitted_link.netloc
    return domain_name


def get_domain_expiration_date(url):
    domain_name = get_domain_name(url)
    whois_response = whois.whois(domain_name)
    domain_expiration_date = whois_response.expiration_date
    if type(domain_expiration_date) is list:
        first_expiration_date = domain_expiration_date[0]
        return first_expiration_date
    return domain_expiration_date


def check_expiration_date(exp_date):
    current_date = datetime.today()
    time_gap_to_expiration_date = exp_date - current_date
    days_in_month = 31
    return time_gap_to_expiration_date.days >= days_in_month


def print_site_status(link, response, proper_expiry_date):
    response_message = 'OK'
    exp_date_message = 'OK. Domain will not expire within a month'
    if response != 200:
        response_message = 'ATTENTION: {}'.format(response)
    if not proper_expiry_date:
        exp_date_message = 'ATTENTION: domain is going to expire ' \
                           'within a month'
    print('URL: {}; response_status: {}; expiration date status: {}.'.format(
        link, response_message, exp_date_message
    ))


if __name__ == '__main__':
    console_arguments = get_console_arguments()
    input_file_path = console_arguments.file_path
    url_list = get_url_list_for_checking(input_file_path)
    for url in url_list:
        response_status = get_response_status(url)
        if response_status is None:
            exit('Can not connect to the server.')
        expiration_date = get_domain_expiration_date(url)
        proper_expiration_date = check_expiration_date(expiration_date)
        print_site_status(url, response_status, proper_expiration_date)
