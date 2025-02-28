import streamlit as st
from PIL import Image
from datetime import datetime
import requests
from io import BytesIO

# Backend URL
backend_url = "http://127.0.0.1:8080"


# App Title
st.title("Geotagged Image Capture")

# Text input for note or prompt
note = st.text_input("Enter a note or prompt:")

# Camera input for capturing image
image_file = st.camera_input("Capture an image")

# Dummy coordinates for demonstration (Replace with real-time GPS coordinates)
latitude = 28.6139  # Example: New Delhi Latitude
longitude = 77.2090  # Example: New Delhi Longitude

# If an image is captured
if image_file is not None:
    # Display the image
    image = Image.open(image_file)
    st.image(image, caption="Captured Image", use_column_width=True)

    # Display the note
    st.markdown(f"**Note:** {note}")
    st.markdown(f"**Coordinates:** Latitude: {latitude}, Longitude: {longitude}")

    # Save and upload image and metadata
    if st.button("Submit Report"):
        # Convert image to bytes for upload
        img_bytes = BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        
        # Prepare the data for POST request
        files = {'image': ("image.png", img_bytes, "image/png")}
        data = {
            'latitude': latitude,
            'longitude': longitude,
            'location': 'New Delhi',
            'description': note
        }
        
        # Send POST request to FastAPI backend
        response = requests.post(f"{backend_url}/user/report/", files=files, data=data)
        
        if response.status_code == 200:
            st.success("Report submitted successfully!")
        else:
            st.error("Failed to submit report.")
