# Flask chat
A simple demo chat app made with flask and SocketIO

## System requirements
- SQLite
- Python 3
- Virtualenv
- RabitMQ (see docs dir)


## Install
1. Create virtual env
```bash
$ virtualenv venv -p python3
```

2. Install requirements
```bash
$ pip install -r requirements.txt
```

3. Create the table
```bash
$ flask init-db
```

4. Open new terminal tab/window and run the celery worker
```bash
$ celery -A celery_worker.celery worker --loglevel=info
```