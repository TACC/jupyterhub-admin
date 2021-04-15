# Makefile for local development

.PHONY: down clean nuke

ifdef TAG
export TAG := $(TAG)
else
export TAG := dev
endif


# Builds core locally and sets to correct tag. This should take priority over DockerHub images
build-core:
	@docker-compose build

# Builds core locally and then runs pgrest in daemon mode
local-deploy: build-core
	@docker-compose run jupyterhub_admin python manage.py migrate
	@docker-compose up -d jupyterhub_admin

build-dev:
	@docker-compose -f docker-compose.dev.yml build

# Builds core locally and then runs pgrest in daemon mode
dev: build-dev
	@docker-compose -f docker-compose.dev.yml run jupyterhub_admin python manage.py migrate
	@docker-compose -f docker-compose.dev.yml up


# Run unit tests on *unit_test.py
unittest: build-dev
	@docker-compose -f docker-compose.dev.yml run jupyterhub_admin pytest -c unit_test.ini

# Run integration tests on *integration_test.py
integrationtest: build-core
	@docker-compose -f docker-compose.yml run jupyterhub_admin pytest -c integration_test.ini


# Pulls all Docker images not yet available but needed to run pgrest
pull:
	@docker-compose pull


# Ends all active Docker containers needed for pgrest
down:
	@docker-compose down

# Ends all active Docker containers needed for pgrest and clears all volumes
# If this is not used the postgres container will restart with data
down-volumes:
	@docker-compose down
	@docker volume prune -f


# Does a clean and also deletes all images needed for abaco
clean:
	@docker-compose down --remove-orphans -v --rmi all 


# Deletes ALL images, containers, and volumes forcefully
nuke:
	@docker rm -f `docker ps -aq`
	@docker rmi -f `docker images -aq`
	@docker container prune -f
	@docker volume prune -f
