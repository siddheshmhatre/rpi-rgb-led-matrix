import time
import logging
import random

from slack_bolt import App
from slack_sdk.web import WebClient
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from emoji_helpers import return_text_and_emojis, TEXT, EMOJI

# TODO -
# 1. Make sure message is displayed at a particular time
# 5. Write a script that starts the server on start-up
# 6. Ensure security through vpn or evaluate ngrok if safe
# 7. Change Pi-username
# 8. 3D print casing
# 9. Fine tuning to remove flickering https://github.com/hzeller/rpi-rgb-led-matrix#troubleshooting

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
    text = event.get("text")

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
    initial_pos = -canvas_width
    pos = initial_pos
    my_text = text

    # duration = 1800 # 30 mins
    duration = 15 # 10 seconds only for debug

    text_and_emojis = return_text_and_emojis(text)

    start_time = time.time()
    total_width = -1
    while True:
        offscreen_canvas.Clear()
        delta = 0
        for item in text_and_emojis:
            if item[0] == TEXT:
                text_width = graphics.DrawText(offscreen_canvas, font, -pos +
                                               delta, 20, textColor, item[1])
                delta += text_width

            elif item[0] == EMOJI:
                offscreen_canvas.SetImage(item[1], -pos + delta, 4,
                                          unsafe=False)
                delta += item[1].size[1] # Each emoji is 32 x 32 pix

            pos += 1

        if total_width < 0:
            total_width = delta

        if pos > total_width + canvas_width:
            pos = initial_pos

        time.sleep(0.2)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

        time_elapsed = time.time() - start_time

        if time_elapsed > duration:
            break

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.start(3000)
