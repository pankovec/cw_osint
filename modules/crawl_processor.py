"""
crawl_processor module

Contains the functions to process search of open-sourced information connected with specified domain
Search results are returned to report_creation module in order to create .pdf report

Arguments:
short_domain: domain name of certain website
url: http://short_domain/
"""

try:
    import socket
    import whois
    import re
    import requests
    import urllib.parse
    from colorama import Fore, Style
    from urllib.parse import urlparse
    from collections import defaultdict
    from bs4 import BeautifulSoup
    import sys
    import random
except ImportError:
    print(Fore.RED + "Can't import some requirements that are necessary to start program. Please check that all necessary requirements are installed!" + Style.RESET_ALL)
    sys.exit()

def ip_gather(short_domain):
    """
    Function for getting IP address of website
    """
    ip_address = socket.gethostbyname(short_domain)
    return ip_address

def whois_gather(short_domain):
    """
    Function for getting WHOIS information of website
    """
    w = whois.whois(short_domain)
    return w

def mail_gather(url):
    """
    Function for getting emails from website elements
    """
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    mails = []
    for i in soup.find_all(href=re.compile("mailto")):
        i.encode().decode()
        mails.append(i.string)
    return mails

def subdomains_gather(url, short_domain):
    """
    Function for subdomain search
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    linked_domains = set()

    for link in soup.find_all('a', href=True):
        domain = urlparse(link['href']).netloc
        if domain and domain != urlparse(url).netloc:
            linked_domains.add(domain)

    finder = short_domain
    subdomains = [urllib.parse.unquote(i) for i in linked_domains if finder in i]
    subdomains_amount = len(subdomains)
    return subdomains, subdomains_amount

def sm_gather(url):
    """
    Function for getting some basic social networks links from website elements
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    categorized_links = {'Facebook': [], 'Twitter': [], 'Instagram': [],
                         'Telegram': [], 'TikTok': [], 'LinkedIn': [],
                         'VKontakte': [], 'YouTube': [], 'Odnoklassniki': [], 'WeChat': []}

    for link in links:
        if 'facebook.com' in link:
            categorized_links['Facebook'].append(urllib.parse.unquote(link))
        elif 'twitter.com' in link:
            categorized_links['Twitter'].append(urllib.parse.unquote(link))
        elif 'instagram.com' in link:
            categorized_links['Instagram'].append(urllib.parse.unquote(link))
        elif 't.me' in link:
            categorized_links['Telegram'].append(urllib.parse.unquote(link))
        elif 'tiktok.com' in link:
            categorized_links['TikTok'].append(urllib.parse.unquote(link))
        elif 'linkedin.com' in link:
            categorized_links['LinkedIn'].append(urllib.parse.unquote(link))
        elif 'vk.com' in link:
            categorized_links['VKontakte'].append(urllib.parse.unquote(link))
        elif 'youtube.com' in link:
            categorized_links['YouTube'].append(urllib.parse.unquote(link))
        elif 'wechat.com' in link:
            categorized_links['WeChat'].append(urllib.parse.unquote(link))
        elif 'ok.ru' in link:
            categorized_links['Odnoklassniki'].append(urllib.parse.unquote(link))

    return categorized_links

def domains_reverse_research(subdomains):
    """
    Subdomain reverse search function which extracts social networks, emails and IP addresses
    """
    subdomain_urls = []
    subdomain_mails = []
    subdomain_socials = []
    subdomain_ip = []

    try:
        for subdomain in subdomains:
            subdomain_url = "http://" + subdomain + "/"
            subdomain_urls.append(subdomain_url)
    except (socket.gaierror, requests.exceptions.SSLError, requests.exceptions.ConnectionError):
        print(Fore.RED + 'Some URL seems unreachable! Program will continue to work, but the URL causing the error will not be included in the report' + Style.RESET_ALL)
        pass

    try:
        for subdomain in subdomains:
            subdomains_ip = ip_gather(subdomain)
            subdomain_ip.append(subdomains_ip)
            subdomain_ip = list(set(subdomain_ip))
    except (socket.gaierror, requests.exceptions.SSLError, requests.exceptions.ConnectionError):
        print(Fore.RED + 'Some URL seems unreachable! Program will continue to work, but the URL causing the error will not be included in the report' + Style.RESET_ALL)
        pass

    try:
        for subdomain_url in subdomain_urls:
            subdomain_mail = mail_gather(subdomain_url)
            subdomain_mails.append(subdomain_mail)
            subdomain_social = sm_gather(subdomain_url)
            subdomain_socials.append(subdomain_social)
    except (socket.gaierror, requests.exceptions.SSLError, requests.exceptions.ConnectionError):
        print(Fore.RED + 'Some URL seems unreachable! Program will continue to work, but the URL causing the error will not be included in the report' + Style.RESET_ALL)
        pass

    subdomain_ip = ' // '.join(subdomain_ip)
    subdomain_mails = [sublist for sublist in subdomain_mails if sublist]
    subdomain_mails = [sublist for sublist in subdomain_mails if sublist != [None]]
    subdomain_mails = ' // '.join([', '.join(map(str, sublist)) for sublist in subdomain_mails])
    subdomain_socials = [{k: v for k, v in d.items() if v} for d in subdomain_socials]
    subdomain_socials = [d for d in subdomain_socials if d]
    subdomain_socials_grouped = defaultdict(list)

    for d in subdomain_socials:
        for key, value in d.items():
            subdomain_socials_grouped[key].extend(value)

    subdomain_socials_grouped = list(dict(subdomain_socials_grouped).values())

    sd_socials = {'Facebook': [], 'Twitter': [], 'Instagram': [], 'Telegram': [], 'TikTok': [], 'LinkedIn': [],
                  'VKontakte': [], 'YouTube': [], 'Odnoklassniki': [], 'WeChat': []}

    for inner_list in subdomain_socials_grouped:
        for link in inner_list:
            if 'facebook.com' in link:
                sd_socials['Facebook'].append(urllib.parse.unquote(link))
            elif 'twitter.com' in link:
                sd_socials['Twitter'].append(urllib.parse.unquote(link))
            elif 'instagram.com' in link:
                sd_socials['Instagram'].append(urllib.parse.unquote(link))
            elif 't.me' in link:
                sd_socials['Telegram'].append(urllib.parse.unquote(link))
            elif 'tiktok.com' in link:
                sd_socials['TikTok'].append(urllib.parse.unquote(link))
            elif 'linkedin.com' in link:
                sd_socials['LinkedIn'].append(urllib.parse.unquote(link))
            elif 'vk.com' in link:
                sd_socials['VKontakte'].append(urllib.parse.unquote(link))
            elif 'youtube.com' in link:
                sd_socials['YouTube'].append(urllib.parse.unquote(link))
            elif 'wechat.com' in link:
                sd_socials['WeChat'].append(urllib.parse.unquote(link))
            elif 'ok.ru' in link:
                sd_socials['Odnoklassniki'].append(urllib.parse.unquote(link))

    sd_socials = {k: list(set(v)) for k, v in sd_socials.items()}

    return subdomain_mails, sd_socials, subdomain_ip