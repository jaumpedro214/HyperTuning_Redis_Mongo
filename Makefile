
REDIS_CONT_NAME=redis_hpt
REDIS_IMG=redis

MONGODB_CONT_NAME=mongodb_hpt 

start:
	docker start $(REDIS_CONT_NAME)
	
run:
	docker run --name $(REDIS_CONT_NAME) -p 6379:6379 -d $(REDIS_IMG)

stop:
	docker stop $(REDIS_CONT_NAME)

remove: stop
	docker rm $(REDIS_CONT_NAME)
