.PHONY: build up clean

clean:
	docker compose down --rmi all --volumes --remove-orphans

build:
	docker compose build --no-cache

up: clean build
	docker compose up --force-recreate -d