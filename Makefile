DOCKER_TAG ?= reggie

.PHONY: run
run: build
	docker run -d --name $(DOCKER_TAG) $(DOCKER_TAG)

.PHONY: run-dev
run-dev: build
	docker run -it --name $(DOCKER_TAG)-dev $(DOCKER_TAG)

.PHONY: build
build:
	docker build -t $(DOCKER_TAG) .


