#coding=utf-8
from appium import webdriver
import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = 'MI 5'
desired_caps['appPackage'] = 'com.miui.calculator'
desired_caps['appActivity'] = '.cal.CalculatorActivity'
desired_caps['automationName'] = 'UiAutomator1'
print("starting")
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.find_element_by_id("com.miui.calculator:id/btn_5").click()
driver.find_element_by_id("com.miui.calculator:id/btn_mul").click()
driver.find_element_by_id("com.miui.calculator:id/btn_6").click()
driver.find_element_by_id("com.miui.calculator:id/btn_7").click()
driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.ImageView').click()
print("end")
time.sleep(5)
driver.quit()