# Use official Node.js image as a base
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json into the container
COPY package*.json /app/

# Install the dependencies
RUN npm install

# Copy the entire frontend code into the container
COPY . /app/

# Expose the port the frontend will run on (adjust if needed)
EXPOSE 3000

# Set the command to run the React application
CMD ["npm", "start"]
