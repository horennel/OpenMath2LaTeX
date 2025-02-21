from threading import Thread

import rumps

from tools import create_new_listener, stop_listener, open_settings, keyboard_q, get_config, MessageHelper, get_image, \
    OpenAIHelper, to_clip, get_formula, start_key_listener, CFG_ERROR, OCR_ERROR, SUCCESS, NO_COPY_ERROR, WAIT, \
    open_history, save_history
from backend import start_web


class LatexOCRApplication(rumps.App):
    def __init__(self, name):
        super().__init__(name=name, icon='./icons/menu_bar_off.png', quit_button="Quit")
        self.keyboard_listener = None
        self.keyboard_stop_event = None

    @rumps.clicked("Settings")
    def settings_button(self, sender):
        open_settings()

    @rumps.clicked("History")
    def history_button(self, sender):
        open_history()

    @rumps.clicked("On/Off")
    def onoff(self, sender):
        if sender.state == 0:
            self._start_listener()
            self.icon = './icons/menu_bar_on.png'
            sender.state = 1
        else:
            self._stop_listener()
            self.icon = './icons/menu_bar_off.png'
            sender.state = 0

    def keyboard_q_monitoring(self):
        while True:
            keyboard_info = keyboard_q.get()
            keyboard_q.empty()
            cfg = get_config()
            if not cfg:
                rumps.notification(**MessageHelper(CFG_ERROR).to_json())
                continue
            if keyboard_info['duration'] >= cfg.button_time and keyboard_info['keyboard'] == cfg.button_select:
                self._process_image(cfg)

    @staticmethod
    def _process_image(cfg):
        image = get_image()
        if image:
            rumps.notification(**MessageHelper(WAIT).to_json())
            err, result = OpenAIHelper(cfg.base_url, cfg.api_key, cfg.model).chat(image)
            if err:
                rumps.notification(**MessageHelper(OCR_ERROR, result).to_json())
            else:
                formula = get_formula(result)
                if formula:
                    for fs in formula:
                        save_history(fs)
                    to_clip('\n'.join(formula))
                    rumps.notification(**MessageHelper(SUCCESS).to_json())
                else:
                    rumps.notification(**MessageHelper(OCR_ERROR, 'Formula not recognized.').to_json())
        else:
            rumps.notification(**MessageHelper(NO_COPY_ERROR).to_json())

    def _start_listener(self):
        self.keyboard_listener, self.keyboard_stop_event = create_new_listener()
        Thread(target=start_key_listener, args=(self.keyboard_listener, self.keyboard_stop_event)).start()

    def _stop_listener(self):
        stop_listener(self.keyboard_listener, self.keyboard_stop_event)

    def run(self, **options):
        Thread(target=self.keyboard_q_monitoring).start()
        Thread(target=start_web).start()
        super().run(**options)


if __name__ == "__main__":
    LatexOCRApplication(name='').run()
