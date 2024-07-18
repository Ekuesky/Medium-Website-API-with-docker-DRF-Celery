FROM redis:7-alpine

# Copy the start.sh script into the container
COPY ./docker/local/redis/start.sh /usr/local/bin/start.sh

# Make the script executable
RUN chmod +x /usr/local/bin/start.sh

# Set the entrypoint to use the start.sh script
ENTRYPOINT ["/usr/local/bin/start.sh", "redis-server"]
