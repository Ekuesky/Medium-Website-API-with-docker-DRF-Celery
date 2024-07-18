# Set the base Python version
ARG PYTHON_VERSION=3.10.14-bullseye
FROM python:${PYTHON_VERSION} as python

# FIRST STAGE (BUILD STAGE)
FROM python as python-build-stage

# Set the build environment (local by default)
ARG BUILD_ENVIRONMENT=local_req

# Install dependencies for building Python packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

# Copy requirements files
COPY ./requirements /requirements

# Install Python dependencies into wheels directory
RUN pip wheel --wheel-dir /wheels -r /requirements/${BUILD_ENVIRONMENT}.txt

# SECOND STAGE (RUN STAGE)
FROM python as python-run-stage

# Set the build environment (local by default)
ARG BUILD_ENVIRONMENT=local

# Set the working directory for the application
ARG APP_HOME=/app
WORKDIR ${APP_HOME}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

# Install runtime dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    && apt-get purge -y --auto-remove -o APT:AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Copy the wheel files from the build stage to the current stage
COPY --from=python-build-stage /wheels /wheels

# Install the Python dependencies from the wheels directory
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/*

# Copy the rest of the application code
COPY . ${APP_HOME}

# Copy entrypoint script and make it executable
COPY ./docker/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# Copy start script and make it executable
COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./docker/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./docker/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower


# Set the entrypoint for the container
ENTRYPOINT ["/entrypoint"]
