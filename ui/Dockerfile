# Stage 1: build
FROM node:22-alpine AS build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# Stage 2: production with Nginx
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

# Expose default port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
