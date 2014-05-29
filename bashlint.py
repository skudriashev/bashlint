#!/usr/bin/env python

import os

from fnmatch import fnmatch


def filename_match(filename, patterns, default=True):
    """Check if patterns contains a pattern that matches filename.

    If patterns is not specified, this always returns True.
    """
    if not patterns:
        return default

    return any(fnmatch(filename, pattern) for pattern in patterns)


class StyleGuide(object):
    """Bash style guide."""

    FILE_PATTERNS = ("*.sh", )

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
            for filename in files:
                if filename_match(filename, self.FILE_PATTERNS):
                    self._run_checks(os.path.join(root, filename))

    def _run_checks(self, filename):
        """Run checks for a given file."""
        print("Checking %s file." % filename)


def main():
    guide = StyleGuide()
    guide.check_paths()


if __name__ == "__main__":
    main()
