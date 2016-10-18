class ProgressManager:
    
    def __init__(self, max_entity_count, progress_entity):
        self._max_entity_count = max_entity_count
        self._progress_entity = progress_entity
        self._is_allowed_to_print = True
        self._is_allowed_to_publish = False
        self._begin_tag = 'PROGRESS: '
        self._end_tag = 'Done'

    def _print_if_allowed(self, *args, **kwargs):
        if self._is_allowed_to_print:
            print(*args, **kwargs)

    def publish(self, progress_percent):
        assert self._is_allowed_to_publish is True
        while self._max_entity_count * progress_percent / 100 >= self._current_entity_count:
            self._current_entity_count += 1
            self._print_if_allowed(self._progress_entity, end = '', flush = True)

    def allow_to_print(self, is_allowed_to_print):
        self._is_allowed_to_print = is_allowed_to_print

    def setMaxProgressEntityCount(self, count):
        self._max_entity_count = count

    def set_begin_tag(self, begin_tag):
        self._begin_tag = begin_tag

    def set_end_tag(self, end_tag):
        self._end_tag = end_tag

    def begin(self):
        self._current_entity_count = 1
        self._print_if_allowed(self._begin_tag, end = '', flush = True)
        self._is_allowed_to_publish = True

    def end(self):
        while self._current_entity_count <= self._max_entity_count:
            self._current_entity_count += 1
            self._print_if_allowed(self._progress_entity, end = '', flush = True)
        self._print_if_allowed(self._end_tag, end = '', flush = True)
        tot_len = len(self._begin_tag) + len(self._end_tag) + self._max_entity_count * len(self._progress_entity)
        self._print_if_allowed(end = '\r')
        for i in range(tot_len):
            self._print_if_allowed(' ', end = '', flush = True)
        self._print_if_allowed(end = '\r')
        self._is_allowed_to_publish = False

    def setProgressEntity(self, progress_entity):
        self._progres_entity = progress_entity

def main():
    progress_mgr = ProgressManager(50, '>')
    progress_mgr.allow_to_print(True)
    progress_mgr.begin()
    n = 1000000
    for i in range(1,n+1):
        progress_mgr.publish(i/n * 100)
    progress_mgr.end()

if __name__  == '__main__':
    main()
    
