# __author__ = 'ɐʞƨ!uɐʞ'

import unittest
import csv
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select


class ExtractData(unittest.TestCase):
    def setUp(self):
        # Creating the Firefox Profile
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get('http://tdil-dc.in/indowordnet/index.jsp')
        self.driver.implicitly_wait(5)

    def test_WordNet(self):
        # Reading the Input File line by line
        ip = open('input.csv', encoding='utf8')
        for i in csv.reader(ip):
            # Choosing Tamil from 'Select Language' option
            Select(self.driver.find_element_by_xpath(".//*[@id='lang']")).select_by_value('14')
            # Inputting data into 'Search Word' field
            self.driver.find_element_by_xpath(".//*[@id='queryword']").send_keys(i)
            # Clicking the 'Search' button
            self.driver.find_element_by_xpath(".//*[@id='search_button']").click()
            # Words having output
            if not self.driver.find_element_by_xpath("html/body/div[3]").text:
                # Creating and Appending data into the Output File
                op = open(str(i).strip("['']") + '.txt', 'a', encoding='utf8')
                op.write('Input: ' + str(i).strip("['']") + '\n\n')
                time.sleep(2)
                # Extracting data from Home Page
                op.write(self.driver.find_element_by_class_name("abc").text + '\n\n')
                # Extracting data from 'Relations' option
                path1 = "html/body/div[4]/table/tbody/tr/td[1]/div/div[2]/div[2]/div["
                path2 = "]/table/tbody/tr/td[2]"
                j = 1
                while j < 11:
                    self.driver.find_element_by_xpath(path1 + str(j) + path2).click()
                    time.sleep(2)
                    op.write(self.driver.find_element_by_class_name("middle_area").text + '\n\n')
                    time.sleep(2)
                    j += 1
                # Closing the Output File
                op.close()
            # Words having no output
            else:
                # Creating and Appending data into the Output File
                op = open(str(i).strip("['']") + '.txt', 'a', encoding='utf8')
                op.write('Word ' + str(i).strip("['']") + ' not found in wordnet. ')
                # Closing the Output File
                op.close()

        # Closing the Input File
        ip.close()

    def tearDown(self):
        # Closing the Firefox Profile
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
