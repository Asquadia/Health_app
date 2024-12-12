FROM python:3.11-slim

WORKDIR /app


COPY requirements.txt .


RUN python -m venv /app/venv


ENV PATH="/app/venv/bin:$PATH"


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 5000 5001 5002


RUN echo '#!/bin/bash\nsource /app/venv/bin/activate\npython backend/app.py & \npython bmi_service/app.py & \npython bmr_service/app.py & \nwait' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
