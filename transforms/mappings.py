# transforms/mappings.py
import math
from typing import Dict, Any, List

READING_SPEED = 200.0  # chars per second

def estimate_duration(text: str, base: float = 1.0, min_dur: float = 1.5, max_dur: float = 8.0) -> float:
    chars = len(text or "")
    extra = chars / READING_SPEED
    dur = base + extra
    return max(min_dur, min(max_dur, dur))

def create_title_frame(title: str) -> Dict[str, Any]:
    return {
        "id": "title",
        "type": "frame",
        "start": 0.0,
        "end": 2.5,
        "camera": {"type": "static", "zoom": 1.0},
        "background": {"color": "#FFFFFF"},
        "actors": [
            {"kind": "text", "id": "title_text", "text": title, "pos": [0, 1.5], "font_size": 56,
             "animate": {"in": "fade_in", "duration": 0.6}}
        ]
    }

def transform(input_json: Dict[str, Any]) -> Dict[str, Any]:
    title = input_json.get("title", "Untitled")
    style = input_json.get("style", "lecture")
    steps = input_json.get("steps", [])
    # metadata duration estimate: we will sum durations
    scene_sequence: List[Dict[str, Any]] = []
    # title
    scene_sequence.append(create_title_frame(title))
    t = 2.5
    for idx, step in enumerate(steps):
        text = step.get("text", "")
        # choose kind: if contains latex markers, use math
        kind = "text"
        if "$" in text or "\\" in text or "f(" in text:
            kind = "math"
        duration = estimate_duration(text)
        actor = {"kind": kind, "id": f"actor_{idx}", "text": text, "pos": [0, 1.0], "font_size": 36,
                 "animate": {"in": "write", "duration": min(1.5, duration / 2)}}
        if kind == "math":
            actor["latex"] = text
        scene = {
            "id": f"scene_{idx}",
            "type": "frame",
            "start": round(t, 3),
            "end": round(t + duration, 3),
            "camera": {"type": "static"},
            "actors": [actor]
        }
        scene_sequence.append(scene)
        t += duration
    total_duration = round(t, 3)
    dsl = {
        "metadata": {"title": title, "fps": 30, "duration": total_duration, "style": style},
        "scene_sequence": scene_sequence,
        "assets": []
    }
    return dsl

# quick test:
if __name__ == "__main__":
    sample = {"title":"Test","steps":[{"text":"Definition of limit."},{"text":"Example: f(x)=x^2"}],"style":"lecture"}
    import json
    print(json.dumps(transform(sample), indent=2))
