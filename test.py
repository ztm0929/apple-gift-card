import time
from playwright.sync_api import sync_playwright
import json

def read_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def fill_gift_card_info(page, config):
    page.fill('input[name="toName"]', config['toName'])
    page.fill('input[name="toEmail"]', config['toEmail'])
    page.fill('input[name="fromName"]', config['fromName'])
    page.fill('input[name="fromEmail"]', config['fromEmail'])

def fill_input_by_span_text(page, span_text, value):
    input_xpath = f"//span[text()='{span_text}']/preceding-sibling::input[1]"
    page.fill(input_xpath, value)


def main():
    config = read_config('config.json')  # 假设在同一目录下有一个名为 config.json 的配置文件
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False
        )
        page = browser.new_page()
        
        page.goto("https://www.apple.com/shop/buy-giftcard/giftcard")
        
        # 等待特定的选择器，而不是任意的超时
        page.wait_for_selector('text=Email')
        page.click('text=Email')
        
        page.wait_for_selector('text=Other Amount')
        page.click('text=Other Amount')
        
        page.keyboard.type(config['amount'])
        page.click('body')
        
        # 等待表单准备就绪
        page.wait_for_selector('input[name="toName"]')
        fill_gift_card_info(page, config)

        # page.click('text=Add to Bag')
        page.click('button[title="Add to Bag"]')



        # # 等待页面跳转完成
        # with page.expect_navigation():
        #     page.click('text=Add to Bag')

        time.sleep(5)

        
        # 确保“Check Out”按钮已经出现并点击
        page.wait_for_selector('text=Check Out')
        with page.expect_navigation():
            page.click('text=Check Out')
        
        # 在新页面上，确保“Continue as Guest”按钮已经出现并点击
        page.wait_for_selector('text=Continue as Guest')
        with page.expect_navigation():
            page.click('text=Continue as Guest')

        page.wait_for_selector('text=Credit or Debit Card')
        page.click('text=Credit or Debit Card')


        # 使用 config 中的支付信息填充表单
        fill_input_by_span_text(page, 'Credit/Debit Card Number', config['payment']['cardNumber'])
        fill_input_by_span_text(page, 'Expiration MM/YY', config['payment']['expiration'])
        fill_input_by_span_text(page, 'CVV', config['payment']['CVV'])
        fill_input_by_span_text(page, 'First Name', config['payment']['firstName'])
        fill_input_by_span_text(page, 'Last Name', config['payment']['lastName'])
        fill_input_by_span_text(page, 'Email Address', config['payment']['email'])
        fill_input_by_span_text(page, 'Street Address', config['payment']['streetAddress'])
        fill_input_by_span_text(page, 'Zip Code', config['payment']['zipCode'])
        fill_input_by_span_text(page, 'Phone Number', config['payment']['phoneNumber'])

        time.sleep(5)
        page.click('text=Continue to Review')

        # page.wait_for_selector('text=Continue to Review')
        # with page.expect_navigation():
        #     page.click('text=Continue to Review')

        # with page.expect_navigation():
        #     page.click('text=Place Your Order')

        time.sleep(5)

        page.wait_for_selector('input[type="checkbox"]')
        page.check('input[type="checkbox"]')

        page.wait_for_selector('text=Place Your Order')
        page.click('text=Place Your Order')

       


        time.sleep(30000)

if __name__ == "__main__":
    main()
