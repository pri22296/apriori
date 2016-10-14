class ProgressManager:
    
    def __init__(self, max_entity_count, progress_entity):
        self._max_entity_count = max_entity_count
        self._progress_entity = progress_entity
        self._is_allowed_to_print = True

    def _print_if_allowed(self, *args, **kwargs):
        if self._is_allowed_to_print:
            print(*args, **kwargs)

    def publish(self, progress_percent):
        while self._max_entity_count * progress_percent / 100 > self._current_entity_count:
            self._current_entity_count += 1
            self._print_if_allowed(self._progress_entity, end = '')

    def allow_to_print(self, is_allowed_to_print):
        self._is_allowed_to_print = is_allowed_to_print

    def setMaxProgressEntityCount(self, count):
        self._max_entity_count = count

    def begin(self):
        self._current_entity_count = 1
        self._print_if_allowed("PROGRESS: ", end = '')

    def end(self):
        while self._current_entity_count < self._max_entity_count:
            self._current_entity_count += 1
            self._print_if_allowed(self._progress_entity, end = '')
        self._print_if_allowed()

    def setProgressEntity(self, progress_entity):
        self._progres_entity = progress_entity
    
