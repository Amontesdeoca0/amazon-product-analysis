import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import time
import random
from tqdm import tqdm
import logging
import re
import os
import html
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

os.makedirs('../../data/raw', exist_ok = True)
os.makedirs('../../logs', exist_ok = True)

file_path = '../../data/raw/AmazonData.xlsx'

log_path = '../../logs/scraper_log.txt'

# logs configuration
logging.basicConfig(
    filename = log_path,
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

# urls list
urls = [
    'https://www.amazon.com/dp/B09BSGKCSL/ref=sspa_dk_detail_0?sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWwy&customId=B0752XJYNL&customizationToken=MC_Assembly_1%23B0752XJYNL&psc=1',
    'https://www.amazon.com/dp/Camiseta-texto-ingl%C3%A9s-Morning-Analyst/dp/B0CR96KMVP/ref=pd_sbs_d_sccl_2_1/136-0523038-3930252?psc=1',
    'https://www.amazon.com/dp/Lam%C3%A9rselo-Peri%C3%B3dica-Graciosa-Profesor-Estudiante/dp/B0F88TNWKW/ref=pd_sbs_d_sccl_2_2/136-0523038-3930252?psc=1',
    'https://www.amazon.com/dp/Avoid-Top-Bell-Curve-estad%C3%ADsticas/dp/B09BT31TM4/ref=pd_sbs_d_sccl_2_3/136-0523038-3930252?psc=1',
    'https://www.amazon.com/dp/Ciencia-datos-An%C3%A1lisis-Camiseta-cient%C3%ADficos/dp/B09RBGMLVB/ref=pd_sbs_d_sccl_2_4/136-0523038-3930252?psc=1',
    'https://www.amazon.com/dp/datos-persona-camiseta-opini%C3%B3n-Negro/dp/B0CR96B1JD/ref=pd_sbs_d_sccl_2_5/136-0523038-3930252?psc=1',
    'https://www.amazon.com/dp/Ingeniero-software-ingeniero-computadora-nerd/dp/B07TTQ4VX1/ref=pd_sbs_d_sccl_2_6/136-0523038-3930252?psc=1'
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
]

session = requests.Session()

def safe_get(url, retries = 5):
    for attempt in range(retries):
        try:
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "DNT": "1",
                "Referer": "https://www.amazon.com/",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
            }

            response = session.get(url, headers = headers, timeout = 20)
            
            if response.status_code == 200:
                if "captcha" in response.text.lower():
                    logging.warning(f"Captcha detected (attempt {attempt+1})")
                    time.sleep(random.uniform(5, 10))
                    continue
                
                logging.info(f"Successful: {url}")
                return response
            else:
                logging.warning(f"Status code {response.status_code} for {url}")
            
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {e} - {url}")
            
        time.sleep(random.uniform(5, 10))
        
    return None

def scrap_reviews(soup):
    reviews = []

    review_list = soup.find('ul', id="cm-cr-dp-review-list")

    if not review_list:
        if soup.find(id="acrCustomerReviewText"):
            logging.info("No reviews but section exists")
            return []
        else:
            logging.warning("Reviews not loaded properly")
            return None

    for li in review_list.find_all('li', {'data-hook': 'review'}):
        try:
            # review star rating
            stars = None
            stars_tag = li.find('i', {'data-hook': 'review-star-rating'}) or li.find('i', {'data-hook': 'cmps-review-star-rating'})

            if stars_tag:
                span = stars_tag.find('span', class_="a-icon-alt")
                if span:
                    stars_text = span.get_text(strip=True)
                    match = re.search(r'(\d+[.,]?\d*)', stars_text)
                    if match:
                        stars = float(match.group(1).replace(',', '.'))

            # review title
            review_title = "N/A"
            title_tag = li.find('a', {'data-hook': 'review-title'})

            if title_tag:
                spans = title_tag.find_all('span')

                found = False

                for span in spans:
                    text = span.get_text(strip=True)

                    if text and "out of" not in text.lower():
                        review_title = text
                        found = True
                        break
                    
                if not found:
                    review_title = "N/A"
                
            # verified purchase
            verified = li.find('span', {'data-hook': 'avp-badge'})
            verified_text = verified.get_text(strip = True) if verified else "No"

            # review date
            date_tag = li.find('span', {'data-hook': 'review-date'})
            review_date_raw = date_tag.get_text(strip = True) if date_tag else "N/A"

            # clean date
            review_date = "N/A"
            if review_date_raw != "N/A":
                match = re.search(r'(\d{1,2})\s+de\s+([a-zA-Z]+)\s+de\s+(\d{4})', review_date_raw)
                if match:
                    day, month_str, year = match.groups()
                    meses = {
                        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
                        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
                        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
                    }
                    month = meses.get(month_str.lower(), '01')
                    review_date = f"{year}-{month}-{day.zfill(2)}"
                else:
                    # if its in engligh or other format
                    match_en = re.search(r'([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})', review_date_raw)
                    if match_en:
                        month_str, day, year = match_en.groups()
                        meses_en = {
                            'January': '01', 'February': '02', 'March': '03', 'April': '04',
                            'May': '05', 'June': '06', 'July': '07', 'August': '08',
                            'September': '09', 'October': '10', 'November': '11', 'December': '12'
                        }
                        month = meses_en.get(month_str, "01")
                        review_date = f"{year}-{month}-{day.zfill(2)}"
            else:
                review_date = review_date_raw
            
            # review body
            body_tag = li.find('span', {'data-hook': 'review-body'})
            body = None
            if body_tag:
                span = body_tag.find('span')
                if span:
                    text = span.get_text(strip=True)
                else:
                    text = body_tag.get_text(strip=True) 
                
                if text:
                    body = text
                else:
                    body = None
                
                # limitar si opinión es muy larga
                if body and len(body) > 200:
                    body = body[:200] + "..."

            reviews.append([
                stars,
                review_title,
                verified_text,
                review_date,
                body
            ])
        
        except Exception as e:
            logging.error(f"Error in reviews: {e}")
            continue

    return reviews

