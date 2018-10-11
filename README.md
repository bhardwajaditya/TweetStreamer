# Tweet Streamer

##### Uses "Twitter Streaming API" to get the target tweets(real-time) for a recent high traffic event(s), and storing them in MongoDB. Later, tweets can be filtered using REST API
#


### API Provides :-

* Endpoints to start streaming.
* Time limit based streaming.
* Ordering of tweets based on particular fields.
* Searching of words/text in tweets.
* Searching of tweets based on username.
* Filtering of data in integer fields based on min/max value provided
* Filtering of data in string fields based on ending or starting word or a word that the field should contain.
* Filtering of data based on starting and ending dates
* CSV export support

### Setup and Installation :-

1. Clone the git repository.
2. Make sure python3.5+ is installed.
3. Install the requirements listed in requirements.txt

### Twitter Authentication :-

1. Open file **settings.py** 
2. Replace your-keys* , your-tokens* with your authentication keys and access tokens.

### Creating Database and establishing the server
Open the terminal and enter:- 

```emacs
$ cd TweetStreamer
$ mkdir data
$ echo 'mongod --bind_ip=$IP --dbpath=data --nojournal --rest "$@"' > mongod
$ chmod a+x mongod
```
To start the Mongo Server :-
```emacs
$ ./mongod
```

### Running the REST Server
```emacs
$ cd TweetStreamer
$ python app.py
```
## Schema

**Fields**: In MongoDB, every document ```tweet```  will contain following fields - 

* _```tweet_text```_: string, 

* _```screen_name```_ : string,

* _```user_name```_: string, 

* _```location```_: string, 

* _```source_device```_: string, 

* _```is_retweeted```_: boolean, 

* _```retweet_count```_: integer,

* _```country```_: string, 

* _```country_code```_: string, 

* _```reply_count```_: integer, 

* _```favorite_count```_: integer, 

* _```created_at```_: datetime, 

* _```timestamp_ms```_: long, 

* _```lang```_: string, 

* _```hashtags```_: array,

* _```quote_count```_: integer 

### API Endpoints :-

### 1. To start/trigger streaming :-


##### GET /stream?keywords=______________

* here replace ____ by keywords you want to search seperated by a comma

##### GET /stream?keywords=________  &time_limit=____________

* here replace {any-keyword} by keywords you want to search,
* {time-limit} by an integer value in seconds stating the time limit for which you want to stream the tweets.
* default time limit is 100 seconds

*Response*

```javascript
{
  "status": "success",
  "message": "Started streaming tweets with keywords [u'cricket', u'football', u'Rafale']"
}
```
### 2. To fetch the tweets :-

##### GET /tweets/?limit=_____ & page=______

* to return a limited number of tweets :- replace limit=______ with an integer value
* to return based on page number with 50 tweets per page :- replace page=____ with an integer value

### 3. To fetch the users :-

##### GET /users/name=____________

* here replace ______ by username to search for a particular user 

### 4. To search in tweets :-

##### GET /tweets/?search=______

* here replace ______ by the appropriate words you want to search for in tweet text

### 5. To sort/order the tweets with respect to a particular field :-

##### GET /tweets/?ordering=________

* for ascending :- replace ______ by field-name and 
* for descending :- replace _______ by -field-name

### 6. To search based on max/min in integer columns :-

##### GET /tweets/string_search?column_name=________ & start=______ & end=______ 

* here enter the integer column name in which you want to search in the space column_name=______
* replace the space in end variable with the end word you want to search in the given column
* replace the space in start variable with the starting word you want to search in the given column
* enter both in case you want to give both constraints
 
##### GET /tweets/string_search?column_name=________ &contain=_______

* here enter the integer column name in which you want to search in the space column_name=______
* replace the contain variable with the word you want the resulting column entries must contain

##### GET /tweets/string_search?column_name=________ & match=_____


* here enter the integer column name in which you want to search in the space column_name=______
* replace the match variable with the word to list down the entries with that word in the given column

 

#### 7. To search based on max/min in integer columns :-

##### GET /tweets/integer_search?column_name=________ & max=______ & min=______

* here enter the integer column name in which you want to search in the space column_name=______
* replace the space in max variable with the maximum value for the column name
* replace the space in min variable with minimum value for the column name
* enter both in case you want to give both constraints

#### 8. To filter based on Date :-

##### GET /tweets/date?startDate=________ & endDate=_______


* replace the space in startDate variable with the starting date from which you want the tweets to be displayed
* replace the space in endDate variable with the ending date from which you want the tweets to be displayed
* enter both in case you want to give both constraints

### 9. To export tweets data as CSV:-

##### GET /csv/


### Technologies used :-

1. Python 3.5
2. Flask Framework
3. MongoDB
4. Tweepy (twitter streaming library in python)
### Sample Response
```javascript
[
    {
        "hashtags": [],
        "user_name": "Zesty StL Blues",
        "country": "",
        "is_retweeted": false,
        "location": "St Louis, MO",
        "tweet_text": "Blues defenseman Dunn upset by apparent benching https://t.co/1gYP1FafRDhttps://t.co/FDWEZYTmUi",
        "reply_count": 0,
        "created_at": "Thu Oct 11 10:04:58 +0000 2018",
        "source_device": "<a href=\"http://zestynews.com\" rel=\"nofollow\">Zesty Blues Tweets</a>",
        "favorite_count": 0,
        "country_code": "",
        "timestamp_ms": "1539252298068",
        "lang": "en",
        "screen_name": "zesty_blues",
        "quote_count": 0,
        "retweet_count": 0
    },
    {......},
    {......},
    {......},
    {......}
]
```
