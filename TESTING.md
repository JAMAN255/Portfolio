# Testing Guide

This document provides comprehensive information about testing the Statistical App project.

## Overview

The project includes comprehensive test suites for all Django applications:
- **todo_app**: Todo management functionality
- **calculator**: Statistical calculations
- **homepage**: Website pages and user management
- **insuranceapp**: Insurance management system

## Test Statistics

- **Total Test Cases**: 200+
- **Coverage**: Models, Views, Forms, and Integrations
- **Frameworks**: Django TestCase, unittest

## Local Testing

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-django pytest-cov coverage tox flake8
```

### Running Tests

#### Using Django's test runner (recommended for single runs)

```bash
# Run all tests
cd myapp
python manage.py test --verbosity=2

# Run specific app
python manage.py test todo_app --verbosity=2
python manage.py test calculator --verbosity=2
python manage.py test homepage --verbosity=2
python manage.py test insuranceapp --verbosity=2

# Run specific test class
python manage.py test todo_app.tests.TodoItemModelTest

# Run specific test method
python manage.py test todo_app.tests.TodoItemModelTest.test_todo_item_creation
```

#### Using pytest

```bash
# Run all tests with pytest
pytest

# Run specific test file
pytest myapp/todo_app/tests.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=. --cov-report=html
```

#### Using Make commands

```bash
# Run all tests
make test

# Run specific app tests
make test-todo
make test-calculator
make test-homepage
make test-insurance

# Generate coverage report
make coverage

# Run linting
make lint

# Format code
make format
```

### Coverage Reports

Generate and view coverage reports:

```bash
# Using Django
cd myapp
coverage run --source='.' manage.py test
coverage report
coverage html
cd ..

# Using pytest
pytest --cov=myapp --cov-report=html

# View HTML report
open htmlcov/index.html
```

## CI/CD Pipeline Testing

### GitLab CI/CD

The project includes a `.gitlab-ci.yml` file that automatically runs tests on:
- Every push to the repository
- Every merge request

#### Pipeline Stages

1. **test** - Main test stage
   - `test:django` - Tests with PostgreSQL
   - `test:sqlite` - Tests with SQLite
   - `test:checks` - Django system checks
   - Individual app tests

2. **coverage** - Code coverage analysis
   - Generates HTML and XML reports
   - Fails if coverage is below threshold

3. **lint** - Code quality checks
   - Flake8 linting
   - Bandit security checks

4. **deploy** - Deployment (manual trigger)
   - Staging deployment
   - Production deployment

### Running Pipeline Locally

Use GitLab Runner to test the pipeline locally:

```bash
# Install GitLab Runner
# https://docs.gitlab.com/runner/install/

# Run specific job
gitlab-runner exec docker test:django

# Run all jobs
gitlab-runner exec docker
```

## Test Categories

### Model Tests

Test database models and their methods:

```python
# Example: Test model creation
def test_todo_item_creation(self):
    todo = TodoItem.objects.create(name='Test Task')
    self.assertEqual(todo.name, 'Test Task')
```

### View Tests

Test view responses and templates:

```python
# Example: Test view status code
def test_todo_list_view_status_code(self):
    response = self.client.get(reverse('todo_list'))
    self.assertEqual(response.status_code, 200)
```

### Form Tests

Test form validation:

```python
# Example: Test form validation
def test_form_valid_data(self):
    form = TodoItemForm(data={'name': 'Test'})
    self.assertTrue(form.is_valid())
```

### Integration Tests

Test complete workflows:

```python
# Example: Test complete CRUD workflow
def test_complete_todo_workflow(self):
    # Create
    response = self.client.post(create_url, data)
    # Read
    response = self.client.get(detail_url)
    # Update
    response = self.client.post(update_url, data)
    # Delete
    response = self.client.post(delete_url)
```

## Test Organization

### File Structure

```
myapp/
├── todo_app/
│   ├── tests.py         # All todo_app tests
│   ├── models.py
│   ├── views.py
│   └── forms.py
├── calculator/
│   ├── tests.py         # All calculator tests
│   └── models.py
├── homepage/
│   ├── tests.py         # All homepage tests
│   └── models.py
└── insuranceapp/
    ├── tests.py         # All insuranceapp tests
    └── models.py
```

### Test Naming Conventions

- Test classes: `NameModelTest`, `NameViewTest`, `NameFormTest`
- Test methods: `test_specific_functionality`
- Example: `test_todo_item_creation`, `test_todo_list_view_status_code`

## Debugging Tests

### Running tests with debugging

```bash
# Drop into pdb on failure
python manage.py test --pdb

# Add breakpoint in test
import pdb; pdb.set_trace()

# Run with print statements
python manage.py test --verbosity=2
```

### Viewing test database

```bash
# Keep test database after tests
python manage.py test --keepdb

# Access test database
sqlite3 db.sqlite3
```

## Performance

### Test execution time

- Total test suite: ~10-15 seconds (SQLite)
- Per app tests: 1-3 seconds

### Optimizations

- Tests run in transactions (faster cleanup)
- Database can be kept with `--keepdb`
- Parallel testing with pytest-xdist:

```bash
pip install pytest-xdist
pytest -n auto
```

## Continuous Integration Best Practices

1. **Run tests before commit**
   ```bash
   make test
   ```

2. **Check coverage regularly**
   ```bash
   make coverage
   ```

3. **Implement pre-commit hooks**
   ```bash
   pip install pre-commit
   ```

4. **Keep tests organized**
   - One test file per app
   - Logical grouping of test classes

5. **Write meaningful assertions**
   - Use descriptive assertion messages
   - Test both success and failure cases

## Troubleshooting

### Common Issues

**Issue: Tests fail with database errors**
```bash
# Solution: Reset database
rm db.sqlite3
cd myapp
python manage.py migrate
cd ..
```

**Issue: Import errors in tests**
```bash
# Solution: Ensure PYTHONPATH is set
export PYTHONPATH="${PYTHONPATH}:/path/to/myapp"
```

**Issue: Tests slow on first run**
```bash
# Solution: Use --keepdb flag
python manage.py test --keepdb
```

## Test Statistics by App

### todo_app
- Model tests: 15
- View tests: 20
- Form tests: 5
- Integration tests: 3
- **Total: 43**

### calculator
- Calculation tests: 35
- Index calculation tests: 10
- View tests: 15
- Integration tests: 2
- **Total: 62**

### homepage
- Model tests: 15
- View tests: 12
- Authentication tests: 8
- Integration tests: 5
- **Total: 40**

### insuranceapp
- Model tests: 25
- View tests: 20
- Integration tests: 3
- **Total: 48**

## Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [pytest Documentation](https://docs.pytest.org/)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)

## Contributing

When adding new features:

1. Write tests first (TDD approach recommended)
2. Ensure all tests pass
3. Maintain or improve code coverage
4. Follow existing test patterns
5. Document test cases for complex logic

## Support

For issues or questions about testing:

1. Check this documentation
2. Review existing test examples
3. Consult Django/pytest documentation
4. Open an issue on the repository
