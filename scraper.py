from bs4 import BeautifulSoup
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd
import argparse
import sys
import random

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--search', type=str, help='search query')
parser.add_argument('--max', type=int, help='max products to scrape')
parser.add_argument('--retailer', type=str, default="amazon", help='retailer to scrape')
args = parser.parse_args()
search_query = args.search
max_products = args.max
retailer = args.retailer

MIN_WAIT_TIME = 3
MAX_WAIT_TIME = 12

def scrape_plaisio_data(base_url):
    products = []  # List to hold all products


    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    page = 1
    while True:

        url = f"{base_url}&page={page}&resultsPerPage=12"
        print("Scraping:", url)


        driver.get(url)


        time.sleep(10)  # Wait time in seconds, adjust as needed based on page load times


        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')


        product_items = soup.find_all('div', class_="product")
        if not product_items:
            break  # Break the loop if no products are found


        for item in product_items:
            title = item.find('div', itemprop='name')
            if title:
                title = title.get_text(strip=True)
            link = item.find('a')['href']
            price = item.find('div', class_='price')
            if price:
                price = price.get_text(strip=True)


            if title or link or price:
                products.append((title, price, link))


        page += 1


    driver.quit()

    return products

def scrape_amazon(search_query, max_products):

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    products = []  # List to hold product data
    page = 1
    collected_products = 0

    while collected_products < max_products:

        url = f"https://www.amazon.com/s?k={search_query.replace(' ', '+')}&page={page}"
        print("URL:", url)

        try:

            driver.get(url)


            time.sleep(random.uniform(5, 15))  # Randomize delay


            html_content = driver.page_source


            soup = BeautifulSoup(html_content, 'html.parser')


            listings = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            if not listings:  # Break if no listings found
                print("No more products found.")
                break


            for item in listings:
                if collected_products >= max_products:
                    break

                title_element = item.find('span', class_='a-size-medium a-color-base a-text-normal')
                title = title_element.get_text(strip=True) if title_element else "Title not found"

                link_element = item.find('a', class_='a-link-normal')
                link = f"https://www.amazon.com{link_element['href']}" if link_element else None


                price_element = item.find('span', text=lambda x: x and '$' in x)
                price = price_element.get_text(strip=True) if price_element else None

                if title or link or price:
                    print(title, price, link)
                    products.append([title, price, link])
                    collected_products += 1

                    if collected_products % 100 == 0:
                        print(f"Collected {collected_products} products")

            page += 1  # Move to the next page

        except Exception as e:
            print(f"Error encountered: {e}")
            time.sleep(random.uniform(30, 60))  # Wait before retrying


    driver.quit()


    df = pd.DataFrame(products, columns=['Title', 'Price', 'Link'])

    print("Collected Products: ", df.shape[0])
    return df

def scrape_ebay(search_query, max_products):

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    products = []  # List to hold product data
    page = 1
    collected_products = 0

    while collected_products < max_products:

        url = f"https://www.ebay.com/sch/i.html?_nkw={search_query.replace(' ', '+')}&_pgn={page}"
        print("URL:", url)


        driver.get(url)


        time.sleep(10)  # Adjust this delay as needed based on your network speed


        html_content = driver.page_source


        soup = BeautifulSoup(html_content, 'html.parser')


        listings = soup.find_all('div', class_="s-item__wrapper clearfix")
        
        if not listings:  # Break if no listings found
            print("No more products found.")
            break


        for item in listings:
            if collected_products >= max_products:
                break

            title_div = item.find('div', class_='s-item__title')
            if title_div:
                title_span = title_div.find('span', role='heading')
                if title_span:
                    title = title_span.get_text(strip=True)
                else:
                    title = title_div.get_text(strip=True)  # Fallback if no span is found
            else:
                title = None

            link = item.find('a', class_='s-item__link')['href']

            price = item.find('span', class_='s-item__price')
            if price:
                price = price.text.strip()

            if title and link and price:
                products.append([title, price, link])
                collected_products += 1

        page += 1  # Move to the next page


    driver.quit()


    df = pd.DataFrame(products, columns=['Title', 'Price', 'Link'])

    return df

