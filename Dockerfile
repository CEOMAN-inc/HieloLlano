FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar el backend al contenedor (asegúrate de que contiene la carpeta "app")
COPY ./backend /app

# Instalar dependencias directamente
RUN pip install --no-cache-dir fastapi uvicorn psycopg2-binary python-dotenv pydantic[email] passlib[bcrypt] python-jose[cryptography] python-multipart bcrypt==3.2.0

# Exponer el puerto de la aplicación
EXPOSE 8000

# Comando para correr la app con recarga automática (dev)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
