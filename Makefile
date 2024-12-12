# Makefile for managing the microservice application

.PHONY: init test run_backend run_bmi_service run_bmr_service run_all clean build_docker run_docker

# Virtual environment directory
VENV_DIR := venv

# Path to the Python interpreter inside the virtual environment
VENV_PYTHON := $(VENV_DIR)/bin/python3

# Init target to create venv and install dependencies
init: $(VENV_PYTHON)
	$(VENV_PYTHON) -m pip install -r requirements.txt

# Create the virtual environment if it doesn't exist
$(VENV_PYTHON):
	python3 -m venv $(VENV_DIR)

# Test target to run tests using unittest
test: $(VENV_PYTHON)
	$(VENV_PYTHON) test/app.py

# Target to run the backend service
run_backend: $(VENV_PYTHON)
	$(VENV_PYTHON) backend/app.py

# Target to run the BMI service
run_bmi_service: $(VENV_PYTHON)
	$(VENV_PYTHON) bmi_service/app.py

# Target to run the BMR service
run_bmr_service: $(VENV_PYTHON)
	$(VENV_PYTHON) bmr_service/app.py

# Target to run all services in the background
run_all: build_docker run_docker
	# start the container in detached mode

# Clean target to remove temporary files
clean:
	rm -rf __pycache__
	rm -rf $(VENV_DIR)
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

# Target to build the Docker image
build_docker:
	docker build -t health-app .

# Target to run the Docker container
run_docker:
	docker run -d -p 5000:5000 -p 5001:5001 -p 5002:5002 --name health-app-container health-app
