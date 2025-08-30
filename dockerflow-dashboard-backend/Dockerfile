# Etap 1: budowa zależności
FROM python:3.12-slim AS builder

# Ustaw workdir
WORKDIR /app

# Zainstaluj build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Skopiuj pliki zależności
COPY requirements.txt .

# Zainstaluj zależności do katalogu /install
RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt

# Etap 2: finalny lekki obraz
FROM python:3.12-slim

WORKDIR /app

# Skopiuj zbudowane pakiety
COPY --from=builder /install /usr/local

# Skopiuj cały kod aplikacji
COPY . .

# Tworzymy nie-root usera
RUN useradd -m dockerflow && chown -R dockerflow:dockerflow /app
USER dockerflow

# Eksponujemy port FastAPI
EXPOSE 8000

# Komenda startowa
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
