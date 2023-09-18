test:
    mypy src/ && poetry run pytest src/tests/*
run:
    poetry run python src/opus/main.py
fmt:
    black src
