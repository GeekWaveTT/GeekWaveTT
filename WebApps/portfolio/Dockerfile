# Use a minimal NGINX image
FROM nginx:alpine

# Remove the default NGINX web files
RUN rm -rf /usr/share/nginx/html/*

# Copy your custom website files to the web root
COPY . /usr/share/nginx/html

# Expose port 80 (default for NGINX)
EXPOSE 80

# Start NGINX server
CMD ["nginx", "-g", "daemon off;"]
