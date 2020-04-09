import re

package_whitelist = ['numpy',
                     'matplotlib',
                     'scipy']

import_checker1 = re.compile(r'(from[ ]+[^ \n;]+[ ]+)?(import[ ]+)([^ \n;.]+)')
import_checker2 = re.compile(r'(from[ ]+)([^ \n;.]+)([ ]+import)')

phrase_blacklist = [re.compile(r'input[ ]*\('),
                    re.compile(r'open[ ]*\(')]


def security_check(source_code: str) -> list:
    # will run the source code as a string through the security checkers and return a list of issues
    issues = []
    for issue in check_packages(source_code):
        issues.append(f'Illegal package imported: {issue}')
    for issue in check_phrases(source_code):
        issues.append(f'Contained illegal phrase: {issue}')
    return issues


def check_packages(source_code: str) -> set:
    # use the regex to detect a set of the pakages imported
    bad_packages = set()

    for match in re.findall(import_checker1, source_code):
        if match[0] == '' and match[2] not in package_whitelist:
            bad_packages.add(match[2])
    for match in re.findall(import_checker2, source_code):
        if match[1] not in package_whitelist:
            bad_packages.add(match[1])

    return bad_packages


def check_phrases(source_code: str) -> set:
    # check for bas strings inside the source code
    bad_phrases = set()
    for phrase in phrase_blacklist:
        match = re.match(phrase, source_code)
        if match:
            bad_phrases.add(match)
    return bad_phrases
