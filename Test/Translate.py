__author__ = 'Kan!skA'

import unittest, xlrd, xlwt, time
from selenium import webdriver
from ddt import ddt, data, unpack

def get_data(Trans):
    rows = dict()
    book = xlrd.open_workbook(Trans)
    sheet = book.sheet_by_index(0)
    for row_idx in range(1, sheet.nrows):
        rows[row_idx] = list(sheet.row_values(row_idx, 0, sheet.ncols))
    return rows

@ddt
class NagpurTrans(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        time.sleep(2)
        cls.driver.maximize_window()
        cls.driver.get("http://www.techunfold.com/NagpurTrans/pages/translator.jsp")
        time.sleep(2)
        cls.driver.find_element_by_xpath(".//*[@id='username']").send_keys("babitag")
        cls.driver.find_element_by_xpath(".//*[@id='password']").send_keys("babitag123")
        cls.driver.find_element_by_xpath(".//*[@id='myform']/div[3]/input").click()
        cls.wb = xlwt.Workbook(encoding="utf-8")
        cls.ws = cls.wb.add_sheet("Sheet1", cell_overwrite_ok=True)
        time.sleep(2)

    @data(*get_data("Translate.xls").items())
    @unpack
    def test_Translation(self, input_row, input_data):
        self.driver.find_element_by_xpath(".//*[@id='sinputText']").send_keys(input_data)
        self.driver.find_element_by_xpath(".//*[@id='btnTranslate']").click()
        time.sleep(15)
        op = self.driver.find_element_by_xpath(".//*[@id='vboText']").get_attribute('value')
        self.ws.write(0, 0, 'Input')
        self.ws.write(0, 1, 'Output')
        self.ws.write(input_row, 0, input_data)
        self.ws.write(input_row, 1, op)
        time.sleep(2)
        self.driver.find_element_by_xpath(".//*[@id='btnReset']").click()

    @classmethod
    def tearDownClass(cls):
        cls.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[4]/a").click()
        time.sleep(2)
        cls.driver.quit()
        cls.wb.save("TransOutput.xls")
if __name__ == '__main__':
    unittest.main()