from modulebase import GitModuleBase
import pygit2

class Diff(GitModuleBase):
  def __init__(self, **kwargs):
    super(Diff, self).__init__(**kwargs)
    self.commit_id = kwargs["commit_id"]

  def execute(self):
    diff = self.repo.diff(str(self.commit_id), str(self.commit_id) + "^")
    diff_data = {}

    for patch in diff:
      commit_file_path_rel = patch.delta.new_file.path
      diff_data[commit_file_path_rel] = []

      commit_file_lines = self._get_patch_file_lines(patch)

      last_lineno = 1
      for hunk in patch.hunks:
        last = " "
        new_hunk = self._initHunk()
        for line in hunk.lines:
          if line.origin == "+" or line.origin == "-":
            new_last_linenum = line.new_lineno if line.new_lineno != -1 else line.old_lineno
            if last == line.origin:
              new_hunk["lines"].append(line.content.strip('\n'))
            else:
              if len(new_hunk["lines"]) == 0:
                new_hunk["lines"] = commit_file_lines[last_lineno:new_last_linenum]
              if len(new_hunk["lines"]) > 0:
                diff_data[commit_file_path_rel].append(new_hunk)
              new_hunk = self._initHunk(line.origin)
              new_hunk["lines"].append(line.content.strip('\n'))
              last = line.origin
            last_lineno = new_last_linenum

        if len(new_hunk["lines"]) == 0:
          new_hunk["lines"] = commit_file_lines[last_lineno:]
        if len(new_hunk["lines"]) > 0:
          diff_data[commit_file_path_rel].append(new_hunk)

    # print diff_data

    super(Diff, self).returnFinalResult(diff_data)


    # for cur_file in diff_data:
      # counter = 1
      # for hunk in diff_data[cur_file]:
        # print hunk["type"]
        # temp_counter = counter
        # for line in hunk["lines"]:
          # print temp_counter, [line]
          # temp_counter += 1
        # if hunk["type"] != "-":
          # counter = temp_counter

  def _get_patch_file_lines(self, patch):
    # First try to get the new version of the file, if there is none (in
    # the case of a deleted file) use the old file
    commit_file = self.repo.get(patch.delta.new_file.id)
    if commit_file == None:
      commit_file = self.repo.get(patch.delta.old_file.id)

    # Get the lines, in the case of an empty file don't split the lines
    commit_file_lines = commit_file.data
    if commit_file_lines != None:
      commit_file_lines = commit_file_lines.splitlines()

    return commit_file_lines

  def _initHunk(self, hunk_type = " "):
    return {"type": hunk_type, "lines": []}