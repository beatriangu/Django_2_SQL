# Name of the Django container and the database
DJANGO_CONTAINER = django-2-sql-db-1
ADMINER_CONTAINER = django-2-sql-adminer-1
DB_USER = djangouser
DB_NAME = djangotraining

# Target to bring up the containers
up:
	docker-compose up -d

# Target to stop and remove the containers
down:
	docker-compose down

# Target to remove specific containers if they exist
clean:
	@docker ps -a -q --filter "name=$(ADMINER_CONTAINER)" | grep -q . && docker rm -f $(ADMINER_CONTAINER) || echo "No $(ADMINER_CONTAINER) container to remove"
	@docker ps -a -q --filter "name=$(DJANGO_CONTAINER)" | grep -q . && docker rm -f $(DJANGO_CONTAINER) || echo "No $(DJANGO_CONTAINER) container to remove"

# Target to check the running containers
ps:
	docker ps

# Target to access the Django container and connect to the database interactively
db:
	docker exec -it $(DJANGO_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)

# Target to run the entire workflow automatically
run: clean up
	sleep 10  # Waits for the services to be fully up
	docker-compose ps
	docker exec -it $(DJANGO_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)

# Includes a help target to list available commands
help:
	@echo "Available commands:"
	@echo "  make up     - Brings up the containers in detached mode"
	@echo "  make down   - Stops and removes the containers, networks, volumes, and images"
	@echo "  make ps     - Checks the running containers"
	@echo "  make db     - Accesses the Django container and connects to the database interactively"
	@echo "  make run    - Runs the entire workflow automatically"
	@echo "  make help   - Displays this help message"

# Specifies that help is the default goal if none is specified
.DEFAULT_GOAL := help
