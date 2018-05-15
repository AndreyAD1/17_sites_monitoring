import argparse
import requests
import whois
from datetime import datetime
import socket


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


def does_server_respond_with_ok(url):
    try:
        response = requests.get(url)
        return response.ok
    except requests.exceptions.ConnectionError:
        return None


def get_domain_expiration_date(url):
    try:
        whois_response = whois.whois(url)
        domain_expiration_date = whois_response.expiration_date
        if type(domain_expiration_date) is list:
            first_exp_date_index = 0
            first_expiration_date = domain_expiration_date[first_exp_date_index]
            return first_expiration_date
        return domain_expiration_date
    except socket.gaierror:
        return None


def check_expiration_date(exp_date, days_number=31):
    if exp_date is None:
        return None
    current_date = datetime.today()
    time_gap_to_expiration_date = exp_date - current_date
    return time_gap_to_expiration_date.days >= days_number


def print_site_status(link, ok_response, proper_expiry_date):
    response_message = 'OK'
    exp_date_message = 'OK (domain will not expire soon)'
    if ok_response is None:
        response_message = 'No connection'
    if ok_response is False:
        response_message = 'WARNING! Response status is not OK'
    if proper_expiry_date is None:
        exp_date_message = 'WARNING! Can`t get the expiration date of domain'
    if proper_expiry_date is False:
        exp_date_message = 'WARNING! Domain is going to expire within a month'
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
        server_responds_ok = does_server_respond_with_ok(url)
        expiration_date = get_domain_expiration_date(url)
        proper_expiration_date = check_expiration_date(expiration_date)
        print_site_status(url, server_responds_ok, proper_expiration_date)
