from collections import namedtuple
from dataclasses import dataclass
from typing import List
import humps


@dataclass
class Datatype:
    id: str
    description: str = None
    extends: str = None

    def __str__(self):
        return self.id


@dataclass
class Dimension:
    value: str
    description: str = None


@dataclass
class DimensionList:
    id: str
    dimensions: List[Dimension]

    @property
    def values(self):
        return [d.value for d in self.dimensions]


@dataclass
class Field:
    id: str
    type: Datatype
    name: str = None
    description: str = None
    comments: str = None
    primary_key: bool = False
    foreign_keys: List = None
    dimension: DimensionList = None


@dataclass
class RecordType:
    id: str
    description: str = None
    fields: List[Field] = None

    @property
    def primary_keys(self) -> List[Field]:
        return [f for f in self.fields or [] if f.primary_key]

    @property
    def foreign_keys(self) -> List[Field]:
        return [f for f in self.fields or [] if f.foreign_keys]

    @property
    def key_class(self) -> namedtuple:
        return namedtuple(humps.pascalize(f"{self.id}_key"), ['record'] + [k.id for k in self.primary_keys])

    @property
    def record_class(self) -> namedtuple:
        return namedtuple(humps.pascalize(f"{self.id}_record"), [f.id for f in self.fields])

    def get_key(self, **kwargs):
        return self.key_class(record=self.id, **kwargs)

    def field_by_id(self, id):
        return [r for r in self.fields if r.id == id][0]


@dataclass
class Specification:
    record_types: List[RecordType]
    dimensions: List[DimensionList]
    data_types: List[Datatype]

    @property
    def fields(self):
        for type in self.record_types:
            for field in type.fields:
                yield field, type

    def record_type_by_id(self, id):
        return [r for r in self.record_types if r.id == id][0]

    def record_type_references(self, record_name):
        references = []
        for other_rec in self.record_types:
            for fk_field in other_rec.foreign_keys:
                for fk in fk_field.foreign_keys:
                    if fk['record'] == record_name:
                        references.append(dict(record=other_rec, field=fk_field, foreign_key=fk))
        return references

    @property
    def top_level_records(self):
        for rec in self.record_types:
            fks = [f for f in rec.fields if f.foreign_keys]
            if len(fks) == 0:
                yield rec

    def dimension_by_id(self, id):
        return [r for r in self.dimensions if r.id == id][0]

    def field_by_id(self, record_id, field_id):
        record = self.record_type_by_id(record_id)
        return record.field_by_id(field_id)