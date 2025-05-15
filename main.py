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
