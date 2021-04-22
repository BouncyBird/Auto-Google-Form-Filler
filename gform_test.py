from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import configparser
import pyinputplus as pyip

config = configparser.ConfigParser()

url = input("Enter the URL of the form you want to fill\n")


def setconfig():
    config.read("settings.ini")
    curn = config.sections()

    while True:
        cname = input("What would you like to name this configuration?\n")
        if cname in curn:
            print("That name is already taken")
            continue
        break

    fn = input("What is your first name?\n")
    ln = input("What is your last name?\n")
    fullname = fn + " " + ln
    emailc = pyip.inputEmail("What is your email address?\n")
    autosubmit = pyip.inputYesNo(
        "Would like to have the form automatically submitted?\n"
    )
    config[cname] = {
        "First Name": fn,
        "Last Name": ln,
        "Fullname": fullname,
        "Email": emailc,
        "Auto Submit": autosubmit,
    }
    with open("settings.ini", "w") as configfile:
        config.write(configfile)


source = requests.get(url).text

soup = BeautifulSoup(source, "lxml")

browser = webdriver.Firefox(
    executable_path="C:\\Users\\eshan\\OneDrive\\Documents\\gd\\geckodriver.exe"
)
browser.get(url)

divs = soup.find_all(
    "div",
    class_="freebirdFormviewerComponentsQuestionBaseTitle",
)

for div in divs:
    if (
        "Email" in div.text
        or "email" in div.text
        or "eMail" in div.text
        or "EMAIL" in div.text
        or "e-mail" in div.text
        or "E-mail" in div.text
        or "E-MAIL" in div.text
    ):
        emid = div.get("id")
    elif (
        "First Name" in div.text
        or "first name" in div.text
        or "First name" in div.text
        or "FIRST NAME" in div.text
    ):
        fnid = div.get("id")

    elif (
        "Last Name" in div.text
        or "last name" in div.text
        or "Last name" in div.text
        or "LAST NAME" in div.text
    ):
        lnid = div.get("id")
    elif (
        "Full Name" in div.text
        or "full name" in div.text
        or "Full name" in div.text
        or "FULL NAME" in div.text
        or "NAME" in div.text
        or "name" in div.text
        or "Name" in div.text
    ):
        nid = div.get("id")

config.read("settings.ini")
if config.sections() == []:
    z = False
else:
    z = True

if z == False:
    print("You have not created a configuration file yet")
    setconfig()

print(
    f"The current configurations are {config.sections()}. Enter the configuration name you want. Or type 'new' to create a new configuration."
)
cdec = input()
if cdec.lower() == "new":
    setconfig()
    print(
        f"The current configurations are {config.sections()}. Enter the configuration name you want."
    )
    cdec = input()

email = config[cdec]["Email"]
full_name = config[cdec]["Fullname"]
first_name = config[cdec]["First Name"]
last_name = config[cdec]["Last Name"]
auto_submit = config[cdec]["Auto Submit"]


try:
    email_field = browser.find_element_by_css_selector("input[type='email']")
    email_field.send_keys(email)
except NoSuchElementException:
    email_field = browser.find_element_by_css_selector(
        f"input[aria-labelledby='{emid}']"
    )
    email_field.send_keys(email)
except NoSuchElementException:
    print("Error: Email field not found")
except:
    print("ERROR")

try:
    fname_field = browser.find_element_by_css_selector(
        f"input[aria-labelledby='{fnid}']"
    )
    fname_field.send_keys(first_name)
except NoSuchElementException:
    print("Error: First Name field not found")
except:
    print("ERROR")

try:
    lname_field = browser.find_element_by_css_selector(
        f"input[aria-labelledby='{lnid}']"
    )
    lname_field.send_keys(last_name)
except NoSuchElementException:
    print("Error: Last Name field not found")
except:
    print("ERROR")

try:
    name_field = browser.find_element_by_css_selector(f"input[aria-labelledby='{nid}']")
    name_field.send_keys(full_name)
except NoSuchElementException:
    print("Error: Full Name field not found")
except:
    pass

if auto_submit == "yes":
    browser.find_element_by_class_name("appsMaterialWizButtonPaperbuttonLabel").click()

time.sleep(5)

browser.quit()