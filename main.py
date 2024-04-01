import requests
import json
import re
import random
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['city_inspections']
collection = db['inspections']


# Function to fetch and insert data if database is empty
def fetch_and_insert_data(url):
    if collection.count_documents({}) == 0:
        response = requests.get(url)
        for line in response.iter_lines():
            if line:
                document = json.loads(line)
                document['_id'] = document['_id']['$oid']
                collection.insert_one(document)
        print("Documents inserted successfully.")
    else:
        print("Database already contains data. No need to fetch.")

url = "https://raw.githubusercontent.com/ozlerhakan/mongodb-json-files/master/datasets/city_inspections.json"
fetch_and_insert_data(url)

# Task 2 Count the number of inspections 

def count_inspections_by_year(year):
    # Define the query to filter documents by year
    query = {
        "date": {"$regex": f".*{year}.*"}
    }
    
    # Count the number of documents matching the query
    count = collection.count_documents(query)
    return count

# Task 3 


def check_violation_for_business(business_name):
    # Define a regular expression pattern for case-insensitive matching
    regex_pattern = re.compile(f'^{business_name}$', re.IGNORECASE)
    
    # Search for the business in the collection
    query = {"business_name": regex_pattern}
    result = collection.find_one(query)
    
    if result:
        if result['result'] == "Violation Issued":
            print(f"The business '{result['business_name']}' has a violation.")
        else:
            print(f"The business '{result['business_name']}' has no violation.")
    else:
        print("Business not found.")

# Task 4

# return a cursor for all businesses in a specified borough
def cursor_of_businesses_in_borough(borough_name):
    borough_name = borough_name.lower()
    
    # start zip is the lower zip code in the range for specified borough
    start_zip = 0
    
    # end zip is upper zip code in the range for specified borough
    end_zip = 0
    
    # Queens has two ranges for zip codes. remain 0 if the borough is not queens
    start_zip2 = 0
    end_zip2 = 0
    
    if borough_name == "bronx":
        start_zip = 10451
        end_zip = 10475
        
    elif borough_name == "brooklyn":
        start_zip = 11201
        end_zip = 11256
        
    elif borough_name == "manhattan":
        start_zip = 10001
        end_zip = 10282
        
    elif borough_name == "queens":
        start_zip = 11004
        end_zip = 11109
        
        start_zip2 = 11351
        end_zip2 = 11697
        
    elif borough_name == "staten island":
        start_zip = 10301
        end_zip = 10314
        
    else:
        print("Invalid entry. Must enter the name of a borough")
        return
        
    # create cursor for all businesses whos zip codes fall in the range for the specified borough and return
    cursor = collection.find({"$or":[{"address.zip": {"$gte": start_zip, "$lte": end_zip}}, 
                                     {"address.zip": {"$gte": start_zip2, "$lte": end_zip2}}]})
    return cursor
        

# return the number of violations in a specified borough
def num_violations_by_borough(borough_name):
    # get a cursor, businesses, of all businesses in the specified borough
    businesses = cursor_of_businesses_in_borough(borough_name)
    total = 0
    
    # iterate through the cursor and add 1 to the counter, total, every time there is a business with a violation issued
    for x in businesses:
        if x.get("result") == "Violation Issued":
            total += 1
    return total

# print the first 5 businesses that are found in a specific borough
def print_first_five_businesses_in_borough(borough):
    # obttain cursor for first 5 businesses in a specified borough
    cursor = cursor_of_businesses_in_borough(borough).limit(5)
    print ("First 5 businesses in " + borough)
    
    # iterate through the cursor and print the business_name for each item
    for business in cursor:
        print (business.get("business_name"))
        print (business.get("address"))
        print()

# Task 5

# return the number of violations found in a specific zip code
def num_violations_by_zipcode(zip_code):
    query = {"$and": [{"address.zip": zip_code}, {"result": "Violation Issued"}]}
    
    # Count the number of documents matching the query
    count = collection.count_documents(query)
    return count
    
# return the number of businesses in a specific zip code
def num_businesses_in_zip_code(zip_code):
    return collection.count_documents({"address.zip":zip_code})

# print 5 random businesses in a specific zip code
def print_random_five_businesses_by_zip_code(zip_code):
    # first calculate the number of businesses in the zip code
    num_businesses = num_businesses_in_zip_code(zip_code)
    
    # if no businesses are found, print "Zip-code Not found." and return from function
    if num_businesses == 0:
        print("Zip-code Not found.")
        return
    
    # if there are 5 or less businesses in the specified zip code, print them all out and return from function
    if(5 >= num_businesses):
            print("There are only " + str(num_businesses) + " in the given zip code:")
            cursor = collection.find({"address.zip":zip_code})
            for business in cursor:
                print(business.get("business_name"))
            return
            
    # if more than 5 businesses, randomly generate 5 numbers and print the associated business
    print("5 random businesses in the zip code: " + str(zip_code))
    random_numbers = random.sample(range(num_businesses), 5)
    for randnum in random_numbers:
        business = collection.find_one({"address.zip":zip_code}, skip=randnum)
        print(business.get("business_name"))
        

def main():
    year = input("Enter the year to count inspections: ")
    total_inspections = count_inspections_by_year(year)
    print(f"Total inspections in {year}: {total_inspections}")

    business_name = input("Enter the name of the business: ")
    check_violation_for_business(business_name)
    
    count_bronx = num_violations_by_borough("bronx")
    print("Number of violations in the Bronx " + str(count_bronx))
    
    count_brooklyn = num_violations_by_borough("brooklyn")
    print("Number of violations in Brooklyn " + str(count_brooklyn))
    
    print("The difference between the number of violations in Brooklyn and the Bronx is " + str(abs(count_bronx-count_brooklyn)))
    
    print("-------------")
    print_first_five_businesses_in_borough("brooklyn")
    
    print("-------------")
    print_first_five_businesses_in_borough("bronx")
    
    zip_code = int(input("Enter a zip code in one of the 5 boroughs: "))
    print_random_five_businesses_by_zip_code(zip_code)
    

if __name__ == "__main__":
    main()