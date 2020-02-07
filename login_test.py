import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

DELAY_TIME = 5      #change delay seconds depending on the internet speed 

class Login_Chrome(unittest.TestCase):

    DRIVER = webdriver.Chrome()

    #tests if the login page loaded correctly, by comparing the current URL with the expected URL
    def test_1_LoadLogin(self):     
        self.DRIVER.get('https://ataylorprint.printercloud.com/admin/index.php')
        self.assertIn('https://ataylorprint.printercloud.com/admin/index.php', self.DRIVER.current_url, 'correct login webpage did not load')
        self.assertIn("PrinterLogic", self.DRIVER.title, 'correct title did not load')
        sleep(DELAY_TIME)        

    #tests if the privacy policy link takes you to the correct webpage
    def test_2_PrivacyPolicyLink(self):
        privacy_element = self.DRIVER.find_element_by_link_text('Privacy Policy')
        window_before = self.DRIVER.window_handles[0]
        privacy_element.click()
        sleep(DELAY_TIME)
        window_after = self.DRIVER.window_handles[-1]
        self.DRIVER.switch_to.window(window_after)       
        self.assertIn('https://www.printerlogic.com/privacy-policy/', self.DRIVER.current_url, 'correct privacy policy webpage did not load')
        sleep(DELAY_TIME)      
        self.DRIVER.close()    
        self.DRIVER.switch_to.window(window_before)   

    #tests if the password reset link takes you to the correct webpage
    def test_3_PasswordReset(self):
        passreset_element = self.DRIVER.find_element_by_link_text('Lost Password')
        passreset_element.click()
        self.assertIn('https://ataylorprint.printercloud.com/admin/password/reset/', self.DRIVER.current_url, 'correct password reset webpage did not load')
        sleep(DELAY_TIME)        
        self.DRIVER.back()    

    #tests if only entering the username prompt with a variety of input results in a login error
    def test_4_UsernamePrompt(self):
        #tries only 'testusername' in the username field
        username_element = self.DRIVER.find_element_by_id('relogin_user')
        username_element.send_keys('testusername')
        login_element = self.DRIVER.find_element_by_id('admin-login-btn')
        login_element.click()       
        login_text_error = self.DRIVER.find_element_by_id('logintext')
        self.assertIn('Please enter your username and password:', login_text_error.text, 'login error message with only username:testusername did not display properly')
        self.DRIVER.refresh()     
        sleep(DELAY_TIME)       

        #tries only empty space in the username field
        username_element = self.DRIVER.find_element_by_id('relogin_user')
        username_element.send_keys('        ')
        login_element = self.DRIVER.find_element_by_id('admin-login-btn')
        login_element.click()      
        login_text_error = self.DRIVER.find_element_by_id('logintext')
        self.assertIn('Please enter your username and password:', login_text_error.text, 'login error message with only empty space in the username field did not display properly')
        self.DRIVER.refresh()      
        sleep(DELAY_TIME)  

        #tries 64 character long string in the username field
        username_element = self.DRIVER.find_element_by_id('relogin_user')
        username_element.send_keys('asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;')
        login_element = self.DRIVER.find_element_by_id('admin-login-btn')
        login_element.click()      
        login_text_error = self.DRIVER.find_element_by_id('logintext')
        self.assertIn('Please enter your username and password:', login_text_error.text, 'login error message with a long 64 character string in the username field did not display properly')
        self.DRIVER.refresh()      
        sleep(DELAY_TIME)  

    #tests if only entering the password prompt with a variety of input results in a login error
    def test_5_PasswordPrompt(self):
        #tries only 'testpassword' in the password field
        password_element = self.DRIVER.find_element_by_id('relogin_password')
        password_element.send_keys('testpassword')
        login_element = self.DRIVER.find_element_by_id('admin-login-btn')
        login_element.click()       
        login_text_error = self.DRIVER.find_element_by_id('logintext')
        self.assertIn('Please enter your username and password:', login_text_error.text, 'login error message with only password:testpassword did not display properly')
        self.DRIVER.refresh()       
        sleep(DELAY_TIME)

        #tries only empty space in the password field
        password_element = self.DRIVER.find_element_by_id('relogin_password')
        password_element.send_keys('         ')
        login_element = self.DRIVER.find_element_by_id('admin-login-btn')
        login_element.click()       
        login_text_error = self.DRIVER.find_element_by_id('logintext')
        self.assertIn('Please enter your username and password:', login_text_error.text, 'login error message with only empty space in the password field did not display properly')
        self.DRIVER.refresh()       
        sleep(DELAY_TIME)

        #tries 64 character long string in the password field
        password_element = self.DRIVER.find_element_by_id('relogin_password')
        password_element.send_keys('asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;')
        login_element = self.DRIVER.find_element_by_id('admin-login-btn')
        login_element.click()       
        login_text_error = self.DRIVER.find_element_by_id('logintext')
        self.assertIn('Please enter your username and password:', login_text_error.text, 'login error message with a long 64 character string in password field did not display properly')
        self.DRIVER.refresh()       
        sleep(DELAY_TIME)      

    #tries logging in with a variety of wrong logins, and also one correct login
    def test_6_LoginAttempt(self):
        logins = open('passwords.txt')
        loginsdict = {}
        for line in logins:
            line = line.split()
            loginsdict[line[0]] = line[1]
        logins.close()

        #tries an invalid username and password
        username_element = self.DRIVER.find_element_by_id('relogin_user')
        password_element = self.DRIVER.find_element_by_id('relogin_password')
        username_element.send_keys(loginsdict['invaliduser:'])
        password_element.send_keys(loginsdict['invalidpass:'])
        login_element = self.DRIVER.find_element_by_id('admin-login-btn')
        login_element.click()       
        self.assertIn('https://ataylorprint.printercloud.com/admin/index.php', self.DRIVER.current_url, 'let the user login with an invalid username and password')
        self.DRIVER.refresh()
        sleep(DELAY_TIME)  

        #tries empty space as the username and password
        username_element = self.DRIVER.find_element_by_id('relogin_user')
        password_element = self.DRIVER.find_element_by_id('relogin_password')
        username_element.send_keys('        ')
        password_element.send_keys('        ')
        login_element = self.DRIVER.find_element_by_id('admin-login-btn')
        login_element.click()       
        self.assertIn('https://ataylorprint.printercloud.com/admin/index.php', self.DRIVER.current_url, 'let the user login with empty space as the username and password')
        self.DRIVER.refresh()
        sleep(DELAY_TIME)

        #tries a long 64 character string as the username and password
        username_element = self.DRIVER.find_element_by_id('relogin_user')
        password_element = self.DRIVER.find_element_by_id('relogin_password')
        username_element.send_keys('asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;')
        password_element.send_keys('asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;')
        login_element = self.DRIVER.find_element_by_id('admin-login-btn')
        login_element.click()       
        self.assertIn('https://ataylorprint.printercloud.com/admin/index.php', self.DRIVER.current_url, 'let the user login with an invalid long 64 character string as the username and password')
        self.DRIVER.refresh()
        sleep(DELAY_TIME)

        #tries a valid username and password
        username_element = self.DRIVER.find_element_by_id('relogin_user')
        password_element = self.DRIVER.find_element_by_id('relogin_password')
        username_element.send_keys(loginsdict['dummyuser:'])
        password_element.send_keys(loginsdict['dummypass:'])
        login_element = self.DRIVER.find_element_by_id('admin-login-btn')
        login_element.click()       
        sleep(DELAY_TIME)        
        try:
            self.DRIVER.find_element_by_id('user-menu')
        except:
            raise Exception('login test failed with a valid username and password')

    #closes the browser after the tests have run
    def test_7_tearDown(self):
        self.DRIVER.close()

#inherits all tests from the Login_Chrome class, only change is the web browser used
class Login_Firefox(Login_Chrome, unittest.TestCase):
    
    DRIVER = webdriver.Firefox()


if __name__ == "__main__":
    print()
    print('Running all tests in google chrome:')
    chrome_test = unittest.defaultTestLoader.loadTestsFromTestCase(Login_Chrome)
    unittest.TextTestRunner().run(chrome_test)

    print()
    print('Running all tests in firefox:')
    firefox_test = unittest.defaultTestLoader.loadTestsFromTestCase(Login_Firefox)
    unittest.TextTestRunner().run(firefox_test)
