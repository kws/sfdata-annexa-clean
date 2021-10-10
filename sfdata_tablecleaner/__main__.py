from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Union, List


@dataclass
class Source:
    filename: str
    sheetname: str = None
    type: str = None


def source_scan(patterns: Iterable[str]) -> List[Source]:
    """
    Scan for sources based on filenames or glob patterns
    """
    pass


def load_sources(filename: Union[Path, str]) -> List[Source]:
    """
    Load sources from file.
    """
    pass


def main(
        source_patterns: Iterable[str] = None,
        source_file: Union[Path, str] = None,
        source_outfile: Union[Path, str] = None,
):
    sources: List[Source] = []
    if source_patterns:
        sources += source_scan(source_patterns)

    if source_file:
        sources += load_sources(source_file)

    sources = match_sources(sources)

    if source_outfile:
        save_sources(sources, source_outfile)

    tables = load_tables(sources)



    pass