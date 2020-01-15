#coding=utf-8
from appium import webdriver
import time

from selenium.common.exceptions import NoSuchElementException

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '10.129.33.79:8020'
desired_caps['appPackage'] = 'com.ss.android.article.news'
desired_caps['appActivity'] = '.activity.MainActivity'
desired_caps['automationName'] = 'UiAutomator1'
desired_caps['noReset'] = True
print("starting")
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# 等待数据加载,可能会存在广告
time.sleep(10)
# 隐私访问权限
# 是：android:id/button1
# /hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button[2]
# 个人信息保护指引
# 我知道了：com.ss.android.article.news: id / a5e
try:
    check_info = driver.find_element_by_id('com.ss.android.article.news:id/a5e')
    check_info.click()
    # 跟新内容
    driver.swipe(900, 700, 900, 1300)
    time.sleep(5)
except NoSuchElementException as err:
    print("不存在个人信息保护指引")
for i in range(20):
    try:
        driver.swipe(900, 1700, 900, 500)
    except:
        print('第{}次滑屏错误'.format(i))
    # print(i)
    time.sleep(0.5)
    # 判断头条是否需要更新
    try:
        updata_info = driver.find_element_by_id('com.ss.android.article.news:id/dju')
        print("出现更新信息")
        # 不需要更新
        updata_info.click()
    except NoSuchElementException as err:
        pass
print("end")
driver.quit()