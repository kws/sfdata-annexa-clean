import argparse
from pathlib import Path
from typing import Iterable, Union, List

from sfdata_schema.data import Specification
from sfdata_schema.parser import SchemaSpecParser
from sfdata_tablecleaner.sources import Source


def load_sources(filename: Union[Path, str], schema: Specification) -> List[Source]:
    """
    Load sources from file.
    """
    pass


def match_sources(sources: List[Source], schema: Specification, source_map=None) -> List[Source]:
    """

    Try to identify a RecordType for each Source

    """
    pass


def main(
        schema_dir: Union[Path, str],
        source_patterns: Iterable[str] = None,
        source_file: Union[Path, str] = None,
        source_outfile: Union[Path, str] = None,
        source_map: Union[Path, str] = None,
):
    schema: Specification = SchemaSpecParser(schema_dir).schema

    sources: List[Source] = []
    if source_patterns:
        sources += source_scan(source_patterns)

    if source_file:
        sources += load_sources(source_file, schema)

    sources = match_sources(sources, schema, source_map=source_map)

    if source_outfile:
        save_sources(sources, source_outfile)

    tables = load_tables(sources)



    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Test'
    )
    parser.add_argument("specfolder", type=str, help="Folder holding data specification")

    args = parser.parse_args()
    main(args.specfolder)