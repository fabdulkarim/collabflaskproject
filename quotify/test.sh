clear && clear

export FLASK_ENV=testing
pytest --verbose --cov-report html --cov=blueprints tests/
export FLASK_ENV=development