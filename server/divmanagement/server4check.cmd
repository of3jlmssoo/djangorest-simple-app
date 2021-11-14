cp db.sqlite3 db.sqlite3.backup
cp db.sqlite3.empty db.sqlite3
python manage.py runserver
cp db.sqlite3.backup db.sqlite3
