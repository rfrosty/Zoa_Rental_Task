from utils.classes import BaseElement, BasePage
import utils.locators as locator


def fill_form(window, first_name='0', last_name='0', email='0@0', mobile='0', delivery_address='20a Scotland Street, Edinburgh, EH36PX'):
    BaseElement(window, locator.delivery_first_name, clickable=True).input_text(first_name)
    BaseElement(window, locator.delivery_last_name, clickable=True).input_text(last_name)
    BaseElement(window, locator.delivery_email, clickable=True).input_text(email)
    BaseElement(window, locator.delivery_mobile, clickable=True).input_text(mobile)
    BaseElement(window, locator.delivery_address, clickable=True).input_text(delivery_address)


def accept_terms(window):
    BaseElement(window, locator.delivery_terms_checkbox, locator_js=locator.delivery_terms_checkbox_js, scroll_into_view=True)
    BaseElement(window, locator.delivery_terms_checkbox, clickable=True).click()


def submit_delivery_form(window):
    BaseElement(window, locator.delivery_continue, clickable=True).click()