def scrape_product(url):
    # ASIN
    try:
        match = re.search(r'/dp/([A-Z0-9]{10})', url)
        if match:
            asin = match.group(1)
        else:
            logging.error(f"ASIN not found: {url}")
            return None, [], []
    except IndexError:
        logging.error(f"Invalid URL format: {url}")
        return None, [], []

    clean_url = f"https://www.amazon.com/dp/{asin}"
    
    response = safe_get(clean_url)
    
    if not response:
        return None, [], []

    soup = BeautifulSoup(response.content, "html.parser")

    # validate page content
    if soup.find(id="title") is None:
        logging.warning("Invalid product page")
        return None, [], []

    # title
    title_tag = soup.find(id = 'title')
    title = title_tag.get_text(strip = True) if title_tag else "N/A"

    # price
    price = None

    price_candidates = []

    # first method
    price_tag = soup.find(id="apex-pricetopay-accessibility-label")
    if price_tag:
        price_candidates.append(price_tag.get_text(strip=True))
    
    # second method
    price_container = soup.find('span', class_='a-price')
    if price_container:
        whole = price_container.find('span', class_='a-price-whole')
        fraction = price_container.find('span', class_='a-price-fraction')
        if whole and fraction:
            price_candidates.append(f"{whole.get_text(strip=True)}.{fraction.get_text(strip=True)}")
    
    # third method
    price_tag = soup.find('span', class_='a-offscreen')
    if price_tag:
        price_candidates.append(price_tag.get_text(strip=True))
    
    currency = None
    
    # clean and convert price
    for price_text in price_candidates:
        try:
            # get currency symbol
            if 'MX$' in price_text or 'MXN' in price_text:
                currency = 'MXN'
            elif '$' in price_text:
                currency = 'USD'
            
            clean = re.sub(r'[^\d.,]', '', price_text)

            if ',' in clean and '.' in clean:
                clean = clean.replace(',', '')
            elif ',' in clean:
                clean = clean.replace(',', '.')

            price = float(clean)
            break
        except:
            continue
    
    # convert to dolars assuming 1 USD = 18 MXN and round to 2 decimals
    exchange_rate = 18
    if price is not None:
        if currency == 'MXN':
            price = price / exchange_rate
        price = round(price, 2)
    else:
        logging.warning(f"Price not found or parsed: {url}")
        price = None
       
    # rating
    rating = None
    rating_tag = soup.find('i', {'data-hook': 'rating-out-of-text'})
    
    if not rating_tag:
        rating_tag = soup.select_one('#acrPopover span.a-icon-alt')

    if rating_tag:
        rating_text = rating_tag.get_text(strip=True)

        match = re.search(r'(\d+[.,]?\d*)', rating_text)
        if match:
            rating = float(match.group(1).replace(',', '.'))
        
    # review count
    review_count = None
    review_tag = soup.find(id="acrCustomerReviewText")
    if not review_tag:
        review_tag = soup.find('span', {'data-hook': 'total-review-count'})

    if review_tag:
        review_text = review_tag.get_text(strip = True)
        # get number
        match = re.search(r'[\d,]+', review_text)
        if match:
            review_count = int(match.group(0).replace(',', ''))

    today = datetime.date.today().strftime('%Y-%m-%d')

    # product data
    product_data = {
        'ASIN': asin,
        'Title': title,
        'Price': price,
        'Rating': rating,
        'Review Count': review_count,
        'Date': today,
        'URL': clean_url
    }

    # reviews data
    reviews_raw = scrap_reviews(soup)
    reviews_data = []

    # if wrong page
    if reviews_raw is None:
        reviews_raw = []
    
    for review in reviews_raw:
        stars, review_title, verified_text, review_date, review_body = review
        
        reviews_data.append({
            'ASIN': asin,
            'Stars': stars,
            'Review_Title': review_title,
            'Verified_Purchase': verified_text,
            'Review_Date': review_date,
            'Review_Body': review_body,
            'Extraction_Date': today
        })
    
    related_products = get_related_products(soup)
    logging.info(f"{asin} -> {len(related_products)} related products")

    return product_data, reviews_data, related_products

