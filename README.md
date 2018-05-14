# Sites Monitoring Utility

This script gets urls from a text file 
and returns an information about every given url:
response status and message if a domain name is going
to expire within a month.

# How to Install

Python v3.5 should be already installed. 
Afterwards use pip (or pip3 if there is a conflict with old Python 2 setup)
to install dependecies:

```bash
pip install -r requirements.txt # alternatively try pip3
```
Remember that it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) 
for better isolation.

# Quick Start

The path of text file containing urls is the positional argument 
of the script.

To run script on Linux:
```bash
$ python check_sites_health.py sites.txt
URL: http://yandex.ru; response_status: OK; expiration date status: OK. Domain will not expire within a month.
URL: http://devman.org; response_status: OK; expiration date status: OK. Domain will not expire within a month.
```

Windows usage is the same.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
