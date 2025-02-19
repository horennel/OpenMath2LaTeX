from threading import Thread

import rumps

from tools import onoff_q, open_settings, keyboard_q, get_config, MessageHelper, get_image, OpenAIHelper, to_clip, \
    get_formula, start_key_listener, CFG_ERROR, ORC_ERROR, SUCCESS, NO_COPY_ERROR, WAIT
from backend import start_web


class LatexOrcApplication(rumps.App):
    def __init__(self, name):
        super(LatexOrcApplication, self).__init__(name=name, icon='./icons/menu_bar_off.png', quit_button="Quit")

    @rumps.clicked("ORC on/off")
    def onoff(self, sender):
        if sender.state == 0:
            onoff_q.put(True)
            self.icon = './icons/menu_bar_on.png'
            sender.state = 1
        else:
            onoff_q.put(False)
            self.icon = './icons/menu_bar_off.png'
            sender.state = 0

    @rumps.clicked("Settings")
    def settings_button(self, sender):
        open_settings()

    def keyboard_q_monitoring(self):
        while True:
            keyboard_info = keyboard_q.get()
            cfg = get_config()
            if not cfg:
                rumps.notification(**MessageHelper(CFG_ERROR).to_json())
                continue
            if keyboard_info['duration'] >= cfg.button_time and keyboard_info['keyboard'] == cfg.button_select:
                image = get_image()
                if image:
                    rumps.notification(**MessageHelper(WAIT).to_json())
                    err, result = OpenAIHelper(cfg.base_url, cfg.api_key, cfg.model).chat(image)
                    if err:
                        rumps.notification(**MessageHelper(ORC_ERROR, result).to_json())
                    else:
                        to_clip(get_formula(result))
                        rumps.notification(**MessageHelper(SUCCESS).to_json())
                else:
                    rumps.notification(**MessageHelper(NO_COPY_ERROR).to_json())

    def run(self, **options):
        Thread(target=start_key_listener).start()
        Thread(target=self.keyboard_q_monitoring).start()
        Thread(target=start_web).start()
        super().run(**options)


if __name__ == "__main__":
    LatexOrcApplication(name='').run()
