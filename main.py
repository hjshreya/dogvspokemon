import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
from st_social_media_links import SocialMediaIcons

# Load the SVG logo from a file
with open("data/logo.svg", "r") as svg_file:
    svg_logo = svg_file.read()

# Embed the SVG logo using HTML
st.markdown(f'<div style="text-align:center">{svg_logo}</div>', unsafe_allow_html=True)
st.subheader("Find out which Pokémon your dog would fight against") 

# Function to crop and resize the image
def crop_and_resize(image, size=(255, 255)):
    # Convert the image to RGBA
    image = image.convert("RGBA")
    width, height = image.size

    # Calculate the central crop size
    new_size = min(width, height)
    left = (width - new_size) / 2
    top = (height - new_size) / 2
    right = (width + new_size) / 2
    bottom = (height + new_size) / 2

    # Crop the image to the center
    cropped_image = image.crop((left, top, right, bottom))

    # Resize the cropped image
    resized_image = cropped_image.resize(size, Image.LANCZOS)
    return resized_image
