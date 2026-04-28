# Use an official Python runtime as a parent image
FROM python:3.14-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY --chown=568:568 requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY --chown=568:568 . /app/



# Ensure database directory has write permissions
RUN chown -R 568:568 /app/lunar_birthday_config
RUN chmod 755 /app/lunar_birthday_config

USER 568

# Set Python path and working directory to the Django project
ENV PYTHONPATH=/app
WORKDIR /app/lunar_birthday_config

# Expose the port Django runs on
EXPOSE 9000

# Run the application (using Gunicorn for production)
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "lunar_birthday_config.wsgi:application"]