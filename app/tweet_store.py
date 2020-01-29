import simplejson as json
import redis

class TweetStore:

    dbfile_path = '../config/db.json'

    with open(dbfile_path) as f:
        db_config = json.loads(f.read())

    # Redis configuration
    redis_host = db_config["redis_host"]
    redis_port = db_config["redis_port"]
    redis_password = db_config["redis_password"]

    # Tweet config
    redis_key = 'tweets'
    num_tweets =  20


    def __init__(self):
        self.db = r = redis.Redis(
            host = self.redis_host,
            port = self.redis_port,
            password = self.redis_password
        )
        self.trim_count = 0

    def push(self,data):
        self.db.lpush(self.redis_key, json.dumps(data))
        self.trim_count += 1

        # periodically trim the list so it doe s not grow too large
        if self.trim_count > 100:
            self.db.ltrim(self.redis_key, 0, self.num_tweets)
            self.trim_count = 0

    def tweets(self, limit=25):
        tweets = []

        for item in self.db.lrange(self.redis_key, 0, limit-1):
            tweet_obj = json.loads(item)
            tweets.append(tweet_obj)
        
        return tweets

