import requests
import json
import re
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['city_inspections']
collection = db['inspections']

'''
url = "https://raw.githubusercontent.com/ozlerhakan/mongodb-json-files/master/datasets/city_inspections.json"
response = requests.get(url)

# Task 1 , parse each line as JSON and insert into the collection
for line in response.iter_lines():
    if line:
        document = json.loads(line)
        # Assigning value of $oid directly to _id
        document['_id'] = document['_id']['$oid']
        collection.insert_one(document)

print("Documents inserted successfully.")

'''

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

def main():
    
    year = input("Enter the year to count inspections: ")
    
    # Call the function to count inspections for the specified year
    total_inspections = count_inspections_by_year(year)
    
    # Display the result
    print(f"Total inspections in {year}: {total_inspections}")


    business_name = input("Enter the name of the business: ")
    
    # Call the function to check violation for the input business
    check_violation_for_business(business_name)



if __name__ == "__main__":
    main()