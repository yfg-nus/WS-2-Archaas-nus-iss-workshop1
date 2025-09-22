
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta
import os, json

from langchain_core.tools import tool

DATA_FP = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data", "mock_forecast.json")
MEM_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "memory")
PROFILE_FP = os.path.join(MEM_DIR, "profile.json")

DEFAULT_PROFILE = {
    "regions_allowed": ["SG", "EU_WEST", "US_WEST"],
    "allowed_shift_minutes": 60
}

def _read_json(fp, default):
    if os.path.exists(fp):
        with open(fp, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                pass
    return default

def _write_json(fp, data):
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_profile():
    os.makedirs(MEM_DIR, exist_ok=True)
    return _read_json(PROFILE_FP, DEFAULT_PROFILE.copy())

def save_profile(p):
    _write_json(PROFILE_FP, p)

def snap_15(dt: datetime) -> datetime:
    minutes = (dt.minute // 15) * 15
    return dt.replace(minute=minutes, second=0, microsecond=0)

def load_forecast():
    with open(DATA_FP, "r", encoding="utf-8") as f:
        return json.load(f)

@tool("get_profile", return_direct=False)
def get_profile_tool() -> dict:
    """Return current persistent preferences: regions_allowed, allowed_shift_minutes."""
    return load_profile()

@tool("list_regions", return_direct=False)
def list_regions_tool() -> list:
    """List accessible regions from persistent preferences."""
    return load_profile().get("regions_allowed", DEFAULT_PROFILE["regions_allowed"])

@tool("update_prefs", return_direct=False)
def update_prefs_tool(regions_allowed: Optional[str] = None, allowed_shift_minutes: Optional[int] = None) -> dict:
    """Update persistent preferences. 
    - regions_allowed: optional comma-separated regions like 'SG,EU_WEST'
    - allowed_shift_minutes: optional integer shift window
    Returns the updated profile.
    Use this tool whenever the user says 'I prefer...' or 'remember...' about regions/shift, or otherwise expresses a clear preference update.
    """
    p = load_profile()
    if regions_allowed:
        regions = [r.strip().upper() for r in regions_allowed.split(",") if r.strip()]
        if regions:
            p["regions_allowed"] = regions
    if allowed_shift_minutes is not None:
        p["allowed_shift_minutes"] = int(allowed_shift_minutes)
    save_profile(p)
    return p

@tool("parse_time", return_direct=False)
def parse_time_tool(text_time: str, now_iso: Optional[str] = None) -> str:
    """Parse a natural-language time into ISO-8601 (snapped to 15 min). 
    Examples: 'tomorrow 10am', '2025-09-13 10:30', 'next Monday 9:00'.
    If parsing fails, return empty string.
    """
    # Minimal naive parser for workshop (no external libs).
    # Accepts formats like 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DD HH:MM', 'HH:MM', '10am', '10:30am', 'tomorrow 10am'.
    from dateutil import parser as dparser
    base_dt = datetime.fromisoformat(now_iso) if now_iso else datetime.now()
    try:
        dt = dparser.parse(text_time, default=base_dt)
        return snap_15(dt).isoformat()
    except Exception:
        return ""

@tool("get_region_forecast", return_direct=False)
def get_region_forecast_tool(region: str) -> list:
    """Return 15-min forecast entries [{'ts': ISO, 'g': int}] for a region from local dataset."""
    data = load_forecast()
    return data.get(region.upper(), [])

@tool("best_slot_in_window", return_direct=False)
def best_slot_in_window_tool(region: str, start_iso: str, window_mins: int) -> dict:
    """Given region, requested start ISO time, and window minutes, return the best slot in the window.
    Output: {'region': str, 'ts': ISO, 'g': int, 'baseline_g': int, 'shift_minutes': int}
    """
    data = load_forecast()
    entries = data.get(region.upper(), [])
    if not entries:
        return {}
    start_dt = snap_15(datetime.fromisoformat(start_iso))
    lo = start_dt - timedelta(minutes=window_mins)
    hi = start_dt + timedelta(minutes=window_mins)
    best = None
    baseline = None
    # baseline: nearest slot to original
    nearest = None
    # Nearest tracks the forecast slot closest in time to the original start (which had already been snapped to 15 min).
    for e in entries:
        ts = datetime.fromisoformat(e["ts"])
        diff = abs((ts - start_dt).total_seconds())
        g = e["g"]
        if nearest is None or diff < nearest[0] or (diff == nearest[0] and g < nearest[1]):
            nearest = (diff, g, ts)
        if lo <= ts <= hi:
            if best is None or g < best[1] or (g == best[1] and ts < best[0]):
                best = (ts, g)
    if best is None:
        return {}
    baseline_g = nearest[1]
    shift_minutes = int((best[0] - start_dt).total_seconds() // 60)
    return {"region": region.upper(), "ts": best[0].isoformat(), "g": best[1], "baseline_g": baseline_g, "shift_minutes": shift_minutes}

@tool("recommend_best", return_direct=False)
def recommend_best_tool(start_iso: str) -> dict:
    """Use current persistent preferences to recommend the best (region, time).
    Looks across all allowed regions and the allowed shift window, returns the globally best pick.
    Output: {'region': str, 'ts': ISO, 'g': int, 'baseline_g': int, 'shift_minutes': int}
    """
    p = load_profile()
    regions = p.get("regions_allowed", DEFAULT_PROFILE["regions_allowed"])
    window = int(p.get("allowed_shift_minutes", DEFAULT_PROFILE["allowed_shift_minutes"]))
    data = load_forecast()
    start_dt = snap_15(datetime.fromisoformat(start_iso))
    best_global = None
    for r in regions:
        entries = data.get(r, [])
        if not entries:
            continue
        # local best within window
        lo = start_dt - timedelta(minutes=window)
        hi = start_dt + timedelta(minutes=window)
        best = None
        nearest = None
        for e in entries:
            ts = datetime.fromisoformat(e["ts"])
            g = e["g"]
            diff = abs((ts - start_dt).total_seconds())
            if nearest is None or diff < nearest[0] or (diff == nearest[0] and g < nearest[1]):
                nearest = (diff, g, ts)
            if lo <= ts <= hi:
                if best is None or g < best[1] or (g == best[1] and ts < best[0]):
                    best = (ts, g)
        if best is None:
            continue
        candidate = {
            "region": r,
            "ts": best[0].isoformat(),
            "g": best[1],
            "baseline_g": nearest[1],
            "shift_minutes": int((best[0] - start_dt).total_seconds() // 60)
        }
        if best_global is None or candidate["g"] < best_global["g"] or (candidate["g"] == best_global["g"] and candidate["ts"] < best_global["ts"]):
            best_global = candidate
    return best_global or {}
