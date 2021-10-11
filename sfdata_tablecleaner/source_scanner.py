from pathlib import Path
from typing import List, Iterable, Union

from sfdata_tablecleaner.sources import Source


def source_scan(pattern_list: Iterable[Union[Path, str]], relative_to: Path = None) -> List[Source]:
    """
    Scan for sources based on filenames or glob patterns
    """
    if not relative_to:
        relative_to = Path.cwd()
    else:
        relative_to = Path(relative_to)

    files: List[Path] = []
    for pattern in pattern_list:
        files += list(relative_to.glob(pattern))

    for f in files:
        print(f.relative_to(relative_to))


source_scan(['examples/**/*.*'], relative_to=Path(__file__).parent.parent)