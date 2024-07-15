# General: The Makefile is used for plugin development is used to simplify the execution of command sequences.
# Recommended VSCode plugin: Makefile-Tools (extension ID: ms-vscode.makefile-tools)
# To trigger a Makefile command (target), the following line must be written in the terminal window of VSCode, for example:
# make cbuild

# Parameter
PYTHON_VER?=3.12
NETBOX_VER?=v4.0.2

NAME=netbox-qrcode

COMPOSE_FILE=./develop/docker-compose.yml
COMPOSE_FILE_DEBUG=./develop/docker-compose-debug.yml
BUILD_NAME=netbox_qrcode
VERFILE=./netbox_qrcode/version.py

# Build Docker with the specific Python and Netbox version
cbuild:
	docker-compose -f ${COMPOSE_FILE} \
		-p ${BUILD_NAME} build \
		--build-arg netbox_ver=${NETBOX_VER} \
		--build-arg python_ver=${PYTHON_VER}

# Start Docker with terminal window output
debug:
	@echo "Starting Netbox .. "
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} up

# Start Docker with terminal window output.
# Brakepoints in e.g. Python files are supported in VSCode. Changes in Python and HTML are applied after saving.
debug-vscode:
	@echo "Starting Netbox debug for VSCode.. "
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} -f ${COMPOSE_FILE_DEBUG} up --build

# Start Docker without connecting to the terminal window. (Runs independently of the terminal window.).
start:
	@echo "Starting Netbox in detached mode.. "
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} up -d

# Stop Docker Container
stop:
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} down

# Stop Docker and remove containers
destroy:
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} down
	docker volume rm -f ${BUILD_NAME}_pgdata_netbox_qrcode

# Calls the Netbox shell. Exit with exit()
# NetBox includes a Python shell within which objects can be directly queried, created, modified, and deleted.
nbshell:
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} run netbox python manage.py nbshell

# Calls the Python shell. Exit with exit()
shell:
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} run netbox python manage.py shell

# To create the Django Superuser to be able to log on to Netbox Web.
adduser:
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} run netbox python manage.py createsuperuser

# Django collectstatic
collectstatic:
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} run netbox python manage.py collectstatic

# Migrate the Netbox system depending on the Django model
migrations:
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} up -d postgres
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} \
	run netbox python manage.py makemigrations --name ${BUILD_NAME}
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} down


relpatch:
	$(eval GSTATUS := $(shell git status --porcelain))
ifneq ($(GSTATUS),)
	$(error Git status is not clean. $(GSTATUS))
endif
	git checkout develop
	git remote update
	git pull origin develop
	$(eval CURVER := $(shell cat $(VERFILE) | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'))
	$(eval NEWVER := $(shell pysemver bump patch $(CURVER)))
	$(eval RDATE := $(shell date '+%Y-%m-%d'))
	git checkout -b release-$(NEWVER) origin/develop
	echo '__version__ = "$(NEWVER)"' > $(VERFILE)
	git commit -am 'bump ver'
	git push origin release-$(NEWVER)
	git checkout develop

pbuild:
	python3 -m pip install --upgrade build
	python3 -m build

pypipub:
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*
