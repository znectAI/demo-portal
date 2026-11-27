"""spec_check: the specs are valid, traced to tests, and match the code.

    python -m tools.spec_check [--root .] [--strict]

Vendored into each spec-driven project repo from the znectAI platform repo (tools/spec_check);
no agent may change it there. Exit status 1 if there are errors.

What it checks (see the spec-driven delivery design, section 3):
  validity       canonical.yaml is valid JSON Schema 2020-12 and its $refs resolve;
                 persistence.yaml maps to fields that exist, and every non-derived field of a
                 stored entity is stored (or listed under not_stored); use cases have the
                 template's sections, unique criterion IDs, and cite patterns, invariants and
                 NFRs that exist; consumer examples are well formed with unique IDs.
  traceability   every ID a test cites exists; every criterion a plan promises
                 (docs/plans/*.md "Criteria:") has a test; the examples of each mapping
                 module that exists are run by a test.
  conformance    each canonical model class in app.canonical matches canonical.yaml: the same
                 fields, the same required fields, the same enum values.

Work that isn't planned yet is not an error: untested criteria nobody has promised, and
canonical types with no class yet, are warnings. --strict turns them into errors (use it to
check a finished system).

A project's specs arrive in stages (requirements, then use cases, then the design), and each
stage is checked as far as it goes:
  requirements   specs/requirements/requirements.md: item ids (**R-XXX-n**) are well formed and
                 unique. With nothing else yet, that is all there is to check.
  use cases      the use-case checks above; until the design exists (architecture/overview.md
                 or model/canonical.yaml), the model and persistence aren't required yet.
                 With requirements: every use case names the requirements it covers
                 ("Requirements: R-USE-1, ..."), every id cited exists, and specs/coverage.md
                 accounts for every requirement (see check_coverage).
  design         everything.
"""

from __future__ import annotations

import argparse
import importlib
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

SPEC_ID = re.compile(r"\b(?:UC-\d{3}\.AC\d+|NFR-\d+|EX-[A-Z]+-\d+|INV-\d+)\b")
REQ_DEF = re.compile(r"\*\*(R-[A-Z]+-\d+)\*\*")
REQ_LIKE = re.compile(r"\*\*(R-[A-Za-z]+-[^*\s]*)\*\*")  # an attempt at an id, e.g. **R-use-9**
STORY_ID = re.compile(r"\b[A-Z][A-Z0-9]*\.AC\d+\b")  # e.g. BOOT.AC2: story-level, not in specs
AC_DEF = re.compile(r"\*\*(UC-\d{3}\.AC\d+)\*\*")
REQ_CALL = re.compile(r"""req\(\s*((?:["'][^"']+["']\s*,?\s*)+)\)""")
TS_TITLE_ID = re.compile(r"\[((?:UC-\d{3}\.AC\d+)|(?:EX-[A-Z]+-\d+))\]")
YAML_BLOCK = re.compile(r"```yaml\n(.*?)```", re.DOTALL)
USE_CASE_SECTIONS = [
    "Goal",
    "Actors",
    "Trigger",
    "Preconditions",
    "Main flow",
    "Alternative and error flows",
    "Data",
    "Rules",
    "Acceptance criteria",
    "Non-functional",
]


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


# ---------------------------------------------------------------- loading


def load_yaml(path: Path, report: Report) -> Any:
    try:
        return yaml.safe_load(path.read_text())
    except FileNotFoundError:
        report.error(f"{path}: missing")
    except yaml.YAMLError as exc:
        report.error(f"{path}: not valid YAML ({exc})")
    return None


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


# ---------------------------------------------------------------- canonical model


