etl-init:
	docker compose up airflow-init
	docker compose build
etl-start:
	docker compose up -d
etl-stop:
	docker compose stop
etl-rm:
	docker compose down --volumes --remove-orphans
	docker compose down --volumes --rmi all