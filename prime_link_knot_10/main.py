"""Load and enumerate the bundled prime knot/link catalogue."""

from ast import literal_eval
from collections import Counter
from functools import cache
from pathlib import Path

from link_rep import LinkId


PACKAGE_DIR = Path(__file__).resolve().parent
DATA = PACKAGE_DIR / "data"
AMPHICHEIRAL = DATA / "amphicheiral"
PD_CODE = DATA / "pd_code"


def _read_nonempty_lines(folder: Path):
    for path in sorted(folder.iterdir(), key=lambda item: item.name):
        if not path.is_file():
            continue
        for line_number, raw_line in enumerate(
            path.read_text(encoding="utf-8-sig").splitlines(), start=1
        ):
            line = raw_line.strip()
            if line:
                yield path, line_number, line


def _validate_pd_code(name: str, pd_code: object) -> list[list[int]]:
    if not isinstance(pd_code, list):
        raise ValueError(f"{name} PD code is not a list")
    normalized: list[list[int]] = []
    for crossing in pd_code:
        if not isinstance(crossing, (list, tuple)) or len(crossing) != 4:
            raise ValueError(f"{name} contains a malformed crossing")
        if any(isinstance(label, bool) or not isinstance(label, int) for label in crossing):
            raise ValueError(f"{name} contains a non-integer label")
        normalized.append(list(crossing))
    counts = Counter(label for crossing in normalized for label in crossing)
    if any(count != 2 for count in counts.values()):
        raise ValueError(f"{name} labels do not occur exactly twice")
    return normalized


@cache
def load_amphicheiral() -> set[str]:
    result = set()
    for path, line_number, name in _read_nonempty_lines(AMPHICHEIRAL):
        try:
            LinkId.get_link_id_from_string(name)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"invalid name at {path}:{line_number}: {name}") from exc
        result.add(name)
    return result


@cache
def load_pd_code() -> dict[str, list[list[int]]]:
    result: dict[str, list[list[int]]] = {}
    for path, line_number, line in _read_nonempty_lines(PD_CODE):
        if ":" not in line:
            raise ValueError(f"malformed PD record at {path}:{line_number}")
        name, raw_pd_code = (part.strip() for part in line.split(":", 1))
        LinkId.get_link_id_from_string(name)
        try:
            pd_code = _validate_pd_code(name, literal_eval(raw_pd_code))
        except (SyntaxError, ValueError) as exc:
            raise ValueError(f"invalid PD record at {path}:{line_number}") from exc
        if name.startswith("m") and name[1:] in load_amphicheiral():
            continue
        if name in result:
            raise ValueError(f"duplicate PD definition for {name}")
        result[name] = pd_code
    return result


@cache
def get_link_name_sort_index(link_name: str) -> tuple:
    link_id = LinkId.get_link_id_from_string(link_name)
    return (
        link_id.crossing_num,
        link_id.knot_or_link,
        link_id.alter_or_nonalter,
        link_id.inner_index,
        link_id.mirror,
    )


def sort_link_name_list(link_name_list: list[str]) -> list[str]:
    return sorted(link_name_list, key=get_link_name_sort_index)


@cache
def get_all_prime_under10() -> list[str]:
    return sort_link_name_list(list(load_pd_code()))


def dfs(
    last_pos: int,
    cur_cross: int,
    arr: list[str],
    sol: list[list[str]],
    all_knots: list[str],
    total_crossing: int,
):
    if cur_cross > total_crossing:
        return
    if arr:
        sol.append(arr.copy())
    for index in range(last_pos, len(all_knots)):
        name = all_knots[index]
        new_crossings = LinkId.get_link_id_from_string(name).crossing_num
        if cur_cross + new_crossings > total_crossing:
            break
        arr.append(name)
        dfs(index, cur_cross + new_crossings, arr, sol, all_knots, total_crossing)
        arr.pop()


def get_all_combination(total_crossing: int) -> list[list[str]]:
    """Enumerate non-empty factor multisets within a crossing bound."""

    if isinstance(total_crossing, bool) or not isinstance(total_crossing, int):
        raise TypeError("total_crossing must be an integer")
    if total_crossing < 0:
        raise ValueError("total_crossing must be non-negative")
    solutions: list[list[str]] = []
    dfs(0, 0, [], solutions, get_all_prime_under10(), total_crossing)
    return solutions
