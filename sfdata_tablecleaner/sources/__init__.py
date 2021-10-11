from dataclasses import dataclass

from sfdata_schema.data import RecordType


@dataclass
class Source:
    name: str
    sheet_name: str = None
    record_type: RecordType = None

