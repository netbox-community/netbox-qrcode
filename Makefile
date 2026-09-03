PYTHON_VER?=3.14
NETBOX_VER?=feature

# Branch that releases are cut from. `main` holds the released code; `feature` is
# for active development of future releases and is merged into `main` to release.
RELEASE_BRANCH?=main

NAME=netbox-qrcode

COMPOSE_FILE=./develop/docker-compose.yml
BUILD_NAME=netbox_qrcode
VERFILE=./netbox_qrcode/version.py


cbuild:
	docker compose -f ${COMPOSE_FILE} \
		-p ${BUILD_NAME} build \
		--build-arg netbox_ver=${NETBOX_VER} \
		--build-arg python_ver=${PYTHON_VER}

debug:
	@echo "Starting Netbox .. "
	docker compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} up

start:
	@echo "Starting Netbox in detached mode.. "
	docker compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} up -d

stop:
	docker compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} down

destroy:
	docker compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} down
	docker volume rm -f ${BUILD_NAME}_pgdata_netbox_qrcode

nbshell:
	docker compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} run netbox python manage.py nbshell

shell:
	docker compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} run netbox python manage.py shell

adduser:
	docker compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} run netbox python manage.py createsuperuser

collectstatic:
	docker compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} run netbox python manage.py collectstatic

migrations:
	docker compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} up -d postgres
	docker compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} \
	run netbox python manage.py makemigrations --name ${BUILD_NAME}
	docker compose -f ${COMPOSE_FILE} -p ${BUILD_NAME} down


relpatch:
	$(eval CURVER := $(shell cat $(VERFILE) | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'))
	$(eval NEWVER := $(shell pysemver bump patch $(CURVER) 2>/dev/null))
	@# Guards run before any git mutation. These are shell tests rather than make
	@# conditionals because a make `ifneq` is evaluated at parse time, before the
	@# recipe's $(eval) has run, so it can never see the git status.
	@test -z "$$(git status --porcelain)" || { \
		echo "Error: git status is not clean. Commit or stash first:"; \
		git status --porcelain; \
		exit 1; \
	}
	@command -v pysemver >/dev/null 2>&1 || { \
		echo "Error: pysemver not found. Install it with: pip install semver"; \
		exit 1; \
	}
	@test -n "$(CURVER)" || { echo "Error: no version found in $(VERFILE)"; exit 1; }
	@test -n "$(NEWVER)" || { echo "Error: could not compute the next version"; exit 1; }
	git checkout $(RELEASE_BRANCH)
	git remote update
	git pull origin $(RELEASE_BRANCH)
	git checkout -b release-$(NEWVER) origin/$(RELEASE_BRANCH)
	echo '__version__ = "$(NEWVER)"' > $(VERFILE)
	git commit -am 'bump ver'
	git push origin release-$(NEWVER)
	git checkout $(RELEASE_BRANCH)

pbuild:
	python3 -m pip install --upgrade build
	python3 -m build

pypipub:
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*
