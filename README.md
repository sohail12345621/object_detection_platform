# 🤖 Vision AI: Object Detection & Tracking Platform

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/sohail12345621/object_detection_platform)

A production-grade AI-powered Object Detection and Tracking Platform built with Python, YOLOv8, OpenCV, FastAPI, Streamlit, and Docker. This project features a highly scalable and modular architecture suitable for real-world AI SaaS products.

## Features

- **Object Detection**: High-performance image and video object detection using Ultralytics YOLOv8.
- **Multi-Object Tracking**: Advanced tracking across video frames using `supervision` and ByteTrack.
- **Modern Dashboard**: An interactive, responsive, dark-themed Streamlit UI.
- **Modular Backend**: FastAPI backend supporting async video processing and RESTful API endpoints.
- **Scalable Deployment**: Fully containerized with Docker and Docker Compose.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI, SQLAlchemy, SQLite
- **AI/ML**: YOLOv8, OpenCV, PyTorch, Supervision (ByteTrack)
- **Deployment**: Docker, Docker Compose

## Quick Start (Docker)

The easiest way to run the platform is using Docker Compose.

1. Clone the repository and navigate to the project root:
   ```bash
   cd object_detection_platform
   ```

2. Start the services:
   ```bash
   docker-compose up --build
   ```

3. Access the platform:
   - **Frontend UI**: [http://localhost:8501](http://localhost:8501)
   - **Backend API Docs**: [http://localhost:8000/api/v1/openapi.json](http://localhost:8000/api/v1/openapi.json)

## Manual Installation (Local Setup)

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Backend API:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Run the Frontend Dashboard (in a new terminal):
   ```bash
   streamlit run frontend/app.py
   ```

## Directory Structure

- `app/`: FastAPI Backend
- `frontend/`: Streamlit Dashboard
- `docker/`: Docker configurations
- `uploads/`: Temporary uploaded files
- `outputs/`: Processed videos and images
- `weights/`: YOLOv8 pretrained model weights

## Future Enhancements
- PostgreSQL integration for robust production databases.
- Real-time webcam WebRTC integration.
- Advanced analytics with interactive time-series charts.
