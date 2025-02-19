import time
from queue import Queue
from threading import Thread

from pynput import keyboard

key_press_times = {}
monitored_keys = [keyboard.Key.alt, keyboard.Key.ctrl]
keyboard_q = Queue(maxsize=1)
onoff_q = Queue(maxsize=1)
onoff = False


def on_press(key):
    if key in monitored_keys:
        key_press_times[key] = {'press_time': time.time()}


def on_release(key):
    if key in monitored_keys:
        press_time = key_press_times.get(key, {}).get('press_time')
        if press_time:
            duration = time.time() - press_time
            if duration > 1.5 and onoff is True:
                keyboard_q.put({
                    'keyboard': 'option' if key == keyboard.Key.alt else 'control',
                    'duration': duration
                })


def get_onoff():
    global onoff
    while True:
        time.sleep(0.1)
        onoff = onoff_q.get()


def start_key_listener():
    Thread(target=get_onoff).start()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
