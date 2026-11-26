
import csv
import json
import requests
from dotenv import load_dotenv
import os


# 1. Load environment variables
load_dotenv()

api_key = os.getenv("API_KEY")
print("API Key loaded:", "Yes" if api_key else "No")


# 2. Read employees.csv
with open("data/employees.csv", "r", newline="") as file:
    reader = csv.DictReader(file)
    employees = list(reader)

print("Rows read:", len(employees))


# 3. Write employees.json
with open("data/employees.json", "w") as file:
    json.dump(employees, file, indent=4)


# 4. Write high_earners.csv
high_earners = [
    emp for emp in employees if int(emp["salary"]) > 50000
]

with open("data/high_earners.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=employees[0].keys())
    writer.writeheader()
    writer.writerows(high_earners)

print("High earners:", len(high_earners))


# 5. GET API request
url = "https://jsonplaceholder.typicode.com/users"

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    users = response.json()

    for user in users[:3]:
        print(
            user["id"], "-",
            user["name"], "-",
            user["email"]
        )

    # Parse nested JSON using get()
    for user in users[:3]:
        address = user.get("address", {})
        city = address.get("city", "Unknown")
        print("City:", city)

    with open("data/users.json", "w") as file:
        json.dump(users, file, indent=4)

except requests.exceptions.Timeout:
    print("API Error: Request timed out")

except requests.exceptions.ConnectionError:
    print("API Error: Connection failed")

except requests.exceptions.HTTPError as error:
    print("API HTTP Error:", error)


# 6. Test 404 error
try:
    response = requests.get(
        "https://jsonplaceholder.typicode.com/users/9999",
        timeout=5
    )

    if response.status_code == 404:
        print("/users/9999 -> 404 Not found")
    else:
        response.raise_for_status()

except requests.exceptions.Timeout:
    print("404 test timed out")

except requests.exceptions.ConnectionError:
    print("404 test connection failed")