class Canonical:
    def __init__(self, data: dict):
        self.data = data
        self.defs: dict[str, dict] = data.get("$defs") or {}

    def resolve(self, schema: dict) -> tuple[str | None, dict]:
        """Follow a $ref: (def name or None, schema)."""
        ref = schema.get("$ref")
        if isinstance(ref, str) and ref.startswith("#/$defs/"):
            name = ref.removeprefix("#/$defs/")
            return name, self.defs.get(name, {})
        return None, schema

    def field_schema(self, def_name: str, path: str) -> dict | None:
        """The schema of a dotted field path inside a def, or None if it doesn't exist."""
        schema = self.defs.get(def_name)
        for part in path.split("."):
            if schema is None:
                return None
            _, schema = self.resolve(schema)
            schema = (schema.get("properties") or {}).get(part)
        return schema

    def collection_item(self, spec: str) -> str | None:
        """'Order.lines' -> the def name of the items of Order.lines."""
        owner, _, prop = spec.partition(".")
        schema = self.field_schema(owner, prop)
        if not schema or schema.get("type") != "array":
            return None
        name, _ = self.resolve(schema.get("items") or {})
        return name

    def leaves(self, def_name: str) -> tuple[list[str], list[str], list[str]]:
        """(stored leaf paths, derived paths, collection paths) of a def's fields."""
        stored, derived, collections = [], [], []

        def walk(schema: dict, prefix: str) -> None:
            for name, prop in (schema.get("properties") or {}).items():
                path = f"{prefix}{name}"
                if prop.get("x-derived"):
                    derived.append(path)
                    continue
                if prop.get("type") == "array":
                    collections.append(path)
                    continue
                ref_name, target = self.resolve(prop)
                if ref_name and target.get("type") == "object":
                    walk(target, path + ".")
                else:
                    stored.append(path)

        walk(self.defs.get(def_name, {}), "")
        return stored, derived, collections


def check_canonical(root: Path, report: Report) -> Canonical | None:
    path = root / "specs/architecture/model/canonical.yaml"
    data = load_yaml(path, report)
    if not isinstance(data, dict):
        return None
    try:
        from jsonschema import Draft202012Validator
        from jsonschema.exceptions import SchemaError

        try:
            Draft202012Validator.check_schema(data)
        except SchemaError as exc:
            report.error(f"canonical.yaml is not valid JSON Schema 2020-12: {exc.message}")
    except ImportError:
        report.error(
            "the jsonschema package is needed to validate canonical.yaml "
            "(add it to requirements-dev.txt)"
        )
    model = Canonical(data)
    if not model.defs:
        report.error("canonical.yaml has no $defs")

    def refs(node: Any) -> Iterable[str]:
        if isinstance(node, dict):
            if isinstance(node.get("$ref"), str):
                yield node["$ref"]
            for value in node.values():
                yield from refs(value)
        elif isinstance(node, list):
            for value in node:
                yield from refs(value)

    for ref in sorted(set(refs(data))):
        if not ref.startswith("#/$defs/") or ref.removeprefix("#/$defs/") not in model.defs:
            report.error(f"canonical.yaml: $ref {ref} does not resolve")
    ids = [inv.get("id") for inv in data.get("x-invariants") or []]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        report.error(f"canonical.yaml: invariant {dup} is defined twice")
    return model


def invariant_ids(model: Canonical | None) -> set[str]:
    return {str(i.get("id")) for i in (model.data.get("x-invariants") or [])} if model else set()


# ---------------------------------------------------------------- persistence


