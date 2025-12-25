from PIL import Image

def validate_image(uploaded_file):
    """Memastikan file yang diupload valid"""
    if uploaded_file is None:
        return None
    try:
        image = Image.open(uploaded_file)
        return image
    except Exception:
        return None