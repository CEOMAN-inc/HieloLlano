FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias directamente
RUN pip install --no-cache-dir fastapi uvicorn[standard] python-jose[cryptography] passlib[bcrypt]


# Copiar el código fuente
COPY ./backend/app ./app

# Comando para iniciar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