def check_persistence(root: Path, model: Canonical, report: Report) -> None:
    data = load_yaml(root / "specs/architecture/persistence.yaml", report)
    if not isinstance(data, dict):
        return
    tables = data.get("tables") or {}
    not_stored = {str(item.get("field")) for item in data.get("not_stored") or []}
    stored_fields: dict[str, set[str]] = {}  # def name -> stored dotted paths
    child_tables: set[str] = set()  # "Order.lines"

    for table, spec in tables.items():
        if not isinstance(spec, dict) or spec.get("sequence") or spec.get("entity") is None:
            continue
        entity = str(spec["entity"])
        if "." in entity:
            def_name = model.collection_item(entity)
            if def_name is None:
                report.error(
                    f"persistence.yaml: table {table}: {entity} is not a collection "
                    "of a canonical type"
                )
                continue
            child_tables.add(entity)
        else:
            def_name = entity
            if def_name not in model.defs:
                report.error(
                    f"persistence.yaml: table {table}: entity {entity} is not in canonical.yaml"
                )
                continue
        for column, col in (spec.get("columns") or {}).items():
            if "field" in col:
                if model.field_schema(def_name, str(col["field"])) is None:
                    report.error(
                        f"persistence.yaml: {table}.{column} maps to {def_name}."
                        f"{col['field']}, which canonical.yaml doesn't define"
                    )
                stored_fields.setdefault(def_name, set()).add(str(col["field"]))
            elif "parent_key" in col:
                owner, _, key = str(col["parent_key"]).partition(".")
                if model.field_schema(owner, key) is None:
                    report.error(
                        f"persistence.yaml: {table}.{column}: parent key "
                        f"{col['parent_key']} doesn't exist"
                    )

    for spec in tables.values():
        if not isinstance(spec, dict) or spec.get("sequence") or spec.get("entity") is None:
            continue
        entity = str(spec["entity"])
        def_name = model.collection_item(entity) if "." in entity else entity
        if not def_name or def_name not in model.defs:
            continue
        stored, _derived, collections = model.leaves(def_name)
        for path in stored:
            if (
                path not in stored_fields.get(def_name, set())
                and f"{def_name}.{path}" not in not_stored
            ):
                report.error(
                    f"persistence.yaml: {def_name}.{path} is neither stored nor listed "
                    "under not_stored"
                )
        for path in collections:
            if f"{def_name}.{path}" not in child_tables and f"{def_name}.{path}" not in not_stored:
                report.error(
                    f"persistence.yaml: collection {def_name}.{path} has no table and "
                    "isn't listed under not_stored"
                )
    for item in not_stored:
        owner, _, path = item.partition(".")
        if model.field_schema(owner, path) is None:
            report.error(
                f"persistence.yaml: not_stored lists {item}, which canonical.yaml doesn't define"
            )


# ---------------------------------------------------------------- use cases


def check_use_cases(
    root: Path, known_refs: set[str], patterns: set[str], report: Report
) -> dict[str, list[str]]:
    """Returns {use case id: [criterion ids]}."""
    criteria: dict[str, list[str]] = {}
    for path in sorted((root / "specs/use-cases").glob("UC-*.md")):
        name = rel(path, root)
        m = re.match(r"(UC-\d{3})-", path.name)
        if not m:
            report.error(f"{name}: file names are UC-nnn-<name>.md")
            continue
        uc = m.group(1)
        text = path.read_text()
        first = text.splitlines()[0] if text else ""
        if not first.startswith(f"# {uc} "):
            report.error(f"{name}: the first line must be '# {uc} <Name>'")
        headings = re.findall(r"^## (.+)$", text, re.M)
        for section in USE_CASE_SECTIONS:
            if not any(h.strip().startswith(section) for h in headings):
                report.error(f"{name}: missing section '## {section}'")
        ids = AC_DEF.findall(text)
        if not ids:
            report.error(f"{name}: no acceptance criteria (**{uc}.AC1** ...)")
        for dup in sorted({i for i in ids if ids.count(i) > 1}):
            report.error(f"{name}: criterion {dup} is defined twice")
        for wrong in sorted({i for i in ids if not i.startswith(uc + ".")}):
            report.error(f"{name}: criterion {wrong} doesn't belong to {uc}")
        criteria[uc] = ids
        for p in sorted(set(re.findall(r"\bP\d+\b", text))):
            if p not in patterns:
                report.error(f"{name}: cites pattern {p}, which patterns.md doesn't define")
        for ref in sorted(set(re.findall(r"\b(?:INV|NFR)-\d+\b", text))):
            if ref not in known_refs:
                report.error(f"{name}: cites {ref}, which isn't defined")
    if not criteria:
        report.error("specs/use-cases/ has no use cases")
    all_ids = [i for ids in criteria.values() for i in ids]
    for dup in sorted({i for i in all_ids if all_ids.count(i) > 1}):
        report.error(f"criterion {dup} is defined in more than one use case")
    return criteria


def pattern_ids(root: Path) -> set[str]:
    path = root / "specs/architecture/patterns.md"
    return set(re.findall(r"^## (P\d+)\b", path.read_text(), re.M)) if path.exists() else set()


def nfr_ids(root: Path) -> set[str]:
    path = root / "specs/architecture/overview.md"
    return (
        set(re.findall(r"^\|\s*(NFR-\d+)\s*\|", path.read_text(), re.M)) if path.exists() else set()
    )


# ---------------------------------------------------------------- consumers


