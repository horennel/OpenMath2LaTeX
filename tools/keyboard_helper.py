import time
from queue import Queue
from threading import Event
from collections import defaultdict

from pynput import keyboard

key_press_times = defaultdict(lambda: {'press_time': None})
monitored_keys = [keyboard.Key.alt, keyboard.Key.ctrl]
keyboard_q = Queue(maxsize=1)


def on_press(key):
    if key in monitored_keys:
        key_press_times[key] = {'press_time': time.time()}


def on_release(key):
    if key in monitored_keys:
        press_time = key_press_times[key]['press_time']
        if press_time:
            duration = time.time() - press_time
            if duration > 1.5:
                keyboard_q.put({
                    'keyboard': 'option' if key == keyboard.Key.alt else 'control',
                    'duration': duration
                })


def create_new_listener():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_stop_event = Event()
    return listener, keyboard_stop_event


def stop_listener(listener, event):
    event.set()
    listener.join()


def start_key_listener(listener, event):
    with listener:
        while not event.is_set():
            time.sleep(0.1)
        listener.stop()
