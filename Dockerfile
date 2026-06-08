# =========================================================
# ÉTAPE 1 : La construction (Build stage)
# =========================================================
FROM dhi.io/python:3-dev AS builder
WORKDIR /app
RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =========================================================
# ÉTAPE 2 : L'exécution (Runtime stage)
# =========================================================
FROM dhi.io/python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY app/ /app/app/
COPY run.py /app/
COPY instance/ /tmp/instance/

EXPOSE 5000

CMD ["gunicorn", "-w", "1", "--threads", "4", "-b", "0.0.0.0:5000", "--timeout", "60", "app:create_app()"]
