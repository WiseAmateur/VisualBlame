from collections import namedtuple
import pygit2

from modules.modulebase import GitModuleBase


class Diff(GitModuleBase):
  def __init__(self, **kwargs):
    super(Diff, self).__init__(**kwargs)
    self.commit_id = kwargs["commit_id"]

  def execute(self):
    try:
      diff = self._repo.diff(str(self.commit_id) + "^", str(self.commit_id), context_lines=0, flags=pygit2.GIT_DIFF_INCLUDE_UNMODIFIED)
      # Merge the diffs that are caused by a renamed file
      diff.find_similar()
    except KeyError:
      # First commit has no parent, manually get all the lines from that commit
      super(Diff, self).return_final_result(self._get_first_commit_diff_data(self.commit_id))
      return

    diff_data = {}

    for commit_file in diff:
      # TODO now exludes renamed but unmodified files, include later
      # with check: commit_file.delta.status == pygit2.GIT_DELTA_RENAMED
      if not len(commit_file.hunks):
        continue

      commit_file_path_rel = commit_file.delta.old_file.path

      commit_new_file_lines = self._get_patch_new_file_lines(commit_file)

      diff_data[commit_file_path_rel] = self._create_diff_hunk_list(commit_new_file_lines, commit_file.hunks)

    super(Diff, self).return_final_result(diff_data)

  # From a list containing the lines of the new version of that file and
  # a list of diff hunks of that file, create a new sorted list with
  # hunks containing only neutral, added or removed lines
  def _create_diff_hunk_list(self, file_lines, diff_hunks):
    commit_file_hunks = []

    # The counter is used to keep track of the difference between the
    # old file line number and the new file line number, to determine
    # where removed lines have to be added between the new files lines.
    old_file_diff_counter = 0
    last_lineno = 1

    for hunk in diff_hunks:
      if hunk.lines[0].new_lineno != -1:
        hunk_first_lineno = hunk.lines[0].new_lineno
      else:
        hunk_first_lineno = hunk.lines[0].old_lineno + old_file_diff_counter

      # Add a neutral line hunk if there are lines between the end of
      # the last hunk and the start of this hunk
      if hunk_first_lineno > last_lineno:
        commit_file_hunks.append(self._init_hunk(" ", file_lines[last_lineno-1:hunk_first_lineno-1]))
        last_lineno = hunk_first_lineno

      for line in hunk.lines:
        # Only do something if the line is added or removed (can be "<"
        # in the case if the last line has no newline).
        if line.origin == "+":
          last_lineno += 1
          old_file_diff_counter += 1
        elif line.origin == "-":
          old_file_diff_counter -= 1
        else:
          continue

        line_content = line.content.strip('\n')

        # Add the line to the last hunk if the origin is the same, else
        # create a new hunk with the line
        try:
          if commit_file_hunks[-1].origin == line.origin:
            commit_file_hunks[-1].lines.append(line_content)
          else:
            commit_file_hunks.append(self._init_hunk(line.origin, [line_content]))
        except IndexError:
          # In the case the line is the first, there won't be a hunk in the
          # results yet, thus create it here
          commit_file_hunks.append(self._init_hunk(line.origin, [line_content]))

    # If there are lines in the file after the last hunk, add them here
    if last_lineno < len(file_lines):
      commit_file_hunks.append(self._init_hunk(" ", file_lines[last_lineno-1:len(file_lines)]))

    return commit_file_hunks

  def _get_patch_new_file_lines(self, patch):
    # First try to get the new version of the file, if there is none (in
    # the case of a deleted file) return an empty list instead
    commit_file = self._repo.get(patch.delta.new_file.id)
    if commit_file == None:
      return []

    # Get the lines, in the case of an empty file don't split the lines
    commit_file_lines = commit_file.data
    if commit_file_lines != None:
      commit_file_lines = commit_file_lines.splitlines()

    return commit_file_lines

  def _init_hunk(self, hunk_type = " ", lines = []):
    FileDiffHunk = namedtuple('FileDiffHunk', ['origin', 'lines'])
    return FileDiffHunk(hunk_type, lines)

  def _get_first_commit_diff_data(self, first_commit_id):
    TreeData = namedtuple('TreeData', ['prepend', 'tree'])
    diff_data = {}

    trees = [TreeData('', self._repo.get(str(first_commit_id)).tree)]

    # Add every blob in the whole tree to the diff data as a newly added
    # file with the correct directory prefix
    while len(trees) > 0:
      tree_data = trees.pop(0)
      tree = tree_data.tree
      prepend = tree_data.prepend
      for entry in tree:
        if entry.type == "blob":
          blob = self._repo.get(str(entry.id))
          lines = blob.data.splitlines()
          diff_data[prepend + entry.name] = [self._init_hunk("+", lines)]
        elif entry.type == "tree":
          prepend += entry.name
          trees.append(TreeData(prepend + entry.name + "/", self._repo.get(str(entry.id))))

    return diff_data
