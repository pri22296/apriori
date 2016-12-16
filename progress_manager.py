class ProgressManager:
    """Utility Class to display Progress Bars in console.

    Parameters
    ----------

    max_entity_count : int
        Number of entities in the progress bar.

    progress_entity_completed : str
        Symbol which is used to show completed part of the progress bar. 

    progress_entity_pending : str
        Symbol which is used to show incomplete part of the progress bar.
        
    """
    
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
        """Update the progress bar to display current progress aaccording to `progress_percent`.

        Parameters
        ----------

        progress_percent : float or int
            The current progress in percentage. It should be between 0 and 100. 
        """
        
        assert self._is_allowed_to_publish is True
        
        while self._max_entity_count * progress_percent / 100 >= self._current_entity_count:
            self._current_entity_count += 1
            self._print_if_allowed(self._progress_entity_completed, end = '', flush = True)

    def _print_progress_bar(self, entity_count_completed, entity_count_pending):
        #this method should be used to print the progress bar whenever it needs to be updated
        #currently it is not used in such a manner
        #need to update the code so that things like printing percentage, time remaining, etc
        #can be achived.
        self._print_if_allowed(self._begin_tag, end = '', flush = True)
        
        for i in range(entity_count_completed):
            self._print_if_allowed(self._progress_entity_completed, end = '', flush = True)
            
        for i in range(entity_count_pending):
            self._print_if_allowed(self._progress_entity_pending, end = '', flush = True)
            
        self._print_if_allowed(end = '\r', flush = True)

    def allow_to_print(self, is_allowed_to_print : bool):
        """Set whether ProgressManager instance is allowed to print to console.

        Parameters
        ----------

        is_allowed_to_print
            whether ProgressManager instance has permission to print to console
        """
        self._is_allowed_to_print = is_allowed_to_print

    def set_max_entity_count(self, count : int):
        """Set the total number of entities in the Progress Bar.

        Parameters
        ----------

        count
            value of entity count
        """
        
        self._max_entity_count = count

    def set_begin_tag(self, begin_tag : str):
        """Set the beggining tag of the Progress Bar.

        Parameters
        ----------

        begin_tag
            The value of the new beginning tag. It is printed before the Progress Bar.
            By default, it is 'PROGRESS: '
        """
        
        self._begin_tag = begin_tag

    def set_end_tag(self, end_tag):
        """Set the ending tag of the Progress Bar.

        Parameters
        ----------

        end_tag
            The value of the new ending tag. It is printed after the Progress Bar when
            progress reaches 100 percent. By default, it is 'Done'
        """
        
        self._end_tag = end_tag

    def begin(self):
        """Performs initial tasks prior to printing progress bar.

        It is recommended to perform all customization to the ProgressManager
        instance before calling this method. This method is necessary to call
        for printing Progress Bar. publish() can only be called after calling
        this method.
        """
        
        self._current_entity_count = 0
        self._print_progress_bar(0, self._max_entity_count)
        self._print_if_allowed(self._begin_tag, end = '', flush = True)
        self._is_allowed_to_publish = True

    def end(self):
        """Performs clean up tasks after printing Progress Bar.

        This method should always be called after task is complete. This method
        forces the progress Bar to show progress to 100 percent. after calling
        this method publish() can no longer be called. This method removes the
        Progress Bar from the console. The console should support printing carriage
        returns.
        """
        
        while self._current_entity_count <= self._max_entity_count:
            self._current_entity_count += 1
            self._print_if_allowed(self._progress_entity_completed, end = '', flush = True)
            
        self._print_if_allowed(self._end_tag, end = '', flush = True)
        tot_len = len(self._begin_tag)\
                        + len(self._end_tag)\
                        + self._max_entity_count * len(self._progress_entity_completed)\
                        + 1
        self._print_if_allowed(end = '\r')
        
        for i in range(tot_len):
            self._print_if_allowed(' ', end = '', flush = True)
            
        self._print_if_allowed(end = '\r')
        self._is_allowed_to_publish = False

    def set_progress_entity_completed(self, progress_entity_completed : str):
        """Set the completed entity for the Progress Bar.

        Parameters
        ----------

        progress_entity_completed
            string value of the completed entity.
        """
        
        self._progres_entity_completed = progress_entity_completed

    def set_progress_entity_pending(self, progress_entity_pending):
        """Set the pending entity for the Progress Bar.

        Parameters
        ----------

        progress_entity_pending
            string value of the pending entity.
        """
        
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
    
