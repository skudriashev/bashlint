#!/usr/bin/env python

import fnmatch
import inspect
import optparse
import os
import re
import sys

REGEXP_SEMICOLON_OK = re.compile(r'(?:\s*;;\s*|\s+\\;\s*)$')
REGEXP_SEMICOLON_WARN = re.compile(r'.*\s*;\s*$')


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
    """Trailing whitespace is superfluous.

    Okay: echo Test#
    W201: echo Test #
    Okay: #
    W202:  #
    """
    physical_line = physical_line.rstrip('\n')    # chr(10), newline
    physical_line = physical_line.rstrip('\r')    # chr(13), carriage return
    physical_line = physical_line.rstrip('\x0c')  # chr(12), form feed, ^L
    stripped = physical_line.rstrip(' \t\v')
    if physical_line != stripped:
        if stripped:
            return len(stripped), "W201 Trailing whitespace"
        else:
            return 0, "W202 Blank line contains whitespace"


def checker_trailing_semicolon(physical_line):
    """Trailing semicolon is superfluous.

    Okay: echo Test#
    W203: echo Test;#
    """
    if not REGEXP_SEMICOLON_OK.search(physical_line):
        if REGEXP_SEMICOLON_WARN.search(physical_line):
            return physical_line.rfind(';'), "W203 Trailing semicolon"


class Violation(object):
    """Represents a single violation."""

    __slots__ = ['_filename', '_line', '_line_number', '_offset', '_text']

    def __init__(self, filename, line, line_number, offset, text):
        self._filename = filename
        self._line = line
        self._line_number = line_number
        self._offset = offset
        self._text = text

    def __str__(self):
        return "%s:%s:%s: %s" % (self._filename, self._line_number,
                                 self._offset, self._text)

    @property
    def line(self):
        return self._line[:-1]

    @property
    def pointer(self):
        return ' ' * self._offset + '^'


class StyleGuide(object):
    """Bash style guide."""

    FILE_PATTERNS = ('*.sh',)

    def __init__(self, options):
        self._options = options
        self._reporter = Reporter(options.show_source)
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

        if self._options.verbose > 1:
            print("Loaded %s checker(s)." % len(checkers))

        return checkers

    def check_paths(self, paths=None):
        """Run all checks on the paths."""
        try:
            for path in paths or ["."]:
                if os.path.isdir(path):
                    self._check_dir(path)
        except KeyboardInterrupt:
            print("... stopped")

    def _check_dir(self, path):
        """Check all files in the given directory and all subdirectories."""
        for root, dirs, files in os.walk(path):
            for filename in sorted(files):
                if filename_match(filename, self.FILE_PATTERNS):
                    if self._options.verbose:
                        print("Checking %s" % filename)
                    self._check_file(os.path.join(root, filename))

    def _check_file(self, filename):
        """"Run checks for a given file."""
        for line_number, line in enumerate(read_lines(filename), 1):
            for checker in self._checkers:
                result = checker(line)
                if result is not None:
                    self._errors_count += 1
                    offset, text = result
                    violation = Violation(filename=filename,
                                          line=line,
                                          line_number=line_number,
                                          offset=offset,
                                          text=text)
                    self._report(violation)

    def _report(self, violation):
        """Report a violation using reporter."""
        self._reporter.report(violation)


class Reporter(object):
    """Standard output violations reporter."""

    def __init__(self, show_source=False):
        self._show_source = show_source

    def report(self, violation):
        """Report given violations."""
        print(violation)
        if self._show_source:
            print(violation.line)
            print(violation.pointer)


def parse_args():
    parser = optparse.OptionParser(prog='bashlint',
                                   usage="%prog [options] [<path>]...")
    parser.add_option('-v', '--verbose', default=0, action='count',
                      help="print debug messages")
    parser.add_option('--show-source', action='store_true',
                      help="show source code for each error")
    return parser.parse_args()


def main():
    options, args = parse_args()
    guide = StyleGuide(options)
    guide.check_paths(args)
    if guide.errors_count:
        sys.exit(1)


if __name__ == "__main__":
    main()
