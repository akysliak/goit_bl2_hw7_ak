To start a container with PostgreSQL, run:

    docker run --name postgres_07 -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres

To initialize alembic:

    poetry run alembic init alembic

To set up the alembic environment:

    poetry run copy backup\env.py alembic\

To create tables in the db:

    poetry run alembic revision --autogenerate -m 'Init'
    poetry run alembic upgrade head

To populate the db

    poetry run python seed.py

To run queries:

    poetry run python my_select.py
