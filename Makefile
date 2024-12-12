# Variables
PYTHON_INTERPRETER = python
PYTHON_VENV = /app/venv
DOCKER_IMAGE_NAME = my-health-app
DOCKER_CONTAINER_NAME = my-health-app-container

# Build 
build:
	docker build -t $(DOCKER_IMAGE_NAME) -f Dockerfile .

# y a ecrit build bordel et install
init: build
	docker run -it --rm --name $(DOCKER_CONTAINER_NAME) $(DOCKER_IMAGE_NAME) bash -c \
	"source $(PYTHON_VENV)/bin/activate && pip install -r requirements.txt"

# Lance tout
run_all:
	docker run -d \
	--name $(DOCKER_CONTAINER_NAME) \
	-p 5000:5000 -p 5001:5001 -p 5002:5002 \
	$(DOCKER_IMAGE_NAME)

# STOP
stop:
	docker stop $(DOCKER_CONTAINER_NAME)

# Run tests
test: $(VENV_PYTHON)
	$(VENV_PYTHON) test/app.py

# Menage
clean: stop
	docker rmi $(DOCKER_IMAGE_NAME)
	rm -rf $(PYTHON_VENV)

.PHONY: build init run_all stop clean test