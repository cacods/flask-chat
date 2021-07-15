# Flask chat
A simple demo chat app made with flask and SocketIO

## System requirements
- SQLite
- Python 3
- Virtualenv
- RabitMQ (see docs dir)


## Install
1. Clone repository and cd into `flask_app` folder


2. Create virtual env
```bash
$ virtualenv venv -p python3
```

3. Install requirements
```bash
$ pip install -r requirements.txt
```

4. Export flask environment variables
```bash
$ export FLASK_APP=chat_app
$ export FLASK_ENV=development
```

4. Create the table
```bash
$ flask init-db
```

5. Open new terminal tab/window and run the celery worker
```bash

$ celery -A celery_worker.celery worker --loglevel=info
```

6. Run the app
```bash
$ flask run
```