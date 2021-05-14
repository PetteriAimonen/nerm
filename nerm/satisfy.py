'''Checks requirement satisfaction rules.'''

import re

def check_rule(requirement, rule, settings):
    '''Check if a single rule is satisfied.
    The rule is a list of terms, all of which must be satisfied.
    Returns list of crossrefs or None.
    '''
    if isinstance(rule, str):
        rule = [rule] # String is same as rule list with one term

    remaining = set(re.compile(term) for term in rule)
    crossrefs = []

    for crossref in requirement.crossrefs:
        template = settings['satisfy_template'].format(c = crossref, r = requirement)

        for term in list(remaining):
            if term.search(template):
                remaining.remove(term)
                crossrefs.append(crossref)

    if remaining:
        return None
    else:
        return crossrefs

def is_requirement_satisfied(requirement, settings):
    '''Checks if the requirement has been satisfied.
    Returns combination of crossrefs that is met, or None if not satisfied.
    '''
    if not requirement.crossrefs:
        return None # Requirement with no references cannot be satisfied.

    for tag_pattern, rules in settings['satisfy_rules']:
        if re.search(tag_pattern, requirement.tag):
            # The rules consist of list of lists.
            # The top-level lists are ORed together and the inner lists are ANDed.
            # E.g. [[1, 2], 3] means (1 and 2) or 3
            if isinstance(rules, str):
                rules = [rules]

            for rule in rules:
                satisfied_by = check_rule(requirement, rule, settings)
                if satisfied_by:
                    return satisfied_by

    return None

def check_satisfied(requirements, settings):
    '''Go through all requirements and cross-references and determine
    if they are satisfied. Updates Requirement.satisfied.
    Implements [FR-Satisfy]
    '''
    for req in requirements.values():
        req.satisfied_by = is_requirement_satisfied(req, settings)

# For manual testing run with `python -m nerm.satisfy`
if __name__ == '__main__':
    from . import nermfile, reqfile, crossrefs
    settings = nermfile.load_settings("Nermfile", False)
    reqs = reqfile.find_requirements(settings)
    crossrefs.find_cross_references(reqs, settings)
    check_satisfied(reqs, settings)
    for req in reqs.values():
        if req.satisfied_by:
            crossrefs = ' && '.join('{c.basename}:{c.lineno}'.format(c = c) for c in req.satisfied_by)
            print('%s: Satisfied by %s' % (req.tag, crossrefs))
        else:
            print('%s: Not satisfied' % req.tag)
