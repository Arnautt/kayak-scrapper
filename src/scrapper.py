from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

from src.utils import sort_dictionary


class KayakScrapper:
    """
    Kayak web scrapper

    Parameters
    ----------
    cfg: dict
        Trip parameters as a dictionary
    timeout: float
        Maximum time to wait a selenium element
    """

    def __init__(self, cfg, timeout=20):
        self.cfg = cfg
        self.timeout = timeout

    def click_search(self, driver):
        """Click on search button on the main page"""
        e_search = WebDriverWait(driver, self.timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "//button[@class='Iqt3 Iqt3-mod-bold Button-No-Standard-Style Iqt3-mod-variant-solid Iqt3-mod-theme-progress Iqt3-mod-shape-rounded-small Iqt3-mod-shape-mod-default Iqt3-mod-spacing-default Iqt3-mod-size-large-legacy Iqt3-mod-animation-search']"))
        )
        e_search.click()

        # Wait for the page to be loaded
        WebDriverWait(driver, self.timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='_ihz _irp _iqB _ilc _iai']"))
        )

    @staticmethod
    def _init_options():
        """Instantiate options for webdriver"""
        options = Options()
        options.headless = True
        return options

    def get_driver(self):
        """Get driver to scrape Kayak"""
        options = self._init_options()
        driver = webdriver.Firefox(service=Service(
            GeckoDriverManager().install()), options=options)
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get("https://www.kayak.fr")
        return driver

    def quit_cookies(self, driver):
        """Quit cookies popup (present for all European websites)"""
        element_cookies = WebDriverWait(driver, self.timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='dDYU-close dDYU-mod-variant-default dDYU-mod-size-default']"))
        )
        element_cookies.click()

    def clear_cached_cities(self, driver):
        """Remove pre-filled cities"""
        _ = WebDriverWait(driver, self.timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "//div[@class='vvTc-item-button']"))
        )

        buttons = driver.find_elements(
            By.XPATH, "//div[@class='vvTc-item-button']")
        for button in buttons:
            try:
                button.click()
            except:
                pass

    def set_from_city(self, driver, city="Paris"):
        """Set the departure city"""
        e_from_city = WebDriverWait(driver, self.timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@class='k_my-input']"))
        )
        e_from_city.send_keys(city)

    def set_first_airport_founded(self, driver):
        """Set the first airport founded in the combobox after filling the departure city"""
        _ = WebDriverWait(driver, self.timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "//ul[@class='QHyi QHyi-mod-variant-bordered-first QHyi-pres-padding-default QHyi-mod-alignment-left']"))
        )

        buttons = driver.find_elements(
            By.XPATH, "//div[@class='JyN0-checkbox']")
        buttons[0].click()

    @staticmethod
    def from_to_to_city(driver):
        """Going from 'from' button to 'to' button"""
        actions = ActionChains(driver)
        actions.send_keys(Keys.ENTER)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.perform()

    def set_anywhere_destination(self, driver):
        """Set anywhere as a destination to have all possibilities"""
        e_anywhere = WebDriverWait(driver, self.timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@class='hpCj hpCj-pres-item-horizon hpCj-clickable hpCj-anywhere']"))
        )
        e_anywhere.click()

    def get_all_results(self, driver):
        """Get all results of the research by clicking on load more"""
        while True:
            try:
                e = WebDriverWait(driver, self.timeout).until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                         "//button[@class='xzUt xzUt- xzUt- xzUt-mod-bold xzUt-mod-theme-action xzUt-mod-variant-solid xzUt-mod-shape-rounded-small xzUt-mod-shape-mod-default xzUt-mod-spacing-default xzUt-mod-shadow-none xzUt-mod-size-medium Button-No-Standard-Style ']"))
                )

            except TimeoutException:
                break

            e.click()

    @staticmethod
    def get_all_trips(driver):
        """Get all possible trips founded by Kayak"""
        cities = driver.find_elements(
            By.XPATH, "//div[@class='_ib0 _igh _ial _1O _iaj City__Name']")
        prices = driver.find_elements(
            By.XPATH, "//div[@class='_ib0 _18 _igh _ial _iaj']")

        all_trips = {}
        for city_element, price_element in zip(cities, prices):
            try:
                city = city_element.text
                price = price_element.text.split(" ")[1]
                all_trips[city] = float(price)
            except:
                pass

        return all_trips

    @staticmethod
    def filter_all_trips(all_trips, max_price):
        """Get all trips below a certain price threshold"""
        possible_trips = {city: price for city,
                          price in all_trips.items() if price <= max_price}
        possible_trips = sort_dictionary(possible_trips)
        return possible_trips

    @staticmethod
    def convert_datetime_kayak_format(date):
        """Get data on the right format for Kayak"""
        date_time_obj = datetime.strptime(date, '%d/%m/%Y')
        date_time_obj = date_time_obj.strftime("%Y%m%d")
        return date_time_obj

    def change_date_in_url(self, driver):
        """In the URL, change date trip option"""
        curr_url = driver.current_url
        departure_date = self.convert_datetime_kayak_format(
            self.cfg["departure_date"])
        arrival_date = self.convert_datetime_kayak_format(
            self.cfg["arrival_date"])
        new_url = "/".join(curr_url.split("/")
                           [:-1]) + f"/{departure_date},{arrival_date}"
        driver.get(new_url)

        # wait until load more is visible
        WebDriverWait(driver, self.timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//button[@class='xzUt xzUt- xzUt- xzUt-mod-bold xzUt-mod-theme-action xzUt-mod-variant-solid xzUt-mod-shape-rounded-small xzUt-mod-shape-mod-default xzUt-mod-spacing-default xzUt-mod-shadow-none xzUt-mod-size-medium Button-No-Standard-Style ']"))
        )

    def scrape(self):
        """Scrape the website and enjoy"""
        driver = self.get_driver()
        self.quit_cookies(driver)
        self.clear_cached_cities(driver)
        self.set_from_city(driver, self.cfg["from_city"])
        self.set_first_airport_founded(driver)
        self.from_to_to_city(driver)
        self.set_anywhere_destination(driver)
        self.click_search(driver)
        self.change_date_in_url(driver)
        self.get_all_results(driver)
        all_trips = self.get_all_trips(driver)
        possible_trips = self.filter_all_trips(
            all_trips, self.cfg["max_price"])
        return possible_trips
