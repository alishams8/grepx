VENV_DIR = venv
PYTHON = python
POETRY = poetry
POETRY_VENV_DIR = $(shell $(POETRY) env info --path)
POETRY_BIN = $(POETRY_VENV_DIR)/bin
PYTHON_ENV = $(POETRY_BIN)/python

# Default target
all: setup install

# Create the virtual environment using Poetry
setup:
	$(POETRY) install --no-root

# Install the required packages using Poetry
install: setup
	@echo "Dependencies installed with Poetry."