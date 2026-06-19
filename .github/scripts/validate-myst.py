"""Validate myst.yml structure and file references.

Checks:
1. Required keys exist: project.toc, site.options.base_url
2. Every TOC entry's file exists on disk
3. Asset files (logo, favicon) referenced in site.options exist on disk
"""

import sys
import os
import yaml

REQUIRED_PATHS = [
    ["project", "toc"],
    ["site", "options", "base_url"],
]

ASSET_KEYS = ["logo", "favicon"]


def load_config(path="myst.yml"):
    with open(path) as f:
        return yaml.safe_load(f)


def get_nested(d, keys):
    """Traverse a dict by a list of keys, return (value, True) or (None, False)."""
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return None, False
        d = d[k]
    return d, True


def check_required_keys(config):
    errors = []
    for path in REQUIRED_PATHS:
        _, found = get_nested(config, path)
        if not found:
            errors.append(
            f"myst.yml is missing the required key '{'.'.join(path)}'. "
            f"Add it to myst.yml under {' -> '.join(path[:-1])}."
        )
    return errors


def check_toc_files(toc):
    errors = []

    def walk(items):
        for item in items:
            if "file" in item:
                if not os.path.exists(item["file"]):
                    errors.append(
                        f"The sidebar entry in myst.yml references '{item['file']}', "
                        f"but that file does not exist. Check for typos in the path or "
                        f"create the file."
                    )
            if "children" in item:
                walk(item["children"])

    walk(toc)
    return errors


def check_assets(options):
    errors = []
    for key in ASSET_KEYS:
        if key in options:
            path = options[key]
            if not os.path.exists(path):
                errors.append(
                    f"The '{key}' setting in myst.yml points to '{path}', "
                    f"but that file does not exist. Check the path under "
                    f"site -> options -> {key}."
                )
    return errors


def main():
    config = load_config()
    errors = []

    errors.extend(check_required_keys(config))

    toc, has_toc = get_nested(config, ["project", "toc"])
    if has_toc:
        errors.extend(check_toc_files(toc))

    options, has_options = get_nested(config, ["site", "options"])
    if has_options:
        errors.extend(check_assets(options))

    if errors:
        print("myst.yml validation failed:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("myst.yml validation passed.")


if __name__ == "__main__":
    main()

