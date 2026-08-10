from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "contributions.json"
COUNT_RE = re.compile(r"([\d,]+)\s+contributions?", re.IGNORECASE)


class ContributionParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.days: list[dict[str, object]] = []
        self.seen_dates: set[str] = set()
        self.day_indexes: dict[str, int] = {}
        self.tooltip_target: str | None = None
        self.tooltip_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        day = attributes.get("data-date")
        if day and tag in {"td", "rect"}:
            try:
                level = max(0, min(4, int(attributes.get("data-level", "0"))))
            except ValueError:
                level = 0
            identifier = attributes.get("id")
            record: dict[str, object] = {"date": day, "level": level, "count": None}
            if day not in self.seen_dates:
                self.days.append(record)
                self.seen_dates.add(day)
                if identifier:
                    self.day_indexes[identifier] = len(self.days) - 1

        if tag == "tool-tip" and attributes.get("for") in self.day_indexes:
            self.tooltip_target = attributes["for"]
            self.tooltip_text = []

    def handle_data(self, data: str) -> None:
        if self.tooltip_target:
            self.tooltip_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "tool-tip" or not self.tooltip_target:
            return
        value = " ".join(self.tooltip_text).strip()
        match = COUNT_RE.search(value)
        count = int(match.group(1).replace(",", "")) if match else (0 if value.lower().startswith("no contributions") else None)
        self.days[self.day_indexes[self.tooltip_target]]["count"] = count
        self.tooltip_target = None
        self.tooltip_text = []


def calendar_start(end: date) -> date:
    current_week_sunday = end - timedelta(days=(end.weekday() + 1) % 7)
    return current_week_sunday - timedelta(weeks=52)


def fetch_html(username: str, start: date, end: date) -> str:
    query = urlencode({"from": start.isoformat(), "to": end.isoformat()})
    url = f"https://github.com/users/{username}/contributions?{query}"
    request = Request(
        url,
        headers={
            "Accept": "text/html,application/xhtml+xml",
            "User-Agent": "github-profile-svg-generator/1.0",
        },
    )
    verify_paths = ssl.get_default_verify_paths()
    system_bundle = Path("/etc/ssl/cert.pem")
    context = ssl.create_default_context(
        cafile=str(system_bundle) if not verify_paths.cafile and system_bundle.is_file() else None
    )
    with urlopen(request, timeout=25, context=context) as response:
        if response.status != 200:
            raise RuntimeError(f"GitHub returned HTTP {response.status}")
        return response.read().decode("utf-8", errors="replace")


def parse_days(html: str, start: date, end: date) -> list[dict[str, object]]:
    parser = ContributionParser()
    parser.feed(html)
    unique = {item["date"]: item for item in parser.days}
    parsed = [unique[key] for key in sorted(unique) if start.isoformat() <= key <= end.isoformat()]
    if len(parsed) < 300:
        raise RuntimeError(f"GitHub response contained only {len(parsed)} calendar days")
    return parsed


def write_if_changed(payload: dict[str, object]) -> bool:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if DATA_FILE.exists() and DATA_FILE.read_text(encoding="utf-8") == content:
        return False
    temporary = DATA_FILE.with_suffix(".json.tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(DATA_FILE)
    return True


def cache_is_usable(username: str) -> bool:
    try:
        cached = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return cached.get("status") == "ok" and cached.get("username", "").lower() == username.lower() and len(cached.get("days", [])) >= 300


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a public GitHub contribution calendar.")
    parser.add_argument("--username", default=os.getenv("PROFILE_USERNAME", "YashBhawarkar"))
    arguments = parser.parse_args()

    end = date.today()
    start = calendar_start(end)
    try:
        yearly_calendars = []
        for year in range(start.year, end.year + 1):
            yearly_calendars.append(
                fetch_html(arguments.username, date(year, 1, 1), date(year, 12, 31))
            )
        days = parse_days("\n".join(yearly_calendars), start, end)
        payload = {
            "days": days,
            "range": {"end": end.isoformat(), "start": start.isoformat()},
            "source": "github-public-contribution-calendar",
            "status": "ok",
            "username": arguments.username,
        }
        changed = write_if_changed(payload)
        print(f"fetched {len(days)} contribution days ({'updated' if changed else 'unchanged'})")
        return 0
    except (HTTPError, URLError, TimeoutError, RuntimeError, OSError) as error:
        print(f"warning: contribution fetch failed: {error}", file=sys.stderr)
        if cache_is_usable(arguments.username):
            print("using the last valid contribution cache", file=sys.stderr)
            return 0
        fallback = {
            "days": [],
            "range": {"end": end.isoformat(), "start": start.isoformat()},
            "source": "github-public-contribution-calendar",
            "status": "unavailable",
            "username": arguments.username,
        }
        write_if_changed(fallback)
        print("wrote an honest unavailable-data fallback", file=sys.stderr)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
