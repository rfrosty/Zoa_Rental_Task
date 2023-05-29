from utils.classes import BaseElement
import utils.locators as locator


def submit_billing_form(window):
    BaseElement(window, locator.billing_continue, clickable=True).click()
