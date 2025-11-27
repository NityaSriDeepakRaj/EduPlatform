# dev/run_stub.py
import json
import sys
from jsonschema import validate, ValidationError
from pathlib import Path
from transforms.mappings import transform

SCHEMA_PATH = Path(__file__).parent.parent / "schema" / "scene_dsl_schema.json"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def pretty_print_timeline(dsl):
    print("\n=== Timeline ===")
    for s in dsl["scene_sequence"]:
        start = s["start"]; end = s["end"]
        actors = ", ".join([a["kind"] + ":" + a["id"] for a in s["actors"]])
        print(f"{s['id']}: {start:.2f}s → {end:.2f}s  | actors: {actors}")
    print("================\n")

def main(input_path):
    inp = load_json(input_path)
    dsl = transform(inp)
    # validate
    schema = load_json(SCHEMA_PATH)
    try:
        validate(instance=dsl, schema=schema)
        print("DSL validation: OK")
    except ValidationError as e:
        print("DSL validation: FAILED")
        print(e)
        sys.exit(1)
    # print DSL to file
    out_path = Path(input_path).with_name("output_dsl.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dsl, f, indent=2)
    print(f"DSL written to {out_path}")
    pretty_print_timeline(dsl)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dev/run_stub.py examples/sample_input.json")
        sys.exit(1)
    main(sys.argv[1])
