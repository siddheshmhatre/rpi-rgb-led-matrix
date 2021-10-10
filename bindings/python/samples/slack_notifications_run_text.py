import time
import logging
import random
from slack_bolt import App
from slack_sdk.web import WebClient

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions

# TODO -
# 1. Make sure message is displayed at a particular time
# 2. Message is displayed only for an hour or so
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

@app.event("message")
def message(event, client):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    options = RGBMatrixOptions()
    options.cols = 64
    options.hardware_mapping = 'adafruit-hat'

    matrix = RGBMatrix(options = options)

    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("../../../fonts/7x13.bdf")
    #textColor = graphics.Color(255, 255, 0)
    textColor = graphics.Color(*rand_color())
    pos = offscreen_canvas.width
    my_text = text


    start_time = time.time()
    while True:
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, pos, 20, textColor, my_text)
        pos -= 1
        if (pos + len < 0):
            pos = offscreen_canvas.width

        time.sleep(0.05)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

        time_elapsed = time.time() - start_time

        if time_elapsed > 10:
            break

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.start(3000)
