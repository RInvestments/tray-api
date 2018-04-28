NAME="app.py"
NUM_WORKERS=3

gunicorn $NAME:app -b 127.0.0.1:5000 \
  --name $NAME \
  --workers $NUM_WORKERS \
