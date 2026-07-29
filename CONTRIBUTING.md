# Contributing to YOLO Image Search

Thank you for your interest in contributing! This document provides guidelines and instructions.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive criticism
- Help others learn and grow
- Report violations to maintainers

## Getting Started

### 1. Fork the Repository
```bash
# Click "Fork" on GitHub to create your copy
```

### 2. Clone Your Fork
```bash
git clone https://github.com/your-username/yolo-image-search.git
cd yolo-image-search
```

### 3. Set Up Development Environment
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

### 4. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or for bug fixes
git checkout -b bugfix/issue-description
```

## Development Workflow

### Before Making Changes

1. **Check existing issues**: Avoid duplicate work
2. **Discuss major changes**: Create an issue for discussion first
3. **Read relevant docs**: DEVELOPMENT.md and README.md

### Making Changes

1. **Write code** following the style guide (see below)
2. **Add tests** for new functionality
3. **Update documentation** if needed
4. **Run linting and tests**

### Code Style Guide

#### Type Hints (Required)
```python
# Good
def search_records(
    records: list[dict[str, Any]],
    classes: list[str],
    mode: str,
    confidence: float,
) -> list[dict[str, Any]]:
    """Filter records by selected classes."""
    pass

# Bad
def search_records(records, classes, mode, confidence):
    pass
```

#### Docstrings (Required for Public Functions)
```python
def load_metadata(path: str | Path) -> list[dict[str, Any]]:
    """Load and validate JSON metadata.
    
    Args:
        path: File path to metadata JSON
        
    Returns:
        List of normalized image records
        
    Raises:
        FileNotFoundError: File doesn't exist
        ValueError: Invalid JSON or no valid records
    """
    pass
```

#### Naming Conventions
- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private functions: `_leading_underscore`

#### Comments
- Explain WHY, not WHAT
- Keep comments close to code
- Update comments when code changes
- Remove commented-out code

```python
# Good
if isinstance(payload, dict):
    # Support both {records: [...]} and {images: [...]} formats
    payload = payload.get("images", payload.get("records", []))

# Bad
# Loop through records
for record in records:
    pass
```

#### Line Length
- Maximum 88 characters (Black standard)
- Use black for auto-formatting

```bash
black app.py src/ test/
```

### Testing

#### Write Tests
```python
import unittest
from src.image_search.core import search_records

class TestSearchRecords(unittest.TestCase):
    def setUp(self):
        """Prepare test data"""
        self.records = [...]
    
    def test_or_mode_returns_union(self):
        """Test OR mode includes any selected class"""
        result = search_records(self.records, ["cat"], "OR", 0.7)
        self.assertGreater(len(result), 0)
    
    def test_and_mode_returns_intersection(self):
        """Test AND mode includes all selected classes"""
        result = search_records(self.records, ["cat", "dog"], "AND", 0.7)
        # Assert result
```

#### Run Tests
```bash
# All tests
python -m unittest test.test_core -v

# With coverage
coverage run -m unittest test.test_core
coverage report
coverage html
```

#### Test Coverage Requirements
- Minimum 80% code coverage
- All public functions should be tested
- Test both success and error cases
- Use descriptive test names

### Linting and Formatting

#### Format Code
```bash
black app.py src/ test/
```

#### Check Code Quality
```bash
flake8 app.py src/ test/
mypy app.py src/ test/
```

#### Common Issues
```bash
# Too long lines
black --line-length 88 app.py

# Unused imports
flake8 --select=F401 app.py

# Type errors
mypy --strict app.py
```

### Documentation

#### Update README
- Major features need README updates
- Add to appropriate section
- Keep format consistent

#### Update DEVELOPMENT.md
- New development patterns
- API changes
- Testing examples

#### Docstrings
- Use Google-style docstrings
- Include parameter types and return types
- Document exceptions raised

### Committing Changes

#### Commit Message Format
```
type: brief description (50 chars max)

Longer explanation (wrap at 72 chars)
- Point 1
- Point 2

Fixes #123
```

#### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `chore`: Build, dependencies, etc.

#### Examples
```bash
git commit -m "feat: add area filtering to search

- Adds min/max bounding box area parameters
- Updates search_records() function
- Includes unit tests
- Updates API documentation

Closes #456"
```

#### Good Practices
- One logical change per commit
- Write descriptive messages
- Reference related issues
- Keep commits small and focused

### Before Submitting a Pull Request

1. **Update your branch**
```bash
git fetch upstream
git rebase upstream/main
```

2. **Run all checks**
```bash
# Format
black app.py src/ test/

# Lint
flake8 app.py src/ test/

# Type check
mypy app.py src/ test/

# Test
python -m unittest test.test_core -v
coverage run -m unittest test.test_core
coverage report --fail-under=80
```

3. **Verify changes**
- Test locally
- Check for breaking changes
- Ensure backward compatibility

## Pull Request Process

### 1. Push Your Branch
```bash
git push origin feature/your-feature-name
```

### 2. Create Pull Request
- Go to GitHub and click "New Pull Request"
- Select your branch
- Fill in the PR template

### PR Title Format
```
[FEATURE|FIX|DOCS] Brief description
```

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Code coverage > 80%

## Checklist
- [ ] Code follows style guidelines
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Tested on local machine

## Related Issues
Fixes #123
```

### 3. Respond to Feedback
- Be open to suggestions
- Ask for clarification if needed
- Update code based on feedback
- Respond to all comments

### 4. Rebase if Needed
```bash
git fetch upstream
git rebase upstream/main
git push --force-with-lease origin feature/your-feature-name
```

## Review Process

### Code Review Criteria
- Code quality and style
- Test coverage
- Documentation completeness
- Performance impact
- Security considerations
- Backward compatibility

### Approval Process
- Minimum 1 approval required
- All checks must pass
- No unresolved conversations

### Merging
- Squash and merge for small changes
- Rebase and merge for feature branches
- Delete branch after merge

## Reporting Issues

### Bug Reports
```markdown
## Description
What is the bug?

## Steps to Reproduce
1. Step 1
2. Step 2

## Expected Behavior
What should happen?

## Actual Behavior
What actually happens?

## Environment
- OS: Windows/macOS/Linux
- Python: 3.x
- YOLO Image Search: v1.0.0

## Additional Context
Screenshots, logs, etc.
```

### Feature Requests
```markdown
## Description
What feature?

## Problem Statement
What problem does it solve?

## Proposed Solution
How to implement?

## Alternatives Considered
Other approaches?

## Additional Context
Examples, links, etc.
```

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributors page

## Questions?

- Check existing issues/discussions
- Read DEVELOPMENT.md
- Ask in GitHub Discussions
- Email maintainers

## Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## License

By contributing, you agree your code will be licensed under the same license as the project.

Thank you for contributing! 🎉
