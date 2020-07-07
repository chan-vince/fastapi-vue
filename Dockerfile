# Build stage for frontend
FROM node:lts-alpine as build-stage

WORKDIR /frontend
COPY frontend_gui/practice-manager/package*.json ./
RUN npm install
COPY frontend_gui/practice-manager ./
RUN npm run build

# Base the production image fromfrontend the python image
FROM python:3.8-slim
RUN apt update -y && apt upgrade -y

# Install nginx
RUN apt install -y nginx

# Bring over the build artifacts from the node build stage
COPY --from=build-stage /frontend/dist /app
COPY nginx.conf /etc/nginx/nginx.conf

# Install python poetry
RUN apt install -y curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"

# Install backend deps
WORKDIR /backend
COPY backend_api/poetry.lock .
COPY backend_api/pyproject.toml .
RUN poetry install

# Copy source for the backend
COPY mock_data /mock_data
COPY backend_api .
COPY entrypoint.sh .

EXPOSE 80
EXPOSE 5000
CMD ["./entrypoint.sh"]