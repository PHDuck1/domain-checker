import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from checker import DomainChecker

URL = 'https://cyberconnect.me/mint'


class CyberconnectChecker(DomainChecker):
    def login(self) -> None:
        self.driver.get(URL)
        time.sleep(2)

        # get connect wallet button
        connect_wallet = self.driver.find_elements(By.TAG_NAME, "button")[8]
        connect_wallet.click()
        time.sleep(1)

        # get metamask button
        metamask = self.driver.find_elements(By.TAG_NAME, "button")[10]
        metamask.click()

        # get send message button
        wait = WebDriverWait(self.driver, 60)
        wait.until(EC.text_to_be_present_in_element(
                (By.XPATH, "//*[contains(text(), 'Send message')]"), 'Send message'))
        time.sleep(1)
        send_message = self.driver.find_elements(By.TAG_NAME, "button")[11]
        send_message.click()

        # get field
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//input)[1]")))


if __name__ == '__main__':
    ch = CyberconnectChecker(URL, output_dir='cyber_out')
    ch.run('text.txt', taken_text='Handle is not available')
