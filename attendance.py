"""Attendance tracking based on one-time keys and a class schedule.

The schedule is a CSV file with the following columns:

    <COURSE_CODE>,<LECTURE_CODE>,<DATE>,<START_TIME>,<END_TIME>

The same lecture is often taught twice (e.g., once in Czech and once in
English). Such classes share the LECTURE_CODE, so attendance is counted only
once per student and lecture code.

One-time keys are listed in a plain text file, one key per line, optionally
followed by a tab and the name of the batch the key was printed in. Empty
lines and comments starting with '#' are ignored; revoked keys are kept as
'# REVOKED' comment lines.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import csv
import datetime
import os
import secrets


# Alphabet without characters that are easy to confuse when read from paper.
KEY_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
KEY_LENGTH = 8

# How long before the start and after the end of a class the check-in link
# still works.
GRACE_BEFORE = datetime.timedelta(minutes=15)
GRACE_AFTER = datetime.timedelta(minutes=15)

DATE_FORMATS = ["%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"]
TIME_FORMATS = ["%H:%M", "%H:%M:%S", "%H.%M"]


def generate_key() -> str:
    return "".join(secrets.choice(KEY_ALPHABET) for _ in range(KEY_LENGTH))


def _parse_date(value: str) -> datetime.date:
    for fmt in DATE_FORMATS:
        try:
            return datetime.datetime.strptime(value.strip(), fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date '{value}'.")


def _parse_time(value: str) -> datetime.time:
    for fmt in TIME_FORMATS:
        try:
            return datetime.datetime.strptime(value.strip(), fmt).time()
        except ValueError:
            continue
    raise ValueError(f"Cannot parse time '{value}'.")


@dataclass(frozen=True)
class ClassSlot:
    """One concrete occasion when a class takes place."""

    course_code: str
    lecture_code: str
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time

    @property
    def slot_id(self) -> str:
        return (f"{self.course_code}/{self.lecture_code}/"
                f"{self.date.isoformat()}/{self.start_time.strftime('%H:%M')}")

    @property
    def start(self) -> datetime.datetime:
        return datetime.datetime.combine(self.date, self.start_time)

    @property
    def end(self) -> datetime.datetime:
        return datetime.datetime.combine(self.date, self.end_time)

    @property
    def label(self) -> str:
        return (f"{self.course_code} – {self.lecture_code} "
                f"({self.start_time.strftime('%H:%M')}–"
                f"{self.end_time.strftime('%H:%M')})")

    def is_open_at(self, now: datetime.datetime) -> bool:
        return self.start - GRACE_BEFORE <= now <= self.end + GRACE_AFTER


class Schedule:
    """The class schedule, reloaded whenever the CSV file changes."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.slots: List[ClassSlot] = []
        self.errors: List[str] = []
        self._mtime: Optional[float] = None
        self.reload()

    def reload(self) -> None:
        self.slots = []
        self.errors = []
        if not os.path.exists(self.path):
            self._mtime = None
            self.errors.append(f"Schedule file '{self.path}' does not exist.")
            return
        self._mtime = os.path.getmtime(self.path)
        with open(self.path, encoding="utf-8") as f_csv:
            for line_no, row in enumerate(csv.reader(f_csv), start=1):
                if not row or not row[0].strip() or row[0].lstrip().startswith("#"):
                    continue
                if len(row) < 5:
                    self.errors.append(f"Line {line_no}: expected 5 columns.")
                    continue
                if row[0].strip().upper() == "COURSE_CODE":  # header line
                    continue
                try:
                    self.slots.append(ClassSlot(
                        course_code=row[0].strip(),
                        lecture_code=row[1].strip(),
                        date=_parse_date(row[2]),
                        start_time=_parse_time(row[3]),
                        end_time=_parse_time(row[4])))
                except ValueError as error:
                    self.errors.append(f"Line {line_no}: {error}")
        self.slots.sort(key=lambda slot: (slot.start, slot.course_code))

    def refresh_if_changed(self) -> None:
        mtime = (os.path.getmtime(self.path)
                 if os.path.exists(self.path) else None)
        if mtime != self._mtime:
            self.reload()

    def open_slots(self, now: datetime.datetime) -> List[ClassSlot]:
        """Slots that students can currently check in for."""
        self.refresh_if_changed()
        return [slot for slot in self.slots if slot.is_open_at(now)]

    def slot_by_id(self, slot_id: str) -> Optional[ClassSlot]:
        self.refresh_if_changed()
        for slot in self.slots:
            if slot.slot_id == slot_id:
                return slot
        return None

    @property
    def course_codes(self) -> List[str]:
        return sorted({slot.course_code for slot in self.slots})

    def lecture_codes(self, course_code: str) -> List[str]:
        """Lecture codes of a course, ordered by their first occurrence."""
        seen: List[str] = []
        for slot in self.slots:
            if slot.course_code == course_code and slot.lecture_code not in seen:
                seen.append(slot.lecture_code)
        return seen


