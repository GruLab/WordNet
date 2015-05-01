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
class GoogleTrans(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        time.sleep(2)
        cls.driver.maximize_window()
        cls.driver.get("https://translate.google.com/")
        time.sleep(2)
        cls.driver.find_element_by_xpath(".//*[@id='gt-sl-gms']").click()
        time.sleep(1)
        cls.driver.find_element_by_xpath(".//*[@id=':k']/div").click()
        time.sleep(1)
        cls.driver.find_element_by_xpath(".//*[@id='gt-tl-gms']/div[2]").click()
        time.sleep(1)
        cls.driver.find_element_by_xpath(".//*[@id=':46']/div").click()
        time.sleep(1)
        cls.wb = xlwt.Workbook(encoding="utf-8")
        cls.ws = cls.wb.add_sheet("Sheet1", cell_overwrite_ok=True)
        time.sleep(2)

    @data(*get_data("Translate.xls").items())
    @unpack
    def test_Translation(self, input_row, input_data):
        self.driver.find_element_by_xpath(".//*[@id='source']").send_keys(input_data)
        time.sleep(1)
        self.driver.find_element_by_xpath(".//*[@id='gt-submit']").click()
        time.sleep(5)
        op = self.driver.find_element_by_xpath(".//*[@id='result_box']").text
        self.ws.write(0, 0, 'Input')
        self.ws.write(0, 1, 'Output')
        self.ws.write(input_row, 0, input_data)
        self.ws.write(input_row, 1, op)
        time.sleep(1)
        self.driver.find_element_by_xpath(".//*[@id='source']").clear()

    @classmethod
    def tearDownClass(cls):
        time.sleep(5)
        cls.wb.save("TranslationOut.xls")
        time.sleep(5)
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main()