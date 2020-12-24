"""
Generate a CHANGELOG type file based on the edit log in SO
"""
from typing import Union

import stackexchange


def changelog_for_post(
    post: Union[stackexchange.Question, stackexchange.Answer], module_folder: str
) -> None:
    """Requirements for running `safety`"""
    try:
        post.revisions.fetch()
    except KeyError as ke:
        if "user_id" in str(ke):
            # BUG: bug in fetch!
            return
    if len(post.revisions) <= 1:
        return
    count = 0
    with open(
        module_folder + "/CHANGELOG", "w", encoding="utf-8", errors="replace"
    ) as log:
        log.write("Change Log\n\n")
        for revision in post.revisions:
            count += 1
            author = revision.user.display_name
            author_id = revision.user.id
            if hasattr(revision, "comment"):
                comment = revision.comment
            else:
                comment = ""
            if hasattr(revision, "revision_number"):
                revision_number = revision.revision_number
            else:
                revision_number = -1
            rollback = "Rollback " if revision.is_rollback else ""
            log_entry = (
                f"- {rollback} {revision_number}: {author} ({author_id}), {comment}"
            )

            log.write(log_entry + "\n")
    if count == 0:
        raise TypeError("What")
