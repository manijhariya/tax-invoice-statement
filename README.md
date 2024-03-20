# tax-invoice-statement

1. Install all dependecies
```bash
pip install -r requirements.txt
```

2. Make necessary migrations
```bash
python3 manage.py makemigrations
```

3. Migrate your local migrations
```bash
python3 manage.py migrate
```

4. Run Django Server
```bash
python3 manage.py runserver
```

## Brower Access
1. Go to http://localhost:8000/etl/ -- for uploading file and building database from invoice files
2. Got to http://localhost:8000/operations/ -- for performing the operations on sql. 