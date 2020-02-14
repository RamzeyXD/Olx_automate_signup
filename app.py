from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import clipboard
import time
from python_rucaptcha import ReCaptchaV2


# Api key of RuCaptcha
RUCAPTCHA_KEY = "Token"

# Password is the same for all of those acoounts
accounts = []


class OlxBot:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)

        self.mail = TempMail(self.driver)
        time.sleep(3)

        self.mail.get_mail()

        # Save Account login(email)
        accounts.append(clipboard.paste())

        self.driver.execute_script("window.open('https://www.olx.ua/account/?ref%5B0%5D%5Baction%5D=myaccount&ref%5B0%5D%5Bmethod%5D=index#register', 'new window')")
        self.driver.switch_to_window(self.driver.window_handles[-1])

    def registrate(self):
        time.sleep(5)
        # Fill up the email form
        self.driver.find_element_by_id("userEmailPhoneRegister").send_keys(Keys.CONTROL + 'v')

        # Fill up the password form
        self.driver.find_element_by_id("userPassRegister").send_keys("123BotPassword")

        # Push checkbox
        self.driver.find_element_by_xpath("/html/body/div[3]/section/div[2]/div/ul/li[2]/form/div[3]/div/div/label[1]").click()

        # Get data for ruCaptcha
        url = self.driver.current_url
        site_key = self.driver.find_element_by_class_name("g-recaptcha").get_attribute('data-sitekey')

        # Get result of ruCaptcha
        response = captcha(site_key, url)

        self.driver.execute_script("document.getElementById('g-recaptcha-response').style.display = 'block';")
        self.driver.find_element_by_id("g-recaptcha-response").send_keys(response['captchaSolve'])
        self.driver.find_element_by_xpath("/html/body/div[3]/div[6]/button").click()
        self.driver.find_element_by_id("button_register").click()

    def verify_email(self):
        self.driver.switch_to_window(self.driver.window_handles[0])

        self.mail.verify()

    def __repr__(self):
        return "New bot object was created"


class TempMail():
    def __init__(self, driver):
        self.driver = driver

        self.driver.get("https://temp-mail.org")

    def get_mail(self):
        # --- Copy email ---
        self.driver.find_elements_by_class_name("click-to-copy")[1].click()
    
    def change(self):
        # --- Change email ---
        self.driver.find_element_by_id("click-to-delete").click()

    def verify(self):
        # --- Open mail and click on a verify link ---
        time.sleep(10)
        title = self.driver.find_elements_by_class_name("inboxSenderName")

        if "OLX" in title[1].text:
            title[1].click()

            self.driver.find_element_by_xpath("//*[@id='confirmLink']").click()

    def __repr__(self):
        return f"{TempMail.__name__}, was created"

        





def captcha(SITE_KEY, PAGE_URL):
    # Return JSON data from ruCaptcha
    response = ReCaptchaV2.ReCaptchaV2(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(site_key=SITE_KEY,
                                                                                   page_url=PAGE_URL)

    return response


if __name__ == "__main__":
    bot = OlxBot()

    time.sleep(5)
    bot.registrate()
    time.sleep(5)
    bot.verify_email()
    print(accounts)


