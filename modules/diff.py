from modulebase import GitModuleBase
from collections import namedtuple
import pygit2

class Diff(GitModuleBase):
  def __init__(self, **kwargs):
    super(Diff, self).__init__(**kwargs)
    self.commit_id = kwargs["commit_id"]

  def execute(self):
    # TODO add support for the edge case where the commit_id is the first commit
    diff = self.repo.diff(str(self.commit_id), str(self.commit_id) + "^", context_lines=0)
    diff_data = {}

    for commit_file in diff:
      commit_file_path_rel = commit_file.delta.new_file.path

      commit_file_lines = self._get_patch_file_lines(commit_file)

      diff_data[commit_file_path_rel] = self._createDiffHunkList(commit_file_lines, commit_file.hunks)

    # for key in diff_data:
      # print "---"
      # print key
      # for hunk in diff_data[key]:
        # print hunk
      # print "---"

    super(Diff, self).returnFinalResult(diff_data)

  # From a list containing the lines of a file and a list of diff hunks of that
  # file, create a new sorted list with hunks containing only neutral,
  # added or removed lines
  def _createDiffHunkList(self, file_lines, diff_hunks):
    commit_file_hunks = []

    last_lineno = 1
    for hunk in diff_hunks:
      # Either new or old lineno is -1, the other one we need is > 0
      hunk_first_lineno = max(hunk.lines[0].new_lineno, hunk.lines[0].old_lineno)

      # Add a neutral line hunk if there are lines between the end of
      # the last hunk and the start of this hunk
      if hunk_first_lineno > last_lineno:
        commit_file_hunks.append(self._initHunk(" ", file_lines[last_lineno-1:hunk_first_lineno-1]))

      for line in hunk.lines:
        # Only do something if the line is added or removed (can be < in
        # the case if the last line is not an enter). If it is an added
        # line, also increment the last line number
        if line.origin == "+":
          last_lineno = max(line.new_lineno, line.old_lineno)
        elif line.origin != "-":
          continue

        line_content = line.content.strip('\n')

        # Add the line to the last hunk if the origin is the same, else
        # create a new hunk with the line
        try:
          if commit_file_hunks[-1].origin == line.origin:
            commit_file_hunks[-1].lines.append(line_content)
          else:
            commit_file_hunks.append(self._initHunk(line.origin, [line_content]))
        except IndexError:
          # In the case the line is the first, there won't be a hunk in the
          # results yet, thus create it here
          commit_file_hunks.append(self._initHunk(line.origin, [line_content]))

    # If there are lines in the file after the last hunk, add them here
    if last_lineno < len(file_lines):
      commit_file_hunks.append(self._initHunk(" ", file_lines[last_lineno:len(file_lines)]))

    return commit_file_hunks

  def _get_patch_file_lines(self, patch):
    # First try to get the new version of the file, if there is none (in
    # the case of a deleted file) return an empty list instead
    commit_file = self.repo.get(patch.delta.new_file.id)
    if commit_file == None:
      return []

    # Get the lines, in the case of an empty file don't split the lines
    commit_file_lines = commit_file.data
    if commit_file_lines != None:
      commit_file_lines = commit_file_lines.splitlines()

    return commit_file_lines

  def _initHunk(self, hunk_type = " ", lines = []):
    FileDiffHunk = namedtuple('FileDiffHunk', ['origin', 'lines'])
    return FileDiffHunk(hunk_type, lines)