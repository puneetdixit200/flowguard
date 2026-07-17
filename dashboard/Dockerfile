# =========================
# Stage 1: Build React app
# =========================
FROM node:22-alpine AS build

# All commands run inside /app
WORKDIR /app

# Copy package files first so Docker can cache dependencies
COPY package.json package-lock.json ./

# Install exact dependency versions
RUN npm ci

# Copy index.html, src/, public/, vite.config.js, etc.
COPY . .

# Build the React application
# Vite creates the final files inside /app/dist
RUN npm run build


# =========================
# Stage 2: Serve with Nginx
# =========================
FROM nginx:alpine

# Remove Nginx's default website
RUN rm -rf /usr/share/nginx/html/*

# Copy the compiled React files from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Nginx listens on port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
