from .worker import GenerationWorker
class JobController:
    def __init__(self): self.worker=None
    def start(self,settings): self.worker=GenerationWorker(settings); return self.worker.run()
    def stop(self):
        if self.worker: self.worker.stop()
