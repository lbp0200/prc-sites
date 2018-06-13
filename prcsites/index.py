from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from browsermobproxy import Server
import re

server = Server(path='/opt/browsermob-proxy-2.1.4/bin/browsermob-proxy', options={'port': 8301})
server.start()

# global prc_sites
prc_sites = {}
clicked = {}

proxy = server.create_proxy()
proxy.new_har()
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--proxy-server={host}:{port}'.format(host='localhost', port=proxy.port))

driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)
driver.set_page_load_timeout(30)


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


def add_link(url):
    if url.startswith('http') and not url.endswith('#') and not url.endswith('apk') and not url.endswith(
            'exe') and link not in clicked:
        add_domain(link)
        try:
            driver.get(link)
            clicked[url] = 1
            print('add link %s' % url)
            return True
        except Exception as e:
            print(e)

    return False


try:
    driver.get("https://www.hao123.com")
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
                    p2_link_list.append(elem2.get_attribute("href"))
                except Exception as e:
                    print(e)
            for link2 in p2_link_list:
                if add_link(link2):
                    pass
            # break
    all_requests = [entry['request']['url'] for entry in proxy.har['log']['entries']]
    for l in all_requests:
        add_link(l)
except Exception as e:
    print(e)
finally:
    driver.quit()
    server.stop()
    with open('../.env/prc-sites.txt', 'w') as f:
        f.writelines([domain + "\n" for domain in prc_sites.keys()])

    with open('../.env/clicked.txt', 'w') as f:
        f.writelines([domain + "\n" for domain in clicked.keys()])
