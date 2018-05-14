import argparse
import requests
import whois
from datetime import datetime
import requests.exceptions as exc


def get_console_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file_path',
        default='url_list.txt',
        help='Enter the path of file containing url list.'
    )
    arguments = parser.parse_args()
    return arguments


def load_url_list_for_checking(path):
    try:
        with open(path, 'r', encoding='utf-8') as file_with_urls:
            file_content = file_with_urls.read()
        urls = file_content.split()
        return urls
    except FileNotFoundError:
        return None


def get_response_status(url):
    try:
        response = requests.get(url)
        return response.ok
    except (exc.MissingSchema, exc.InvalidSchema, exc.InvalidURL):
        return 'invalid URL'
    except exc.ConnectionError:
        return None


def get_domain_expiration_date(url):
    whois_response = whois.whois(url)
    domain_expiration_date = whois_response.expiration_date
    if type(domain_expiration_date) is list:
        first_exp_date_index = 0
        first_expiration_date = domain_expiration_date[first_exp_date_index]
        return first_expiration_date
    return domain_expiration_date


def check_expiration_date(exp_date, days_number=31):
    current_date = datetime.today()
    time_gap_to_expiration_date = exp_date - current_date
    return time_gap_to_expiration_date.days >= days_number


def print_site_status(link, response_status, proper_expiry_date):
    response_message = 'OK'
    exp_date_message = 'OK (domain will not expire soon)'
    if response_status is None:
        response_message = 'no connection'
    if response_status == 'invalid URL':
        print('{} is invalid URL.'.format(url))
        return
    if response_status is False:
        response_message = 'WRONG'
    if not proper_expiry_date:
        exp_date_message = 'WARNING: domain is going to expire within a month'
    print(
        '{}\nResponse: {}. Expiration date: {}.'.format(
            link,
            response_message,
            exp_date_message
        )
    )


if __name__ == '__main__':
    console_arguments = get_console_arguments()
    input_file_path = console_arguments.file_path
    url_list = load_url_list_for_checking(input_file_path)
    if url_list is None:
        exit('Can not find the input file.')
    for url in url_list:
        response_status = get_response_status(url)
        expiration_date = get_domain_expiration_date(url)
        proper_expiration_date = check_expiration_date(expiration_date)
        print_site_status(url, response_status, proper_expiration_date)
