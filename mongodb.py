from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

# Create a MongoDB client
client = MongoClient('')  # Replace with your MongoDB server URI

# Access a database (if it doesn't exist, MongoDB will create it)
db = client[' ']  # Use 'Database' as the database name

# Access a collection named 'Collection' (if it doesn't exist, MongoDB will create it)
collection = db[' ']  # Give a collection name

# Function to scrape data from a webpage based on a keyword
def scrape_data_by_keyword(url, keyword):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract relevant data from the webpage based on the keyword
        keyword_data = []
        for paragraph in soup.find_all('p'):
            if keyword.lower() in paragraph.text.lower():
                keyword_data.append(paragraph.text.strip())

        if keyword_data:
            data = {
                'keyword': keyword,
                'content': '\n'.join(keyword_data)
            }

            return data
        else:
            print(f"No content related to the keyword '{keyword}' found on the webpage.")
            return None

    except Exception as e:
        print(f"Error scraping data: {e}")
        return None

# URL of the webpage to scrape
webpage_url = ' '  # Replace with the URL of the webpage you want to scrape
keyword_to_search = ' '  # Replace with the keyword you want to search for

# Scrape data from the webpage based on the keyword
scraped_data = scrape_data_by_keyword(webpage_url, keyword_to_search)

if scraped_data:
    # Insert the scraped data into the MongoDB collection
    inserted_document = collection.insert_one(scraped_data)
    print(f"Inserted document ID: {inserted_document.inserted_id}")
else:
    print("No data to insert.")

# Close the MongoDB client connection when done
client.close()
