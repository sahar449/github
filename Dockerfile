# בסיס: פייתון 3.9 (יכול לשנות לגרסה אחרת אם תרצה)
FROM python:3.9-slim

# מתקינים תלותים
RUN pip install --no-cache-dir flask mysql-connector-python

# יוצרים תיקייה לאפליקציה
WORKDIR /app

# מעתיקים את הקוד
COPY app.py .

# פותחים פורט 5000
EXPOSE 5000

# מריצים את האפליקציה
CMD ["python", "app.py"]
