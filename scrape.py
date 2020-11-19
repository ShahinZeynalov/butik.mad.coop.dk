from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from tasks import scrape_data
import uuid
import csv
from pathlib import Path
from selenium.webdriver.common.action_chains import ActionChains
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

class CoopScraper():
    def __init__(self):
        self.file_name = self.create_file()
        opts = Options()
        opts.headless = False
        opts.add_argument("--proxy-server=http://qtsdugh7:f2cc5y3t@regina.ltespace.com:16890/")
        profile = webdriver.FirefoxProfile()

        profile.set_preference("dom.webnotifications.enabled", False)
        self.browser = webdriver.Firefox(firefox_profile=profile, options=opts, executable_path=f'{BASE_DIR}/geckodriver')
        self.coop_list()
        # self.scrape_urls()
        # self.get_urls()
        # self.browser.close()

    def coop_list(self):

        with open('scraped_urls.txt', 'r') as file:
            urls = file.readlines()
        with open(f'all_scraped_data/{self.file_name}.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            clicked = False
            for i, url in enumerate(urls):
                print('--', i, url)
                self.browser.get(url)
                # self.browser.find_element_by_id('acceptAllButton').click()
                if not clicked:
                    self.browser.find_element_by_class_name('coi-banner__accept').click()
                    clicked = True

                # break
                time.sleep(1)
                breadcrumb = ''
                product_header = ''
                product_name = ''
                basic_info = ''
                labels = ''
                current_price = ''
                original_price = ''
                weight = ''
                product_info = ''
                opbevaring = ''
                ingrediencer = ''
                tilbereding = ''
                basic_info_wrap_div = self.browser.find_element_by_class_name('c-product-detail__basic-info-wrap')
                try:
                    breadcrumb = self.browser.find_element_by_class_name('c-breadcrumb').text
                except:
                    breadcrumb = []
                try:
                    product_header = basic_info_wrap_div.find_element_by_tag_name('p').text
                except:
                    product_name=''
                try:
                    product_name = basic_info_wrap_div.find_element_by_class_name('c-product-detail__title').text
                except:
                    product_name=''
                try:
                    basic_info = basic_info_wrap_div.find_element_by_class_name('c-product-detail__product-info').text
                except:
                    basic_info = ''
                try:
                    labels = [i.get_attribute('title') for i in basic_info_wrap_div.find_elements_by_tag_name('i')]
                except:
                    labels = []
                try:
                    current_price = basic_info_wrap_div.find_element_by_class_name('c-product-detail__price').text
                    current_price = current_price[:-3]+'.'+current_price[-2:]
                except:
                    current_price = ''
                try:
                    original_price = self.browser.find_element_by_class_name('line-through').text
                    original_price = original_price[:-3]+'.'+original_price[-2:]
                except:
                    original_price = ''
                try:
                    weight = self.browser.find_elements_by_class_name('text-grey-darker')[-1].text
                except:
                    weight = ''

                try:
                    self.browser.execute_script("window.scrollTo(0, window.scrollY + 500)") 
                    time.sleep(1)
                    self.browser.save_screenshot('detail.png')
                    tabs = self.browser.find_elements_by_class_name('tabs-component-tab-a')
                    for i in range(len(tabs)):
                        tabs[i].click()
                        tab_text = tabs[i].text
                        panel_text = self.browser.find_element_by_class_name('tabs-component-panels').text
                        print('-- tab text', tab_text)
                        if tab_text.lower() == 'produktinfo':
                            product_info = panel_text
                        elif tab_text.lower() == 'opbevaring':
                            opbevaring = panel_text
                        elif tab_text.lower() == 'ingredienser':
                            ingrediencer = panel_text
                        elif tab_text.lower() == 'tilberedning':
                            tilbereding = panel_text
                        else:
                            continue
                        
                        # print(product_info.text)
                    time.sleep(1)
                except Exception as e:
                    product_detail = ''
                labels = ','.join([str(elem) for elem in labels])
                # breadcrumb = ' > '.join([str(elem) for elem in breadcrumb])
                url = self.browser.current_url

                data = [
                    breadcrumb, product_header, product_name, 
                    basic_info, labels, current_price, original_price, weight, 
                    product_info, opbevaring, ingrediencer, tilbereding, url
                ]

                if len(product_name) != 0:
                    writer.writerow(data)

        # with open('scraped_urls9001-10073.txt', 'r') as file:
        #     urls = file.readlines()
        #     with open(f'all_scraped_data/{self.file_name}.csv', 'a+', newline='') as file:
        #         writer = csv.writer(file)
        #         click = True
        #         for i, url in enumerate(urls):
        #             print('-----------------------------', i, url)
        #             self.browser.get(url)
        #             if click:
        #                 self.browser.find_element_by_class_name('coi-banner__accept').click()
        #                 click = False
        #             time.sleep(1)
        #             breadcrumb = ''
        #             product_name = ''
        #             weight = ''

        #             brand = ''
        #             egnet_til = ''
        #             emballage = ''
        #             farve = ''
        #             klasse = ''
        #             land = ''
        #             markininger = ''
        #             oprindes = ''
        #             sort = ''
        #             storelse = ''
        #             type_of_product = ''

        #             product_detail_labels = ''
        #             base_price = ''
        #             discounted_price = ''
        #             product_attributes = ''
        #             product_detail = ''
        #             url = ''

        #             try:
        #                 breadcrumb = self.browser.find_element_by_tag_name('breadcrumb')
        #                 breadcrumb = [i.text for i in breadcrumb.find_elements_by_tag_name('li')]
        #             except:
        #                 breadcrumb = []
        #             try:
        #                 product_name = self.browser.find_element_by_class_name('product-detail__header').text
        #             except:
        #                 product_name=''
        #             try:
        #                 weight = self.browser.find_element_by_class_name('product-detail__subheader').text
        #             except:
        #                 product_name_subheader = ''
        #             try:
        #                 labels = [i.get_attribute('alt') for i in self.browser.find_elements_by_class_name('labels__item-image')]

        #             except:
        #                 labels = []
        #             try:
        #                 base_price = self.browser.find_element_by_class_name('pricecontainer__base-price').text
        #                 base_price = base_price[:-3]+'.'+base_price[-2:]
        #             except:
        #                 base_price = ''
        #             try:
        #                 discounted_price = self.browser.find_element_by_class_name('pricecontainer__campaign-price').text
        #                 discounted_price = discounted_price[:-3]+'.'+discounted_price[-2:]
        #             except:
        #                 discounted_price = ''
        #             try:
        #                 product_attributes = self.browser.find_elements_by_class_name('product-detail__attribute')
                        
        #                 for i in range(len(product_attributes)):
        #                     key = product_attributes[i].find_element_by_class_name('product-detail__attribute-key').text
        #                     values = product_attributes[i].find_elements_by_class_name('product-detail__attribute-value')
        #                     value = ' '.join([str(elem.text) for elem in values])
        #                     if key.startswith('Brand'):
        #                         brand = value
        #                     elif key.startswith('Egnet'):
        #                         egnet_til = value
        #                     elif key.startswith('Emballage'):
        #                         emballage = value
        #                     elif key.startswith('Farve'):
        #                         farve = value
        #                     elif key.startswith('Klas'):
        #                         klasse = value
        #                     elif key.startswith('Land'):
        #                         land = value
        #                     elif key.startswith('Mærk'):
        #                         markininger = value
        #                     elif key.startswith('Opri'):
        #                         oprindes = value
        #                     elif key.startswith('Sort'):
        #                         sort = value
        #                     elif key.startswith('Stø'):
        #                         storelse = value
        #                     elif key.startswith('Type'):
        #                         type_of_product = value

        #             except Exception as e:
        #                 pass
        #             try:
        #                 self.browser.execute_script("window.scrollTo(0, window.scrollY + 500)") 
        #                 time.sleep(1)
        #                 self.browser.save_screenshot('detail.png')
        #                 product_detail = self.browser.find_element_by_class_name('product-detail__description-text').text
        #                 time.sleep(1)
        #             except Exception as e:
        #                 product_detail = ''
        #             labels = ','.join([str(elem) for elem in labels])
        #             breadcrumb = ' > '.join([str(elem) for elem in breadcrumb])
        #             url = self.browser.current_url

        #             data = [
        #                 breadcrumb, product_name, weight, 
        #                 labels, base_price, discounted_price, brand, egnet_til, 
        #                 emballage, farve, klasse, land, markininger, 
        #                 oprindes, sort, storelse, type_of_product, product_detail, url
        #             ]
        #             if len(product_name) != 0:
        #                 writer.writerow(data)

    def create_file(self):
        filename = 'nemlig'+uuid.uuid4().hex

        header = [
            'Breadcrumb','Product header','Product name', 'Product basic info',
            'Labels', 'Current price', 'Original price', 'weight', 'product info', 'Opbevaring',
            'Ingrediencer', 'Tilbereding', 'URL'
        ]
        new_file = open(f'all_scraped_data/{filename}.csv', 'w')
        writer = csv.writer(new_file)
        writer.writerow(header)
        new_file.close()
        return filename

    def scrape_urls(self):
        with open('urls.txt', 'r') as f:
            urls = f.readlines()
            # print('-----', len(urls))
            sum = 0
            with open('scraped_urls.txt', 'a+') as f:
                clicked = False
                for i, url in enumerate(urls):
                    print('--', i, url)
                    self.browser.get(url)
                    # self.browser.find_element_by_id('acceptAllButton').click()
                    if not clicked:
                        self.browser.find_element_by_class_name('coi-banner__accept').click()
                        clicked = True

                    # print('---', self.browser.find_element_by_class_name('coi-banner__accept').text)
                    time.sleep(5)
                    # self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    # self.browser.execute_script("arguments[0].scrollIntoView();", one_row_wrap[i])
                    div = self.browser.find_element_by_class_name('o-tile-grid')
                    # self.browser.execute_script("arguments[0].scrollIntoView();", div)
                    time.sleep(5)
                    articles = div.find_elements_by_tag_name('article')
                    print('-----', len(articles))
                    for i in range(len(articles)):
                        self.browser.save_screenshot('qqq.png')
                        # time.sleep(1)
                        a = articles[i].find_element_by_tag_name('a').get_attribute('href')
                        self.browser.execute_script("arguments[0].scrollIntoView();", articles[i].find_element_by_tag_name('a'))
                        f.writelines(a+'\n')
                        print('----', a)
                    
                    sum+=len(articles)
                    self.browser.save_screenshot('coop.png')
                print('---sum', sum)
        # with open('urls0-300.txt', 'r') as file:
        #     lines = file.readlines()
        #     new_links = set()
        #     print('--links without set', len(lines))
        #     for l in lines:
        #         new_links.add(l)
        #     print(len(new_links))
        #     with open('scraped_urls0-300.txt', 'a+') as f:
        #         for i, link in enumerate(new_links):
        #             print(i, link)
        #             self.browser.get(link)
        #             time.sleep(1)
        #             try:
        #                 self.browser.find_element_by_class_name('coi-banner__accept').click()
        #             except:
        #                 pass
        #             self.browser.save_screenshot('last.png')
        #             time.sleep(3)
        #             l = self.browser.find_elements_by_tag_name('productlist-item')
        #             spots = self.browser.find_elements_by_class_name('productlistshowallspot')
        #             one_row_wrap = self.browser.find_elements_by_class_name('productlist-onerow__item-wrap')
        #             new_file = open('scraped_urls.txt', 'w')
        #             new_file.close()
        #             for i in range(len(one_row_wrap)):
        #                 time.sleep(2)
        #                 self.browser.save_screenshot('aaaa.png')
        #                 self.browser.execute_script("arguments[0].scrollIntoView();", one_row_wrap[i])
        #                 time.sleep(4)
        #                 for i in one_row_wrap[i].find_elements_by_tag_name('productlist-item'):
        #                     try:
        #                         a_tag = i.find_element_by_tag_name('a').get_attribute('href')
        #                         print(a_tag)
        #                         f.writelines(a_tag+'\n')
        #                     except:
        #                         pass
        #             for i in range(len(spots)):
        #                 self.browser.execute_script("arguments[0].scrollIntoView();", spots[i])
        #                 time.sleep(4)
        #                 for i in spots[i].find_elements_by_tag_name('productlist-item'):
        #                     try:
        #                         a_tag = i.find_element_by_tag_name('a').get_attribute('href')
        #                         print(a_tag)
        #                         f.writelines(a_tag+'\n')
        #                     except:
        #                         pass

CoopScraper()




