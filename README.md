# WebFileSystem

A web-based file management system built using Django that supports folder/file management, user authentication, and real-time monitoring.

## Features
- Create, rename, delete, upload, and download files and folders.
- User authentication (Login, Register, Password Reset).
- File trash system with restore and permanent deletion.
- System monitoring for admins (disk usage, CPU usage).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Xherloque/Web-File-System.git

2. Navigate to the project directory:
    cd Web-File-System

3. Create and activate a virtual environment:
    python -m venv env
    source env/bin/activate  # On Windows: .\env\Scripts\activate

4. Install the required dependencies:
    pip install -r requirements.txt

5. Apply database migrations:
    python manage.py migrate

6. Start the development server:
    python manage.py runserver


## Usage
Access the web application in your browser at http://127.0.0.1:8000/.
Register a user account to access file management features.
 
## Changing the Database Configuration

By default, the project is configured to use SQLite, which is a lightweight database for development purposes. 
To switch to a different database (e.g., MySQL or PostgreSQL), follow these steps:

1. Install the required database adapter:
   - For MySQL:
     ```bash
     pip install mysqlclient
     ```
   - For PostgreSQL:
     ```bash
     pip install psycopg2
     ```

2. Update the `DATABASES` setting in `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',  # Use 'postgresql' for PostgreSQL
           'NAME': 'your_database_name',
           'USER': 'your_database_user',
           'PASSWORD': 'your_database_password',
           'HOST': 'your_database_host',  # Use 'localhost' for local installations
           'PORT': 'your_database_port',  # Default MySQL port: 3306, PostgreSQL port: 5432
       }
   }
3. Apply database migrations
    python manage.py migrate

4. Start development server
    python manage.py runserver
    
## For additional configuration details, refer to the Django Database Documentation.


## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, please contact sherloque7374@gmail.com
