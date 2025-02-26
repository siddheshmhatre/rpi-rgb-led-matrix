import time
import logging
import random
from queue import Queue
from threading import Thread

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
message_queue = Queue()
users_to_notify = []

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
    global message_queue
    logger.info(event)
    text = event.get("text")
    text_and_emojis = return_text_and_emojis(text)
    message_queue.put(text_and_emojis)

    userid = event.get("user")
    userinfo = client.users_info(user=userid)
    logger.info(userinfo)
    username = userinfo.get('user').get('real_name')
    global users_to_notify

    for user in users_to_notify:
        if user != userid:
            result = client.chat_postMessage(
                        channel=user,
                        text=f"You have a new message from {username}"
                    )
            logger.info(result)
    time.sleep(10)

def display_message(message_queue, matrix, font, canvas_width, offscreen_canvas):
    while True:
        textColor = graphics.Color(*rand_color())
        initial_pos = -canvas_width
        pos = initial_pos

        total_num_times = 3
        num_times = 0

        if not message_queue.empty():
            logger.info(f"Message queue size BEFORE {message_queue.qsize()}")

            text_and_emojis = message_queue.get()
            logger.info(f"Message queue size AFTER {message_queue.qsize()}")
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
                    num_times += 1

                time.sleep(0.15)
                offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

                if num_times >= total_num_times:
                    break

        time.sleep(5)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    options = RGBMatrixOptions()
    canvas_width = 64
    options.cols = canvas_width
    options.hardware_mapping = 'adafruit-hat'
    options.pwm_lsb_nanoseconds = 280
    font = graphics.Font()
    font.LoadFont("../../../fonts/7x13.bdf")

    matrix = RGBMatrix(options = options)
    offscreen_canvas = matrix.CreateFrameCanvas()

    display_thread = Thread(target = display_message, args =(message_queue,
                                                             matrix, font,
                                                             canvas_width,
                                                             offscreen_canvas))
    display_thread.start()
    app.start(3000)
