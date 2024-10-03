# Use official Node.js image
FROM node:20.16.0

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy project files
COPY . .

# Expose Next.js port
EXPOSE 3000

# Start Next.js
CMD ["npm", "run", "dev"]
