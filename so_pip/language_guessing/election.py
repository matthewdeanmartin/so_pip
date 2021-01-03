"""
Ranked choice election
"""
from typing import List, Optional

import pyrankvote
from pyrankvote import Ballot, Candidate

from so_pip.language_guessing.extension_based import guess_by_extension
from so_pip.language_guessing.keyword_based import guess_by_keywords
from so_pip.language_guessing.regex_based import language_by_regex_features
from so_pip.language_guessing.shebang_based import language_by_shebang
from so_pip.language_guessing.tag_based import match_tag_to_languages


def guess_language_all_methods(
    code: str,
    file_name: str = "",
    surrounding_text: str = "",
    tags: Optional[List[str]] = None,
) -> Optional[str]:
    """
    Choose language with multiple algorithms via ranked choice.

    Ensemble classifier in fancy talk.
    """
    vote_by_keyword = guess_by_keywords(code)
    vote_by_shebang = language_by_shebang(code)
    vote_by_tags = match_tag_to_languages(tags)
    vote_by_extension = guess_by_extension(file_name)
    vote_by_extension_in_text = guess_by_extension(surrounding_text)
    vote_by_regex_features = language_by_regex_features(code)

    candidates = {}
    ballots = []
    for ballot in [
        vote_by_tags,
        vote_by_keyword,
        vote_by_shebang,
        vote_by_extension,
        vote_by_extension_in_text,
        vote_by_regex_features,
    ]:
        for candidate in ballot:
            candidates[candidate] = Candidate(candidate)
        if ballot:
            ranked_ballot = Ballot(ranked_candidates=[candidates[_] for _ in ballot])
            ballots.append(ranked_ballot)
        # else abstains

    if len(candidates) == 1:
        return list(candidates.values())[0].name

    election_result = pyrankvote.instant_runoff_voting(
        list(candidates.values()), ballots
    )

    winners = election_result.get_winners()
    if not winners:
        return None
    return winners[0].name
