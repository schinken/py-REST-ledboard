from flask import Flask, request
from ledutils import textutil, ledloard
import settings
import threading

app = Flask(__name__)

send_msg_lock = threading.Semaphore(4)

class SendMessage(threading.Thread):

    def __init__(self, message, font, lock):
        self.message = message
        self.font = font
        self.lock = lock

        super(SendMessage, self).__init__()

    def run(self):

        if not self.lock.acquire(False):
            return False

        ll = ledloard.Client(settings.ledloard_host, settings.ledloard_port)
        ll.set_priority(ledloard.Client.PRIO_HIGH)
        
        dw = textutil.DrawText(self.message, settings.font_list[self.font])
        for frame_index in xrange(dw.get_frame_count()):
            ll.write_frame(dw.get_frame(frame_index), 96, 16)


@app.route("/send_text")
def send_message():
    message = request.values.get('message')
    font = request.values.get('font', settings.font_default)

    SendMessage(message, font, send_msg_lock).start()

    return "ok"


if __name__ == '__main__':
    app.debug = True
    app.run( )