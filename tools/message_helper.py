SUCCESS = 0
NO_COPY_ERROR = 1
ORC_ERROR = 2
CFG_ERROR = 3
WAIT = 4


class MessageHelper(object):
    def __init__(self, msg_type, message=None):
        messages = {
            SUCCESS: ("Success!", 'Success!Copied to clipboard.', ''),
            WAIT: ("Wait!", 'Image recognition in progress.', ''),
            NO_COPY_ERROR: ('Error!', 'You did not copy the screenshot.', 'Please copy the picture first.'),
            ORC_ERROR: ('Error!', 'orc error', message),
            CFG_ERROR: ('Error!', 'settings error', 'Please check the settings.')
        }
        self.title, self.subtitle, self.message = messages.get(msg_type, ('Error!', '', ''))

    def to_json(self):
        attrs = vars(self)
        attrs = {k: v for k, v in attrs.items() if not k.startswith('__') and not callable(v)}
        return attrs
