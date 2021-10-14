import re
from PIL import Image

TEXT = 'text'
EMOJI = 'emoji'

def parse_emoji(text):
    match = re.search(":(.*?):", text)

    if match:
        emoji = match.group(1)
        return emoji

def return_text_and_emojis(text):
        # Create list to return
        text_and_emojis = []

        index = 0
        sub_text = ''

        while index < len(text):
                char = text[index]
                if char == '[':
                        if len(sub_text != 0):
                                text_and_emojis.append((TEXT, sub_text))
                                sub_text = ''
                        emoji_name = ''
                        while char != ']':
                                index += 1
                                emoji_name += char
                        emoji_image = Image.open(f"images/{emoji_name}.png").convert('RGB')
                        text_and_emojis.append((EMOJI, emoji_image))
                else:
                        sub_text += char

        if len(sub_text != 0):
                text_and_emojis.append(('text', sub_text))

        return text_and_emojis