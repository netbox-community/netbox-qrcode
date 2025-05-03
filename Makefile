PYTHON_VER?=3.12
NETBOX_VER?=v4.3.0

NAME=netbox-qrcode

COMPOSE_FILE=./develop/docker-compose.yml
BUILD_NAME=netbox_qrcode
VERFILE=./netbox_qrcode/version.py


cbuild:
	docker-compose -f ${COMPOSE_FILE} \
		-p ${BUILD_NAME} build \
		--build-arg netbox_ver=${NETBOX_VER} \
		--build-arg python_ver=${PYTHON_VER}

debug:
	@echo "Starting Netbox .. "
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} up

start:
	@echo "Starting Netbox in detached mode.. "
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} up -d

stop:
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} down

destroy:
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} down
	docker volume rm -f ${BUILD_NAME}_pgdata_netbox_qrcode

nbshell:
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} run netbox python manage.py nbshell

shell:
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} run netbox python manage.py shell

adduser:
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} run netbox python manage.py createsuperuser

collectstatic:
	docker-compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} run netbox python manage.py collectstatic

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
