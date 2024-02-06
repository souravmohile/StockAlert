import requests
import datetime as dt
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = "3IS0Z9CQQ8GMKPOT"
NEWS_API_KEY = "cecef1e1e6e845459054bd107c0b4075"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# TODO 1. - Get yesterday's closing stock price.
# Hint: You can perform list comprehensions on Python dictionaries.
# e.g. [new_value for (key, value) in dictionary.items()]

# GETTING ALL DATA FROM API
stock_response = requests.get(STOCK_ENDPOINT + f"?function=TIME_SERIES_DAILY&symbol={STOCK_NAME}&apikey={STOCK_API_KEY}")
data = stock_response.json()

# GETTING TODAY'S DATE
now = dt.datetime.now()
day = now.day
month = now.month
year = now.year

# FOR MONTHS AND DAYS THAT NEED 0 BEFORE ANOTHER NUMBER
if month < 10:
    month = f"0{month}"

yesterday = day - 1
if yesterday < 10:
    yesterday = f"0{yesterday}"

day_before_yesterday = day - 20
if day_before_yesterday < 10:
    day_before_yesterday = f"0{day_before_yesterday}"

# GETTING YESTERDAYS DATE
yesterdays_date = data["Time Series (Daily)"][f"{year}-{month}-{yesterday}"]

# GETTING YESTERDAYS CLOSING
yesterdays_closing = yesterdays_date["4. close"]

# TODO 2. - Get the day before yesterday's closing stock price
# GETTING DAY BEFORE YESTERDAYS DATE
day_before_yesterdays_date = data["Time Series (Daily)"][f"{year}-{month}-{day_before_yesterday}"]

# GETTING DAY BEFORE YESTERDAYS CLOSING
day_before_yesterdays_closing = day_before_yesterdays_date["4. close"]

# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
# Hint: https://www.w3schools.com/python/ref_func_abs.asp
positive_difference = round(float(yesterdays_closing) - float(day_before_yesterdays_closing), 3)

# TODO 4. - Work out the percentage difference in price b/w the closing prices.
percentage_change = abs(round((float(positive_difference) / float(day_before_yesterdays_closing)) * 100, 2))
display_percentage = f"{percentage_change}%"

# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if percentage_change > 5:
    print("get news")

# STEP 2: https://newsapi.org/
# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

news_response = requests.get(NEWS_ENDPOINT + f"?q=tesla&apiKey={NEWS_API_KEY}")
data = news_response.json()
article_1 = data["articles"][0]["title"]
article_2 = data["articles"][1]["title"]
article_3 = data["articles"][2]["title"]

# TODO 7. - Use Python slice operator to create a list that contains the first 3 articles.
# Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
articles = [article_1, article_2, article_3]

# STEP 3: Use twilio.com/docs/sms/quickstart/python
#to send a separate message with each article's title and description to your phone number.

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

#TODO 9. - Send each article as a separate message via Twilio.

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message1 = client.messages \
                .create(
                     body=f"TSLA: {display_percentage}\nNews: {article_1}",
                     from_="+15075961455",
                     to="+919869280544"
                )

message2 = client.messages \
                .create(
                     body=f"TSLA: {display_percentage}\nNews: {article_2}",
                     from_="+15075961455",
                     to="+919869280544"
                )

message3 = client.messages \
                .create(
                     body=f"TSLA: {display_percentage}\nNews: {article_3}",
                     from_="+15075961455",
                     to="+919869280544"
                )



#Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the
coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file 
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
"""
