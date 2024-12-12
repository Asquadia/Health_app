FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y make && apt-get clean

COPY requirements.txt .
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000 5001 5002

RUN echo '#!/bin/bash\n\
source /app/venv/bin/activate\n\
python backend/app.py & \n\
python bmi_service/app.py & \n\
python bmr_service/app.py & \n\
wait' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]