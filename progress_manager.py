class ProgressManager:
    
    def __init__(self, max_entity_count, progress_entity):
        self._max_entity_count = max_entity_count
        self._progress_entity = progress_entity
        self._is_allowed_to_print = True
        self._is_allowed_to_publish = False

    def _print_if_allowed(self, *args, **kwargs):
        if self._is_allowed_to_print:
            print(*args, **kwargs)

    def publish(self, progress_percent):
        if not self._is_allowed_to_publish:
            #TODO: Raise an appropriate exception here
            pass
        while self._max_entity_count * progress_percent / 100 >= self._current_entity_count:
            self._current_entity_count += 1
            self._print_if_allowed(self._progress_entity, end = '')

    def allow_to_print(self, is_allowed_to_print):
        self._is_allowed_to_print = is_allowed_to_print

    def setMaxProgressEntityCount(self, count):
        self._max_entity_count = count

    def begin(self, begin_tag = 'PROGRESS: '):
        self._current_entity_count = 1
        self._print_if_allowed(begin_tag, end = '')
        self._is_allowed_to_publish = True

    def end(self, end_tag = '\n'):
        while self._current_entity_count <= self._max_entity_count:
            self._current_entity_count += 1
            self._print_if_allowed(self._progress_entity, end = '')
        self._print_if_allowed(end_tag, end = '')
        self._is_allowed_to_publish = False

    def setProgressEntity(self, progress_entity):
        self._progres_entity = progress_entity

def main():
    progress_mgr = ProgressManager(50, '>')
    progress_mgr.begin('PROGRESS_BAR: ')
    n = 1000000
    for i in range(n):
        progress_mgr.publish(i/n * 100)
    progress_mgr.end()

if __name__  == '__main__':
    main()
    
