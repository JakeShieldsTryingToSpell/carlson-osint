"""Start one research assignment or validate the archive. Python 3, standard library."""
import argparse
import json
import re
import subprocess
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent
REPO = "JakeShieldsTryingToSpell/carlson-osint"
HOLD = timedelta(hours=24)
MARKER = re.compile(r"^Archive (claim|release|review) ([0-9a-f]{32})$", re.M)


def gh(*args):
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "GitHub CLI request failed.")
    return json.loads(result.stdout)


def pages(route):
    return [item for page in gh("api", "--paginate", "--slurp", route) for item in page]


def assignment(comments, now):
    """Replay in server order so simultaneous reservations resolve to one winner."""
    owner = token = None
    expires = None
    for comment in sorted(comments, key=lambda c: c["id"]):
        stamp = datetime.fromisoformat(comment["created_at"].replace("Z", "+00:00"))
        if expires and expires <= stamp:
            owner = token = expires = None
        match = MARKER.fullmatch(comment["body"].strip())
        if not match:
            continue
        action, code = match.groups()
        author = comment["user"]["login"]
        if action == "claim" and token is None:
            owner, token, expires = author, code, stamp + HOLD
        elif (author, code) == (owner, token):
            if action == "release":
                owner = token = expires = None
            elif action == "review":
                expires = None
    return (owner, token) if not expires or now < expires else (None, None)


def start(repo, preview):
    issue_path = "repos/" + repo + "/issues"
    issues = pages(issue_path + "?state=open&per_page=100")
    issues = sorted(issues, key=lambda i: (not i["title"].lower().startswith("review:"), i["number"]))
    login = None
    for issue in issues:
        if "pull_request" in issue:
            continue
        is_document = any(label["name"] == "document" for label in issue.get("labels", []))
        if not is_document and not issue["title"].lower().startswith(("research:", "review:")):
            continue
        if issue["title"].lower().startswith("review:"):
            author = re.search(r"^Researcher: @([A-Za-z0-9-]+)\s*$", issue["body"] or "", re.M)
            if not author:
                continue
            if login is None:
                login = gh("api", "user")["login"].lower()
            if login == author.group(1).lower():
                continue
        path = issue_path + "/" + str(issue["number"])
        route = path + "/comments"
        comments = pages(route + "?per_page=100")
        if issue["assignees"] or assignment(comments, datetime.now(timezone.utc))[1]:
            continue
        if not preview:
            token = uuid.uuid4().hex
            gh("api", route, "-f", "body=Archive claim " + token)
            comments = pages(route + "?per_page=100")
            latest = gh("api", path)
            if (latest["state"] != "open" or latest["assignees"]
                    or assignment(comments, datetime.now(timezone.utc))[1] != token):
                gh("api", route, "-f", "body=Archive release " + token)
                continue
            print("Reservation token:", token)
        print(issue["html_url"], issue["title"], issue["body"] or "", sep="\n\n")
        return
    print("No open, unclaimed research issue. See AGENTS.md for proposing new work.")


def check():
    errors = []
    for path in sorted(ROOT.rglob("*.md")):
        for link in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', path.read_text()):
            target = urlparse(link)
            if not target.scheme and target.path and not (path.parent / unquote(target.path)).exists():
                errors.append(f"{path.name}: missing link {target.path}")
    people = {p.stem for p in (ROOT / "people").glob("*.md")}
    dependencies = {}
    for file in sorted((ROOT / "evidence").glob("*.json")):
        try:
            record = json.loads(file.read_text())
            if record["id"] != file.stem or record["status"] not in {"documented", "reported", "disputed"}:
                raise ValueError("invalid ID or evidence status")
            deps = record.get("depends_on", [])
            if not isinstance(deps, list) or not all(isinstance(x, str) for x in deps):
                raise ValueError("depends_on must be a list of claim IDs")
            dependencies[file.stem] = deps
            if not record["statement"].strip() or not record["relation"].strip():
                raise ValueError("missing statement or relation")
            if record["subject"] not in people or not isinstance(record["object"], str) or not record["object"].strip():
                raise ValueError("missing subject profile or object")
            if record["object_kind"] not in {"person", "organization", "event", "record", "office"}:
                raise ValueError("invalid object kind")
            if record["object_kind"] == "person" and record["object"] not in people:
                raise ValueError("missing object profile")
            if not record["sources"] or not all(
                s["title"].strip() and s["locator"].strip() and urlparse(s["url"]).scheme in {"http", "https"}
                and urlparse(s["url"]).netloc for s in record["sources"]
            ):
                raise ValueError("source needs title, URL, and passage locator")
            for person in {record["subject"], record["object"]} & people:
                if f"../evidence/{file.name}" not in (ROOT / "people" / (person + ".md")).read_text():
                    raise ValueError("missing evidence link on profile " + person)
        except (ValueError, TypeError, KeyError, AttributeError) as err:
            errors.append(f"{file.name}: {err}")
    checked = set()
    def visit(node, trail):
        if node in checked:
            return
        if node in trail:
            errors.append("circular evidence chain: " + " -> ".join(trail + [node]))
            return
        for dep in dependencies[node]:
            if dep not in dependencies:
                errors.append(f"{node}: missing supporting record {dep}")
            else:
                visit(dep, trail + [node])
        checked.add(node)
    for node in dependencies:
        visit(node, [])
    if errors:
        raise ValueError("\n".join(errors))
    print(f"Checked {len(people)} profiles, {len(list((ROOT/'evidence').glob('*.json')))} evidence records and local Markdown links.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["start", "next", "check"])
    parser.add_argument("--repo", default=REPO, help="owner/repository of the common research queue")
    args = parser.parse_args()
    try:
        if args.action == "check":
            check()
        else:
            start(args.repo, preview=args.action == "next")
    except (OSError, ValueError, RuntimeError) as error:
        sys.exit(str(error))
