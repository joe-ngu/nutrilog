# Define variables
COMPOSE=docker compose
SERVICE=fastapi

# Declare targets as PHONY
.PHONY: up build enter migrate help

# Default target
help: 
	@echo "Available targets:"
	@echo "  up       - Start the Docker containers"
	@echo "  build    - Build the Docker images"
	@echo "  enter    - Enter the running container"
	@echo "  migrate  - Run migration script"

# Start the Docker containers
up:
	@$(COMPOSE) up

# Build the Docker images
build:
	@$(COMPOSE) build

# Enter the running container
enter:
	@$(COMPOSE) exec $(SERVICE) bash

# Run migration script
migrate:
	@python migrate.py || echo "Migration failed"

