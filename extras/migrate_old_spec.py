from pathlib import Path

import yaml
from yaml import safe_load

PROJECT_ROOT = Path(__file__).parent / ".."


def main():
    spec_file = PROJECT_ROOT / "sfdata_annexa_clean/assets/config/annex-a-merge.yml"
    with open(spec_file, 'rt') as file:
        old_spec = safe_load(file)

    map_file = PROJECT_ROOT / "sfdata_annexa_clean/assets/config/data-map.yml"
    with open(map_file, 'rt') as file:
        old_mapping = safe_load(file)['data_config']

    category_values = {}
    category_names = {}
    field_dimension = {}

    for type_name, categories in old_mapping.items():
        for category_name, values in categories.items():
            key = tuple(v['code'] for v in values)
            field_dimension[(type_name, category_name)] = key
            category_values[key] = values
            if key[0] == "a) Yes":
                category_name = "YesNo"
            category_names[key] = category_name

    annex_a_root = PROJECT_ROOT / "examples/annex_a"

    category_folder = annex_a_root / "spec/categories"
    category_folder.mkdir(parents=True, exist_ok=True)

    for key, name in category_names.items():
        categories = category_values[key]
        categories = [c['code'] for c in categories]
        with open(category_folder / f"{name}.yml", 'wt') as file:
            yaml.dump(categories, file, sort_keys=False)

    category_mappings = {}
    for key, name in category_names.items():
        categories = category_values[key]
        mappings = category_mappings[category_names[key]] = {}
        for c in categories:
            values = mappings[c['code']] = [c['name']]
            for r in c.get('regex', []):
                values.append(r)

    with open(annex_a_root / f"category_resolver.yml", 'wt') as file:
        yaml.dump(category_mappings, file, sort_keys=False)

    types_folder = annex_a_root / "spec/types"
    types_folder.mkdir(parents=True, exist_ok=True)
    for ds in old_spec['datasources']:
        name = ds['name']
        spec = {
            "description": f"This is the type specification for Annex A {name}."
        }
        fields = spec['fields'] = {}
        for col in ds['columns']:
            f = fields[col['name']] = {}

            category_key = field_dimension.get((name, col['name']))

            if category_key:
                f['type'] = 'categorical'
                f['dimension'] = category_names[category_key]
            elif col.get('type'):
                f['type'] = col['type']
            else:
                f['type'] = "string"
            if col.get('unique'):
                f['primary_key'] = True

        with open(types_folder / f"{name}.yml", 'wt') as file:
            yaml.dump(spec, file, sort_keys=False)






if __name__ == "__main__":
    main()