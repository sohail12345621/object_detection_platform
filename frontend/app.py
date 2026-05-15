import streamlit as st
import requests
import os
from PIL import Image

# Setup page configuration
st.set_page_config(
    page_title="AI Object Detection Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for dark futuristic theme
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .sidebar .sidebar-content {
        background: #1a1c23;
    }
    h1, h2, h3 {
        color: #00ffcc !important;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background-color: #00ffcc;
        color: #0e1117;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00ccaa;
        box-shadow: 0 0 10px #00ffcc;
    }
    .metric-card {
        background-color: #1a1c23;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00ffcc;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Define API URL
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

st.title("🤖 Vision AI: Object Detection & Tracking")
st.markdown("---")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Image Detection", "Video Tracking", "Live Webcam"])

st.sidebar.markdown("---")
st.sidebar.header("Settings")
model_choice = st.sidebar.selectbox("Select Model", ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt"])
conf_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.25, 0.05)

if page == "Dashboard":
    st.header("Overview Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card"><h3>Total Processed</h3><h1>1,245</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>Active Tasks</h3><h1>2</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>System Uptime</h3><h1>99.9%</h1></div>', unsafe_allow_html=True)

    st.markdown("### Recent Detections")
    # Placeholder for a chart or table
    st.info("Analytics charts will be populated here as detections occur.")

elif page == "Image Detection":
    st.header("Upload Image for Detection")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Original Image', use_column_width=True)
        
        if st.button("Run Detection"):
            with st.spinner("Processing..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "image/jpeg")}
                response = requests.post(
                    f"{API_URL}/detect/image", 
                    files=files,
                    params={"model_name": model_choice, "conf_threshold": conf_threshold}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    file_id = data["id"]
                    
                    # Fetch result
                    result_response = requests.get(f"{API_URL}/detect/result/{file_id}")
                    if result_response.status_code == 200:
                        st.success("Detection Complete!")
                        st.image(result_response.content, caption="Annotated Image", use_column_width=True)
                    else:
                        st.error("Failed to retrieve result.")
                else:
                    st.error(f"Error: {response.text}")

elif page == "Video Tracking":
    st.header("Upload Video for Tracking")
    uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "avi", "mov"])
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        
        if st.button("Run Tracking"):
            with st.spinner("Starting video processing... (This may take a while)"):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "video/mp4")}
                response = requests.post(
                    f"{API_URL}/detect/video", 
                    files=files,
                    params={"model_name": model_choice, "conf_threshold": conf_threshold}
                )
                
                if response.status_code == 200:
                    st.success("Video processing started! Please check back later for results.")
                else:
                    st.error(f"Error: {response.text}")

elif page == "Live Webcam":
    st.header("Real-time Webcam Detection")
    st.warning("WebRTC integration required for browser-based live streaming. This placeholder demonstrates where it will be.")
    # For actual implementation, streamlit-webrtc would be used here.
    st.info("Please implement `streamlit-webrtc` configuration here.")

