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