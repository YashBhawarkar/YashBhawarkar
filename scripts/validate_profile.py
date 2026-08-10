from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
WORKFLOW = ROOT / ".github" / "workflows" / "update-profile.yml"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"


def validate_svgs() -> None:
    assets = sorted((ROOT / "assets").glob("*.svg"))
    if not assets:
        raise ValueError("no SVG assets found")
    for asset in assets:
        root = ET.parse(asset).getroot()
        if root.tag != f"{{{SVG_NAMESPACE}}}svg":
            raise ValueError(f"{asset}: root element is not SVG")
        if not root.get("viewBox"):
            raise ValueError(f"{asset}: missing viewBox")
        if root.find(f"{{{SVG_NAMESPACE}}}title") is None:
            raise ValueError(f"{asset}: missing accessible title")


def validate_readme_paths() -> None:
    content = README.read_text(encoding="utf-8")
    references = re.findall(r'(?:src="|!\[[^]]*\]\()([^)"]+\.svg)', content)
    if not references:
        raise ValueError("README does not reference any SVG assets")
    for reference in references:
        candidate = (ROOT / reference).resolve()
        if not candidate.is_relative_to(ROOT) or not candidate.is_file():
            raise ValueError(f"broken README image path: {reference}")


def validate_workflow_contract() -> None:
    content = WORKFLOW.read_text(encoding="utf-8")
    required = ("schedule:", "workflow_dispatch:", "contents: write", "git diff --cached --quiet", "github.repository_owner")
    for marker in required:
        if marker not in content:
            raise ValueError(f"workflow is missing required behavior: {marker}")
    if re.search(r"(?:ghp_|github_pat_|GITHUB_TOKEN\s*:.*[A-Za-z0-9]{20})", content):
        raise ValueError("workflow appears to contain a hardcoded credential")


def main() -> None:
    validate_svgs()
    validate_readme_paths()
    validate_workflow_contract()
    print("validated SVG structure, README image paths, and workflow contract")


if __name__ == "__main__":
    main()
