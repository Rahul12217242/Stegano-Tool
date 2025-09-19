# Stegano-Tool

A web-based steganography tool built with Python and Flask that allows users to hide a secret text message within an image file and later extract it. This project demonstrates a classic cybersecurity technique through a containerized web application.

## Features

-   **Encode:** Upload a PNG or BMP image and a secret message to generate a new image with the message hidden inside.
-   **Decode:** Upload a previously encoded image to reveal the hidden secret message.
-   **Error Handling:** Provides user feedback for invalid file types or when a message is too large for the chosen image.

## Tech Stack

-   **Backend:** Python, Flask
-   **Steganography Logic:** `stegano`, `Pillow`
-   **Containerization:** Docker
-   **Deployment:** Hosted on AWS EC2
-   **Frontend:** HTML, CSS

## Running Locally with Docker

1.  **Prerequisites:** Make sure you have Docker installed and running.

2.  **Build the Docker Image:**
    From the root of the project directory, run:
    ```bash
    docker build -t stegano-app .
    ```

3.  **Run the Docker Container:**
    ```bash
    docker run -d --name my-stegano-app -p 8000:5000 stegano-app
    ```

4.  **Access the Application:**
    Open your web browser and navigate to `http://localhost:8000`.
