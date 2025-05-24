# Contributing to Pickyfy

Thank you for your interest in contributing to Pickyfy! This document provides guidelines and information for contributors.

## able of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Contribution Guidelines](#contribution-guidelines)
5. [Pull Request Process](#pull-request-process)
6. [Issue Guidelines](#issue-guidelines)
7. [Style Guidelines](#style-guidelines)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

### Our Standards
- **Be Respectful**: Treat everyone with respect and kindness
- **Be Inclusive**: Welcome newcomers and diverse perspectives
- **Be Collaborative**: Work together towards common goals
- **Be Professional**: Maintain professional communication

### Unacceptable Behavior
- Harassment, discrimination, or offensive comments
- Personal attacks or trolling
- Spam or promotional content
- Publishing private information without permission

## Getting Started

### Prerequisites
- Python 3.8+
- Git
- GitHub account
- Basic knowledge of machine learning and web development

### Development Setup
1. **Fork the repository**
   ```bash
   # Click 'Fork' on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/Pickyfy.git
   cd Pickyfy
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/Aqilrmm/Pickyfy.git
   ```

## Development Workflow

### 1. Create Feature Branch
```bash
# Update your fork
git checkout main
git fetch upstream
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Write clean, well-documented code
- Follow existing code style and patterns
- Add tests for new functionality
- Update documentation as needed

### 3. Test Changes
```bash
# Run the application
streamlit run app.py

# Test manually
# - Check all features work
# - Test different user scenarios
# - Verify UI responsiveness
```

### 4. Commit Changes
```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add new recommendation algorithm"
```

### 5. Push and Create PR
```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

## Contribution Guidelines

### Types of Contributions

#### Bug Fixes
- Fix existing bugs
- Improve error handling
- Performance optimizations

#### New Features
- New recommendation algorithms
- UI/UX improvements
- Analytics enhancements
- API integrations

#### Documentation
- README improvements
- Code comments
- Setup guides
- API documentation

#### Testing
- Unit tests
- Integration tests
- Performance tests
- User acceptance tests

### Priority Areas
1. **Algorithm Improvements**: Better recommendation accuracy
2. **Performance**: Faster response times and lower memory usage
3. **User Experience**: Better UI/UX and accessibility
4. **Data Integration**: Support for external data sources
5. **Documentation**: Clear guides and examples

## Pull Request Process

### Before Submitting
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] No console errors or warnings
- [ ] Feature works on different screen sizes

### PR Title Format
Use conventional commit format:
- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `style:` formatting changes
- `refactor:` code refactoring
- `test:` adding tests
- `chore:` maintenance tasks

### PR Description Template
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Manual testing completed
- [ ] All features work as expected
- [ ] No console errors

## Screenshots (if applicable)
Add screenshots of UI changes.

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

### Review Process
1. **Automated Checks**: CI/CD will run basic checks
2. **Code Review**: Maintainers will review your code
3. **Testing**: Manual testing of new features  
4. **Approval**: At least one maintainer approval required
5. **Merge**: Maintainer will merge the PR

## Issue Guidelines

### Before Creating Issues
1. **Search Existing Issues**: Check if issue already exists
2. **Use Latest Version**: Ensure you're using the latest code
3. **Minimal Reproduction**: Create minimal example that reproduces the issue

### Issue Types

#### Bug Report
```markdown
**Describe the Bug**
Clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g. Windows 10]
- Python: [e.g. 3.9.0]
- Browser: [e.g. Chrome 95]

**Additional Context**
Any other context about the problem.
```

#### Feature Request
```markdown
**Is your feature request related to a problem?**
Clear description of the problem.

**Describe the solution you'd like**
Clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions you've considered.

**Additional context**
Screenshots, mockups, or examples.
```

#### Question/Support
```markdown
**Question**
Clear question about the project.

**Context**
What you're trying to achieve.

**What you've tried**
Steps you've already taken.
```

## Style Guidelines

### Python Code Style

#### Follow PEP 8
```python
# Good
def calculate_user_similarity(user1_ratings, user2_ratings):
    """Calculate cosine similarity between two users."""
    return cosine_similarity([user1_ratings], [user2_ratings])[0][0]

# Bad  
def calcUsrSim(u1,u2):
    return cosine_similarity([u1],[u2])[0][0]
```

#### Documentation
```python
def collaborative_filtering_recommendations(self, user_id, n_recommendations=5):
    """
    Generate recommendations using collaborative filtering.
    
    Args:
        user_id (str): Target user ID
        n_recommendations (int): Number of recommendations to return
        
    Returns:
        list: List of recommended product IDs
        
    Raises:
        ValueError: If user_id is not found
    """
    # Implementation here
```

#### Error Handling
```python
# Good
try:
    recommendations = self.generate_recommendations(user_id)
except KeyError:
    st.error(f"User {user_id} not found in dataset")
    recommendations = self.popular_recommendations()
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    recommendations = []

# Bad
recommendations = self.generate_recommendations(user_id)  # No error handling
```

### Streamlit Code Style

#### Component Organization
```python
# Good - Organized layout
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Users", len(users))
with col2:
    st.metric("Products", len(products))
with col3:
    st.metric("Transactions", len(transactions))

# Bad - Cluttered
st.metric("Users", len(users))
st.metric("Products", len(products))
st.metric("Transactions", len(transactions))
```

#### State Management
```python
# Good - Use session state appropriately
if 'recommender' not in st.session_state:
    st.session_state.recommender = ProductRecommender()

# Bad - Recreate objects unnecessarily
recommender = ProductRecommender()  # Creates new instance each time
```

### Git Commit Messages

#### Format
```
<type>(<scope>): <description>

<body>

<footer>
```

#### Examples
```bash
# Good
feat(recommendations): add hybrid recommendation algorithm

Combines collaborative filtering and content-based filtering
with configurable weights for better accuracy.

Closes #123

# Bad
fix bug
```

#### Types
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

## Recognition

### Contributors Wall
All contributors will be recognized in:
- `README.md` contributors section
- Release notes for their contributions
- Special mentions for significant contributions

### Contribution Levels
- **Core Contributor**: 10+ merged PRs
- **Feature Contributor**: Added major features
- **Bug Hunter**: Fixed multiple bugs
- **Documentation Master**: Improved documentation significantly
- **Test Champion**: Added comprehensive tests

## Development Resources

### Useful Links
- **Streamlit Documentation**: https://docs.streamlit.io
- **Scikit-learn**: https://scikit-learn.org/stable/
- **Pandas**: https://pandas.pydata.org/docs/
- **Plotly**: https://plotly.com/python/

### Learning Resources
- **Recommendation Systems**: [Andrew Ng's Course](https://www.coursera.org/learn/machine-learning)
- **Streamlit**: [30 Days of Streamlit](https://30days.streamlit.app/)
- **Python Best Practices**: [Real Python](https://realpython.com/)

## Questions?

If you have questions about contributing:

1. **Check existing issues and discussions**
2. **Read the documentation thoroughly**
3. **Ask in GitHub Discussions**
4. **Contact maintainers directly**

---

**Thank you for contributing to Pickyfy!**

Every contribution, no matter how small, makes this project better for everyone.