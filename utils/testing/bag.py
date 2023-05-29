from utils.scraping.bag.functions import return_price_text_as_num
from utils.classes import BaseElement
import utils.locators as locator
from utils.config import variable_dict


def welcome20_discount_info_present_in_sidecart(window):
    BaseElement(window, locator.sidecart_welcome20)
    discount_value_text = BaseElement(window, locator.sidecart_discount_value).text
    assert discount_value_text[0:1] == '-'
    assert return_price_text_as_num(discount_value_text) == variable_dict['discount_value']
    assert return_price_text_as_num(BaseElement(window, locator.sidecart_total_value).text) == variable_dict['new_total_value']