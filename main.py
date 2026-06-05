"""MkDocs macros hook — loads resources.yml and provides a render macro."""

import yaml
from pathlib import Path

TYPE_BADGES = {
    "dashboard": ":material-monitor-dashboard: Dashboard",
    "report": ":material-file-document-outline: Report",
    "tool": ":material-wrench-outline: Tool",
    "dataset": ":material-database-outline: Dataset",
    "package": ":material-package-variant: Package",
}


def define_env(env):
    data_file = Path("data/resources.yml")
    with open(data_file) as f:
        all_resources = yaml.safe_load(f) or []

    @env.macro
    def render_resources(section):
        entries = [r for r in all_resources if r.get("section") == section]
        if not entries:
            return "*No resources listed yet.*"

        parts = []
        for r in entries:
            badge = TYPE_BADGES.get(r.get("type", ""), r.get("type", ""))
            title = r.get("title", "")

            meta = [badge]
            if r.get("organisation"):
                meta.append(f"**{r['organisation']}**")
            if r.get("authors"):
                meta.append(r["authors"])

            lines = [
                f"### {title}",
                f"",
                f"<small>{' · '.join(meta)}</small>",
                f"",
                f"{r.get('description', '')}",
            ]

            if r.get("url"):
                lines.append(f"")
                lines.append(f":octicons-arrow-right-16: [{r['url']}]({r['url']})")

            if r.get("notes"):
                lines.append(f"")
                lines.append(f"*{r['notes']}*")

            parts.append("\n".join(lines))

        return "\n\n---\n\n".join(parts)
