
# Import necessary modules
from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import os

# Create the Flask application
app = Flask(__name__)

# Define the home route
@app.route('/')
def home():
    """
    Renders the home page with the meme creation form.
    """
    return render_template('index.html')

# Define the generate route
@app.route('/generate', methods=['POST'])
def generate():
    """
    Generates the meme based on the user input and displays it.
    """
    # Retrieve the user input from the form
    image_url = request.form['image_url']
    top_text = request.form['top_text']
    bottom_text = request.form['bottom_text']
    font_size = int(request.form['font_size'])

    # Download the image from the given URL
    image = Image.open(requests.get(image_url, stream=True).raw)

    # Create a drawing context to add text to the image
    draw = ImageDraw.Draw(image)

    # Load the font
    font = ImageFont.truetype('Helvetica.ttf', font_size)

    # Calculate the text sizes and positions
    top_text_size = draw.textsize(top_text, font=font)
    bottom_text_size = draw.textsize(bottom_text, font=font)
    top_text_x = (image.width - top_text_size[0]) / 2
    top_text_y = 0
    bottom_text_x = (image.width - bottom_text_size[0]) / 2
    bottom_text_y = image.height - bottom_text_size[1]

    # Draw the text on the image
    draw.text((top_text_x, top_text_y), top_text, font=font, fill=(255, 255, 255))
    draw.text((bottom_text_x, bottom_text_y), bottom_text, font=font, fill=(255, 255, 255))

    # Save the modified image
    image.save('static/meme.jpg')

    # Render the result page with the generated meme
    return render_template('result.html')

# Run the Flask application
if __name__ == '__main__':
    app.run()
