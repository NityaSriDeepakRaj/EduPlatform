# converter/to_manim.py
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import argparse

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"

def load_dsl(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def render_template(dsl: dict, out_path: Path):
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape([])
    )
    tpl = env.get_template("scene_template.py.j2")
    rendered = tpl.render(**dsl)
    out_path.write_text(rendered, encoding="utf-8")
    print(f"Wrote Manim file: {out_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dsl", help="Path to DSL JSON")
    parser.add_argument("--out", help="Output .py path", default="output/generated_scene.py")
    args = parser.parse_args()

    dsl = load_dsl(Path(args.dsl))
    # Basic normalization: ensure keys present
    if "scene_sequence" not in dsl:
        raise ValueError("DSL missing scene_sequence")
    # Render
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    render_template(dsl, out_path)

if __name__ == "__main__":
    main()
