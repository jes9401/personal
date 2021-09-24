from queue import Queue
import threading
import traceback
import logging
import sys


class QueueListener(threading.Thread):

    def __init__(self, queue, stream_h):
        threading.Thread.__init__(self)
        self.handler = stream_h
        self.queue = queue
        self.daemon = True
        self.logger = logging.getLogger("")
        self.logger.addHandler(self.handler)

    def run(self):
        while True:
            try:
                record = self.queue.get()
                self.logger.callHandlers(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except:
                traceback.print_exc(file=sys.stderr)


class QueueHandler(logging.Handler):

    def __init__(self, queue):
        logging.Handler.__init__(self)
        self.queue = queue

    def emit(self, record):
        self.queue.put(record)


if __name__ == '__main__':
    logging_q = Queue(-1)
    stream_h = logging.StreamHandler()
    log_queue_reader = QueueListener(logging_q, stream_h)
    log_queue_reader.start()

    handler = QueueHandler(logging_q)
    root = logging.getLogger()
    root.addHandler(handler)

    # 사용
    root.error("queue handler test!!")