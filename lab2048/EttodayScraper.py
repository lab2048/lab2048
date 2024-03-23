from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import datetime
import pickle

class EttodayScraper:
    def __init__(self, keyword, driver_path):

        service = Service(driver_path)
        if "chromedriver" in driver_path:
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')            
            self.driver = webdriver.Chrome(service=service, options=options)
        else:
            options = webdriver.FirefoxOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')            
            self.driver = webdriver.Firefox(service=service, options=options)
        self.keyword = keyword
        self.allpages = []
        self.error_page_id = []
        self.dates = []
        self.titles = []
        self.paragraphs = []
        self.tags = []
        self.current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        
    def scrape_pages(self, start_page=1, end_page=139):
        for pagenum in range(start_page, end_page):
            url = f"https://finance.ettoday.net/search.php7?keyword={self.keyword}&page={pagenum}"
            self.driver.get(url)
            subpages = self.driver.find_elements(By.CLASS_NAME, 'piece')
            for page in subpages:
                href = page.get_attribute('href')
                if href is not None:
                    self.allpages.append(href)
        print("Scraped Links: ", len(scraper.allpages))

    def close_driver(self):
        self.driver.quit()

    def save_pages_to_file(self, file_path=None):
        if file_path is None:
            file_path = f"ettoday-pages-{self.keyword}.txt"
        with open(file_path, 'w+') as f:
            for href in self.allpages:
                f.write(f'{href}\n')
        print(f"Saved pages of links to {file_path}")

    def print_summary(self):
        # 印出抓取結果摘要
        print(self.allpages)
        print(f'total page: {len(self.allpages)}')

    def load_pages_from_file(self, file_path):
        with open(file_path, 'r') as f:
            self.allpages = f.readlines()
        self.allpages = [x.strip() for x in self.allpages]


    def scrape_news(self, pages):
        for pagenum, url in enumerate(pages):
            print(f'pagenum: {pagenum+1}')
            try:
                self.driver.get(url)
                date = self.driver.find_element(By.TAG_NAME, 'time').text
                title = self._get_title()

                # get context paragraph
                paragraph = self._get_paragraph()

                # get tag words
                tag_word_list = self._get_tags()

                self.dates.append(date)
                self.titles.append(title)
                self.paragraphs.append(paragraph)
                self.tags.append(tag_word_list)
            
            except Exception as e:
                self.error_page_id.append(pagenum)
                print(f'error happened at pagenum {pagenum}: {e}')
            # if pagenum+1 == 13:
            #     break

        self.driver.quit()

    def _get_title(self):
        header1s = self.driver.find_elements(By.TAG_NAME, 'h1')
        for header in header1s:
            if header.get_attribute("class") == "title":
                return header.text
        return ""

    def _get_paragraph(self):
        contents = self.driver.find_elements(By.TAG_NAME, 'p')
        paragraph = ""
        for content in contents:
            text = content.text

            if "▲" in text:
                continue
            elif "關鍵字" in text:
                break
            else:
                paragraph += text + '\n'
        return paragraph

    def _get_tags(self):
        try:
            tag_words = self.driver.find_elements(By.CLASS_NAME, 'tag')
            tag_word_list = [word.text for tag_word in tag_words for word in tag_word.find_elements(By.TAG_NAME, 'a')]
            return ', '.join(tag_word_list)
        except:
            return ""

    def save_pickle(self, filename=None):
        info_dict = {'dates': self.dates,
                     'titles': self.titles,
                     'context': self.paragraphs,
                     'tags': self.tags}

        df = pd.DataFrame.from_dict(info_dict)
        
        if filename is None:
            filename = f"ettoday-{self.keyword}-{self.current_date}.pkl"
        df.to_pickle(filename)
        return df


# 使用範例


if __name__ == "__main__":
    
    
    # pip install git+https://github.com/lab2048/lab2048.git
    
    from lab2048.EttodayScraper import EttodayScraper
    keyword = "chatgpt"
    driver_path = '/Users/jirlong/Downloads/geckodriver'
    scraper = EttodayScraper(keyword, driver_path)
    
    scraper.scrape_pages(1, 2) 
    scraper.save_pages_to_file()
    
    # scraper.load_pages_from_file("ettoday-pages-chatgpt.txt")
    
    scraper.scrape_news(scraper.allpages)  # assuming 'pages' is a list of URLs
    df = scraper.save_pickle()
    df
    scraper.close_driver()
    