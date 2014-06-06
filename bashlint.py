#!/usr/bin/env python

import fnmatch
import inspect
import optparse
import os
import re
import sys

REGEXP_SEMICOLON = '.+[\s]*;[\s]*$'


def filename_match(filename, patterns, default=True):
    """Check if patterns contains a pattern that matches filename.

    If patterns is not specified, this always returns True.
    """
    if not patterns:
        return default

    return any(fnmatch.fnmatch(filename, pattern) for pattern in patterns)


def read_lines(filename):
    """Read all lines from a given file."""
    with open(filename) as fp:
        return fp.readlines()


def checker_trailing_whitespace(physical_line):
    """Trailing whitespace is superfluous."""
    physical_line = physical_line.rstrip('\n')    # chr(10), newline
    physical_line = physical_line.rstrip('\r')    # chr(13), carriage return
    physical_line = physical_line.rstrip('\x0c')  # chr(12), form feed, ^L
    stripped = physical_line.rstrip(' \t\v')
    if physical_line != stripped:
        if stripped:
            return len(stripped), "Trailing whitespace"
        else:
            return 0, "Blank line contains whitespace"


def checker_trailing_semicolon(physical_line):
    """Trailing semicolon is superfluous."""
    if re.search(REGEXP_SEMICOLON, physical_line):
        return physical_line.rfind(';'), "Trailing semicolon"


class StyleChecker(object):
    """Coding style checker."""

    def __init__(self):
        self._checkers = self._load_checkers()
        self._errors_count = 0

    @property
    def errors_count(self):
        return self._errors_count

    def _load_checkers(self):
        """Load checkers from the current module."""
        checkers = []
        current_module = sys.modules.get(__name__)
        if current_module is not None:
            for name, func in inspect.getmembers(current_module,
                                                 inspect.isfunction):
                if name.startswith('checker'):
                    checkers.append(func)

        print("Loaded %s checker(s)." % len(checkers))

        return checkers

    def check_file(self, filename):
        """"Run checks for a given file."""
        print("Checking %s" % filename)

        for i, line in enumerate(read_lines(filename), 1):
            for checker in self._checkers:
                result = checker(line)
                if result is not None:
                    self._errors_count += 1
                    offset, text = result
                    print("%s:%s:%s: %s" % (filename, i, offset, text))
                    print(line[:-1])
                    print(' '*offset + '^')


class StyleGuide(object):
    """Bash style guide."""

    FILE_PATTERNS = ('*.sh',)

    def __init__(self, options):
        self._options = options
        self._checker = StyleChecker()

    @property
    def errors_count(self):
        return self._checker.errors_count

    def check_paths(self, paths=None):
        """Run all checks on the paths."""
        try:
            for path in paths or ["."]:
                if os.path.isdir(path):
                    self._check_dir(path)
        except KeyboardInterrupt:
            print("... stopped")

    def _check_dir(self, path):
        """Check all files in this directory and all subdirectories."""
        for root, dirs, files in os.walk(path):
            for filename in sorted(files):
                if filename_match(filename, self.FILE_PATTERNS):
                    self._checker.check_file(os.path.join(root, filename))


def parse_args():
    parser = optparse.OptionParser(prog='bashlint',
                                   usage="%prog [options] input ...")
    return parser.parse_args()


def main():
    options, args = parse_args()
    guide = StyleGuide(options)
    guide.check_paths(args)
    if guide.errors_count:
        sys.exit(1)


if __name__ == "__main__":
    main()
