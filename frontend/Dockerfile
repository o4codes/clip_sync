# Use an official Node.js runtime as a parent image
FROM node:16.17.0-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the package.json and package-lock.json files into the container at /app
COPY package*.json ./

# Install any needed packages specified in package.json
RUN npm install

# Copy the rest of the application code into the container at /app
COPY . .

# Build the Vue.js app for production
RUN npm run build