def check_consumers(root: Path, report: Report) -> dict[str, list[str]]:
    """Returns {consumer spec stem: [example ids]}."""
    examples: dict[str, list[str]] = {}
    seen: list[str] = []
    for path in sorted((root / "specs/architecture/consumers").glob("*.md")):
        if path.name == "README.md":
            continue
        ids = []
        for block in YAML_BLOCK.findall(path.read_text()):
            try:
                data = yaml.safe_load(block)
            except yaml.YAMLError as exc:
                report.error(f"{rel(path, root)}: an example block is not valid YAML ({exc})")
                continue
            if not isinstance(data, dict) or "id" not in data:
                continue
            missing = [k for k in ("mapping", "input", "output") if k not in data]
            if missing:
                report.error(f"{rel(path, root)}: example {data['id']} has no {', '.join(missing)}")
            if not re.fullmatch(r"EX-[A-Z]+-\d+", str(data["id"])):
                report.error(
                    f"{rel(path, root)}: example id {data['id']} should look like EX-WEB-1"
                )
            ids.append(str(data["id"]))
        seen += ids
        examples[path.stem] = ids
    for dup in sorted({i for i in seen if seen.count(i) > 1}):
        report.error(f"example {dup} is defined more than once")
    return examples


# ---------------------------------------------------------------- traceability


def test_citations(root: Path) -> dict[str, set[str]]:
    """{cited id: {test files}} from pytest req markers and [ID] in Vitest titles."""
    cited: dict[str, set[str]] = {}
    py = [p for p in root.rglob("*.py") if "tests" in p.parts or p.name.startswith("test_")]
    ts = [
        p
        for pattern in ("*.test.ts", "*.test.tsx", "*.spec.ts", "*.spec.tsx")
        for p in root.rglob(pattern)
    ]
    for path in py + ts:
        if any(part in (".venv", "node_modules", ".git") for part in path.parts):
            continue
        if path.is_relative_to(root / "tools"):
            continue
        text = path.read_text(errors="ignore")
        found: set[str] = set()
        if path.suffix == ".py":
            for args in REQ_CALL.findall(text):
                found |= set(re.findall(r"""["']([^"']+)["']""", args))
        else:
            found |= set(TS_TITLE_ID.findall(text))
        for cid in found:
            cited.setdefault(cid, set()).add(rel(path, root))
    return cited


def promised_criteria(root: Path) -> dict[str, set[str]]:
    """{criterion id: {plan files}} from the 'Criteria:' line of each plan."""
    promised: dict[str, set[str]] = {}
    for path in sorted((root / "docs/plans").glob("*.md")):
        for line in path.read_text(errors="ignore").splitlines():
            if line.lower().startswith("criteria:"):
                for cid in re.findall(r"UC-\d{3}\.AC\d+", line):
                    promised.setdefault(cid, set()).add(rel(path, root))
    return promised


def examples_run_generically(root: Path) -> bool:
    """A test that loads every example from the consumer specs (the recommended way)."""
    for path in (root / "tests").rglob("*.py") if (root / "tests").exists() else []:
        if "architecture/consumers" in path.read_text(errors="ignore"):
            return True
    return False


def check_traceability(
    root: Path,
    criteria: dict[str, list[str]],
    examples: dict[str, list[str]],
    known: set[str],
    strict: bool,
    report: Report,
) -> None:
    cited = test_citations(root)
    for cid, files in sorted(cited.items()):
        if SPEC_ID.fullmatch(cid):
            if cid not in known:
                report.error(f"{', '.join(sorted(files))} cites {cid}, which no spec defines")
        elif STORY_ID.fullmatch(cid):
            report.notes.append(f"{cid} is a story-level criterion (not in specs)")
        else:
            report.error(f"{', '.join(sorted(files))} cites {cid!r}, which isn't a criterion ID")

    promised = promised_criteria(root)
    for cid, plans in sorted(promised.items()):
        if cid not in known:
            report.error(f"{', '.join(sorted(plans))} promises {cid}, which no spec defines")
        elif cid not in cited:
            report.error(f"{cid} is promised by {', '.join(sorted(plans))} but no test cites it")
    for uc, ids in sorted(criteria.items()):
        untested = [i for i in ids if i not in cited and i not in promised]
        tested = len(ids) - len([i for i in ids if i not in cited])
        report.notes.append(f"{uc}: {tested} of {len(ids)} criteria tested")
        if untested:
            msg = f"{uc}: no test yet for {', '.join(untested)}"
            report.error(msg) if strict else report.warn(msg)

    generic = examples_run_generically(root)
    for stem, ids in sorted(examples.items()):
        module = root / "app" / "mapping" / f"{stem.replace('-', '_')}.py"
        missing = [] if generic else [i for i in ids if i not in cited]
        if module.exists() and missing:
            report.error(
                f"{rel(module, root)} exists but no test runs examples {', '.join(missing)}"
            )
        elif not module.exists() and ids:
            msg = f"no mapping module {rel(module, root)} yet for examples {', '.join(ids)}"
            report.error(msg) if strict else report.warn(msg)


