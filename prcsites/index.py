from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
import re

global prc_sites
prc_sites = {}


def get_root_domain(url):
    r = re.findall(':\/\/([\w\.]+\.)?(\w+\.\w+)', url)
    for m in r:
        if len(m) == 2:
            return m[1]
        else:
            print(m)
            raise m


def add_domain(url):
    domain = get_root_domain(url)
    if domain is not None and not domain.endswith('.cn') and domain not in prc_sites:
        prc_sites[domain] = 1
        print('add domain', domain)
    else:
        # print(domain)
        pass


chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)
try:
    clicked = {}
    driver.get("https://www.hao123.com")
    # ':\/\/(www[0-9]?\.)?(.[^/:]+)'
    elems = driver.find_elements_by_xpath("//a[@href]")
    print(len(elems))
    for elem in elems:
        link = elem.get_attribute("href")
        print(link)
        add_domain(link)
        # continue
        if link.startswith('http') and link not in clicked:
            driver.get(link)
            elems2 = driver.find_elements_by_xpath("//a[@href]")
            for elem2 in elems2:
                link2 = elem2.get_attribute("href")
                print(link2)
                add_domain(link2)
                # domain = get_root_domain(link2)
                # prc_sites[link2] = 1
            clicked[link] = 1
            # break

except:
    pass
finally:
    driver.quit()
    with open('prc-sites.txt', 'w') as f:
        f.writelines([domain + "\n" for domain in prc_sites.keys()])