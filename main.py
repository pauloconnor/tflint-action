#!/usr/bin/env python3

import argparse
import json
import git
import os
import subprocess

from pathlib import Path


def get_command_line_options(extra_options, enabled_rules, disabled_rules, config_file):
    options = []

    if extra_options:
        options.append(extra_options)

    if config_file == "true" and os.path.isfile("/github/workspace/.tflint.hcl"):
        options.append("--config /github/workspace/.tflint.hcl")

    if enabled_rules:
        for enabled_rule in enabled_rules.split(" "):
            options.append("--enable-rule " + enabled_rule)

    if disabled_rules:
        for disabled_rule in disabled_rules.split(" "):
            options.append("--disable-rule " + disabled_rule)

    return " ".join(options)


def get_file_list(changed_only, src, recurse):
    files = []

    if changed_only == "true":
        event_path = os.environ.get("GITHUB_EVENT_PATH")
        event_data = ""
        with open(event_path) as f:
            event_data = json.load(f)
        if os.environ.get("GITHUB_EVENT_NAME") == "pull_request":
            base = event_data["pull_request"]["base"]["sha"]
        elif os.environ.get("GITHUB_EVENT_NAME") == "push":
            base = event_data["before"]
        else:
            base = ""

        repo = git.Repo(os.environ.get("GITHUB_WORKSPACE"))

        for item in repo.index.diff(str(base)):
            files.append(item.a_path)
    elif recurse == "true":
        for file in Path(src).rglob("*.tf"):
            files.append(str(file.parent) + "/" + file.name)
    return files


def parse_message(message):
    error = ""
    level = ""
    filename = ""
    line_number = ""
    base_path = os.environ.get("GITHUB_WORKSPACE")

    for line in message.splitlines():
        if line.startswith(("Error", "Notice", "Warning")):
            level = line.split(":")[0].lower()
            if level == "warning":
                level = "error"
            elif level == "notice":
                level = "warning"
            error = line.split(":")[1].strip()
        elif line.startswith("  on"):
            filename = line.split(" ")[3]
            filename = filename.replace(base_path, "")
            line_number = line.split(" ")[5].replace(":", "")
        elif line.startswith("Reference"):
            error = error + " " + line
            print("::%s file=%s,line=%s::%s" % (level, filename, line_number, error))
            error = ""


def run_tflint(args):

    if not os.path.isfile("/usr/local/bin/tflint"):
        print("::debug::tflint is required to perform this action")
        exit(1)

    options = get_command_line_options(
        args.extra_options, args.enabled_rules, args.disabled_rules, args.config_file
    )
    file_list = get_file_list(args.changed_only, args.path, args.recurse)
    exit_code = 0

    for file in file_list:
        command_string = "/usr/local/bin/tflint " + options + " " + file
        if args.debug == "true":
            print(command_string)

        result = subprocess.run(
            [command_string], capture_output=True, text=True, shell=True
        )
        if result.stdout and args.tag_lines == "true":
            parse_message(result.stdout)
        if result.returncode > exit_code:
            exit_code = result.returncode
    exit(exit_code)


def main():
    parser = argparse.ArgumentParser(description="TFLint github action")
    parser.add_argument(
        "--changed_only", default=os.environ.get("INPUT_TFLINT_CHANGED_ONLY")
    )
    parser.add_argument(
        "--config_file", default=os.environ.get("INPUT_TFLINT_CONFIG_FILE")
    )
    parser.add_argument("--debug", default=os.environ.get("INPUT_TFLINT_DEBUG"))
    parser.add_argument(
        "--disabled_rules", default=os.environ.get("INPUT_TFLINT_DISABLED_RULES")
    )
    parser.add_argument(
        "--enabled_rules", default=os.environ.get("INPUT_TFLINT_ENABLED_RULES")
    )
    parser.add_argument(
        "--extra_options", default=os.environ.get("INPUT_TFLINT_EXTRA_OPTIONS")
    )
    parser.add_argument("--path", default=os.environ.get("INPUT_TFLINT_PATH"))
    parser.add_argument("--recurse", default=os.environ.get("INPUT_TFLINT_RECURSE"))
    parser.add_argument("--tag_lines", default=os.environ.get("INPUT_TFLINT_TAG_LINES"))

    args = parser.parse_args()
    run_tflint(args)


if __name__ == "__main__":
    main()
