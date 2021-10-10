import time
import logging
from slack_bolt import App
from slack_sdk.web import WebClient

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions

# Initialize a Bolt for Python app
app = App()

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
    textColor = graphics.Color(255, 255, 0)
    pos = offscreen_canvas.width
    my_text = text


    start_time = time.time()
    while True:
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
        pos -= 1
        if (pos + len < 0):
            pos = offscreen_canvas.width

        time.sleep(0.05)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

        time_elapsed = time.time() - start_time

        if time_elapsed > 20:
            break

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.start(3000)
