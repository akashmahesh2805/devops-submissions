FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ex3_flash_sale.py ./

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "ex3_flash_sale:app"]
