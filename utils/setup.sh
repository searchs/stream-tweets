#!/bin/sh

# non-persistent storage
docker run --name nlytics-redis -d redis

# with persistent storage
docker run --name nlytics-redis -d redis redis-server --appendonly yes

# connecting via redic-cli
docker run -it --network nlytics-network --rm redis redis-cli -h nlytics-redis

# using custom redis conf
FROM redis
COPY redis.conf /usr/local/etc/redis/redis.conf
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]

# one-liner
docker run -v /localredis/conf/redis.conf:/usr/local/etc/redis/redis.conf --name nyltics-redis redis redis-server /usr/local/etc/redis/redis.conf

