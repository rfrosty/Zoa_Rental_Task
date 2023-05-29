import time
import re
from selenium.common.exceptions import TimeoutException
from utils.classes import BaseElement
import utils.locators as locator


def return_price_text_as_num(price_text):
    start_index = re.search(r'\d', price_text).start()
    return float(price_text[start_index:])


def scroll_to_discount_section(window):
    BaseElement(window, locator.bag_discount_code_section, locator_js=locator.bag_discount_code_section_js, scroll_into_view=True)


def click_discount_input_reveal_btn(window):
    BaseElement(window, locator.bag_discount_input_reveal_btn, clickable=True).click()


def apply_discount_code(code, window):
    try:
        scroll_to_discount_section(window)
        BaseElement(window, locator.bag_discount_input)
    except TimeoutException:
        click_discount_input_reveal_btn(window)
    BaseElement(window, locator.bag_discount_input, clickable=True).input_text(code)
    BaseElement(window, locator.bag_discount_apply_btn, clickable=True).click()
    # Good idea to wait for the page to reload after the discount's applied to stop a StaleElement Exception.
    time.sleep(4)


def return_total_outfit_price(window):
    return return_price_text_as_num(BaseElement(window, locator.bag_total_outfit_price).text)


def return_total_price(window):
    return return_price_text_as_num(BaseElement(window, locator.bag_total_price).text)


def go_to_checkout(window):
    scroll_to_discount_section(window)
    checkout_btn = BaseElement(window, locator.bag_checkout_btn, clickable=True).click() # locator_js=locator.cart_checkout_btn_js, scroll_into_view=True