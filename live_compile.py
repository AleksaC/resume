#!/usr/bin/env python

import base64
import os
import subprocess
import sys
import time

FILES = {"resume.md", "style.css"}
CHROME = os.getenv("CHROME", "chrome")


def run_command(command, capture_output=True):
    res = subprocess.run(command.split(), capture_output=capture_output, check=True)

    return res


def compile(verbose=False):
    res = run_command(
        "pandoc --data-dir . --template default --css style.css --embed-resources --standalone resume.md",
    )
    base64_res = base64.b64encode(res.stdout).decode()

    run_command(
        f"""{CHROME} \
            --headless=new \
            --no-pdf-header-footer \
            --run-all-compositor-stages-before-draw \
            --no-pre-read-main-dll \
            --no-first-run \
            --no-sandbox \
            --no-default-browser-check \
            --print-to-pdf=resume.pdf \
            data:text/html;charset=utf-8;base64,{base64_res}""",
        capture_output=not verbose,
    )


def main():
    verbose = len(sys.argv) == 2 and sys.argv[1] == "--verbose"

    print(f"Watching for changes in files: {FILES}")
    compile(verbose)

    mtimes = {}
    while True:
        time.sleep(0.2)
        changed = False

        for file in FILES:
            if not os.path.exists(file):
                print(f"{file} does not exist!")
                continue

            prev_mtime = mtimes.get(file)
            mtime = mtimes[file] = os.path.getmtime(file)

            if prev_mtime and prev_mtime < mtime:
                changed = True

        if changed:
            print("Files changed, compiling...")
            compile(verbose)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping the watcher...")
