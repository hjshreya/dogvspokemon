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

# Upload image
uploaded_image = st.file_uploader("Upload a picture of your dog", type=["jpg", "jpeg", "png"])

# Display the dog's image if uploaded
if uploaded_image is not None:
    st.image(uploaded_image, caption="Your dog's picture")

# Input fields for dog's name and weight
dog_name = st.text_input("Enter your dog's name", "Tobi")
dog_weight = st.number_input("Enter your dog's weight in kg", min_value=1.0, step=0.1)

# Button to find Pokémon opponent (disabled until an image is uploaded)
if st.button("Find Pokémon Opponent", disabled=uploaded_image is None):
    if dog_weight > 0:
        # Convert dog's weight to hectograms
        weight_hectograms = int(dog_weight * 10)

        # Limit search to the first 50 Pokémon to improve speed
        response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=50")
        pokemon_data = response.json()

        # Variable to store the closest matching Pokémon
        closest_pokemon = None
        closest_weight_diff = float('inf')

        # Iterate through each Pokémon to find the closest in weight
        for pokemon in pokemon_data['results']:
            # Get detailed Pokémon information
            pokemon_info = requests.get(pokemon['url']).json()
            pokemon_weight = pokemon_info['weight']

            # Calculate the weight difference
            current_diff = abs(weight_hectograms - pokemon_weight)

            if current_diff < closest_weight_diff:
                closest_weight_diff = current_diff
                closest_pokemon = pokemon_info

        # Display the results
        if closest_pokemon:
            st.write(f"The perfect opponent is **{closest_pokemon['name'].capitalize()}**!")

            # Load the template and fonts
            template = Image.open("data/plantilla.png").convert("RGBA")
            try:
                font_path = "fonts/pokemon_classic.ttf"
                font_name = ImageFont.truetype(font_path, 45)
                font_weight = ImageFont.truetype(font_path, 30)
            except IOError:
                font_name = ImageFont.load_default()
                font_weight = ImageFont.load_default()
