# City Inspections Analysis

## Overview
This project is a Python script that performs analysis on city inspection data retrieved from a MongoDB collection. It connects to a MongoDB instance, fetches inspection data from a provided URL, and then performs various tasks such as counting the number of inspections by year and checking for violations for a specific business.

## Requirements
- Python 3.x
- MongoDB
- pymongo library (`pip install pymongo`)

## Installation
1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/city_inspections_analysis.git
    cd city_inspections_analysis
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure MongoDB is installed and running on your system.

## Usage
1. Run the `main.py` script:

    ```bash
    python main.py
    ```

2. Follow the prompts to perform various tasks:
    - Enter the year to count inspections performed in that year.
    - Enter the name of a business to check if it has any violations.

## Tasks Implemented
1. **Count Inspections by Year**
   - Fetches the total number of inspections performed in a specified year.

2. **Check Violation for Business**
   - Allows the user to input the name of a business.
   - Checks if the business has any violations.

## Notes
- The script fetches inspection data from a specified URL and inserts it into the MongoDB collection. This functionality is commented out in the script, assuming the data is already available in the collection.
- Ensure that the MongoDB instance is running and accessible from the script.

[Feel free to customize this README according to your project's specifics. Let me know if you need further assistance!]