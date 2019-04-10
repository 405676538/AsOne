#!/usr/bin/env python
import os
import sys
import threading
#
# if __name__ == '__main__':
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'untitled4.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


def customization():
    import threading
    t = threading.Thread(target=_run)
    t.setDaemon(True)
    t.start()
    del t


def _run():
    from time import sleep
    from time import ctime

    #
    # logging
    #
    import logging
    logging.basicConfig(
        filename=os.path.join(os.getcwd(), "customization_run.log"),
        level=logging.INFO,
        # level=logging.WARNING,
        format='[%(asctime)s]%(levelname)-9s%(message)s',
    )
    while True:  # loop until universe collapses
        logging.info("customization > _run is running")
        sleep(5)


def Is_child_processing():
    def Is_child_processing():
        from multiprocessing.connection import Listener
        from queue import Queue

        q = Queue()

        def lock_system_port(_port):
            nonlocal q  # it's OK without this announce line
            try:
                listener = Listener(("", _port))
                q.put(False)
            except Exception:  # port be used by parent
                # traceback.print_exc()
                q.put(True)
                return  # child don't listen

            while True:
                serv = listener.accept()  # just bind the port.

        t = threading.Thread(target=lock_system_port, args=(62771,))
        t.setDaemon(True)
        t.start();
        del t;
        return q.get()


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if Is_child_processing():
        customization()

    execute_from_command_line(sys.argv)