def scrape_costco(search_query, max_products):

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    products = []  # List to hold product data
    page = 1
    collected_products = 0

    while collected_products < max_products:

        url = f"https://www.costco.com/CatalogSearch?dept=All&keyword={search_query.replace(' ', '+')}"
        print("URL:", url)


        driver.get(url)


        time.sleep(10)  # Adjust this delay as needed based on your network speed


        html_content = driver.page_source


        soup = BeautifulSoup(html_content, 'html.parser')
        
        print(soup.prettify())

        listings = soup.find_all('div', class_='product')
        
        if not listings:  # Break if no listings found
            print("No more products found.")
            break


        for item in listings:
            print(item)
            if collected_products >= max_products:
                break

            title_div = item.find('p', class_='description')
            if title_div:
                title = title_div.get_text(strip=True)

            link_element = item.find('a')
            link = f"https://www.costco.com{link_element['href']}" if link_element else None

            price_div = item.find('div', class_='price')
            if price_div:
                price = price_div.get_text(strip=True)

            if title or link or price:
                products.append([title, price, link])
                collected_products += 1

        page += 1  # Move to the next page


    driver.quit()


    df = pd.DataFrame(products, columns=['Title', 'Price', 'Link'])

    return df

def scrape_bestbuy(search_query, max_products):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get("https://www.bestbuy.com")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.us-link"))).click()  # Adjust the selector based on the needed country


    products = []  # List to hold product data
    page = 1
    collected_products = 0

    while collected_products < max_products:

        url = f"https://www.bestbuy.com/site/searchpage.jsp?st={search_query.replace(' ', '+')}&cp={page}"
        print("URL:", url)


        driver.get(url)


        time.sleep(MIN_WAIT_TIME)  # Adjust this delay as needed based on your network speed


        html_content = driver.page_source


        soup = BeautifulSoup(html_content, 'html.parser')




        listings = soup.find_all('li', class_='sku-item')
        
        if not listings:  # Break if no listings found
            print("No more products found.")
            break


        for item in listings:

            if collected_products >= max_products:
                break


            title_element = item.find('h4', class_='sku-title')
            if title_element:
                link = title_element.find('a')['href']
                title = title_element.get_text(strip=True)
                link = f"https://www.bestbuy.com{link}"
            else:
                title = None
                link = None
            
            if title is None:
                title_element = item.find('h4', class_='sku-header')
                if title_element:
                    link = title_element.find('a')['href']
                    title = title_element.get_text(strip=True)
                    link = f"https://www.bestbuy.com{link}"
                if title is None:

                    print(item.prettify())

                    print("TITLE", title)
                    print("LINK", link)
                    sys.exit(-1)

                print("TITLE", title)
                print("LINK", link)



            price_div = item.find('div', class_='priceView-hero-price priceView-customer-price')
            if price_div:
                price = price_div.find('span').get_text(strip=True)
            else:
                price = None

            if title or link or price:
                products.append([title, price, link])
                collected_products += 1

                if collected_products % 100 == 0:
                    print(f"Collected {collected_products} products")

        page += 1  # Move to the next page


    driver.quit()


    df = pd.DataFrame(products, columns=['Title', 'Price', 'Link'])

    return df

