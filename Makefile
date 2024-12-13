DOCKER_IMAGE_NAME = my-health-app
DOCKER_CONTAINER_NAME = my-health-app-container
PYTHON_INTERPRETER = ./venv/bin/python
VENV_PYTHON = /app/venv/bin/python

# Path to the Python interpreter inside the virtual environment
VENV_PYTHON_TEST := $(VENV_DIR)/bin/python3


build:
	docker build -t $(DOCKER_IMAGE_NAME) .

run_all:
	docker run -d \
	--name $(DOCKER_CONTAINER_NAME) \
	-p 5000:5000 -p 5001:5001 -p 5002:5002 \
	$(DOCKER_IMAGE_NAME)

stop:
	docker stop $(DOCKER_CONTAINER_NAME) || true

clean: stop
	docker rm $(DOCKER_CONTAINER_NAME) || true
	docker rmi $(DOCKER_IMAGE_NAME) || true

# Subroutine to set up the virtual environment and install requirements for testing
test_setup: $(VENV_PYTHON_TEST)
	$(VENV_PYTHON_TEST) -m pip install -r requirements.txt

test: test_setup
	bash -c "source $(VENV_DIR)/bin/activate && $(VENV_PYTHON_TEST) test/app.py"



.PHONY: build run_all stop clean test
