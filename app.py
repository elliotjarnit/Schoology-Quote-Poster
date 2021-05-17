import requests
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1
from datetime import datetime, timedelta
from threading import Timer

# This code is very unorganized and could probally have been done better but I did this in a hour during school for a tech project.
# It will post a quote everyday to a updates section of any group/course you want on schoology. It is very simple.

# VARIABLES

# To get consumer and variable go to whatever your school's schoology domain is /api. 
# Example: https://harvard.schoology.com/api

ApiConsumerKey = ''
ApiSecretKey = ''

# Post type can be: group, course

PostType = 'course'

# This is the id of the page you want to post to. To get this go to the page and copy the number part of the url
# Example: https://schoology.com/course/3045989774/updates <- The ID would be 3045989774

PostID = ''

# This is the time that it posts to schoology every day. Use the seperate variables to declare time.
# Example: 2:30 P.M. would be Hours: 14, Minutes: 30

TimeHour = 6
TimeMinutes = 30



print("Starting Quote Machine")

TimerFinished = True

oauth = OAuth1(ApiConsumerKey, client_secret=ApiSecretKey)

if PostType == 'course':
  PostTypeFixed = 'sections'
elif PostType == 'group':
  PostTypeFixed = 'groups'
else:
  print("Invalid Post Type!")
  exit()

def postQuote():

  quoteNumFileRead = open("quoteNum.txt", "r")
  quoteNumber = int(quoteNumFileRead.read())

  print("\nPicking Quote...\n")
  quote = requests.get("https://zenquotes.io/api/random")
  Fixed = quote.text.replace('[ {\"q\":\"', '').split('\"', 1)[0]
  print("Quote found: " + Fixed)

  print("\nPosting quote to Schoology...")

  quoteFixed = "Quote of the day #" + str(quoteNumber) + ": \\n\\n" + Fixed

  postJson = {"body": quoteFixed}

  r = requests.post(url="https://api.schoology.com/v1/groups/4541056059/updates/", auth=oauth, headers={"Accept": "application/json", "Content-Type": "application/json"}, json=postJson)

  if r.status_code == 201:
    print("\nSuccessfully posted quote, restarting timer")

    quoteNumFileWrite = open("quoteNum.txt", "w")
    quoteNumFileWrite.write(str(quoteNumber + 1))
    quoteNumFileWrite.close()
    TimerFinished = True
    return 0
  else:
    print("Error with posting quote\n\nResponse: " + r.text + "\n\nStatus Code: " + str(r.status_code))

dateNow=datetime.today()
dateFixed=dateNow.replace(day=dateNow.day+1, hour=TimeHour, minute=TimeMinutes, second=0, microsecond=0) + timedelta(days=1)
timeLeft=dateFixed-dateNow

postQuoteTime=timeLeft.seconds+1

print("\nCurrent time: " + str(dateNow))
print("Seconds left: " + str(postQuoteTime))


quotePostTimer = Timer(postQuoteTime, postQuote)
while True:
  if TimerFinished:
    TimerFinished = False
    quotePostTimer.start()