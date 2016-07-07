#!/usr/bin/python
#-*- coding: utf-8 -*-

# written by n-taka ( https://n-taka.info )
# PhantomJS is required
from selenium import webdriver
import onamaeSecret

# address for getting my global IP
IPservice = u"http://inet-ip.info/ip"

def getMyGlobalIP(driver):
    # get global IP address of myself
    print "Find my global IP address ...",
    try:
        driver.get(IPservice)
        globalIP = driver.find_element_by_tag_name("pre").text
    except: # this exception is mainly timed out exception
        # http fails
        driver.quit()
        print "fails!! Abort updating DNS record."
        exit(1)
    print str(globalIP)
    return str(globalIP)


def authOnamae(driver):
    print "Authentication ...",
    try:
        # login dialog
        driver.get(u"https://cp.rentalserver.jp/Login.aspx")
        driver.find_element_by_class_name(u"style01").find_element_by_xpath(u"./tbody/tr[1]/td/input").send_keys(onamaeSecret.userId)
        driver.find_element_by_class_name(u"style01").find_element_by_xpath(u"./tbody/tr[2]/td/input").send_keys(onamaeSecret.passWord)
        driver.find_element_by_class_name(u"submit-button").find_element_by_xpath(u"./input").click()
    except:
        driver.quit()
        print "fails!! Abort updating DNS record."
        exit(1)
    print "Done!"


def moveToRecordSetting(driver):
    print "Move to the A record setting ...",
    try:
        driver.find_element_by_id(u"services").find_element_by_xpath(u"./div/div/ul/li[2]/a").click()
        driver.find_element_by_class_name(u"colorfulline").find_element_by_xpath(u"./td[3]/input").click()
        driver.find_element_by_class_name(u"colorfulline").find_element_by_xpath(u"./td[7]/input").click()
    except Exception as e: # this exception is happen when onamae.com changes the structure of html
        print e
        driver.quit()
        print "fails!! Abort updating DNS record."
        exit(1)
    print "Done!"


def updateARecord(driver, globalIPAddr):
    print "Input to the form ...",
    try:
        # confirm that "Use another server"
        driver.find_element_by_name(u"aspnetForm").find_element_by_xpath(u"./div[6]/input").click()

        # input actual global IP address
        driver.find_element_by_name(u"aspnetForm").find_element_by_xpath(u"./table[2]/tbody/tr[2]/td/input[1]").send_keys(globalIPAddr.split(u".")[0])
        driver.find_element_by_name(u"aspnetForm").find_element_by_xpath(u"./table[2]/tbody/tr[2]/td/input[2]").send_keys(globalIPAddr.split(u".")[1])
        driver.find_element_by_name(u"aspnetForm").find_element_by_xpath(u"./table[2]/tbody/tr[2]/td/input[3]").send_keys(globalIPAddr.split(u".")[2])
        driver.find_element_by_name(u"aspnetForm").find_element_by_xpath(u"./table[2]/tbody/tr[2]/td/input[4]").send_keys(globalIPAddr.split(u".")[3])

        # submit
        driver.find_element_by_class_name(u"submit-button").find_element_by_xpath(u"./input[2]").click()
        # confirm
        driver.find_element_by_class_name(u"submit-button").find_element_by_xpath(u"./input[2]").click()
    except:
        driver.quit()
        print "fails!! Abort updating DNS record."
        exit(1)
    print "Done!"


if __name__ == "__main__":
    print "Hello! This is Unofficial onamae DNS record update script."
    driver = webdriver.PhantomJS()
    driver.implicitly_wait(180)
    driver.set_page_load_timeout(180)

    globalIP = getMyGlobalIP(driver)

    authOnamae(driver)
    moveToRecordSetting(driver)
    updateARecord(driver, globalIP)

    print "Update sccusess!!"
    print "Please check your ip adress : nslookup <your domain> <your DNS server>"
    driver.quit()
    exit(0)
