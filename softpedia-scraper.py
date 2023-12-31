import os
import time
import requests
import pandas as pd
import lxml
from string import printable
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *


# prepare the option for the chrome driver
options = webdriver.FirefoxOptions()
options.add_argument('-headless')

# Use Firefox webdriver to automate switching to 'Features' tab while scraping an application
webdriver_path = os.path.join(os.getcwd(), 'geckodriver.exe')


def extract_num_pages(url):
    """
    Extract total numbers of pages for a certain domain
    :param url:
    :return: number of pages
    """

    print(url)
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(5)
    driver.implicitly_wait(5)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    last_page = soup.find(class_='fr ta_right')
    print(last_page)
    
    if last_page:
        page_links = last_page.find_all('a')
        print(page_links)
        a = int(page_links[-2].text)
        print(a)
        return int(page_links[-2].text)
    else:
        # Handle the case where the element is not found, e.g., by returning a default value.
        return 1  # Default to 1 page if element is not found



def scrape_app_features(url):
    """
    :param url: app to be scraped
    :return: a list of requirements
    """
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(5)
    driver.implicitly_wait(5)
    driver.get(url)


    try:
        # switch to 'Feature' tab in the application's page
        feature_tab = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/h3[3]')
        feature_tab.click()
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # highlights can be features, system requirements, or others
        highlights = soup.find(id='specifications').find_all("b", class_='upcase bold')
        for item in highlights:
            if item.text == 'features':
                requirements = []
                features = item.find_next('ul').find_all('li')
                for f in features:
                    if f.has_attr('class'):
                        print('[Summary] %s' % f.text)
                    else:
                        r = ''.join(filter(lambda c: c in printable, f.text))
                        requirements.append(r)

                return requirements
    except (TimeoutException, NoSuchElementException) as e:
        # page took too long to response, or couldn't find the 'Feature' tab
        # stop scraping requirements from this app
        print(e)
        return None
    finally:
        driver.quit()


def scrape_all(path):
    """
    Scrape software requirements from all domains specified in a csv file
    :param path domain file path
    :return: None. Save all scraped requirements to csv files
    """
    domains_df = pd.read_csv(path)
    # domains to be scraped
    domains = domains_df['domain']
    urls = domains_df['url']
    reqs_output = domains_df['output']


        

    for d, u, o in zip(domains, urls, reqs_output):
        # print(d, u, o, sp, ep)
        reqs_df = pd.DataFrame(columns=['domain', 'app', 'requirement', 'url'])
        num_pages = extract_num_pages(u.format(1))  # get number of pages from scraping the first page
        for page in range(1, num_pages+1):
            ll = u.format(page)
            proxy = 'http://107.1.93.222:80'
            
            r = requests.get(u.format(page), proxies={"http": proxy, "https": proxy})
            if r.status_code != 200:
                print('can\'t retrieve the html!')
                continue

            soup = BeautifulSoup(r.content, 'lxml')
            app_items = soup.select('div.grid_48.dlcls')

            for item in app_items:
                url = item.find('h4', class_='ln').find('a')['href']
                app_name = url[url.rfind('/') + 1:len(url)].replace('.shtml', '')
                print('Start scraping requirements from {}'.format(url))
                requirements = scrape_app_features(url)
                if requirements:
                    try:
                        reqs_df = reqs_df.append(pd.DataFrame({
                                                'domain': [d] * len(requirements),
                                                'app': [app_name] * len(requirements),
                                                'requirement': requirements,
                                                'url': [url] * len(requirements)
                                                }))
                        reqs_df.to_csv(os.path.join(os.getcwd(), 'requirement', o), index=False)
                    except Exception as e:
                        print(e)
                time.sleep(0.5)
            print("Finished Page Number {}".format(page))
        print('Completed collecting requirements for domain %s' % d)


if __name__ == '__main__':
    domains_file_path = os.path.join(os.getcwd(), 'domains.csv')
    scrape_all(domains_file_path)

