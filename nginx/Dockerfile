# Uses the Nginx stable version based on Alpine Linux as the base image
FROM nginx:stable-alpine

# Removes the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copies a custom Nginx configuration file into the image
COPY nginx.conf /etc/nginx/conf.d
