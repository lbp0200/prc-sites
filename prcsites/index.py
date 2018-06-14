# coding=utf-8
from __future__ import unicode_literals
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
import re

# global prc_sites
prc_sites = {}
clicked = {}
loaded_url = {}

chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)

firefox_options = Options()
driver = webdriver.Firefox(executable_path='geckodriver', firefox_options=firefox_options)

driver.set_page_load_timeout(5)


def get_root_domain(url):
    r = re.findall(':\/\/([\w\.]+\.)?(\w+\.[a-zA-Z]{2,})', url)
    for m in r:
        if len(m) == 2 and m[1] and 'google' not in m[1]:
            return m[1]
        else:
            print('error get_root_domain ', m)
            # raise m


def get_domain(url):
    r = re.findall(':\/\/([\w\.]+\.[a-zA-Z]{2,})', url)
    if r:
        return r[0]


def add_domain(url):
    domain = get_root_domain(url)
    if domain is not None and not domain.endswith('.cn') and domain not in prc_sites:
        prc_sites[domain] = 1
        print('add domain', domain)
    else:
        # print(domain)
        pass


def add_link(url):
    if url.startswith('http') and 'google' not in url:
        add_domain(url)
        full_domain = get_domain(url)
        if full_domain and full_domain not in clicked:
            try:
                if not url.endswith('apk') and not url.endswith('exe'):
                    driver.get(url)
                    clicked[full_domain] = 1
                    print('full domain %s , add link %s ' % (full_domain, url))
                    timings = driver.execute_script("return window.performance.getEntries();")
                    for pfm in timings:
                        if 'initiatorType' in pfm:
                            # print('loaded resource %s' % pfm['name'])
                            add_domain(pfm['name'])
                            tmp_full_domain = get_domain(pfm['name'])
                            loaded_url[tmp_full_domain] = 1
                    return True
            except Exception as e:
                print(e)
                # driver.refresh()

    return False


try:
    add_link("https://www.hao123.com")

    # driver.get("http://www.people.com.cn/")
    # ':\/\/(www[0-9]?\.)?(.[^/:]+)'
    elems = driver.find_elements_by_xpath("//a[@href]")
    print(len(elems))
    p1_link_list = []
    for elem in elems:
        try:
            p1_link_list.append(elem.get_attribute("href"))
        except Exception as e:
            print(e)

    for link in p1_link_list:
        if add_link(link):

            p2_link_list = []
            elems2 = driver.find_elements_by_xpath("//a[@href]")
            for elem2 in elems2:
                try:
                    if elem2.text == u'更多>>':
                        p2_link_list.append(elem2.get_attribute("href"))
                except Exception as e:
                    print(e)
            for link2 in p2_link_list:
                if add_link(link2):
                    pass
            # break
    # all_requests = [entry['request']['url'] for entry in proxy.har['log']['entries']]
    for l in loaded_url:
        add_domain(l)
except Exception as e:
    print(e)
finally:
    driver.quit()
    with open('../.env/prc-sites.txt', 'w') as f:
        f.writelines([domain + "\n" for domain in prc_sites.keys()])

    with open('../.env/clicked.txt', 'w') as f:
        f.writelines([domain + "\n" for domain in clicked.keys()])
