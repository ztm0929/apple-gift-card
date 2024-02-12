# 导入标准库
import json
import logging

# 导入第三方库
from playwright.sync_api import sync_playwright, TimeoutError, Error

# 定义全局常量
URL_GIFTCARD = "https://www.apple.com/shop/buy-giftcard/giftcard"
CONFIG_FILE_PATH = 'config.json'

# 设置日志
logging.basicConfig(level=logging.INFO)


def read_config(file_path):
    """从指定路径读取配置文件，并返回配置信息"""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError as e:
        logging.error(f"File {file_path} not found.")
        raise e
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON format in {file_path}.")
        raise e


def validate_config(config):
    """验证配置信息是否完整"""
    required_keys = ['toName', 'toEmail', 'fromName', 'fromEmail', 'amount', 'payment']
    for key in required_keys:
        if key not in config:
            logging.error(f"Missing key in config: {key}")
            raise ValueError(f"Missing key in config: {key}")


def fill_input(page, selector, value):
    """填充输入框"""
    page.fill(selector, value)


def fill_gift_card_info(page, config):
    """填充礼品卡信息"""
    fill_input(page, 'input[name="toName"]', config['toName'])
    fill_input(page, 'input[name="toEmail"]', config['toEmail'])
    fill_input(page, 'input[name="fromName"]', config['fromName'])
    fill_input(page, 'input[name="fromEmail"]', config['fromEmail'])


def fill_input_by_span_text(page, span_text, value):
    """通过相关联的span文本找到输入框并填充"""
    input_xpath = f"//span[text()='{span_text}']/preceding-sibling::input[1]"
    page.fill(input_xpath, value)


def main():
    """主函数"""
    config = read_config(CONFIG_FILE_PATH)
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
            page.click('button[data-analytics-title="Add to Bag"]')
            page.wait_for_selector('text=Check Out')
            with page.expect_navigation():
                page.click('text=Check Out')
            page.wait_for_selector('text=Continue as Guest')
            with page.expect_navigation():
                page.click('text=Continue as Guest')
            
            page.wait_for_selector('text=Credit or Debit Card')
            page.click('text=Credit or Debit Card')
            
            # 填写付款详细信息
            fill_input_by_span_text(page, 'Credit/Debit Card Number', config['payment']['cardNumber'])
            fill_input_by_span_text(page, 'Expiration MM/YY', config['payment']['expiration'])
            fill_input_by_span_text(page, 'CVV', config['payment']['CVV'])
            fill_input_by_span_text(page, 'First Name', config['payment']['firstName'])
            fill_input_by_span_text(page, 'Last Name', config['payment']['lastName'])
            fill_input_by_span_text(page, 'Email Address', config['payment']['email'])
            fill_input_by_span_text(page, 'Street Address', config['payment']['streetAddress'])
            fill_input_by_span_text(page, 'Zip Code', config['payment']['zipCode'])
            fill_input_by_span_text(page, 'Phone Number', config['payment']['phoneNumber'])
            
            page.wait_for_timeout(3000)            

            page.click('text=Continue to Review')
            
            page.wait_for_selector('input[type="checkbox"]')
            page.check('input[type="checkbox"]')

            page.wait_for_timeout(1000)

            page.wait_for_selector("#rs-checkout-continue-button-bottom")
            with page.expect_navigation():
                page.click("#rs-checkout-continue-button-bottom")

            page.wait_for_timeout(5000)
            
            logging.info("Gift card purchase was successful.")

    except TimeoutError:
        logging.error("Operation timed out.")
    except Error as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()