@dataclass
class KeyEntry:
    """One one-time key together with the batch it was printed in."""

    key: str
    batch: str
    revoked_at: str = ""

    @property
    def is_revoked(self) -> bool:
        return bool(self.revoked_at)


class KeyStore:
    """The one-time keys, reloaded whenever the key file changes.

    Revoked keys are kept in the file as comments, both as an audit trail and
    so that a revoked key can never be handed out again by chance.
    """

    REVOKED_PREFIX = "# REVOKED"

    def __init__(self, path: str) -> None:
        self.path = path
        self.entries: List[KeyEntry] = []
        self.revoked: List[KeyEntry] = []
        self._mtime: Optional[float] = None
        self.reload()

    def reload(self) -> None:
        self.entries = []
        self.revoked = []
        if not os.path.exists(self.path):
            self._mtime = None
            return
        self._mtime = os.path.getmtime(self.path)
        with open(self.path, encoding="utf-8") as f_keys:
            for line in f_keys:
                entry = self._parse_line(line)
                if entry is None:
                    continue
                if entry.is_revoked:
                    self.revoked.append(entry)
                else:
                    self.entries.append(entry)

    @classmethod
    def _parse_line(cls, line: str) -> Optional[KeyEntry]:
        line = line.rstrip("\n")
        if line.startswith(cls.REVOKED_PREFIX):
            fields = line[len(cls.REVOKED_PREFIX):].strip().split("\t")
            if len(fields) < 2:
                return None
            return KeyEntry(
                key=fields[1], batch=fields[2] if len(fields) > 2 else "",
                revoked_at=fields[0])
        if not line.strip() or line.lstrip().startswith("#"):
            return None
        fields = line.split("\t")
        return KeyEntry(
            key=fields[0].strip(),
            batch=fields[1].strip() if len(fields) > 1 else "")

    @staticmethod
    def _format_line(entry: KeyEntry) -> str:
        if entry.is_revoked:
            return (f"{KeyStore.REVOKED_PREFIX}\t{entry.revoked_at}"
                    f"\t{entry.key}\t{entry.batch}")
        return f"{entry.key}\t{entry.batch}" if entry.batch else entry.key

    def refresh_if_changed(self) -> None:
        mtime = (os.path.getmtime(self.path)
                 if os.path.exists(self.path) else None)
        if mtime != self._mtime:
            self.reload()

    @property
    def keys(self) -> List[str]:
        """All currently valid keys."""
        return [entry.key for entry in self.entries]

    @property
    def all_known_keys(self) -> set:
        """Valid and revoked keys, i.e., keys that must never be reused."""
        return ({entry.key for entry in self.entries}
                | {entry.key for entry in self.revoked})

    @property
    def batches(self) -> List[str]:
        """Batch names of the valid keys, ordered by first occurrence."""
        names: List[str] = []
        for entry in self.entries:
            if entry.batch not in names:
                names.append(entry.batch)
        return names

    def is_valid(self, key: str) -> bool:
        self.refresh_if_changed()
        return any(entry.key == key for entry in self.entries)

    def generate(self, count: int, batch: str) -> List[KeyEntry]:
        """Create `count` new keys, append them to the file and return them."""
        self.refresh_if_changed()
        known = self.all_known_keys
        new_entries = []
        while len(new_entries) < count:
            key = generate_key()
            if key in known:
                continue
            known.add(key)
            new_entries.append(KeyEntry(key=key, batch=batch))
        with open(self.path, "a", encoding="utf-8") as f_keys:
            for entry in new_entries:
                print(self._format_line(entry), file=f_keys)
        self.reload()
        return new_entries

    def revoke(self, keys: List[str]) -> int:
        """Invalidate the given keys; returns how many were actually valid."""
        self.refresh_if_changed()
        to_revoke = set(keys) & {entry.key for entry in self.entries}
        if not to_revoke:
            return 0
        now = datetime.datetime.now().isoformat(timespec="seconds")

        lines = []
        if os.path.exists(self.path):
            with open(self.path, encoding="utf-8") as f_keys:
                lines = f_keys.read().splitlines()

        new_lines = []
        for line in lines:
            entry = self._parse_line(line)
            if entry is not None and not entry.is_revoked and entry.key in to_revoke:
                entry.revoked_at = now
                new_lines.append(self._format_line(entry))
            else:
                new_lines.append(line)

        # Write through a temporary file so that an interrupted write cannot
        # destroy the list of keys.
        tmp_path = self.path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f_keys:
            for line in new_lines:
                print(line, file=f_keys)
        os.replace(tmp_path, self.path)
        self.reload()
        return len(to_revoke)


