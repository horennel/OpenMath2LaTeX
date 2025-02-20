import io
import re
import base64
import webbrowser

import pyperclip
from PIL import ImageGrab

from backend import ConfigModel, SETTINGS_HOST, SETTINGS_PORT


def get_config():
    return ConfigModel.select().first()


def get_image():
    image = ImageGrab.grabclipboard()
    if image:
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=20)
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        return img_base64
    return None


def get_formula(chat_info):
    pattern = r"\$\$(.*?)\$\$"
    matches = re.findall(pattern, chat_info)
    return '\n'.join(matches)


def open_settings():
    url = f"http://{SETTINGS_HOST}:{SETTINGS_PORT}/config"
    webbrowser.open(url)


def to_clip(formula):
    pyperclip.copy(formula)
