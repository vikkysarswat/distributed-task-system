# Contributing to Distributed Task System

Thank you for your interest in contributing to the Distributed Task System! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a code of conduct that promotes respect, inclusivity, and professionalism. By participating, you agree to uphold these standards.

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git
- PostgreSQL (for local development)
- Redis (for local development)

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/distributed-task-system.git
   cd distributed-task-system
   ```

2. **Set up development environment**
   ```bash
   chmod +x scripts/setup_dev.sh
   ./scripts/setup_dev.sh
   ```

3. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Start services**
   ```bash
   docker-compose up -d
   ```

## Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following our coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Run quality checks**
   ```bash
   # Format code
   black .
   
   # Lint code
   ruff check .
   
   # Type checking
   mypy src/
   
   # Security scan
   bandit -r src/
   
   # Run tests
   pytest
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Standards

### Python Code Style

- **Formatting**: Use Black with default settings
- **Linting**: Use Ruff with project configuration
- **Type Hints**: All functions must have type hints
- **Docstrings**: Use Google-style docstrings
- **Line Length**: Maximum 88 characters

### Example Code Style

```python
from typing import List, Optional

def process_tasks(
    task_ids: List[str], 
    priority: Optional[int] = None
) -> List[Task]:
    """Process a list of tasks with optional priority filtering.
    
    Args:
        task_ids: List of task IDs to process
        priority: Optional priority filter
        
    Returns:
        List of processed tasks
        
    Raises:
        TaskNotFoundError: If any task ID is not found
    """
    # Implementation here
    pass
```

### Commit Message Convention

Use conventional commits format:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test additions or changes
- `chore:` - Build process or auxiliary tool changes

Example: `feat: add task priority filtering to API`

## Testing

### Test Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/           # End-to-end tests
└── conftest.py    # Test configuration
```

### Writing Tests

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test complete user workflows
- **Coverage**: Aim for >90% code coverage

### Test Example

```python
import pytest
from src.services.task_service import TaskService
from src.models.task import TaskStatus

@pytest.mark.asyncio
async def test_create_task(db_session, sample_task_data):
    """Test task creation."""
    service = TaskService(db_session)
    
    task = await service.create_task(**sample_task_data)
    
    assert task.id is not None
    assert task.status == TaskStatus.PENDING
    assert task.name == sample_task_data["name"]
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_task_service.py

# Run tests with specific marker
pytest -m "not slow"
```

## Documentation

### API Documentation

- Use FastAPI automatic documentation
- Add comprehensive docstrings to all endpoints
- Include request/response examples
- Document error codes and responses

### Code Documentation

- All public functions and classes must have docstrings
- Use type hints for all parameters and return values
- Include usage examples for complex functions
- Document any side effects or important behavior

### Architecture Documentation

- Update architecture diagrams for significant changes
- Document design decisions and trade-offs
- Maintain API changelog
- Update deployment guides as needed

## Pull Request Process

### Before Submitting

1. **Ensure all tests pass**
   ```bash
   pytest
   ```

2. **Run quality checks**
   ```bash
   black --check .
   ruff check .
   mypy src/
   ```

3. **Update documentation**
   - Update API documentation
   - Add/update docstrings
   - Update README if needed

4. **Update changelog**
   - Add entry to CHANGELOG.md
   - Follow semantic versioning

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass locally
```

### Review Process

1. **Automated Checks**: CI pipeline must pass
2. **Code Review**: At least one maintainer approval
3. **Testing**: All tests must pass
4. **Documentation**: Must be complete and accurate

### Merge Requirements

- All CI checks passing
- At least one approved review
- No merge conflicts
- Branch up to date with main

## Development Tips

### Local Development

```bash
# Start only required services
docker-compose up -d postgres redis

# Run API locally
python -m src.api.main

# Run worker locally
celery -A src.worker.celery_app worker --loglevel=info
```

### Debugging

- Use structured logging throughout
- Add appropriate log levels
- Use debugger for complex issues
- Monitor metrics during development

### Performance

- Profile code for performance bottlenecks
- Use async/await properly
- Monitor database query performance
- Consider caching for expensive operations

## Getting Help

- **Issues**: Create GitHub issues for bugs or feature requests
- **Discussions**: Use GitHub discussions for questions
- **Documentation**: Check project documentation first
- **Code Review**: Request reviews from maintainers

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to the Distributed Task System!