def get_related_products(soup):
    urls = set()

    carousels = soup.find_all('div', attrs = {'data-a-carousel-options': True})

    for carousel in carousels:
        data = carousel.get('data-a-carousel-options')
        
        try:
            # decode HTML entities
            data = html.unescape(data)

            # convert to dict
            data_json = json.loads(data)

            id_list = data_json.get('ajax', {}).get('id_list', [])

            for item in id_list:
                try:
                    item_json = json.loads(item)
                    asin = item_json.get('id')

                    if asin and len(asin) == 10:
                        urls.add(f"https://amazon.com/dp/{asin}")
                
                except:
                    continue
        except Exception as e:
            logging.warning(f"Error parsing carousel JSON: {e}")
            continue

    
    urls = list(urls)
    logging.info(f"Related products found: {len(urls)}")
    
    return urls


def save_to_excel(products, reviews):
    if not products and not reviews:
        print("No data to save")
        logging.warning("No data to save")
        return
    
    try:
        existing_products = pd.read_excel(file_path, sheet_name = 'Products')
        existing_reviews = pd.read_excel(file_path, sheet_name = 'Reviews')
    except Exception as e:
        logging.warning(f"Excel file not found or error reading it: {e}")
        existing_products = pd.DataFrame()
        existing_reviews = pd.DataFrame()
    
    # convert to DataFrames
    new_products = pd.DataFrame(products) if products else pd.DataFrame()
    new_reviews = pd.DataFrame(reviews) if reviews else pd.DataFrame()

    # delete old register with same asin
    if not new_products.empty and 'ASIN' in existing_products.columns:
        existing_products = existing_products[~existing_products['ASIN'].isin(new_products['ASIN'])]

    if not new_reviews.empty and 'ASIN' in existing_reviews.columns:
        existing_reviews = existing_reviews[~existing_reviews['ASIN'].isin(new_reviews['ASIN'])]

    # concat
    all_products = pd.concat([existing_products, new_products], ignore_index=True)
    
    all_reviews = pd.concat([existing_reviews, new_reviews], ignore_index=True) 

    # delete duplicates
    if not all_products.empty:
        all_products.drop_duplicates(subset = 'ASIN', keep = 'last', inplace = True)
    
    if not all_reviews.empty:
        all_reviews.drop_duplicates(subset = ['ASIN', 'Review_Body'], keep = 'last', inplace = True)

    # save to excel
    with pd.ExcelWriter(file_path, engine = 'openpyxl') as writer:
        all_products.to_excel(writer, sheet_name = 'Products', index = False)
        all_reviews.to_excel(writer, sheet_name = 'Reviews', index = False)

def process_url(url):
    try:
        time.sleep(random.uniform(2, 4))

        product, reviews, related = scrape_product(url)
    
        if product:
            return product, reviews or [], related or []
    except Exception as e:
        logging.error(f"Error processing URL {url}: {e}")
         
    return None, [], []

def process_review(review, seen_reviews, all_reviews):
    body = review['Review_Body']
    title = review['Review_Title']
    
    if body and body.strip() and title and title != "N/A":
        clean_body = body.strip()
        key = (review['ASIN'], clean_body)
    
        if key not in seen_reviews:
            seen_reviews.add(key)
            review['Review_Body'] = clean_body
            all_reviews.append(review)

def main():
    all_products = []
    all_reviews = []
    all_related_urls = []

    seen_asins = set()
    seen_reviews = set()

    max_threads = 2

    # first scraping
    with ThreadPoolExecutor(max_workers = max_threads) as executor:
        futures = [executor.submit(process_url, url) for url in urls]

        for future in tqdm(as_completed(futures), total = len(urls), desc = "Scrapping products"):
            product, reviews, related = future.result()

            if product and product['ASIN'] not in seen_asins:
                seen_asins.add(product['ASIN'])
                all_products.append(product)

            for review in reviews:
                process_review(review, seen_reviews, all_reviews)

            
            all_related_urls.extend(related)
    
    # clean related
    all_related_urls = list(set(all_related_urls))

    # avoid repeat original URLS
    all_related_urls = [
        url for url in all_related_urls if url not in urls
    ]

    print(f"Related products to scrape: {len(all_related_urls)}")

    # second scraping
    print("Scraping related products...")

    with ThreadPoolExecutor(max_workers = max_threads) as executor:
        futures = [executor.submit(process_url, url) for url in all_related_urls]

        for future in tqdm(as_completed(futures), total = len(all_related_urls), desc ="Scraping related products"):
            product, reviews, _ = future.result()

            if product and product['ASIN'] not in seen_asins:
                seen_asins.add(product['ASIN'])
                all_products.append(product)
            
            for review in reviews:
                process_review(review, seen_reviews, all_reviews)

    # save scraped info
    save_to_excel(all_products, all_reviews)

    logging.info("Scraping finished")
    print("Scraping finished")

# run
if __name__ == "__main__":
    main()
