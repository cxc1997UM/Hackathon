# frontend/Dockerfile
FROM node:latest

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of the application
COPY . .

# Expose Vite's default port
EXPOSE 5173

# Start development server (host flag allows external access)
CMD ["npm", "run", "dev", "--", "--host"]