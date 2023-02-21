## Setup
Note: I'm using Python 3.9.1
- Create virtual environment
- Note: Ensure you have current project copied at your path
- Install dependencies using requirement.txt
```
pip install -r requirement.txt
```
## Run Migration
```
python manage.py migrate
```
## Run Script to Ingest Data
```
python manage.py migrate_user_data  
```
## Run Server
To run Django server locally, run below command:
```
python manage.py runserver
```
This will start Django server running on port 8000.
