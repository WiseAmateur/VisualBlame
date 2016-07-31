import pygit2

from modules.modulebase import GitModuleBase


class CommitFile(GitModuleBase):
    def __init__(self, commit_id="", file_path="", **kwargs):
        self.commit_id = commit_id
        self.file_path = file_path
        self.key = self.commit_id + self.file_path
        super(CommitFile, self).__init__(**kwargs)

    def get_result_from_cache(self, data):
        try:
            return data[self.key]
        # TypeError if the data is None, KeyError if the data doesn't
        # contain the key of this module
        except (TypeError, KeyError):
            return None

    def execute(self):
        try:
            commit_tree = self._repo.get(str(self.commit_id)).tree
        except ValueError:
            # When the input commit id is not an id, but something like HEAD
            commit_tree = self._repo.revparse_single(self.commit_id).tree

        for path_name in self.file_path.split("/"):
            commit_tree = self._repo.get(commit_tree[path_name].id)

        lines = commit_tree.data.splitlines()

        super(CommitFile, self).return_cache_result(self.key, lines)
        super(CommitFile, self).return_final_result(lines)
