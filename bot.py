import re
import requests
from faker import Faker
import random

# Initialize Faker for generating fake data
faker = Faker()

# Helper functions
def clean(message):
    return message.strip()

def luhn_check(bin_number):
    """Returns True if the BIN is valid according to the Luhn algorithm."""
    sum_digits = 0
    num_digits = len(bin_number)
    odd_even = num_digits & 1

    for i in range(num_digits):
        digit = int(bin_number[i])
        if (i & 1) ^ odd_even:
            digit = digit * 2
            if digit > 9:
                digit -= 9
        sum_digits += digit

    return (sum_digits % 10) == 0

def get_bin_details(bin_number):
    """Send POST request to external BIN service to get BIN details."""
    url = 'http://bins.su/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0'
    }
    data = {
        'action': 'searchbins',
        'bins': bin_number,
        'bank': '',
        'country': ''
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    # Parse the result with regex
    try:
        bank = clean(re.search(r'<td>Bank</td></tr><tr><td>(.*?)</td>', response.text).group(1))
        country = clean(re.search(fr'<td>{bank}</td><td>(.*?)</td>', response.text).group(1))
        brand = clean(re.search(fr'<td>{country}</td><td>(.*?)</td>', response.text).group(1))
        level = clean(re.search(fr'<td>{brand}</td><td>(.*?)</td>', response.text).group(1))
        card_type = clean(re.search(fr'<td>{level}</td><td>(.*?)</td>', response.text).group(1))
        return {
            'bin': bin_number,
            'bank': bank,
            'country': country,
            'brand': brand,
            'level': level,
            'type': card_type
        }
    except AttributeError:
        return None

def generate_fake_ip():
    """Generates a random IP address."""
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

def ipgen(amount=10):
    """Generates a list of fake IP addresses."""
    return [generate_fake_ip() for _ in range(amount)]

def generate_fake_details():
    """Generates fake personal details."""
    return {
        "name": faker.name(),
        "address": faker.address(),
        "country": faker.country(),
        "zip_code": faker.zipcode(),
        "email": faker.email(),
        "phone_number": faker.phone_number(),
        "account_number": faker.bban(),
        "bank": faker.bank(),
        "routing_number": faker.aba()
    }
