import threading

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DirObserver:
    def __init__(self, ini, profiles, o_any_event_func=None, o_move_func=None, o_create_func=None,
                 o_delete_func=None, o_modified_func=None, o_closed_func=None):
        self.path = ini.configs['routes']['inbox_path']
        self.event_handler \
            = self.Handler(o_any_event_func, o_move_func, o_create_func, o_delete_func, o_modified_func, o_closed_func,
                           profiles)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.path, recursive=True)
        self.start_observer()

    class Handler(FileSystemEventHandler):
        def __init__(self, o_any_event_func=None, o_move_func=None, o_create_func=None,
                     o_delete_func=None, o_modified_func=None, o_closed_func=None, profiles=None):
            self.o_any_event_func = o_any_event_func
            self.o_move_func = o_move_func
            self.o_create_func = o_create_func
            self.o_delete_func = o_delete_func
            self.o_modified_func = o_modified_func
            self.o_closed_func = o_closed_func
            self.profiles = profiles

        def on_any_event(self, event):
            pass

        def on_moved(self, event):
            pass

        def on_created(self, event):
            print(event)
            o_c_thread = threading.Thread(target=self.o_create_func, args=(event, self.profiles))
            o_c_thread.start()
            # <FileCreatedEvent: event_type=created, src_path='/data/hu_wagnerj/Downloads/ToDo.txt', is_directory=False>
            # PageProcessor(src) -> Hauptarbeit

            # TODO: Thread stoppen

        def on_deleted(self, event):
            pass

        def on_modified(self, event):
            pass

        def on_closed(self, event):
            pass

    def start_observer(self):
        self.observer.start()

    def stop_observer(self):
        self.observer.stop()

    def join_observer(self):
        self.observer.join()
