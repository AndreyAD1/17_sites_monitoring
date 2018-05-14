import argparse
import requests
import whois
from datetime import datetime
import requests.exceptions as exceptions


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
    try:
        with open(path, 'r', encoding='utf-8') as file_with_urls:
            file_content = file_with_urls.read()
        urls = file_content.split()
        return urls
    except FileNotFoundError:
        return None


def get_response_status(link):
    try:
        response = requests.get(link)
        return response.status_code
    except (exceptions.MissingSchema, exceptions.InvalidURL):
        return False
    except exceptions.ConnectionError:
        return None


def get_domain_expiration_date(link):
    whois_response = whois.whois(link)
    domain_expiration_date = whois_response.expiration_date
    if type(domain_expiration_date) is list:
        earliest_expiration_date = min(domain_expiration_date)
        return earliest_expiration_date
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
    if url_list is None:
        exit('Can not find the input file.')
    for url in url_list:
        response_status = get_response_status(url)
        if response_status is None:
            print('Can not connect to the {}'.format(url))
            continue
        if response_status is False:
            print('{} is invalid URL.'.format(url))
            continue
        expiration_date = get_domain_expiration_date(url)
        proper_expiration_date = check_expiration_date(expiration_date)
        print_site_status(url, response_status, proper_expiration_date)
