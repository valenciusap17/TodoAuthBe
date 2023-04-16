## Backend

1. Create/activate the vitrual environment

```
python -m venv env
.\env\Scripts\activate
```

2. Install all the dependencies required

```
pip install -r requirements.txt
```

3. Migrate the database

```
python manage.py migrate
```

4. Run the app

```
python manage.py runserver
```
