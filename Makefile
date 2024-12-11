# Name of the virtual environment directory
VENV_DIR := python_micro_azure.venv

# Path to the Python interpreter inside the virtual environment
VENV_PYTHON := $(VENV_DIR)/bin/python3

# Rule to create the virtual environment
create:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment in $(VENV_DIR)..."; \
		python3 -m venv $(VENV_DIR); \
		echo "Virtual environment created successfully."; \
	else \
		echo "Virtual environment already exists at $(VENV_DIR)."; \
	fi

# Rule to install dependencies
install: venv
	@if [ -f "requirements.txt" ]; then \
		echo "Installing dependencies from requirements.txt into $(VENV_DIR)..."; \
		"$(VENV_PYTHON)" -m pip install --upgrade pip; \
		"$(VENV_PYTHON)" -m pip install -r requirements.txt; \
		echo "Dependencies installed successfully into virtual environment."; \
	else \
		echo "requirements.txt not found. Skipping installation."; \
	fi

# Rule to check if the virtual environment exists
check:
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Virtual environment exists at $(VENV_DIR)"; \
	else \
		echo "Virtual environment does not exist. Run 'make venv' to create it."; \
	fi

# Rule to activate and enter the virtual environment
run: venv
	@echo "Activating virtual environment $(VENV_DIR)..."
	@bash -c "source $(VENV_DIR)/bin/activate && echo 'Entered virtual environment. Use '\''deactivate'\'' to exit.' && bash"

# Rule to clean the virtual environment
clean:
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Removing virtual environment $(VENV_DIR)..."; \
		rm -rf $(VENV_DIR); \
	else \
		echo "Virtual environment does not exist."; \
	fi
.PHONY: venv check_venv install run clean Makefile
