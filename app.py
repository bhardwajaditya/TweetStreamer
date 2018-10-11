import pymongo
from pymongo import MongoClient
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import sys
from datetime import date
import datetime
from flask import Flask, request,make_response
import os
from settings import twitter_config
from commons import json_response
import csv
import io
from streamListener import listener

client = MongoClient()
db = client['tweets']
tweets = db.tweets


auth = OAuthHandler(twitter_config['consumer_key'], twitter_config['consumer_secret'])
auth.set_access_token(twitter_config['access_token'], twitter_config['access_token_secret'])
app = Flask(__name__)



@app.route('/')
def index():
    return '<h1>Welcome to Tweety!</h1>'

@app.route('/stream')
def stream_event():
    res = dict()
    
    keywords = request.args.get('keywords')
    runtime =request.args.get('timelimit')
    if(runtime==None):
        runtime=100
    if keywords:
        keywords = keywords.split(",")
    else:
        res = {
            "status": "error",
            "message": "Please provide a few keyword(s) (comma-separated)",
            "example": "/stream?keywords=kw1,kw2,abc,xyz"
        }
        return "error"
    
    res['status'] = "success"
    res['message'] = "Started streaming tweets with keywords {}".format(keywords)
    x=tweets.delete_many({})
    print(x.deleted_count, " documents deleted.")
    twitterStream = Stream(auth, listener(time_limit=int(runtime)))
    twitterStream.filter(track=keywords, async=True)
    return json_response(res)
    
    
# ----------------------users route--------------------------------------    
@app.route('/users/')
def users():
    search = request.args.get('name')
    A=[]
    x=tweets.find()
    for i in x:
        i.pop('_id')
        if(search!=None):
            if(i['user_name']==search):
                A.append(i)
        else:
            A.append(i)
    return json_response(A)

# ---------------------------------------------------------------------------

# ----------------------tweets route--------------------------------------  
@app.route('/tweets/<method>')
def retrieve(method):
    l=request.args.get('limit')
    page=request.args.get('page')
    if(l==None):
        l=10
    else:
        l=int(l)
    if(page==None):
        page=1
    page=int(page)-1
    A=[]
    
    if(method=='search'):
        search = request.args.get('search')
        x=tweets.find().limit(l).skip(page*10)
        for i in x:
            i.pop('_id')
            if(search==None):
                A.append(i)
            else:
                if(search in i['tweet_text'] or search in i['user_name'] ):
                    A.append(i)
        
        
    if(method=='order'):
        ordering=request.args.get('ordering')
        if(ordering[0]=='-'):
            field=ordering[1:]
        else:
            field=ordering
        if(ordering[0]=='-'):
            x=tweets.find().sort(field,pymongo.DESCENDING).limit(l).skip(page*10)
        else:
            x=tweets.find().limit(l).sort(field).skip(page*10)
        for i in x:
            i.pop('_id')
            A.append(i)
        
# ----------------------tweets/integer_search route--------------------------------------          
    elif(type=='integer_search'):
        column=request.args.get('column_name')
        maximum=request.args.get('max')
        minimum=request.args.get('min')
        x=tweets.find()
        if(maximum!=None and minimum==None):
            for i in x:
                i.pop('_id')
                if(i[column]<=maximum):
                    A.append(i)
            
        
        elif(maximum==None and minimum!=None):
            for i in x:
                i.pop('_id')
                if(i[column]>=minimum):
                    A.append(i)
            
        
        elif(maximum!=None and minimum!=None):
            for i in x:
                i.pop('_id')
                if(i[column]>=minimum and i[column]<=maximum):
                    A.append(i)
            
# ----------------------tweets/string_search route--------------------------------------  
    elif(method=='string_search'):
        column=request.args.get('column_name')
        start=request.args.get('start')
        end=request.args.get('end')
        contain=request.args.get('contain')
        match=request.args.get('match')
        x=tweets.find()
        B=[]
        if(contain!=None):
            for i in x:
                i.pop('_id')
                if contain in i[column]:
                    A.append(i)
            
        if(match!=None):
            for i in x:
                i.pop('_id')
                if(i[column]==match):
                    A.append(i)
            
            
        if(end!=None and start==None):
            for i in x:
                i.pop('_id')
                B=i[column].split()
                if(B[-1]==end):
                    A.append(i)
            
            
        if(end==None and start!=None):
            for i in x:
                i.pop('_id')
                B=i[column].split()
                if(B[0]==start):
                    A.append(i)
            
            
        if(end!=None and start!=None):
            for i in x:
                i.pop('_id')
                B=i[column].split()
                if(B[-1]==end and B[0]==start):
                    A.append(i)

# ----------------------tweets/date--------------------------------------              
    elif(method=='date'):
        startDate=request.args.get('startDate')
        endDate=request.args.get('endDate')
        x=tweets.find()
        if(startDate!=None and endDate==None):
            startDate=datetime.datetime.strptime(startDate, "%d%m%Y").date()
            for i in x:
                i.pop('_id')
                created_at=datetime.datetime.strptime(i['created_at'], '%a %b %d %H:%M:%S %z %Y').date()
                if(created_at>=startDate):
                    A.append(i)
        
        if(startDate==None and endDate!=None):
            endDate=datetime.datetime.strptime(endDate, "%d%m%Y").date()
            for i in x:
                i.pop('_id')
                created_at=datetime.datetime.strptime(i['created_at'], '%a %b %d %H:%M:%S %z %Y').date()
                if(created_at<=endDate):
                    A.append(i)
        if(startDate!=None and endDate!=None):
            startDate=datetime.datetime.strptime(startDate, "%d%m%Y").date()
            endDate=datetime.datetime.strptime(endDate, "%d%m%Y").date()
            for i in x:
                i.pop('_id')
                created_at=datetime.datetime.strptime(i['created_at'], '%a %b %d %H:%M:%S %z %Y').date()
                if(created_at>=startDate and created_at<=endDate):
                    A.append(i)
            
    return json_response(A)

# -----------------------------------------------------------------------  

# ----------------------csv route--------------------------------------  
@app.route('/csv')
def get_csv():
    si = io.StringIO()
    imp_fields = ['user_name','created_at', 'text', 'retweet_count', 'favorite_count']
    writer = csv.writer(si)
    writer.writerow(imp_fields)
    x=tweets.find()
    for i in x:
        writer.writerow([
            i['user_name'],
			i['created_at'],
			i['tweet_text'],
			i['retweet_count'],
			i['favorite_count'],	
		])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# -----------------------------------------------------------------------  

if __name__ == '__main__':
    app.run( host=os.environ['IP'], port=os.environ['PORT'] ,debug=True)
