import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



class Login(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def testLoad(self):
        self.driver.get('https://ataylorprint.printercloud.com/admin/index.php')
        self.assertIn('https://ataylorprint.printercloud.com/admin/index.php', self.driver.current_url, 'correct webpage did not load')
        self.assertIn("PrinterLogic", self.driver.title, 'correct title did not load')

    def testUsernamePromptLoad(self):
        print(self.driver.find_element_by_class_name('login-inputs'))
    
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Login)
    unittest.TextTestRunner().run(suite)