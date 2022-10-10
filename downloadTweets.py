import sys
import os
import json
import datetime
import tweepy

baseDir = os.getcwd()
tweetOutputDir = "RealTimeOutput"

if not os.path.isdir(tweetOutputDir):
    os.mkdir(tweetOutputDir)

if len(sys.argv) > 1:
    data = json.load(open(sys.argv[1],'r'))
else:
    data = json.load(open('twitterKeys.json','r'))

class TweetStreamer(tweepy.StreamingClient):
    COUNTER = 0
    def on_data(self, rawData):
        decodedData = rawData.decode()
        processedData = json.loads(decodedData)
        tweetDate = datetime.datetime.strptime(processedData['data']['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=datetime.timezone.utc)
        jsonFileName = tweetDate.strftime('%Y-%0m-%0d.txt')
        outputFileName = os.path.abspath(os.path.join(tweetOutputDir, jsonFileName))
        with open(outputFileName, 'a') as fh:
            fh.writelines(["\n",decodedData])
        print(jsonFileName, tweetDate)
        
        self.COUNTER += 1
        if self.COUNTER == 100:
            sys.exit()

    def on_error(self, status_code):
        print('Error occured: Status code {:}'.format(status_code))
        return True

tweetStreamer = TweetStreamer(
    bearer_token = data["bearer_token"],
    return_type = dict,
    wait_on_rate_limit = True)

locationRule = tweepy.StreamRule("place_country:US")
tweetStreamer.add_rules(locationRule)

# Specify the fields necessary
# Refer https://developer.twitter.com/en/docs/twitter-api/fields
tweetStreamer.filter(
    threaded=True,
    expansions="author_id,geo.place_id",
    tweet_fields="created_at,geo,lang",
    user_fields="created_at,location,verified",
    place_fields="country_code,geo,name,place_type"
    )
