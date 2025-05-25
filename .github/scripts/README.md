# GitHub Issue Creation Scripts

This directory contains scripts to help manage GitHub issues programmatically.

## create_issues.py

This script creates GitHub issues for both frontend and backend bugs that were intentionally introduced for testing purposes.

### Prerequisites

1. Python 3.6+
2. GitHub Personal Access Token with `repo` scope

### Setup

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your GitHub token as an environment variable:
   ```bash
   export GITHUB_TOKEN=your_github_token_here
   ```

### Usage

Run the script to create all issues:

```bash
python create_issues.py
```

This will create 10 issues (5 frontend, 5 backend) with appropriate labels and descriptions.

### Issue Types

#### Frontend Issues
1. Undefined Function Error in Welcome Component
2. Infinite Loop in Computed Property
3. Broken Image in Welcome Component
4. Layout Issues in Welcome Component
5. Missing Error Boundaries

#### Backend Issues
1. SQL Injection in Tasks Endpoint
2. Missing Access Control in Tasks Endpoint
3. Information Disclosure in Error Messages
4. Add Input Validation
5. No Transaction Management

## Notes

- The script requires a GitHub Personal Access Token with the `repo` scope.
- Issues will be created in the repository specified by `REPO_OWNER` and `REPO_NAME` in the script.
- The script is idempotent - running it multiple times will create duplicate issues.