def scrape_and_crawl_bestbuy(search_query, max_products):
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get("https://www.bestbuy.com")
    WebDriverWait(driver, MIN_WAIT_TIME*2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.us-link"))).click()  # Adjust the selector based on the needed country

    products = [] 
    page = 1
    collected_products = 0

    while collected_products < max_products:
        url = f"https://www.bestbuy.com/site/searchpage.jsp?st={search_query.replace(' ', '+')}&cp={page}"

        driver.get(url)

        time.sleep(MIN_WAIT_TIME)

        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        listings = soup.find_all('li', class_='sku-item')

        if not listings:
            print("No more products found.")
            break

        for item in listings:
            if collected_products >= max_products:
                break
            
            title_element = item.find('h4', class_='sku-title')
            if title_element:
                link = title_element.find('a')['href']
                title = title_element.get_text(strip=True)
                link = f"https://www.bestbuy.com{link}"
            else:
                title = None
                link = None
            
            price_div = item.find('div', class_='priceView-hero-price priceView-customer-price')
            if price_div:
                price = price_div.find('span').get_text(strip=True)
            else:
                price = None

                with open('no_price.html', 'w') as f:
                    f.write(item.prettify())

            if link:
                driver.get(link)
                time.sleep(MIN_WAIT_TIME) 
                product_html = driver.page_source
                product_soup = BeautifulSoup(product_html, 'html.parser')

                description_element = product_soup.find('div', {'data-testid': 'product-description'})
                if description_element:
                    description = description_element.get_text(strip=True)
                else:
                    description = ""

                additional_info_element = product_soup.find('div', class_='additional-info')
                if additional_info_element:
                    additional_info = additional_info_element.get_text(strip=True)
                else:
                    additional_info = ""

                full_description = f"{description} {additional_info}".strip()

                price_div_detail = product_soup.find('div', class_='priceView-hero-price priceView-customer-price')
                if price_div_detail:
                    price_span_detail = price_div_detail.find('span', aria_hidden='true')
                    if price_span_detail:
                        price = price_span_detail.get_text(strip=True)
                    else:
                        price = price_div_detail.find('span', class_='sr-only').get_text(strip=True).replace('Your price for this item is $', '')

                products.append([title, price, link, full_description])
                collected_products += 1

        print("Page: ", page, " | Collected Products: ", len(products))
        page += 1 

    driver.quit()

    df = pd.DataFrame(products, columns=['Title', 'Price', 'Link', 'Description'])

    return df

def scrape_and_crawl_amazon(search_query, max_products):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    products = []
    page = 1
    collected_products = 0
    one_more_try = False
    while collected_products < max_products:
        url = f"https://www.amazon.com/s?k={search_query.replace(' ', '+')}&page={page}"

        try:
            driver.get(url)
            time.sleep(random.uniform(10, 15))

            html_content = driver.page_source

            soup = BeautifulSoup(html_content, 'html.parser')

            listings = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            if not listings:  # Break if no listings found
                print("No more products found.")
                if one_more_try==False:
                    one_more_try = True
                    time.sleep(random.uniform(10, 15))  # Randomize delay
                else:
                    break


            for item in listings:
                if collected_products >= max_products:
                    break

                title_element = item.find('span', class_='a-size-medium a-color-base a-text-normal')
                title = title_element.get_text(strip=True) if title_element else "Title not found"

                link_element = item.find('a', class_='a-link-normal')
                link = f"https://www.amazon.com{link_element['href']}" if link_element else None


                price_element = item.find('span', text=lambda x: x and '$' in x)
                price = price_element.get_text(strip=True) if price_element else None


                description = extract_description(link, driver) if link else None

                if title or link or price or description:
                    # print(title, price, link, description)
                    products.append([title, price, link, description])
                    collected_products += 1

                    if collected_products % 100 == 0:
                        print(f"Collected {collected_products} products")

            print("Page: ", page, " | Collected Products: ", len(products))
            page += 1  # Move to the next page

        except Exception as e:
            print(f"Error encountered: {e}")
            time.sleep(random.uniform(30, 60))  # Wait before retrying


    driver.quit()


    df = pd.DataFrame(products, columns=['Title', 'Price', 'Link', 'Description'])

    print("Collected Products: ", df.shape[0])
    return df

def extract_description(product_url, driver):
    try:

        driver.get(product_url)


        time.sleep(random.uniform(2, 8))


        html_content = driver.page_source


        soup = BeautifulSoup(html_content, 'html.parser')


        about_section = soup.find('div', {'id': 'feature-bullets'})
        description = about_section.get_text(strip=True) if about_section else None

        return description

    except Exception as e:
        print(f"Error extracting description: {e}")
        return None

def get_product_data(search_query, max_products, eshop):
    
    dfname = search_query.replace(' ', '_') + '.csv'


    if not os.path.exists(eshop):
        os.makedirs(eshop)
    
    dfname = os.path.join(eshop, dfname)

    if os.path.exists(dfname):
        product_df = pd.read_csv(dfname)
    else:
        if eshop == 'amazon':
            product_df = scrape_and_crawl_amazon(search_query, max_products)
        elif eshop == 'ebay':
            product_df = scrape_ebay(search_query, max_products)
        elif eshop == 'costco':
            product_df = scrape_costco(search_query, max_products)
        elif eshop == 'bestbuy':
            product_df = scrape_and_crawl_bestbuy(search_query, max_products)
        else:
            print("Invalid e-shop")
            return None

        print(product_df.shape)

        if product_df.shape[0] == 0:
            print("No products found")
            return None
        print(product_df.head(30))
        product_df.fillna('', inplace=True)
        product_df['id'] = product_df.index
        product_df.to_csv(dfname, index=False)
    
    return product_df

if __name__ == "__main__":

    print("=============================================")
    print("RETAILER:", retailer)
    print("SEARCH QUERY:", search_query)
    print("MAX PRODUCTS:", max_products)
    print("=============================================")

    product_df = get_product_data(search_query, max_products, retailer)

    print("\n\nNumber of products:", product_df.shape[0])
    print("None values per attribute")
    print(product_df.isnull().sum())
