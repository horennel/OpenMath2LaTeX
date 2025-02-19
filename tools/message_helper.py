SUCCESS = 0
NO_COPY_ERROR = 1
ORC_ERROR = 2
CFG_ERROR = 3
WAIT = 4


class MessageHelper(object):
    def __init__(self, msg_type, message=None):
        if msg_type == SUCCESS:
            self.title = "Success!"
            self.subtitle = 'Success!Copied to clipboard.'
            self.message = ''
        elif msg_type == WAIT:
            self.title = "Wait!"
            self.subtitle = 'Image recognition in progress.'
            self.message = ''
        else:
            self.title = 'Error!'
            if msg_type == NO_COPY_ERROR:
                self.subtitle = 'You did not copy the screenshot.'
                self.message = 'Please copy the picture first.'
            elif msg_type == ORC_ERROR:
                self.subtitle = 'orc error'
                self.message = message
            elif msg_type == CFG_ERROR:
                self.subtitle = 'settings error'
                self.message = 'Please check the settings.'

    def to_json(self):
        attrs = vars(self)
        attrs = {k: v for k, v in attrs.items() if not k.startswith('__') and not callable(v)}
        return attrs
