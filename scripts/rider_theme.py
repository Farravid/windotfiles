"""
Generate a Rider (IntelliJ) editor color scheme from the current pywal palette.

Reads the 16-colour palette winwal writes to ~/.cache/wal/colors and emits a
"Winwal" .icls scheme into every Rider config found under %APPDATA%\\JetBrains.
The scheme inherits from Darcula (or the light default for a light wallpaper)
and only overrides the syntax roles worth colouring, so it stays small.

update_winwal_colors.py calls write_theme() as part of the wallpaper pipeline.

Run standalone to (re)generate from the current palette:  python rider_theme.py
Self-test the generated XML (no Rider needed):            python rider_theme.py --selftest

Note: Rider caches colour schemes, so pick "Winwal" once under
Settings > Editor > Color Scheme, and restart Rider to see palette updates.
"""

import os
import sys
from pathlib import Path
from xml.sax.saxutils import quoteattr

WAL_COLORS = Path.home() / ".cache" / "wal" / "colors"


def read_palette() -> list[str]:
    colors = [c for c in WAL_COLORS.read_text(encoding="utf-8").split() if c.startswith("#")][:16]
    if len(colors) < 9:
        raise ValueError(f"{WAL_COLORS} missing or incomplete — run update_winwal_colors.py first")
    return colors


def _mix(a: str, b: str, t: float) -> str:
    """Blend two hex colours; return 6-digit hex without '#'."""
    a, b = a.lstrip("#"), b.lstrip("#")
    ch = lambda s, i: int(s[i:i + 2], 16)
    return "".join(f"{round(ch(a, i) + (ch(b, i) - ch(a, i)) * t):02x}" for i in (0, 2, 4))


def build_icls(colors: list[str]) -> str:
    h = [c.lstrip("#").lower() for c in colors]
    bg, fg, dim = h[0], h[7], h[8]
    r, g, b = int(bg[0:2], 16), int(bg[2:4], 16), int(bg[4:6], 16)
    parent = "Darcula" if (0.299 * r + 0.587 * g + 0.114 * b) < 128 else "Default"

    editor = {
        "CARET_COLOR": fg,
        "CARET_ROW_COLOR": _mix(bg, fg, 0.08),
        "GUTTER_BACKGROUND": bg,
        "CONSOLE_BACKGROUND_KEY": bg,
        "LINE_NUMBERS_COLOR": dim,
        "TEARLINE_COLOR": _mix(bg, fg, 0.15),
        "SELECTION_BACKGROUND": _mix(bg, h[5], 0.40),
        "INDENT_GUIDE": _mix(bg, fg, 0.15),
        "SELECTED_INDENT_GUIDE": _mix(bg, fg, 0.30),
        "WHITESPACES": _mix(bg, fg, 0.20),
    }

    # (role, foreground, font_type)  — font 0 normal, 1 bold, 2 italic
    attrs = [
        ("TEXT", fg, 0, bg),
        ("DEFAULT_KEYWORD", h[5], 1, None),
        ("DEFAULT_STRING", h[2], 0, None),
        ("DEFAULT_VALID_STRING_ESCAPE", h[6], 0, None),
        ("DEFAULT_NUMBER", h[3], 0, None),
        ("DEFAULT_CONSTANT", h[3], 0, None),
        ("DEFAULT_LINE_COMMENT", dim, 2, None),
        ("DEFAULT_BLOCK_COMMENT", dim, 2, None),
        ("DEFAULT_DOC_COMMENT", dim, 2, None),
        ("DEFAULT_FUNCTION_DECLARATION", h[4], 0, None),
        ("DEFAULT_FUNCTION_CALL", h[4], 0, None),
        ("DEFAULT_CLASS_NAME", h[6], 0, None),
        ("DEFAULT_CLASS_REFERENCE", h[6], 0, None),
        ("DEFAULT_INTERFACE_NAME", h[6], 0, None),
        ("DEFAULT_INSTANCE_FIELD", h[1], 0, None),
        ("DEFAULT_STATIC_FIELD", h[1], 0, None),
        ("DEFAULT_PARAMETER", fg, 0, None),
        ("DEFAULT_LOCAL_VARIABLE", fg, 0, None),
        ("DEFAULT_OPERATION_SIGN", h[5], 0, None),
        ("DEFAULT_BRACES", fg, 0, None),
        ("DEFAULT_PARENTHS", fg, 0, None),
        ("DEFAULT_BRACKETS", fg, 0, None),
        ("DEFAULT_DOT", dim, 0, None),
        ("DEFAULT_COMMA", dim, 0, None),
        ("DEFAULT_SEMICOLON", dim, 0, None),
        ("DEFAULT_METADATA", h[3], 0, None),
        ("DEFAULT_TAG", h[1], 0, None),
        ("DEFAULT_ATTRIBUTE", h[3], 0, None),
    ]

    lines = [f'<scheme name="Winwal" version="142" parent_scheme={quoteattr(parent)}>']
    lines.append("  <colors>")
    for name, val in editor.items():
        lines.append(f'    <option name="{name}" value="{val}" />')
    lines.append("  </colors>")
    lines.append("  <attributes>")
    for name, fore, font, back in attrs:
        lines.append(f'    <option name="{name}">')
        lines.append("      <value>")
        lines.append(f'        <option name="FOREGROUND" value="{fore}" />')
        if back:
            lines.append(f'        <option name="BACKGROUND" value="{back}" />')
        if font:
            lines.append(f'        <option name="FONT_TYPE" value="{font}" />')
        lines.append("      </value>")
        lines.append("    </option>")
    lines.append("  </attributes>")
    lines.append("</scheme>")
    return "\n".join(lines) + "\n"


def rider_colors_dirs() -> list[Path]:
    jb = Path(os.environ["APPDATA"]) / "JetBrains"
    return [d / "colors" for d in jb.glob("Rider*") if d.is_dir()]


def write_theme() -> list[Path]:
    icls = build_icls(read_palette())
    dirs = rider_colors_dirs()
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        (d / "Winwal.icls").write_text(icls, encoding="utf-8")
    return dirs


def _selftest():
    import xml.etree.ElementTree as ET
    palette = [f"#{i:02x}{i:02x}{i:02x}" for i in range(0, 256, 16)]  # 16 grey ramp
    root = ET.fromstring(build_icls(palette))
    assert root.tag == "scheme" and root.get("name") == "Winwal"
    assert root.get("parent_scheme") == "Darcula"  # bg #000000 is dark
    text = next(o for o in root.find("attributes") if o.get("name") == "TEXT")
    fg = next(v for v in text.find("value") if v.get("name") == "FOREGROUND")
    assert fg.get("value") == "707070", fg.get("value")  # palette[7]
    # light wallpaper -> light parent
    light = ["#eeeeee"] + palette[1:]
    assert ET.fromstring(build_icls(light)).get("parent_scheme") == "Default"
    print("selftest ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        dirs = write_theme()
        if dirs:
            print("Wrote Winwal.icls to:")
            for d in dirs:
                print(f"  {d}")
            print('Pick "Winwal" under Settings > Editor > Color Scheme (restart Rider for palette updates).')
        else:
            print("No Rider config found under %APPDATA%\\JetBrains.")
