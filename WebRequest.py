import requests
import json

# Create a session to manage cookies and headers
session = requests.Session()

# Define the headers to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

# Function to browse a few websites to gather cookies
def browse_initial_sites(session, headers):
    sites = [
        "https://www.google.com",
        "https://www.wikipedia.org",
        "https://www.github.com"
    ]
    for site in sites:
        session.get(site, headers=headers)

# Browse initial sites to establish session history
browse_initial_sites(session, headers)

# URL to send the request to
url = "https://usa.visa.com/cmsapi/fx/rates"

# Parameters to send in the GET request
params = {
    'amount': '1',
    'fee': '2',
    'utcConvertedDate': '06/22/2024',
    'exchangedate': '06/20/2024',
    'fromCurr': 'USD',
    'toCurr': 'INR'
}

# Update headers to include the referer after browsing initial sites
headers.update({
    'Referer': 'https://usa.visa.com/support/consumer/travel-support/exchange-rate-calculator.html',
})

# Send the GET request to the target URL using the session
response = session.get(url, headers=headers, params=params)

# Check the response status and pretty-print the JSON content if successful
if response.status_code == 200:
    print(json.dumps(response.json(), indent=4))
else:
    print(f"Failed to retrieve data: {response.status_code}")
