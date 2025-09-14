# syntax=docker/dockerfile:1

# Build stage
FROM golang:1.25 as builder
WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code
COPY . .

# Build the Go app
RUN CGO_ENABLED=0 GOOS=linux go build -o app .

# Final stage
FROM alpine:latest
WORKDIR /app

# Copy the binary from builder
COPY --from=builder /app/app ./app

# Expose port (change if needed)
EXPOSE 8080

# Command to run
CMD ["./app"]
