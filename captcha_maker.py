from flask import Flask, render_template, request, session
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import string
import io
import base64

app = Flask(__name__)
app.secret_key = 'key'

def generate_random_text(length=6):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def create_captcha_image(text, width=150, height=60):
   # Create a blank image with white background
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    try:
        # Load a font (ensure you have the font file in your environment)
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        # Fallback to default PIL font if specified font not found
        font = ImageFont.load_default()
    
    # Draw the text on the image
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
   
    # Position text in the center
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))
           
    # Apply some distortion
    image = image.filter(ImageFilter.GaussianBlur(1))
    
    # Add some random lines for additional distortion
    for _ in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=1)
    
    return image

@app.route('/')
def index():
    captcha_text = generate_random_text()
    session['captcha_text'] = captcha_text
    captcha_image = create_captcha_image(captcha_text)
    img_io = io.BytesIO()
    captcha_image.save(img_io, 'PNG')
    img_io.seek(0)
    # Encode image to base64
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return render_template('index.html', captcha_image=img_base64)

@app.route('/verify', methods=['POST'])
def verify():
    user_input = request.form['captcha']
    if user_input == session['captcha_text']:
        return 'CAPTCHA passed!'
    else:
        return 'CAPTCHA failed!'

if __name__ == '__main__':
    app.run(debug=True)




# ***********************************************************************************************
# from PIL import Image, ImageDraw, ImageFont, ImageFilter
# import random
# import string
# import io

# # Text captcha generator

# def generate_random_text(length=6):
#     letters = string.ascii_letters + string.digits
#     return ''.join(random.choice(letters) for i in range(length))

# # Image based text captcha generator

# def create_captcha_image(text, width=150, height=60):
#     # Create a blank image with white background
#     image = Image.new('RGB', (width, height), (255, 255, 255))
#     draw = ImageDraw.Draw(image)
    
#     # Load a font
#     font = ImageFont.truetype("arial.ttf", 36)
    
#     # Calculate text size
#     text_bbox = draw.textbbox((0, 0), text, font=font)
#     text_width = text_bbox[2] - text_bbox[0]
#     text_height = text_bbox[3] - text_bbox[1]
    
#     # Position text in the center
#     text_x = (width - text_width) / 2
#     text_y = (height - text_height) / 2
#     draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))
    
#     # Apply some distortion
#     image = image.filter(ImageFilter.GaussianBlur(1))
    
#     # Add some random lines for additional distortion
#     for _ in range(5):
#         x1 = random.randint(0, width)
#         y1 = random.randint(0, height)
#         x2 = random.randint(0, width)
#         y2 = random.randint(0, height)
#         draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=1)
    
#     return image

# text = generate_random_text()
# captcha_image = create_captcha_image(text)
# captcha_image.show()


# from PIL import Image
# import random
# import os

# def select_random_images(image_folder, num_images=9):
#     all_images = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.jpg')]
#     selected_images = random.sample(all_images, num_images)
#     return selected_images

# image_folder = 'path_to_image_folder'
# selected_images = select_random_images(image_folder)

# # Display the selected images
# for img_path in selected_images:
#     img = Image.open(img_path)
#     img.show()
