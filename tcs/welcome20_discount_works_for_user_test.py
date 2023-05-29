import pytest

from utils.classes import BaseElement
from utils.config import window_dict, variable_dict
import utils.locators as locator
from utils.scraping.bag.functions import apply_discount_code, return_total_outfit_price, return_total_price, \
    return_price_text_as_num, go_to_checkout
from utils.scraping.delivery.functions import submit_delivery_form, accept_terms
from utils.scraping.billing.functions import submit_billing_form
from utils.testing.bag import welcome20_discount_info_present_in_sidecart


class TestWelcome20DiscountWorksForUser:

    def test_discount_works_on_bag_page(self):
        total_outfit_price = return_total_outfit_price(window_dict['window1'])
        initial_total_price = return_total_price(window_dict['window1'])
        apply_discount_code("WELCOME20", window_dict['window1'])
        assert BaseElement(window_dict['window1'], locator.bag_discount_label).text == 'WELCOME20:'
        discount_value_text = BaseElement(window_dict['window1'], locator.bag_discount_value).text
        assert discount_value_text[0:1] == '-'
        variable_dict['discount_value'] = return_price_text_as_num(discount_value_text)
        assert variable_dict['discount_value'] == round(total_outfit_price * 0.2, 2)
        variable_dict['new_total_value'] = return_price_text_as_num(BaseElement(window_dict['window1'], locator.bag_total_price).text)
        assert variable_dict['new_total_value'] == initial_total_price - variable_dict['discount_value']

    def test_discount_visible_on_delivery_tab(self):
        go_to_checkout(window_dict['window1'])
        welcome20_discount_info_present_in_sidecart(window_dict['window1'])
        accept_terms(window_dict['window1'])
        submit_delivery_form(window_dict['window1'])

    def test_discount_visible_on_billing_tab(self):
        welcome20_discount_info_present_in_sidecart(window_dict['window1'])
        submit_billing_form(window_dict['window1'])

    def test_discount_visible_on_payment_tab(self):
        welcome20_discount_info_present_in_sidecart(window_dict['window1'])







