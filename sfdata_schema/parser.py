from pathlib import Path
from typing import Union

import yaml

from sfdata_schema.data import DimensionList, Dimension, RecordType, Field


class SchemaSpecParser:

    def __init__(self, spec_dir: Union[Path, str]):
        self.__spec_dir = Path(spec_dir)

        self._parse_dimensions()
        self._parse_records()

    def _parse_dimensions(self):
        category_file_list = (self.__spec_dir / "categories").glob("*.yml")

        all_categories = []
        for category_file in category_file_list:
            category_id = category_file.stem
            category_list = []
            all_categories.append(DimensionList(id=category_id, dimensions=category_list))
            with open(category_file, 'rt') as file:
                data = yaml.safe_load(file)
            for datum in data:
                if "value" in datum:
                    category_list.append(Dimension(**datum))
                else:
                    category_list.append(Dimension(value=datum))

        self.categories = {c.id : c for c in all_categories}

    def _parse_records(self):
        record_file_list = (self.__spec_dir / "types").glob("*.yml")

        record_list = []
        for record_file in record_file_list:
            with open(record_file, 'rt') as file:
                record_id = record_file.stem
                data = yaml.safe_load(file)

            field_dict = data.get('fields', {})
            data['fields'] = [Field(id=id, **field) for id, field in field_dict.items()]

            for f in data['fields']:
                if f.dimension:
                    f.dimension = self.categories[f.dimension]

            record_list.append(RecordType(id=record_id, **data))

        self.records = {r.id: r for r in record_list}
