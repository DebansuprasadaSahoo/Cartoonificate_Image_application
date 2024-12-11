import cv2  # For image processing
import easygui  # To open the filebox
import numpy as np  # To store image
import os
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

image_path = r"C:\Users\deban\Downloads\GettyImages-962142748-5c4bd5bd46e0fb0001ddde78.jpg"
def cartoonify(ImagePath):
    # Read the image
    original_image = cv2.imread(ImagePath)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # Confirm that image is chosen
    if original_image is None:
        st.error("Cannot find any image. Please choose a valid file.")
        return

    # Resizing the image to fit the display
    resized1 = cv2.resize(original_image, (960, 540))

    # Converting the image to grayscale
    gray_scale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    resized2 = cv2.resize(gray_scale_image, (960, 540))

    # Applying median blur to smoothen the image
    smooth_gray_scale = cv2.medianBlur(gray_scale_image, 5)
    resized3 = cv2.resize(smooth_gray_scale, (960, 540))

    # Retrieving the edges for cartoon effect using thresholding technique
    get_edge = cv2.adaptiveThreshold(smooth_gray_scale, 255, 
                                     cv2.ADAPTIVE_THRESH_MEAN_C, 
                                     cv2.THRESH_BINARY, 9, 9)
    resized4 = cv2.resize(get_edge, (960, 540))

    # Applying bilateral filter to remove noise and keep edges sharp
    color_image = cv2.bilateralFilter(original_image, 9, 300, 300)
    resized5 = cv2.resize(color_image, (960, 540))

    # Masking edged image with the "color" image to get the cartoon effect
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=get_edge)
    resized6 = cv2.resize(cartoon_image, (960, 540))

    # Displaying images in a transition manner
    images = [resized1, resized2, resized3, resized4, resized5, resized6]

    # Show transition images
    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []}, 
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i])

    # Display the cartoonified image
    st.image(resized6, caption='Cartoonified Image', use_column_width=True)

    # Provide option to download the cartoon image
    save_button = st.button("Save Cartoon Image")
    if save_button:
        save_image(resized6, ImagePath)


def save_image(resized6, ImagePath):
    # Saving the cartoon image
    new_name = "cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, new_name + extension)

    # Save the image
    cv2.imwrite(path, cv2.cvtColor(resized6, cv2.COLOR_RGB2BGR))
    
    # Let the user know where the image is saved
    st.success(f"Image saved successfully as {new_name}{extension} at {path}")


# Streamlit App Layout
st.title("Cartoonify Your Image!")
st.write("Upload an image to transform it into a cartoon-style image.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    image_path = os.path.join("temp_image", uploaded_file.name)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Perform cartoonification
    cartoonify(image_path)

# Add custom CSS for background image
bg_image_url = "https://c4.wallpaperflare.com/wallpaper/87/851/622/laptop-backgrounds-nature-images-1920x1200-wallpaper-preview.jpg"  # Replace with your image URL
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{bg_image_url}");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        height: 100vh;
    }}
    </style>
    """, unsafe_allow_html=True)