import pytest
from utils.config import base_url, window_dict, variable_dict
from utils.classes import BaseElement, BasePage


@pytest.fixture(autouse=True, scope='module')
def open_and_close_windows_and_clear_global_dictionaries():
    window_dict['window1'] = BasePage(base_url)
    variable_dict['skip_further_tests'] = False
    yield
    for window in window_dict:
        window_dict[window].close()
    window_dict.clear()
    variable_dict.clear()