MANUAL_KEY_PREFIX = "MANUAL-"


@dataclass
class Attendance:
    """A single confirmed check-in."""

    key: str
    name: str
    login: str
    course_code: str
    lecture_code: str
    slot_id: str
    timestamp: float
    manual: bool = False

    @property
    def time(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.timestamp)

    def to_json(self) -> dict:
        return {
            "key": self.key,
            "name": self.name,
            "login": self.login,
            "course_code": self.course_code,
            "lecture_code": self.lecture_code,
            "slot_id": self.slot_id,
            "timestamp": self.timestamp,
            "manual": self.manual,
        }

    @staticmethod
    def from_json_dict(json_dict: dict) -> "Attendance":
        return Attendance(**json_dict)


def normalize_login(login: str) -> str:
    return login.strip().lower()


def manual_key(known_keys) -> str:
    """A synthetic key for a check-in entered by hand by the teacher.

    The prefix contains a character that cannot occur in a generated key, so
    a manual record can never collide with a printed one-time key.
    """
    while True:
        key = MANUAL_KEY_PREFIX + generate_key()
        if key not in known_keys:
            return key


def attendance_summary(
        records: List[Attendance]) -> Dict[str, Dict[str, dict]]:
    """Aggregate check-ins per course and student.

    Returns course_code -> login -> {name, lecture_codes, manual_lecture_codes,
    count}. A lecture attended twice (e.g., in both language variants) is
    counted once. A lecture code is listed as manual if the only check-in for
    it was entered by hand by the teacher.
    """
    summary: Dict[str, Dict[str, dict]] = {}
    for record in sorted(records, key=lambda r: r.timestamp):
        per_course = summary.setdefault(record.course_code, {})
        student = per_course.setdefault(
            record.login, {"name": record.name, "lecture_codes": [],
                           "manual_lecture_codes": [], "names": [],
                           "count": 0})
        student["name"] = record.name
        if record.name not in student["names"]:
            student["names"].append(record.name)
        if record.lecture_code not in student["lecture_codes"]:
            student["lecture_codes"].append(record.lecture_code)
            if record.manual:
                student["manual_lecture_codes"].append(record.lecture_code)
        elif (not record.manual
                and record.lecture_code in student["manual_lecture_codes"]):
            student["manual_lecture_codes"].remove(record.lecture_code)
        student["count"] = len(student["lecture_codes"])
    return summary


def attended_lecture(
        records: List[Attendance], login: str,
        course_code: str, lecture_code: str) -> Optional[Attendance]:
    """The earlier check-in of the same student for the same lecture, if any."""
    for record in sorted(records, key=lambda r: r.timestamp):
        if (record.login == login and record.course_code == course_code
                and record.lecture_code == lecture_code):
            return record
    return None