# ---------------------------------------------------------------- model conformance


def check_conformance(root: Path, model: Canonical, strict: bool, report: Report) -> None:
    if not (root / "app" / "canonical").exists():
        msg = "app/canonical/ doesn't exist yet: model conformance not checked"
        report.error(msg) if strict else report.warn(msg)
        return
    sys.path.insert(0, str(root))
    try:
        for name in [m for m in list(sys.modules) if m == "app" or m.startswith("app.")]:
            del sys.modules[name]
        module = importlib.import_module("app.canonical")
    except Exception as exc:  # any import failure is a finding, not a crash
        report.error(f"cannot import app.canonical: {type(exc).__name__}: {exc}")
        return
    finally:
        sys.path.remove(str(root))

    from pydantic import BaseModel

    for name, schema in sorted(model.defs.items()):
        cls = getattr(module, name, None)
        if cls is None:
            msg = f"canonical type {name} has no class in app.canonical yet"
            report.error(msg) if strict else report.warn(msg)
            continue
        if "enum" in schema:
            if not (isinstance(cls, type) and issubclass(cls, Enum)):
                report.error(
                    f"app.canonical.{name} should be an Enum (canonical.yaml lists values)"
                )
                continue
            values = {str(v.value) for v in cls}
            expected = {str(v) for v in schema["enum"]}
            if values != expected:
                report.error(
                    f"app.canonical.{name} values {sorted(values)} differ from "
                    f"canonical.yaml {sorted(expected)}"
                )
            continue
        if not (isinstance(cls, type) and issubclass(cls, BaseModel)):
            report.error(f"app.canonical.{name} should be a Pydantic model")
            continue
        props = set((schema.get("properties") or {}).keys())
        fields = {f.alias or key for key, f in cls.model_fields.items()}
        if fields != props:
            missing, extra = sorted(props - fields), sorted(fields - props)
            detail = "; ".join(
                x
                for x in (
                    f"missing {missing}" if missing else "",
                    f"extra {extra}" if extra else "",
                )
                if x
            )
            report.error(f"app.canonical.{name} fields differ from canonical.yaml: {detail}")
        required = set(schema.get("required") or [])
        model_required = {f.alias or key for key, f in cls.model_fields.items() if f.is_required()}
        if model_required != required:
            report.error(
                f"app.canonical.{name} required fields {sorted(model_required)} differ "
                f"from canonical.yaml {sorted(required)}"
            )


# ---------------------------------------------------------------- requirements


def check_requirements(root: Path, report: Report) -> set[str]:
    """The signed-off requirements' item ids: well formed and unique. Returns the ids."""
    path = root / "specs/requirements/requirements.md"
    if not path.exists():
        return set()
    text = path.read_text()
    ids = REQ_DEF.findall(text)
    for bad in sorted({i for i in REQ_LIKE.findall(text)} - set(ids)):
        report.error(f"requirements.md: {bad} is not a requirement id (R-XXX-n)")
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        report.error(f"requirements.md: {dup} is defined twice")
    report.notes.append(f"requirements: {len(set(ids))} items")
    return set(ids)


# ---------------------------------------------------------------- coverage

