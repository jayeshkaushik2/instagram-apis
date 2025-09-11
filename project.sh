if [ "$1" = "dev" ]; then
    python manage.py collectstatic
    python manage.py reset_db
    python manage.py migrate
    uvicorn instagramCloneApis.asgi:application --host 0.0.0.0 --port 8080 --reload
fi

if [ "$1" = "format" ]; then
    black chats
fi