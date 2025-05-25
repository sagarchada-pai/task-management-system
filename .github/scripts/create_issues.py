import os
import requests
from typing import List, Dict

# GitHub repository details
REPO_OWNER = "sagarchada-pai"
REPO_NAME = "task-management-system"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Headers for GitHub API
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def create_issue(title: str, body: str, labels: List[str] = None) -> Dict:
    """Create a GitHub issue."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    data = {
        "title": title,
        "body": body,
        "labels": labels or []
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def main():
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN environment variable not set")
        print("Please set your GitHub token as an environment variable:")
        print("export GITHUB_TOKEN=your_github_token_here")
        return

    # Frontend Issues
    frontend_issues = [
        {
            "title": "Fix: Undefined Function Error in Welcome Component",
            "body": "## Description\nThe Welcome component has a button that triggers a non-existent function, causing runtime errors.\n\n## Steps to Reproduce\n1. Navigate to the home page\n2. Click the red button labeled 'Click me to trigger an error'\n3. Check browser console for error\n\n## Expected Behavior\nEither implement the function or remove the button if not needed.\n\n## Files Affected\n- `frontend/src/components/TheWelcome.vue`",
            "labels": ["bug", "frontend", "high-priority"]
        },
        {
            "title": "Fix: Infinite Loop in Computed Property",
            "body": "## Description\nThe `buggyComputed` property in TheWelcome.vue causes an infinite loop by modifying its own dependency.\n\n## Steps to Reproduce\n1. Open the browser's developer tools\n2. Navigate to the home page\n3. Observe the console for 'Maximum recursive updates' warning\n\n## Expected Behavior\nThe computed property should not modify its own dependencies.\n\n## Files Affected\n- `frontend/src/components/TheWelcome.vue`",
            "labels": ["bug", "frontend", "high-priority"]
        },
        {
            "title": "Fix: Broken Image in Welcome Component",
            "body": "## Description\nThe Welcome component references a non-existent image file.\n\n## Steps to Reproduce\n1. Load the home page\n2. Look for the broken image icon in the header section\n\n## Expected Behavior\nEither add the missing image or remove the image tag.\n\n## Files Affected\n- `frontend/src/components/TheWelcome.vue`",
            "labels": ["bug", "frontend", "low-priority"]
        },
        {
            "title": "Fix: Layout Issues in Welcome Component",
            "body": "## Description\nThere's an absolutely positioned red square that covers UI elements.\n\n## Steps to Reproduce\n1. Load the home page\n2. Notice the red square covering the top-left corner\n\n## Expected Behavior\nRemove or properly position the absolutely positioned element.\n\n## Files Affected\n- `frontend/src/components/TheWelcome.vue`",
            "labels": ["bug", "frontend", "medium-priority"]
        },
        {
            "title": "Fix: Missing Error Boundaries",
            "body": "## Description\nThe application lacks error boundaries, causing the entire app to crash on errors.\n\n## Steps to Reproduce\n1. Trigger any runtime error in the application\n2. Observe the entire application crashes\n\n## Expected Behavior\nImplement error boundaries to gracefully handle errors.\n\n## Files Affected\n- Multiple frontend components\n\n## Additional Context\nConsider using Vue's errorCaptured hook.",
            "labels": ["enhancement", "frontend", "high-priority"]
        }
    ]

    # Backend Issues
    backend_issues = [
        {
            "title": "Security: SQL Injection in Tasks Endpoint",
            "body": "## Description\nThe tasks endpoint is vulnerable to SQL injection due to direct string interpolation in SQL queries.\n\n## Steps to Reproduce\n1. Send a POST request to `/api/v1/tasks/` with a malicious payload\n2. Observe the database query in logs\n\n## Expected Behavior\nUse parameterized queries or ORM methods to prevent SQL injection.\n\n## Files Affected\n- `backend/app/api/v1/endpoints/tasks.py`\n\n## Severity\nCritical",
            "labels": ["security", "backend", "critical"]
        },
        {
            "title": "Security: Missing Access Control in Tasks Endpoint",
            "body": "## Description\nThe tasks endpoint doesn't properly verify if the user has access to the requested resources.\n\n## Steps to Reproduce\n1. Authenticate as a user\n2. Access tasks that belong to other users\n\n## Expected Behavior\nImplement proper access control checks.\n\n## Files Affected\n- `backend/app/api/v1/endpoints/tasks.py`\n\n## Severity\nHigh",
            "labels": ["security", "backend", "high-priority"]
        },
        {
            "title": "Bug: Information Disclosure in Error Messages",
            "body": "## Description\nError messages reveal internal system details.\n\n## Steps to Reproduce\n1. Trigger an error in the API\n2. Observe the detailed error message\n\n## Expected Behavior\nReturn generic error messages in production.\n\n## Files Affected\n- Multiple backend endpoints\n\n## Severity\nMedium",
            "labels": ["bug", "security", "backend"]
        },
        {
            "title": "Enhancement: Add Input Validation",
            "body": "## Description\nMissing input validation in multiple endpoints.\n\n## Expected Behavior\nAdd proper input validation using Pydantic models.\n\n## Files Affected\n- Multiple backend endpoints\n\n## Severity\nMedium",
            "labels": ["enhancement", "backend"]
        },
        {
            "title": "Bug: No Transaction Management",
            "body": "## Description\nDatabase operations are not wrapped in transactions.\n\n## Impact\nCould lead to data inconsistency.\n\n## Expected Behavior\nUse database transactions for related operations.\n\n## Files Affected\n- Multiple backend endpoints\n\n## Severity\nHigh",
            "labels": ["bug", "backend", "database"]
        }
    ]

    # Create issues
    print("Creating frontend issues...")
    for issue in frontend_issues:
        result = create_issue(issue["title"], issue["body"], issue["labels"])
        print(f"Created issue: {result.get('html_url')}")
    
    print("\nCreating backend issues...")
    for issue in backend_issues:
        result = create_issue(issue["title"], issue["body"], issue["labels"])
        print(f"Created issue: {result.get('html_url')}")

if __name__ == "__main__":
    main()
