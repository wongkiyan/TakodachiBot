class ModuleService():
    def __init__(self) -> None:
        self._is_running = False

    def start_service(self):
        if self._is_running:
            return
        self._is_running = True

    def stop_service(self):
        if not self._is_running:
            return
        self._is_running = False

    def is_running(self):
        return self._is_running
