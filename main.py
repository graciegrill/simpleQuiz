#MongoDB connect
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['myQuestions']
collection = db['results']

#User login and showing past player data
playerName = input("Enter player name: ")
results = collection.find({"name":playerName},{'_id':0, 'name':0})
for doc in results:
    for x in doc:
        print(x, ':', doc[x])
    print()


#Quiz part
from datetime import datetime
import json
with open('testQuestions.json', 'r') as file:
    data = json.load(file)
current = "1"
numCorrect = 0
right = []
wrong = []
while True:
    print(data[current]["text"])
    try:
        for i in range(len(data[current]["choices"])):
            print(data[current]["choices"][i]["option"])
        answer = int(input("Enter the answer: "))
        numCorrect+=data[current]["choices"][int(answer)-1]["correct"]
        if (data[current]["choices"][int(answer)-1]["correct"] == 0):
            wrong.append(current)
            print("Wrong!")
        else:
            right.append(current)
            print("Right!")
        current = (str(data[current]["choices"][int(answer)-1]["next"]))
    except:
        break

now = datetime.now()
dateTime = now.strftime("%d/%m/%Y %H:%M:%S")
propCorrect = (numCorrect/5.0)*100.0


#Add player details to MongoDB database
collection.insert_one({'name': playerName, 'score':propCorrect, 'right':right, "wrong":wrong, 'date':dateTime})

#Redis part
import redis
r = redis.Redis(
  host='redis-10160.c14.us-east-1-2.ec2.cloud.redislabs.com',
  port=10160,
  password='dAGRxRlE02o0MLNrVGrOvHpY0JIX9CqG')

prefix = 'frizzell'
scores = f"{prefix}-five-scores"

print()
print("Your current score is "+str(propCorrect))

r.zadd(scores, {playerName: propCorrect})
five_top_scores = r.zrevrange(scores, 0, 4, withscores=True)
for name, score in five_top_scores:
    print(f"{name.decode('utf-8')} {int(score)}")

