import time
from playwright.sync_api import sync_playwright, TimeoutError, Error
import json
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)

# Constants for URLs and selectors
URL_GIFTCARD = "https://www.apple.com/shop/buy-giftcard/giftcard"

def read_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        exit()
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in {file_path}.")
        exit()

def validate_config(config):
    required_keys = ['toName', 'toEmail', 'fromName', 'fromEmail', 'amount', 'payment']
    for key in required_keys:
        if key not in config:
            logging.error(f"Missing key in config: {key}")
            exit()

def fill_gift_card_info(page, config):
    page.fill('input[name="toName"]', config['toName'])
    page.fill('input[name="toEmail"]', config['toEmail'])
    page.fill('input[name="fromName"]', config['fromName'])
    page.fill('input[name="fromEmail"]', config['fromEmail'])

def fill_input_by_span_text(page, span_text, value):
    input_xpath = f"//span[text()='{span_text}']/preceding-sibling::input[1]"
    page.fill(input_xpath, value)

def main():
    config = read_config('config.json')
    validate_config(config)
    
    try:
        with sync_playwright() as p, p.chromium.launch(headless=False) as browser:
            page = browser.new_page()
            
            page.goto(URL_GIFTCARD)
            page.wait_for_selector('text=Email')
            page.click('text=Email')
            page.wait_for_selector('text=Other Amount')
            page.click('text=Other Amount')
            page.keyboard.type(config['amount'])
            page.click('body')
            page.wait_for_selector('input[name="toName"]')
            fill_gift_card_info(page, config)
            page.click('button[title="Add to Bag"]')
            page.wait_for_selector('text=Check Out')
            with page.expect_navigation():
                page.click('text=Check Out')
            page.wait_for_selector('text=Continue as Guest')
            with page.expect_navigation():
                page.click('text=Continue as Guest')
            page.wait_for_selector('text=Credit or Debit Card')
            page.click('text=Credit or Debit Card')
            
            # Filling the payment details
            fill_input_by_span_text(page, 'Credit/Debit Card Number', config['payment']['cardNumber'])
            fill_input_by_span_text(page, 'Expiration MM/YY', config['payment']['expiration'])
            fill_input_by_span_text(page, 'CVV', config['payment']['CVV'])
            fill_input_by_span_text(page, 'First Name', config['payment']['firstName'])
            fill_input_by_span_text(page, 'Last Name', config['payment']['lastName'])
            fill_input_by_span_text(page, 'Email Address', config['payment']['email'])
            fill_input_by_span_text(page, 'Street Address', config['payment']['streetAddress'])
            fill_input_by_span_text(page, 'Zip Code', config['payment']['zipCode'])
            fill_input_by_span_text(page, 'Phone Number', config['payment']['phoneNumber'])
            
            page.click('text=Continue to Review')
            page.wait_for_selector('input[type="checkbox"]')
            page.check('input[type="checkbox"]')
            page.wait_for_selector('text=Place Your Order:nth-match(2)')
            page.click('text=Place Your Order:nth-match(2)')
            logging.info("Gift card purchase was successful.")
    
    except TimeoutError:
        logging.error("Operation timed out.")
    except Error as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()
