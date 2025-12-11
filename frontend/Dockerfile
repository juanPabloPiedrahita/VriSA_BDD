# -----------------------------------------------------------------------------
# Dockerfile for the frontend application (Node.js / Vite)
#
# This Dockerfile sets up the development environment for the frontend.
# It uses Node 20, installs dependencies, and exposes the Vite dev server.
#
# Instructions:
#   1. Build the image:
#        docker build -t frontend .
#   2. Run the container:
#        docker run -p 5173:5173 frontend
# -----------------------------------------------------------------------------

# Use official Node 20 image as base
FROM node:20

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the frontend source code
COPY . .

# Expose the Vite development server port
EXPOSE 5173

# Command to run the frontend in development mode, accessible from any host
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]