UC_REQS = re.compile(r"^Requirements:\s*(.+)$", re.MULTILINE)
REQ_ID = re.compile(r"\bR-[A-Z]+-\d+\b")
AC_FROM = re.compile(r"(?:←|<-)\s*(R-AC-\d+(?:\s*,\s*R-AC-\d+)*)")
COVERAGE = "specs/coverage.md"
# Where each kind of requirement must end up. Prefixes are the requirement document's sections.
CONTEXT = {"GOAL", "HEAD", "SCOPE", "PEOPLE", "IDEA"}  # background: listed, not traced
IN_USE_CASES = {"ROLE", "USE", "RULE", "AC"}  # must reach a use case
IN_DESIGN = {"DATA", "INT", "SRC", "NFR", "SEC", "CON", "TEST"}  # the design's (gate 2)
NOT_TRACED = ("out of scope", "superseded")  # allowed for any item, with a reason


def assumption_ids(text: str) -> set[str]:
    """Ids listed under the requirements' "## Assumptions": guesses nobody confirmed one by one."""
    _, _, rest = text.partition("\n## Assumptions")
    section = rest.split("\n## ", 1)[0]
    return set(REQ_ID.findall(section))


def check_coverage(root: Path, req_ids: set[str], report: Report) -> None:
    """Use cases against the signed-off requirements.

    Each use case cites its requirements on a line "Requirements: R-USE-1, R-RULE-3" under its
    title, and a criterion refined from a requirement's acceptance criterion ends "← R-AC-4".
    A use case that rests on an assumption (the requirements' Assumptions list) lists it under
    "## Assumptions", so reviewers see the guess where it lands.

    specs/coverage.md has one table row per requirement: | R-USE-1 | UC-001 | note |. "Where" is
    use cases (UC-nnn, comma separated), "design" (the design's, gate 2), "context" (background),
    or "out of scope" / "superseded" with a reason in the note."""
    req_text = (root / "specs/requirements/requirements.md").read_text()
    guesses = assumption_ids(req_text)
    cited: dict[str, set[str]] = {}  # requirement id -> use cases that cite it
    ac_sources: set[str] = set()
    ucs: set[str] = set()
    for path in sorted((root / "specs/use-cases").glob("UC-*.md")):
        m = re.match(r"(UC-\d{3})-", path.name)
        if not m:
            continue  # reported by check_use_cases
        uc, name, text = m.group(1), rel(path, root), path.read_text()
        ucs.add(uc)
        line = UC_REQS.search(text)
        mine = set(REQ_ID.findall(line.group(1))) if line else set()
        if not mine:
            report.error(f"{name}: no 'Requirements: R-...' line naming the requirements it covers")
        for i in sorted(set(REQ_ID.findall(text)) - req_ids):
            report.error(f"{name}: cites {i}, which requirements.md doesn't define")
        for line_text in text.splitlines():
            found = AC_FROM.search(line_text)
            if found:
                if not AC_DEF.search(line_text):
                    report.error(f"{name}: '← {found.group(1)}' is not on an acceptance criterion line")
                ac_sources.update(REQ_ID.findall(found.group(1)))
        for i in sorted(set(REQ_ID.findall(text)) & req_ids):
            cited.setdefault(i, set()).add(uc)
        _, _, after = text.partition("\n## Assumptions")
        flagged = set(REQ_ID.findall(after.split("\n## ", 1)[0])) if after else set()
        for i in sorted((set(REQ_ID.findall(text)) & guesses) - flagged):
            report.error(f"{name}: rests on {i}, an assumption nobody confirmed; list it under '## Assumptions'")

    path = root / COVERAGE
    if not path.exists():
        report.error(f"{COVERAGE} is missing: it accounts for every requirement")
        return
    rows: dict[str, tuple[str, str]] = {}
    for raw in path.read_text().splitlines():
        cells = [c.strip() for c in raw.strip().strip("|").split("|")] if raw.lstrip().startswith("|") else []
        if len(cells) < 2 or not re.fullmatch(r"R-[A-Za-z]+-\S*", cells[0]):
            continue
        rid, where, note = cells[0], cells[1], cells[2] if len(cells) > 2 else ""
        if rid not in req_ids:
            report.error(f"{COVERAGE}: {rid} isn't a requirement in requirements.md")
        elif rid in rows:
            report.error(f"{COVERAGE}: {rid} has more than one row")
        else:
            rows[rid] = (where, note)
    for rid in sorted(req_ids - set(rows), key=_req_order):
        report.error(f"{COVERAGE}: {rid} is not accounted for")
    for rid, (where, note) in sorted(rows.items(), key=lambda r: _req_order(r[0])):
        kind = rid.split("-")[1]
        low = where.lower()
        targets = set(re.findall(r"\bUC-\d{3}\b", where))
        if low in NOT_TRACED:
            if not note:
                report.error(f"{COVERAGE}: {rid} is {low}: say why in the note")
            continue
        if targets:
            for uc in sorted(targets - ucs):
                report.error(f"{COVERAGE}: {rid} goes to {uc}, which doesn't exist")
            for uc in sorted((targets & ucs) - cited.get(rid, set())):
                report.error(f"{COVERAGE}: {rid} goes to {uc}, but {uc} doesn't cite it")
            if kind == "AC" and rid not in ac_sources:
                report.error(f"{COVERAGE}: {rid} is an acceptance criterion: a criterion must end '← {rid}'")
            continue
        if low == "context" and kind in CONTEXT:
            continue
        if low == "design" and kind in IN_DESIGN:
            continue
        need = (
            "a use case (UC-nnn)" if kind in IN_USE_CASES
            else "'design'" if kind in IN_DESIGN
            else "'context'" if kind in CONTEXT
            else "a use case, 'design' or 'context'"
        )
        report.error(f"{COVERAGE}: {rid} goes to {where or '(nothing)'}; it needs {need}, or "
                     "'out of scope' / 'superseded' with a reason")
    traced = sum(1 for r in rows if re.search(r"\bUC-\d{3}\b", rows[r][0]))
    report.notes.append(f"coverage: {len(rows)} of {len(req_ids)} requirements accounted for, "
                        f"{traced} traced to use cases")


