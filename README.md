# AI Ticketing System

A Flask-based ticketing system with AI assistance capabilities.

## Prerequisites

- Python 3.11 or higher
- pipenv

## Installation

1. Install pipenv if you haven't already:
   ```bash
   pip install pipenv
   ```

2. Clone the repository:
   ```bash
   git clone <repository-url>
   cd LocalAIAssistant-Ticketing
   ```

3. Install dependencies using pipenv:
   ```bash
   pipenv install
   ```

4. Create a `.env` file in the project root with your configuration:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///instance/tickets.db
   AD_SERVER=ldap://your-ad-server:389
   AD_DOMAIN=yourdomain.com
   AD_BASE_DN=DC=yourdomain,DC=com
   AD_USER_SEARCH_FILTER=(sAMAccountName={})
   AD_GROUP_SEARCH_FILTER=(memberOf=CN=Technicians,OU=Groups,DC=yourdomain,DC=com)
   AD_USERNAME=service_account
   AD_PASSWORD=service_account_password
   ```

## Running the Application

1. Activate the virtual environment:
   ```bash
   pipenv shell
   ```

2. Initialize the database:
   ```bash
   flask db upgrade
   ```

3. Run the application:
   ```bash
   flask run
   ```

## Development

- To add a new package:
  ```bash
  pipenv install <package-name>
  ```

- To add a development package:
  ```bash
  pipenv install --dev <package-name>
  ```

- To update all packages:
  ```bash
  pipenv update
  ```

## Project Structure

```
LocalAIAssistant-Ticketing/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── templates/
│   └── static/
├── instance/
├── migrations/
├── .env
├── .gitignore
├── Pipfile
├── Pipfile.lock
└── README.md
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
