uvicorn main:app --reload
rem gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker