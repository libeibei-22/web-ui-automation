# -*- coding: utf-8 -*-

from selenium import webdriver
import unittest
from PIL import Image
import pytesseract
import requests as req
from io import BytesIO
import time
# url="http://10.51.16.76/xlCloudSound/logout.htm"
# driver=webdriver.Chrome()
# driver.get(url)


class testcase(unittest.TestCase):
    def setUp(self) -> None:
        self.driver=webdriver.Chrome()
        testurl="http://10.51.16.76/xlCloudSound/logout.htm"
        self.driver.get(testurl)
        self.driver.maximize_window()
    def code_ocr(self):
        size = self.driver.find_element_by_id("code").size
        location = self.driver.find_element_by_id("code").location
        self.driver.save_screenshot("image.png")
        left = location["x"] * 2.25
        upper = location["y"] * 2.25
        right = size["width"] * 2.25 + location["x"] * 2.25
        lower = size["height"] * 2.25 + location["y"] * 2.25
        img = Image.open("image.png")
        im = img.crop((left, upper, right, lower))
        im.save('img.png')
        code = pytesseract.image_to_string(Image.open("img.png")).replace(" ","")
        print(code)
        return code
    def testcase01(self):
        self.driver.find_element_by_id("user").click()
        self.driver.find_element_by_id("user").send_keys("libeibei")
        self.driver.find_element_by_id("pwd").send_keys("123456")
        time.sleep(5)
        result=self.code_ocr()
        self.driver.find_element_by_xpath("//input[@id='chknumber']").send_keys(result)
        self.driver.find_element_by_id("suoding").click()
        time.sleep(3)
        try:
            while self.driver.find_element_by_class_name("error").is_displayed():
                codenew = self.code_ocr()
                self.driver.find_element_by_id("chknumber").send_keys(codenew)
                time.sleep(3)
                self.driver.find_element_by_id("suoding").click()
        except Exception as e:
            print('登录成功')
        time.sleep(5)
    def tearDown(self) -> None:
        pass



if __name__=="__main__":
    unittest.main()