def _req_order(rid: str) -> tuple[str, int]:
    kind, _, n = rid[2:].rpartition("-")
    return kind, int(n) if n.isdigit() else 0


# ---------------------------------------------------------------- main


def run(root: Path, strict: bool = False) -> Report:
    report = Report()
    if not (root / "specs" / "constitution.md").exists():
        report.error("no specs/constitution.md: not a spec-driven repo")
        return report
    req_ids = check_requirements(root, report)
    arch = root / "specs/architecture"
    has_design = (arch / "overview.md").exists() or (arch / "model/canonical.yaml").exists()
    has_use_cases = any((root / "specs/use-cases").glob("UC-*.md"))
    if not has_design and not has_use_cases:
        report.notes.append(
            "no use cases or design yet: the architect hasn't written the specs"
            if (root / "specs/requirements/requirements.md").exists()
            else "no requirements yet: a new project"
        )
        return report
    model = None
    if has_design:
        model = check_canonical(root, report)
    else:
        report.notes.append("no design yet: the model and persistence come with the design")
    if model:
        check_persistence(root, model, report)
    patterns = pattern_ids(root)
    if not patterns:
        report.error("specs/architecture/patterns.md defines no patterns (## P1 ...)")
    criteria = check_use_cases(root, invariant_ids(model) | nfr_ids(root), patterns, report)
    if req_ids and has_use_cases:
        check_coverage(root, req_ids, report)
    examples = check_consumers(root, report)
    known = (
        {i for ids in criteria.values() for i in ids}
        | {i for ids in examples.values() for i in ids}
        | nfr_ids(root)
        | invariant_ids(model)
    )
    check_traceability(root, criteria, examples, known, strict, report)
    if model:
        check_conformance(root, model, strict, report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m tools.spec_check", description=__doc__.split("\n")[0]
    )
    parser.add_argument("--root", type=Path, default=Path("."), help="repository root (default: .)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="unplanned and untested work are errors too (for a finished system)",
    )
    parser.add_argument("--quiet", action="store_true", help="only errors and warnings")
    args = parser.parse_args(argv)
    report = run(args.root.resolve(), args.strict)
    for line in report.errors:
        print(f"ERROR  {line}")
    for line in report.warnings:
        print(f"WARN   {line}")
    if not args.quiet:
        for line in report.notes:
            print(f"       {line}")
    print(f"spec_check: {len(report.errors)} errors, {len(report.warnings)} warnings")
    return 1 if report.errors else 0
