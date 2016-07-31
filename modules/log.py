import pygit2
from modules.modulebase import GitModuleBase


class Log(GitModuleBase):
    def __init__(self, commit_id="HEAD", **kwargs):
        super(Log, self).__init__(**kwargs)
        self.amount = 10
        self.commit_id = commit_id
        self.start_commit_id = self._repo.head.target

    def get_result_from_cache(self, data):
        if not data:
            return None

        try:
            return data[self.commit_id]
        except KeyError:
            return None

    def execute(self):
        walker = self._repo.walk(self.start_commit_id)

        commit_obj = walker.next()
        log_data = [commit_obj.hex]

        if self.commit_id == "HEAD":
            self.commit_id = log_data[0]
        else:
            while True:
                commit_id = walker.next().hex

                log_data.append(commit_id)

                if commit_id == self.commit_id:
                    break

        if walker:
            for i in range(0, self.amount):
                try:
                    log_data.append(walker.next().hex)
                except StopIteration:
                    break

        commit_index = log_data.index(self.commit_id)
        result_data = self._reduce_log_result_to_amount(commit_index,
                                                        log_data)

        super(Log, self).return_cache_result(self.commit_id, result_data)
        super(Log, self).return_final_result(result_data)

    def _reduce_log_result_to_amount(self, active_index, log_data):
        reduced_data = [log_data[active_index]]
        half_amount = self.amount / 2

        # Try to fill the amount of entries with half the amount on both
        # boundaries
        min_bound = max(0, active_index - half_amount)
        max_bound = min(len(log_data), active_index + half_amount + 1)

        # If one of the boundaries causes less than the half amount of entries
        # next to the active commit, fill the total amoun with more entries
        # from the other boundary if possible
        min_bound_diff = active_index - min_bound
        if min_bound_diff < half_amount:
            max_bound = min(len(log_data),
                            max_bound + half_amount - min_bound_diff)

        max_bound_diff = max_bound - active_index
        if max_bound_diff < half_amount:
            min_bound = max(0, min_bound - (half_amount - max_bound_diff) - 1)

        return log_data[min_bound:max_bound]
