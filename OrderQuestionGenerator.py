from difflib import SequenceMatcher
from itertools import permutations
from logging import debug
from functools import reduce
from string import Template
from typing import List, Tuple


def rate(reference: list, answer: list):
    debug(reference); debug(answer)
    assert len(reference) == len(answer)
    length = len(reference)

    matcher = SequenceMatcher(None, reference, answer)
    match = matcher.find_longest_match(0, length, 0, length)

    if match.size > 1:
        return match.size
    else:
        has_same_position = reduce(
            lambda res, cur: res or cur,
            map(lambda r, a: r == a, reference, answer),
            False
        )
        return 1 if has_same_position else 0


def ratings(ref: list) -> List[Tuple[List[str], int]]:
    result = []

    for p in permutations(ref):
        p = list(p)
        result.append((p, rate(ref, p)))

    return result


def expression(question, ref):
    t_max = Template('{max($ifs)}')
    t_if = Template('if($cond, $score, 0)')
    t_cond = Template('${question}_${pos}.NAOK==\'${value}\'')

    ifs = []
    for answer, rating in ratings(ref):
        debug("answer: " + str(answer)); debug("rating: " + str(rating))
        conditions = []
        position = 1
        for value in answer:
            conditions.append(t_cond.substitute(question=question, pos=position, value=value))
            position += 1
        ifs.append(t_if.substitute(cond=' && '.join(conditions), score=rating))

    s_ifs = ', '.join(sorted(ifs))

    return t_max.substitute(ifs=s_ifs)


if __name__ == "__main__":
    print(expression('alpha', ['alpha', 'beta', 'gamma', 'delta']))
