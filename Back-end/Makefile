run:
	@uvicorn main:app --reload
create-migrations:
	@PYTHONPATH=$PYTHONPATH: ${pwd} alembic revision --autogenerate -m ${d}
run-migrate:
	@PYTHONPATH=$PYTHONPATH: ${pwd} alembic upgrade head
run-delete:
	@PYTHONPATH=$PYTHONPATH: ${pwd} alembic downgrade head