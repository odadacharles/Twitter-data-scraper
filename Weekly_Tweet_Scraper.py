#import the relevant libraries
import csv
from getpass import getpass
from time import sleep
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.action_chains import ActionChains

#Create an instance of the web driver
options = EdgeOptions()
options.use_chromium = True
driver=Edge(options=options)
#Open twitter's login page
driver.get('https://www.twitter.com/login')
#Allow login page time to load. Enter the username and press enter
sleep(10)
username = driver.find_element_by_xpath('//input[@name="username"]')
username.send_keys('candyphysics@yahoo.com')
username.send_keys(Keys.RETURN)
#Allow page time to load. Input twitter password using getpass
sleep(5)
my_password = getpass()
#Enter the password in twitter
password = driver.find_element_by_xpath('//input[@name="password"]')
password.send_keys(my_password)
password.send_keys(Keys.RETURN)

#Allow page time to load. 
sleep(5)
#Set the time period covered by the search (Past one week)
#start_date = datetime.datetime.now()
#Load the list of cryptocurrencies to scrape data about
file=open('crypto-currency-list.csv')
csvreader = csv.reader(file)
header = []
rows=[]
header = next(csvreader)

end_date = datetime.today() - timedelta(days=7)
year = str(end_date.year)
month = str(end_date.month)
day = str(end_date.day)
stop_date = year+"-"+month+"-"+day

tweet_time = ""

for row in rows:
    while tweet_time!=stop_date:
        search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
        actionChains = ActionChains(driver)
        actionChains.double_click(search_input).perform()
        actionChains.double_click(search_input).perform()
        search_input.send_keys(row)
        search_input.send_keys(Keys.RETURN)
        sleep(3)

        