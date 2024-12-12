# Variables
PYTHON_INTERPRETER = python
PYTHON_VENV = /app/venv
DOCKER_IMAGE_NAME = my-health-app
DOCKER_CONTAINER_NAME = my-health-app-container

# Build the Docker image
build:
	docker build -t $(DOCKER_IMAGE_NAME) -f Dockerfile .

# Create and activate virtual environment inside the container, and install requirements
init: build
	docker run -it --rm --name $(DOCKER_CONTAINER_NAME) $(DOCKER_IMAGE_NAME) bash -c \
		"source $(PYTHON_VENV)/bin/activate && pip install -r requirements.txt"

# Run all services (backend, BMI, BMR)
run_all:
	docker run -d --rm --name $(DOCKER_CONTAINER_NAME) \
	-p 5000:5000 -p 5001:5001 -p 5002:5002 \
	$(DOCKER_IMAGE_NAME) \
	bash -c "source $(PYTHON_VENV)/bin/activate && \
			 python backend/app.py & \
			 python bmi_service/app.py & \
			 python bmr_service/app.py"

# Stop the running container
stop:
	docker stop $(DOCKER_CONTAINER_NAME)

# Run the test without docker or venv just for simplicity
test: $(VENV_PYTHON)
	$(VENV_PYTHON) test/app.py

# Clean up
clean: stop
	docker rmi $(DOCKER_IMAGE_NAME)
	rm -rf $(PYTHON_VENV)

.PHONY: build init run_all stop clean test
