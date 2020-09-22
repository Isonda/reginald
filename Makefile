DOCKER_TAG ?= reggie

.PHONY: run
run: build
	docker run -d --restart always --name $(DOCKER_TAG) $(DOCKER_TAG)

.PHONY: run-dev
run-dev: build
	docker run -it --name $(DOCKER_TAG)-dev $(DOCKER_TAG)

.PHONY: build
build:
	docker build -t $(DOCKER_TAG) .

.PHONY: install-hooks
install-hooks: .tox/pre-commit/bin/pre-commit
.tox/pre-commit/bin/pre-commit:
	tox -e pre-commit -- install -f --install-hooks

.PHONY: test
test: install-hooks
	tox -e pre-commit -- run --all-files
