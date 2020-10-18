import requests
import os
from bs4 import BeautifulSoup

# headers help in bypassing the detection as a scraper
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

# To keep track of the products whose reviews have already been extracted
dire = 'reviews/'
fileNames = os.listdir(str(dire))

def get_page_soup(url):
    """
    Pass any URL as the argument and this function returns the BeautifulSoup format using the pre-mentioned headers
    """
    r = requests.get(url, headers=headers) 
    content = r.content  # extracts all the page information
    soup = BeautifulSoup(content, 'lxml') # BeautifulSoup is used to parse through the html tags of a page
    return soup

def get_phone_name(url):
    """
    Finds the product name from it's Amazon page. 
    """
    try:
        print(url)
        soup = get_page_soup(url)
        d = soup.find('div', attrs={'id':"prodDetails"}) # Finds the name in the product description
        phone_name = d.find('h2').text[:-25]
        return phone_name
    except: # More reliable way to find the product name
        soup = get_page_soup(url)
        # Outer Tag Object
        phone_name = soup.find("span", attrs={"id":'productTitle'}) 
        # Inner NavigableString Object as a string value
        phone_name = phone_name.string.strip()
        return phone_name

def get_reviews(url):
    """
    Given a product URL returns a list of reviews from 10 review pages (total 100 reviews)
    """
    product_soup = get_page_soup(url)
    reviews = []
    # Find the 'see all reviews' button and extract all the reviews
    for i in product_soup.findAll("a",attrs={'data-hook':"see-all-reviews-link-foot"}):
        reviews_link = "https://www.amazon.in"+i.get('href')
        for k in range(10):
            # Find the soup for each review page
            soup = get_page_soup(reviews_link +'&pageNumber='+str(k+1))
            # Find and append the reviews from review body
            for i in soup.findAll("span",attrs={'data-hook':"review-body"}):
                reviews.append(i.text[4:-2]) 

    return reviews

def save(product):
    """
    Given the product name and it's reviews list, this function opens a .txt file with the product name and saves the product's reviews
    """
    # extract the phone name and reviews list
    phone_name = product[0]
    reviews = product[1]
    # Open a new file in reviews/ folder with the phone's name and save it's reviews
    with open('reviews/'+phone_name+'.txt', 'w') as f:
            for review in reviews:
                f.write('%s\n' % review)
    print('Done\n')