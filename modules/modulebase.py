class GitModuleBase(object):
    def __init__(self, **kwargs):
        self._callback_cache = kwargs["callback_cache"]
        self._callback_result = kwargs["callback_result"]
        self._config = kwargs["config"]
        self._repo = kwargs["repo"]

    # To be implemented by the child class
    def get_result_from_cache(self, data):
        pass

    # To be implemented by the child class
    def execute(self):
        pass

    def return_cache_result(self, key, data):
        self._callback_cache(self._config.event, key, data)

    def return_final_result(self, data):
        self._callback_result(self._config, data)
