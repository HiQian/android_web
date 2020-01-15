#coding=utf-8
from appium import webdriver
import time
import logging

from selenium.common.exceptions import NoSuchElementException
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def get_app_driver(desired_caps):
    driver = None
    try:
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        logger.info("driver get success")
        # 等待数据加载,可能会存在广告
        time.sleep(10)
    except BaseException as err:
        logger.error("Android driver failed get")
        logger.error(err.args)
        if driver is not None:
            driver.quit()
    return driver

def  app_check_info(driver, check_id):
    try:
        # 头条id 'com.ss.android.article.news:id/a5e'
        check_info = driver.find_element_by_id(check_id)
        check_info.click()
        # 更新内容
        driver.swipe(900, 700, 900, 1300)
        time.sleep(5)
        logger.info("User is not  logged in ")
    except NoSuchElementException as err:
        logger.info("user have been logged in")

def app_swipe_for_info(driver, count,  update_id, step=1200,):
    for i in range(count):
        begin_posi = (500, 1700)
        end_posi = (begin_posi[0], begin_posi[1]-step)
        try:
            driver.swipe(begin_posi[0], begin_posi[1], end_posi[0], end_posi[1])
        except:
            logger.error('第{}次滑屏错误'.format(i))
        # print(i)
        time.sleep(0.5)
        # 判断头条是否需要更新
        try:
            # 'com.ss.android.article.news:id/dju' app更新id
            updata_info = driver.find_element_by_id(update_id)
            logger.info("update info is shown")
            # 不需要更新
            updata_info.click()
        except NoSuchElementException as err:
            pass

def role_type_bar(driver, direction, step=-200, start_position=(500, 250)):
    if direction == 'right':
        step = abs(step)
    elif direction =='left':
        step = step
    else :
        step=0
    try:
        driver.swipe(start_position[0], start_position[1], start_position[0] + step, start_position[1])
    except:
        logger.error('swipe failed')
    pass


if __name__ == '__main__':
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '6.0.1'
    desired_caps['deviceName'] = '10.129.33.79:8020'
    desired_caps['appPackage'] = 'com.ss.android.article.news'
    desired_caps['appActivity'] = '.activity.MainActivity'
    desired_caps['automationName'] = 'UiAutomator1'
    desired_caps['noReset'] = True
    driver = get_app_driver(desired_caps)
    check_id = 'com.ss.android.article.news:id/a5e'
    app_check_info(driver, check_id)
    swipe_count = 10
    update_id = 'com.ss.android.article.news:id/dju'
    info_topics = ['推荐', '热点', '娱乐', '音乐', '体育', '国际', '财经', '影视', '情感', '历史', '美食', '懂车帝', '科技']
    # info_topics = ['推荐', '热点']
    for info_topic in info_topics:
        max_swipe = 20
        type_swipe_count = 0
        while True:
            try:
                element = driver.find_element_by_accessibility_id(info_topic)
                element_posi = element.location_in_view
                # 超过700 不在屏幕上
                if element_posi.get('x') > 700:
                    raise Exception
                else:
                    element.click()
                    break
            except:
                type_swipe_count  = type_swipe_count + 1
                logger.info(" An element could not be found in the page using the given search info_topic:{}".format(info_topic))
                try:
                    # 'com.ss.android.article.news:id/dju' app更新id
                    updata_info = driver.find_element_by_id('com.ss.android.article.news:id/dju')
                    logger.info("update info is shown")
                    # 不需要更新
                    updata_info.click()
                except NoSuchElementException:
                    pass
                if type_swipe_count < max_swipe:
                    role_type_bar(driver, "left", step=-150)
                else :
                    break
        if type_swipe_count < max_swipe:
            # 更新内容
            driver.swipe(900, 700, 900, 1300)
            time.sleep(5)
            # 滑动获取信息
            app_swipe_for_info(driver, swipe_count, update_id)
        pass
    driver.quit()