# -------------------------------------------------------------
# Dockerfile for the mobile Expo app
# -------------------------------------------------------------
# NOTE: There is an issue with containerizing the Expo app.
# This Dockerfile serves as a reference for future implementations.
# Currently, the mobile app runs locally without Docker.
# -------------------------------------------------------------

# Use Node.js 20 as the base image
FROM node:20

# Set the working directory inside the container
WORKDIR /app

# Install Expo CLI globally
RUN npm install -g expo-cli

# Copy package.json and package-lock.json to the container
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app code into the container
COPY . .

# Start the Expo app using tunnel mode
CMD ["expo", "start", "--tunnel"]
