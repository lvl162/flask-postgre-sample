pip3 install -r requirements.txt
gunicorn -w 2 'app:app'