from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from checker import DomainChecker

PASSPHRASE = 'swallow buffalo check first very refuse fix health when demand traffic sheriff'.split()
PASSWORD = '7$8rt(C*7:+Y-g+2'
URL = 'https://mail.dmail.ai/login?path=%2Fpresale%2F194332'
EXTENSION_PATH = 'extension/metamask_10_28_2.crx'


class DmailChecker(DomainChecker):

    def click_button(self, n) -> None:
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        buttons[n].click()

    def website_prepare(self):
        # open dmail website
        self.driver.get(URL)
        sleep(3)

        metamask_connect = self.driver.find_element(By.CLASS_NAME, "metamask")
        metamask_connect.click()
        sleep(5)

    def login(self) -> None:
        opt = Options()
        opt.add_extension(EXTENSION_PATH)

        self.driver = webdriver.Chrome(options=opt)

        sleep(5)

        # switch the focus to the last tab
        window_handles = self.driver.window_handles
        last_window_handle = window_handles[-1]
        self.driver.switch_to.window(last_window_handle)

        sleep(2)

        # Click to Import existing wallet and No, thanks (to data sending)
        for _ in range(2):
            buttons = self.driver.find_elements(By.TAG_NAME, "button")

            if buttons:
                print(f"Clicked on {buttons[-1].text}")
                buttons[-1].click()
            else:
                print("Buttons not found")

            sleep(1)

        # Fill in passphrase
        inputs = self.driver.find_elements(By.TAG_NAME, 'input')[::2]
        for i, p in zip(inputs, PASSPHRASE):
            i.send_keys(p)

        sleep(1)
        buttons = self.driver.find_elements(By.TAG_NAME, "button")

        if buttons:
            print(f"Clicked on {buttons[-1].text}")
            try:
                buttons[-1].click()
            except:
                print("Incorrect passphrase")
        else:
            print("'Confirm Secret Recovery Phrase' button was not found")

        sleep(1)

        # set up a password
        password_input, confirm_input, checkbox = self.driver.find_elements(By.TAG_NAME, 'input')
        password_input.send_keys(PASSWORD)
        confirm_input.send_keys(PASSWORD)
        checkbox.click()

        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        buttons[-1].click()

        sleep(1)

        # confirm creation
        self.click_button(-1)

        sleep(1)
        # click next
        for _ in range(2):
            self.click_button(-1)
            sleep(0.5)

        sleep(1)
        self.click_button(12)

        # Open website info
        self.website_prepare()

        # switch the focus to the last tab
        window_handles = self.driver.window_handles
        last_window_handle = window_handles[-1]
        self.driver.switch_to.window(last_window_handle)

        self.click_button(-1)
        sleep(1)
        self.click_button(-1)
        sleep(2)
        self.click_button(-1)

        # wait until input tag will be present on the webpage
        sleep(20)

        # switch the focus to the last tab
        window_handles = self.driver.window_handles
        last_window_handle = window_handles[-1]
        self.driver.switch_to.window(last_window_handle)

    def check_if_free(self, check_field, domain: str, free_text: str = None, taken_text: str = None) -> bool:
        """Input domain into field and wait if taken or free tag appeared on the page"""
        if not 4 <= len(domain) <= 11:
            print(f'{domain} is not a valid domain name')
            return False

        check_field.send_keys(domain)

        links = self.driver.find_elements(By.TAG_NAME, "a")
        links[5].click()

        sleep(1)

        # check if free_text in body tag of a page
        for _ in range(10):
            if free_text in self.driver.find_element(By.TAG_NAME, 'body').text:
                return True
            elif taken_text in self.driver.find_element(By.TAG_NAME, 'body').text:
                return False
            sleep(0.3)

        print("Wait time is too long")


def main():
    ch = DmailChecker(URL, output_dir='dmail_out')

    ch.run('text.txt', taken_text='occupied', free_text='available')


if __name__ == '__main__':
    main()
