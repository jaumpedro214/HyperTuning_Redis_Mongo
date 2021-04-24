
REDIS_CONT_NAME=redis_hpt
REDIS_IMG=redis
REDIS_DOC_PORT=6379
REDIS_LOC_PORT=6379

MONGO_CONT_NAME=mongodb_hpt
MONGO_IMG=mongo
MONGO_DOC_PORT=27017
MONGO_LOC_PORT=27017
MONGO_VOL_DIR = /home/mongodb_hpt:/data

start:
	docker start $(REDIS_CONT_NAME)
	docker start $(MONGO_CONT_NAME)

run:
	docker run --name $(REDIS_CONT_NAME) -p $(REDIS_LOC_PORT):$(REDIS_DOC_PORT) -d $(REDIS_IMG)
	docker run --name $(MONGO_CONT_NAME) -p $(MONGO_LOC_PORT):$(MONGO_DOC_PORT) -v $(MONGO_VOL_DIR) -d $(MONGO_IMG)

stop:
	docker stop $(REDIS_CONT_NAME)
	docker stop $(MONGO_CONT_NAME)

remove: stop
	docker rm $(REDIS_CONT_NAME)
	docker rm $(MONGO_CONT_NAME)
