from modules.blame import Blame
from modules.commit_file import CommitFile
from modules.commit_context import CommitContext
from modules.diff import Diff
from modules.log import Log


module_events = {
    "blame": Blame,
    "commit_file": CommitFile,
    "commit_context": CommitContext,
    "diff": Diff,
    "log": Log
}
