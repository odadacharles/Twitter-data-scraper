#import the relevant libraries
import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.action_chains import ActionChains
#import get_tweet_data #import the function that extracts data from a tweet



#Create an instance of the web driver
options = EdgeOptions()
options.use_chromium = True
driver=Edge(options=options)
#Open twitter's login page
driver.get('https://www.twitter.com/login')
#Enter the username and press enter
sleep(10)
username = driver.find_element_by_xpath('//input[@name="username"]')
username.send_keys('candyphysics@yahoo.com')
username.send_keys(Keys.RETURN)
sleep(5)
#input twitter password using getpass
my_password = getpass()
#Enter the password in twitter
password = driver.find_element_by_xpath('//input[@name="password"]')
password.send_keys(my_password)
password.send_keys(Keys.RETURN)
sleep(5)
#Find the search function and doubleclick twice (4 times total). This will select all the text that may already be there
#Input the word(s) to be searched using send_keys and press enter
search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
actionChains = ActionChains(driver)
actionChains.double_click(search_input).perform()
actionChains.double_click(search_input).perform()
search_input.send_keys("$Trac")
search_input.send_keys(Keys.RETURN)
sleep(3)
#Click the 'top' or 'Latest' buttons depending on the order of results you'd like
driver.find_element_by_link_text('Latest').click()

#Define function for extracting tweet data
def get_tweet_data(card):
    "This is a function that extracts the data from a single tweet"
    #Find the the username using xpath and return the text associated with it
    username = card.find_element_by_xpath('.//span').text
    #Get the date when the tweet was posted
    user_handle = card.find_element_by_xpath('.//span[contains(text(),"@")]').text
    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchElementException:
        return
    #Tweet text if dealing with original tweet
    replying_to = card.find_element_by_xpath('.//div/div/div/div[2]/div[2]/div[2]/div[1]/div').text
    tweet_txt = card.find_element_by_xpath('.//div/div/div/div[2]/div[2]/div[2]/div[2]').text
    full_tweet = replying_to+tweet_txt
    #Replies, RTs, and Likes
    replies = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweets = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    likes = card.find_element_by_xpath('.//div[@data-testid="like"]').text
    tweet_data = (username, user_handle, postdate, full_tweet, replies, retweets, likes)
    return tweet_data

#Save all tweets that have been loaded to the page

tweet_data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")

scrolling = True

while scrolling:
    cards = driver.find_elements_by_xpath('//article[@data-testid="tweet"]')
    for card in cards[-15:]:
        tweet = get_tweet_data(card)
        if tweet:
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                tweet_data.append(tweet)
    
    scroll_attempt = 0
    while True:
        #check scroll position
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')#scroll down the full page
        sleep(3) #pause the program for three seconds to allow time to load
        current_position = driver.execute_script("return window.pageYOffset;")
        if last_position == current_position:
            scroll_attempt +=1

            #end of scroll region
            if scroll_attempt>=3:
                scrolling = False
                break
            else:
                sleep(2)
        else:
            last_position = current_position
            break