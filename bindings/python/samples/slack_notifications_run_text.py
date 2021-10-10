import re
import time
import logging
import random

from PIL import Image
from slack_bolt import App
from slack_sdk.web import WebClient
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions

# TODO -
# 1. Make sure message is displayed at a particular time
# 3. Emoji support
#   https://github.com/ryanhagerty/mister-moji
#   https://www.mediacurrent.com/blog/mister-moji-slackbot-raspberry-pi-led-matrix-emoji-party
#   https://github.com/ryanhagerty/unicode-slack-emoji-conversion
# 5. Write a script that starts the server on start-up
# 6. Ensure security through vpn or evaluate ngrok if safe
# 7. Change Pi-username
# 8. 3D print casing

# Initialize a Bolt for Python app
app = App()

def rand_single_color(min=0, max=255):
    return random.randint(min, max)

def rand_color(min=0, max=255):
    color = (rand_single_color(min, max),
             rand_single_color(min, max),
             rand_single_color(min, max))
    return color

def parse_emoji(text):
    match = re.search(":(.*?):", text)

    if match:
        emoji = match.group(1)
        return emoji

@app.event("message")
def message(event, client):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    text = event.get("text")
    emoji = parse_emoji(text)

    if emoji:
        emoji_image = Image.open(f"images/{emoji}.png").convert('RGB')

        # Remove emoji text from string
        text = text.replace(f":{emoji}:", "")

    options = RGBMatrixOptions()
    canvas_width = 64
    options.cols = canvas_width
    options.hardware_mapping = 'adafruit-hat'
    options.pwm_lsb_nanoseconds = 280

    matrix = RGBMatrix(options = options)

    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("../../../fonts/7x13.bdf")
    textColor = graphics.Color(*rand_color())
    pos = offscreen_canvas.width
    my_text = text

    duration = 1800 # 30 mins
    #duration = 10 # 10 seconds only for debug

    start_time = time.time()
    while True:
        offscreen_canvas.Clear()
        text_width = graphics.DrawText(offscreen_canvas, font, -pos, 20, textColor, my_text)
        pos += 1

        if (pos > (canvas_width) + (text_width)):
            pos = -canvas_width

        if emoji:
            offscreen_canvas.SetImage(emoji_image, -pos + (text_width + 12), 4,
                                      unsafe=False)

        time.sleep(0.05)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

        time_elapsed = time.time() - start_time

        if time_elapsed > duration:
            break

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.start(3000)
