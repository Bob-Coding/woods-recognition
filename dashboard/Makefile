# Load environment variables from .env file
include .env

.PHONY: up down tail help

up:
	docker-compose up -d

down:
	docker-compose down

tail:
	docker-compose logs -f

help:
	@echo "Available targets:"
	@echo "  up   - Start the services defined in docker-compose.yml"
	@echo "  down - Stop the services defined in docker-compose.yml"
	@echo "  tail - Show the logs of the services defined in docker-compose.yml"
