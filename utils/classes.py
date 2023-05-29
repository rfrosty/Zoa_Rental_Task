import time

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('disable-infobars')
# chrome_options.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')


class BaseElement(object):
    def __init__(self, window, locator, locator_js=False, clickable=False, text_to_wait_until_present=None, waiting_time=10, waiting_time_after_scrolling_into_view=3, scroll_into_view=False, scroll_by=[], scroll_into_view_false=False):
        self.window = window
        self.driver = window.driver
        self.locator = locator
        if self.locator[0:2] == '//':
            self.by = By.XPATH
        else:
            self.by = By.CSS_SELECTOR
        if locator_js:
            self.locator_js = locator_js.replace('"', '\\"')
        else:
            self.locator_js = locator.replace('"', '\\"')
        self.text_to_wait_until_present = text_to_wait_until_present
        if clickable:
            self.expected_condition = EC.element_to_be_clickable
        else:
            self.expected_condition = EC.visibility_of_element_located
        self.locator = (self.by, self.locator)
        self.web_element = None
        self.waiting_time = waiting_time
        self.time_to_wait_to_be_absent = None
        if scroll_into_view:
            self.scroll_into_view()
            time.sleep(waiting_time_after_scrolling_into_view)
        if scroll_into_view_false:
            self.scroll_into_view_false()
        if scroll_by:
            self.scroll_by(scroll_by[0], scroll_by[1])
        self.find()

    def execute_javascript(self, javascript):
        self.driver.execute_script(javascript)

    def scroll_into_view(self):
        self.execute_javascript(f'''el = document.evaluate("{self.locator_js}", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null); el = el.snapshotItem(0); el.scrollIntoView()''')

    def scroll_into_view_false(self):
        self.execute_javascript(f'''el = document.evaluate("{self.locator_js}", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null); el = el.snapshotItem(0); el.scrollIntoView(false)''')

    def scroll_by(self, x, y):
        self.execute_javascript(f'''window.document.scrollBy({x}, {y})''')

    def scroll_to_btm_of(self):
        self.execute_javascript(f'''el = document.evaluate("{self.locator_js}", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null); el = el.snapshotItem(0); el.scrollBy(0, el.scrollHeight)''')

    def scroll_to_top_of(self):
        self.execute_javascript(f'''el = document.evaluate("{self.locator_js}", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null); el = el.snapshotItem(0); el.scrollTo(0, 0)''')

    def find(self):
        attempts = 0
        while True:
            try:
                if self.text_to_wait_until_present:
                    WebDriverWait(self.driver, self.waiting_time).until(EC.text_to_be_present_in_element(self.locator, self.text_to_wait_until_present))
                self.web_element = WebDriverWait(self.driver, self.waiting_time).until(self.expected_condition(self.locator))
                break
            except StaleElementReferenceException:
                attempts += 1
                if attempts >= 2:
                    raise Exception

    def wait_to_be_absent(self, time):
        self.time_to_wait_to_be_absent = time
        WebDriverWait(self.driver, self.time_to_wait_to_be_absent).until(EC.invisibility_of_element_located(self.locator))

    def move_to_element(self):
        self.window.actions.move_to_element(self.web_element)

    def click(self):
        self.window.actions.move_to_element(self.web_element)
        self.window.actions.click(self.web_element)
        self.window.actions.perform()

    def double_click(self):
        self.click()
        time.sleep(1)
        self.click()

    @property
    def text(self):
        return self.web_element.text.strip()

    def clear_text(self):
        self.web_element.clear()

    def input_text(self, text):
        self.web_element.send_keys(text)

    def clear_text_and_input_text(self, text):
        self.clear_text()
        self.input_text(text)

    def press_enter(self):
        self.web_element.send_keys(Keys.ENTER)

    def press_upwards_key(self):
        self.web_element.send_keys(Keys.UP)

    def get_attribute_value(self, attribute):
        return self.web_element.get_attribute(attribute)

    def find_child_el(self, locator, by=By.CSS_SELECTOR):
        return self.web_element.find_element(by, locator)

    def return_true_if_this_radio_btn_or_checkbox_is_selected(self):
        return self.web_element.is_selected()

    def select_select_tag_option_tag_by_text(self, value):
        Select(self.web_element).select_by_visible_text(value)


class BasePage(object):
    def __init__(self, url, width=None, height=None):
        self.driver = webdriver.Chrome()
        # add this arg to run it in headless mode: `options=chrome_options`
        self.actions = ActionChains(self.driver)
        self.url = url
        self.width = width
        self.height = height
        self.go()
        self.resize()

    def execute_javascript(self, javascript):
        self.driver.execute_script(javascript)

    def go(self):
        self.driver.get(self.url)

    def refresh_current_url(self):
        self.driver.refresh()

    def resize(self):
        self.driver.maximize_window()

    def wait_for_url_to_contain_string(self, string):
        WebDriverWait(self.driver, 20).until(EC.url_contains(string))

    @property
    def url_as_string(self):
        return self.driver.current_url

    def go_to_new_url(self, url):
        self.url = url
        self.go()

    def open_new_tab(self, url):
        self.execute_javascript(f'''window.open("{url}", "_blank")''')

    def switch_tab(self, tab_num):
        self.driver.switch_to.window(self.driver.window_handles[tab_num])

    def duplicate_tab_and_switch_to_it(self, tab_to_switch_to=1):
        self.open_new_tab(self.url_as_string)
        self.switch_tab(tab_to_switch_to)
        self.wait_for_url_to_contain_string(self.url_as_string)

    # def return_list_of_els(self, path, by=By.XPATH):
    #     return self.driver.find_elements(by, path)

    def return_list_of_els_that_have_width_and_height_not_0(self, locator, by=By.CSS_SELECTOR, time_to_wait=20):
        list_of_els = WebDriverWait(self.driver, time_to_wait).until(EC.visibility_of_all_elements_located((by, locator)))
        list_of_base_els = []
        for el in list_of_els:
            new_base_el = BaseElement(self, locator, by=by)
            new_base_el.web_element = el
            list_of_base_els.append(new_base_el)
        return list_of_base_els

    def close_current_tab(self, tab_to_switch_to=0):
        self.driver.close()
        self.switch_tab(tab_to_switch_to)

    def go_back(self):
        self.driver.back()

    def quit(self):
        self.driver.quit()