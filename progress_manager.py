class ProgressManager:
    
    def __init__(self, max_entity_count, progress_entity):
        self.max_entity_count = max_entity_count
        self.progress_entity = progress_entity

    def publish(self, progress_percent):
        while self.max_entity_count * progress_percent / 100 > self.current_entity_count:
            self.current_entity_count += 1
            print(self.progress_entity, end = '')

    def setMaxProgressEntityCount(self, count):
        self.max_entity_count = count

    def begin(self):
        self.current_entity_count = 1
        print("PROGRESS: ", end = '')

    def end(self):
        self.current_entity_count = 1
        print()

    def setProgressEntity(self, progress_entity):
        self.progres_entity = progress_entity
