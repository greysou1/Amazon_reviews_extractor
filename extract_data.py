from helper import *

def get_search_data(search_query, total):
    products = [] 
    phone_names = [] 
    # Search upto 30 pages of search results and extract each search result's data.
    for i in range(30):
        # this URL is used to scrape. the page argument 'page' can be used to parse through different page numbers to get more data. 
        url='https://www.amazon.in/s?k='+search_query+'&page='+str(i+1) 
        print(url)
        soup = get_page_soup(url)
        # Find all search results
        for d in soup.findAll('div', attrs={'data-component-type':'s-search-result'}):
            if len(products) < total: # to check if we have enough search results 
                try:
                    product = []
                    # Extract the URL of the product using its tag name and attributes
                    phone_url = d.find('a', attrs={'class':'a-link-normal a-text-normal'}).get('href')   
                    phone_url = "https://www.amazon.in"+phone_url
                    # Extract the phone name by scraping throught the product's page 
                    phone_name = get_phone_name(phone_url)
                    # If the phone isn't already scraped and the get_phone_name function doesn't return None 
                    # and if it's reviews aren't already present in the reviews folder
                    if (phone_name not in phone_names) and (phone_name != None) and (phone_name+'.txt' not in fileNames):
                        phone_names.append(phone_name)
                        # Extract the reviews of the product
                        reviews = get_reviews(phone_url)
                        product.append(phone_name)
                        product.append(reviews)
                        # Add the product to the total products
                        products.append(product)
                        # Saving the reviews
                        print('Added ' + phone_name + ' to list.')
                        print('Saving...')
                        save(product)
                    else:
                        print("skipping " + phone_name)
                        continue
                except:
                    continue
            else:
                return products

# Search for any product (seperate words using '+'. Ex: 'mobile+phone+cases')
search_query = 'phones'
# Total number of product reviews we require
total = 100
# Start searching for 'total' number of reviews using the 'search_query'
urls = get_search_data(search_query, total)
print(len(urls))