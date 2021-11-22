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
name_header = []
name_rows=[]
name_header = next(csvreader)
for item in csvreader:
    name_rows.append(item)

print(name_rows)

end_date = datetime.today() - timedelta(days=7)
year = str(end_date.year)
month = str(end_date.month)
day = str(end_date.day)
stop_date = year+"-"+month+"-"+day

tweet_time = ""

for row in name_rows:
    while tweet_time!=stop_date:
        search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
        actionChains = ActionChains(driver)
        actionChains.double_click(search_input).perform()
        actionChains.double_click(search_input).perform()
        search_input.send_keys(row)
        search_input.send_keys(Keys.RETURN)
        sleep(3)

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
            tweet_data = [username, user_handle, postdate, replies, retweets, likes, full_tweet]
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
                        with open('crypto_tweets_Nov(16-22).csv', 'a', newline='') as f:
                            header = ['Username', 'Handle', 'Timestamp', 'Comments', 'Likes', 'Retweets','Text']
                            writer = csv.writer(f)
                            print(tweet)
                            writer.writerow(header)
                            writer.writerows(tweet)

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

        