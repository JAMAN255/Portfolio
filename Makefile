.PHONY: help test test-all test-todo test-calculator test-homepage test-insurance coverage lint format clean install dev

help:
	@echo "Available commands:"
	@echo "  make install          - Install dependencies"
	@echo "  make dev              - Install development dependencies"
	@echo "  make test             - Run all tests"
	@echo "  make test-todo        - Run todo_app tests only"
	@echo "  make test-calculator  - Run calculator tests only"
	@echo "  make test-homepage    - Run homepage tests only"
	@echo "  make test-insurance   - Run insuranceapp tests only"
	@echo "  make test-all         - Run all tests with tox"
	@echo "  make coverage         - Run tests with coverage report"
	@echo "  make lint             - Run code linting checks"
	@echo "  make format           - Format code with black and isort"
	@echo "  make clean            - Clean up cache and build files"
	@echo "  make migrations       - Create and apply migrations"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install tox pytest pytest-django pytest-cov coverage
	pip install flake8 black isort pylint

test:
	cd myapp && python manage.py test --verbosity=2 && cd ..

test-todo:
	cd myapp && python manage.py test todo_app --verbosity=2 && cd ..

test-calculator:
	cd myapp && python manage.py test calculator --verbosity=2 && cd ..

test-homepage:
	cd myapp && python manage.py test homepage --verbosity=2 && cd ..

test-insurance:
	cd myapp && python manage.py test insuranceapp --verbosity=2 && cd ..

test-all:
	tox

coverage:
	cd myapp && coverage run --source='.' manage.py test && coverage report && coverage html && cd ..
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	flake8 myapp --max-line-length=100 --exclude=migrations
	pylint myapp --disable=all --enable=E,F

format:
	black myapp
	isort myapp

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .tox -exec rm -rf {} +
	find . -type d -name htmlcov -exec rm -rf {} +
	find . -type f -name .coverage -delete

migrations:
	cd myapp && python manage.py makemigrations && python manage.py migrate && cd ..

run:
	cd myapp && python manage.py runserver && cd ..

shell:
	cd myapp && python manage.py shell && cd ..
