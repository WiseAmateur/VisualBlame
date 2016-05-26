from collections import namedtuple
import pygit2

from modules.modulebase import GitModuleBase


class Diff(GitModuleBase):
  def __init__(self, **kwargs):
    super(Diff, self).__init__(**kwargs)
    self.commit_id = kwargs["commit_id"]

  def execute(self):
    try:
      diff = self.repo.diff(str(self.commit_id), str(self.commit_id) + "^", context_lines=0)
    except KeyError:
      # First commit has no parent, manually get all the lines from that commit
      super(Diff, self).return_final_result(self._get_first_commit_diff_data(self.commit_id))
      return

    diff_data = {}

    for commit_file in diff:
      commit_file_path_rel = commit_file.delta.new_file.path

      commit_file_lines = self._get_patch_file_lines(commit_file)

      diff_data[commit_file_path_rel] = self._create_diff_hunk_list(commit_file_lines, commit_file.hunks)

    super(Diff, self).return_final_result(diff_data)

  # From a list containing the lines of a file and a list of diff hunks of that
  # file, create a new sorted list with hunks containing only neutral,
  # added or removed lines
  def _create_diff_hunk_list(self, file_lines, diff_hunks):
    commit_file_hunks = []

    last_lineno = 0
    for hunk in diff_hunks:
      hunk_first_lineno = max(hunk.lines[0].new_lineno, hunk.lines[0].old_lineno)

      # Add a neutral line hunk if there are lines between the end of
      # the last hunk and the start of this hunk
      if hunk_first_lineno > last_lineno:
        commit_file_hunks.append(self._init_hunk(" ", file_lines[last_lineno:hunk_first_lineno-1]))
        # Do not want to do this in the case the hunk only contains -?
        last_lineno = hunk_first_lineno

      for line in hunk.lines:
        # Only do something if the line is added or removed (can be < in
        # the case if the last line has no newline). If it is an added
        # line, also increment the last line number
        # TODO + and - seems to be switched in pygit2, confirm this
        if line.origin == "-":
          last_lineno = max(line.new_lineno, line.old_lineno)
        elif line.origin != "+":
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
      commit_file_hunks.append(self._init_hunk(" ", file_lines[last_lineno:len(file_lines)]))

    return commit_file_hunks

  def _get_patch_file_lines(self, patch):
    # First try to get the new version of the file, if there is none (in
    # the case of a deleted file) return an empty list instead
    # TODO just like the strange + and - lines being switched thing, it
    # seems as if old_file and new_file are switched.. check with fresh pygit2+libgit2 install
    commit_file = self.repo.get(patch.delta.old_file.id)
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
    diff_data = {}
    prepend = ""

    trees = [self.repo.get(str(first_commit_id)).tree]

    while len(trees) > 0:
      tree = trees.pop(0)
      for entry in tree:
        if entry.type == "blob":
          blob = self.repo.get(str(entry.id))
          lines = blob.data.splitlines()
          # TODO change to + if pygit2 result switch gets resolved
          diff_data[prepend + entry.name] = [self._init_hunk("-", lines)]
        elif entry.type == "tree":
          prepend += entry.name
          trees.append(self.repo.get(str(entry.id)))

    return diff_data
