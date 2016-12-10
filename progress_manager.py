class ProgressManager:
    
    def __init__(self, max_entity_count, progress_entity_completed, progress_entity_pending):
        self._max_entity_count = max_entity_count
        self._progress_entity_completed = progress_entity_completed
        self._progress_entity_pending = progress_entity_pending
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
            self._print_if_allowed(self._progress_entity_completed, end = '', flush = True)

    def _print_progress_bar(self, entity_count_completed, entity_count_pending):
        self._print_if_allowed(self._begin_tag, end = '', flush = True)
        
        for i in range(entity_count_completed):
            self._print_if_allowed(self._progress_entity_completed, end = '', flush = True)
            
        for i in range(entity_count_pending):
            self._print_if_allowed(self._progress_entity_pending, end = '', flush = True)
            
        self._print_if_allowed(end = '\r', flush = True)

    def allow_to_print(self, is_allowed_to_print):
        self._is_allowed_to_print = is_allowed_to_print

    def set_max_entity_count(self, count):
        self._max_entity_count = count

    def set_begin_tag(self, begin_tag):
        self._begin_tag = begin_tag

    def set_end_tag(self, end_tag):
        self._end_tag = end_tag

    def begin(self):
        self._current_entity_count = 0
        self._print_progress_bar(0, self._max_entity_count)
        self._print_if_allowed(self._begin_tag, end = '', flush = True)
        self._is_allowed_to_publish = True

    def end(self):
        while self._current_entity_count <= self._max_entity_count:
            self._current_entity_count += 1
            self._print_if_allowed(self._progress_entity_completed, end = '', flush = True)
            
        self._print_if_allowed(self._end_tag, end = '', flush = True)
        tot_len = len(self._begin_tag) + len(self._end_tag) + self._max_entity_count * len(self._progress_entity_completed) + 1
        self._print_if_allowed(end = '\r')
        
        for i in range(tot_len):
            self._print_if_allowed(' ', end = '', flush = True)
            
        self._print_if_allowed(end = '\r')
        self._is_allowed_to_publish = False

    def set_progress_entity_completed(self, progress_entity_completed):
        self._progres_entity_completed = progress_entity_completed

    def set_progress_entity_pending(self, progress_entity_pending):
        self._progres_entity_pending = progress_entity_pending

def main():
    progress_mgr = ProgressManager(50, '*', '-')
    progress_mgr.allow_to_print(True)
    progress_mgr.begin()
    n = 10000000
    for i in range(1,n+1):
        progress_mgr.publish(i/n * 100)
    progress_mgr.end()

if __name__  == '__main__':
    main()
    
