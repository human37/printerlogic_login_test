import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class Login_Chrome(unittest.TestCase):

    DRIVER = webdriver.Chrome()

    def test_1_LoadLogin(self):
        self.DRIVER.get('https://ataylorprint.printercloud.com/admin/index.php')
        self.assertIn('https://ataylorprint.printercloud.com/admin/index.php', self.DRIVER.current_url, 'correct login webpage did not load')
        self.assertIn("PrinterLogic", self.DRIVER.title, 'correct title did not load')
        sleep(1)        #pausing so everything loads properly for next step
    
    def test_2_PrivacyPolicyLink(self):
        privacy_element = self.DRIVER.find_element_by_link_text('Privacy Policy')
        window_before = self.DRIVER.window_handles[0]
        privacy_element.click()
        window_after = self.DRIVER.window_handles[-1]
        self.DRIVER.switch_to.window(window_after)        #switches to the new tab we opened
        self.assertIn('https://www.printerlogic.com/privacy-policy/', self.DRIVER.current_url, 'correct privacy policy webpage did not load')
        sleep(1)        #pausing so everything loads properly for next step
        self.DRIVER.close()     #closes the new tab we opened 
        self.DRIVER.switch_to.window(window_before)     #switches to the previous tab

    def test_3_PasswordReset(self):
        passreset_element = self.DRIVER.find_element_by_link_text('Lost Password')
        passreset_element.click()
        self.assertIn('https://ataylorprint.printercloud.com/admin/password/reset/', self.DRIVER.current_url, 'correct password reset webpage did not load')
        sleep(1)        #pausing so everything loads properly for next step
        self.DRIVER.back()      #goes back to the login page

    def test_4_UsernamePrompt(self):
        username_element = self.DRIVER.find_element_by_id('relogin_user')
        username_element.send_keys('testusername')
        login_element = self.DRIVER.find_element_by_id('admin-login-btn')
        login_element.click()       #tries to login only entering a username
        login_text_error = self.DRIVER.find_element_by_id('logintext')
        self.assertIn('Please enter your username and password:', login_text_error.text, 'login error message with only a username did not display properly')
        self.DRIVER.refresh()       #refreshes the page
        sleep(1)        #pausing so everything loads properly for next step

    def test_5_PasswordPrompt(self):
        password_element = self.DRIVER.find_element_by_id('relogin_password')
        password_element.send_keys('testpassword')
        login_element = self.DRIVER.find_element_by_id('admin-login-btn')
        login_element.click()       #tries to login only entering a password
        login_text_error = self.DRIVER.find_element_by_id('logintext')
        self.assertIn('Please enter your username and password:', login_text_error.text, 'login error message with only a password did not display properly')
        self.DRIVER.refresh()       #refreshes the page
        sleep(1)        #pausing so everything loads properly for next step

    def test_6_LoginAttempt(self):
        username_element = self.DRIVER.find_element_by_id('relogin_user')
        password_element = self.DRIVER.find_element_by_id('relogin_password')
        #test an invalid username and password
        logins = open('passwords.txt')
        loginsdict = {}
        for line in logins:
            line = line.split()
            loginsdict[line[0]] = line[1]
        logins.close()
        username_element.send_keys(loginsdict['invaliduser:'])
        password_element.send_keys(loginsdict['invalidpass:'])
        sleep(1)
        login_element = self.DRIVER.find_element_by_id('admin-login-btn')
        login_element.click()       #tries to login with an invalid username and password
        self.assertIn('https://ataylorprint.printercloud.com/admin/index.php', self.DRIVER.current_url, 'let the user login with an invalid username and password')
        self.DRIVER.refresh()
        sleep(1)        #pausing so everything loads properly for next step

        #test a valid username and password
        username_element = self.DRIVER.find_element_by_id('relogin_user')
        password_element = self.DRIVER.find_element_by_id('relogin_password')
        username_element.send_keys(loginsdict['dummyuser:'])
        password_element.send_keys(loginsdict['dummypass:'])
        sleep(1)
        login_element = self.DRIVER.find_element_by_id('admin-login-btn')
        login_element.click()       #tries to login with a valid username and password
        sleep(1)        #pausing so everything loads properly for next step
        try:
            self.DRIVER.find_element_by_id('user-menu')
        except:
            raise Exception('login test failed with a valid username and password')
        self.DRIVER.close()

class Login_Safari(Login_Chrome):
    
    DRIVER = webdriver.Safari()


if __name__ == "__main__":
    #running all tests in google chrome and safari
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Login_Chrome)
    unittest.TextTestRunner().run(suite)
    
