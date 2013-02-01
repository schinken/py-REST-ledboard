from flask import Flask, request
from ledutils import textutil, ledloard
import settings
import threading
import Queue

class SendMessage(threading.Thread):

    def __init__(self, queue):
        self.queue = queue
        super(SendMessage, self).__init__()

    def run(self):

        while True:

            message, font = self.queue.get() 

            ll = ledloard.Client(settings.ledloard_host, settings.ledloard_port)
            ll.set_priority(ledloard.Client.PRIO_GOD)
            
            dw = textutil.DrawText(message, font)
            for frame_index in xrange(dw.get_frame_count()):
                ll.write_frame(dw.get_frame(frame_index), 96, 16)

            self.queue.task_done()


app = Flask(__name__)
main_queue = Queue.Queue()

message_thread = SendMessage(main_queue)
message_thread.start()

@app.route("/send_text")
def send_message():
    message = request.values.get('message', False)

    if message:

        font = request.values.get('font', settings.font_default)
        if font in settings.font_list:
            font = settings.font_list[font]
        else:
            font = settings.font_list[settings.font_default]

        main_queue.put([message, font])

        return "ok"
    else:
        return "fail"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
