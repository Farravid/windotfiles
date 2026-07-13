"""
setup_editor.py — a pretty GUI to build startup setups.

Setups are the TOML files in scripts/setups/ that startup.py reads. Pick a
program straight from Explorer: its icon, display name and GlazeWM processName
are grabbed automatically — you only choose the workspace. The window is themed
from the live pywal palette (.config/wezterm/winwal.toml).

Run:  python setup_editor.py
Self-test the TOML round-trip (no window):  python setup_editor.py --selftest
"""

import re
import os
import sys
import tomllib
from pathlib import Path

SETUPS_DIR = Path(__file__).parent / "setups"
WINWAL = Path(__file__).parents[1] / ".config" / "wezterm" / "winwal.toml"
NAME_RE = re.compile(r"[A-Za-z0-9_-]+")


# ------------------------------------------------------------------ TOML I/O
def _toml_str(v: str) -> str:
    """A valid TOML basic string, backslashes and quotes escaped."""
    return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'


def list_setups() -> list[str]:
    return sorted(p.stem for p in SETUPS_DIR.glob("*.toml"))


def read_setup(name: str) -> list[dict]:
    data = tomllib.loads((SETUPS_DIR / f"{name}.toml").read_text(encoding="utf-8"))
    return data.get("apps", [])


def launch_cmd(exe: str, args: str = "") -> str:
    """The shell command that starts `exe`, optionally with extra arguments.

    Args let a card launch a program *inside* another — e.g. a terminal with a
    program already running: exe = wezterm-gui.exe, args = `start -- nvim`.
    """
    cmd = f'start "" "{exe}"'
    return f"{cmd} {args.strip()}" if args.strip() else cmd


def args_of(app: dict) -> str:
    """Arguments a card should show: the stored `args`, else parsed off `launch`."""
    if app.get("args"):
        return app["args"]
    exe, launch = app.get("exe", ""), app.get("launch", "")
    prefix = f'start "" "{exe}"'
    return launch[len(prefix):].strip() if exe and launch.startswith(prefix) else ""


def write_setup(name: str, apps: list[dict]) -> None:
    out = []
    for a in apps:
        out.append("[[apps]]")
        for k in ("name", "exe", "launch", "args", "process"):
            if a.get(k):
                out.append(f"{k} = {_toml_str(str(a[k]))}")
        out.append(f"workspace = {int(a.get('workspace', 1))}")
        out.append("")
    SETUPS_DIR.mkdir(exist_ok=True)
    (SETUPS_DIR / f"{name}.toml").write_text("\n".join(out), encoding="utf-8")


def delete_setup(name: str) -> None:
    (SETUPS_DIR / f"{name}.toml").unlink(missing_ok=True)


def rename_setup(old: str, new: str) -> None:
    (SETUPS_DIR / f"{old}.toml").rename(SETUPS_DIR / f"{new}.toml")


def clone_setup(old: str, new: str) -> None:
    (SETUPS_DIR / f"{new}.toml").write_bytes((SETUPS_DIR / f"{old}.toml").read_bytes())


def exe_of(app: dict) -> str | None:
    """The program path for an app: stored `exe`, else parsed out of `launch`."""
    if app.get("exe"):
        return app["exe"]
    m = re.search(r'"([^"]+\.exe)"|(\S+\.exe)', app.get("launch", ""), re.I)
    return (m.group(1) or m.group(2)) if m else None


def app_from_exe(path: str) -> dict:
    """Build an app dict from a picked program: name/process/icon auto-derived."""
    p = Path(path)
    stem = p.stem
    return {
        "name": stem.replace("-", " ").replace("_", " ").title(),
        "exe": str(p),
        "launch": launch_cmd(str(p)),
        "process": stem,   # GlazeWM reports the exe name without extension
        "workspace": 1,
    }


def _selftest():
    import tempfile
    global SETUPS_DIR
    SETUPS_DIR = Path(tempfile.mkdtemp())
    apps = [app_from_exe(r"C:\Program Files\Foo Bar\slack.exe")]
    apps[0]["workspace"] = 3
    write_setup("t", apps)
    back = read_setup("t")
    assert back == apps, back
    assert exe_of(back[0]) == r"C:\Program Files\Foo Bar\slack.exe"
    assert list_setups() == ["t"]
    rename_setup("t", "t2")
    assert list_setups() == ["t2"] and read_setup("t2") == apps
    rename_setup("t2", "t")
    clone_setup("t", "t-copy")
    assert list_setups() == ["t", "t-copy"] and read_setup("t-copy") == apps
    delete_setup("t-copy")
    # a hand-written entry with no `exe` still yields a path for its icon
    assert exe_of({"launch": 'start /b "" "C:\\x\\brave.exe"'}) == r"C:\x\brave.exe"
    assert exe_of({"launch": "start /b wezterm-gui"}) is None
    # args round-trip: launch is rebuilt to run a program inside the terminal
    term = app_from_exe(r"C:\Program Files\WezTerm\wezterm-gui.exe")
    term["args"] = "start -- nvim"
    term["launch"] = launch_cmd(term["exe"], term["args"])
    write_setup("a", [term])
    got = read_setup("a")[0]
    assert got["args"] == "start -- nvim"
    assert got["launch"] == 'start "" "C:\\Program Files\\WezTerm\\wezterm-gui.exe" start -- nvim'
    assert args_of(got) == "start -- nvim"
    assert args_of(read_setup("t")[0]) == ""   # no args -> empty
    delete_setup("a")
    delete_setup("t")
    assert list_setups() == []
    print("selftest ok")


if "--selftest" in sys.argv:
    _selftest()
    sys.exit(0)


# ------------------------------------------------------------------ GUI
from PySide6.QtCore import Qt, QFileInfo, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QListWidget, QScrollArea,
    QPushButton, QLabel, QLineEdit, QSpinBox, QFileDialog, QInputDialog,
    QMessageBox, QFileIconProvider, QHBoxLayout, QVBoxLayout, QStyle,
    QAbstractSpinBox,
)

_PROV: QFileIconProvider | None = None


def app_icon(exe: str | None, style: QStyle) -> QIcon:
    global _PROV
    if exe and Path(exe).exists():
        _PROV = _PROV or QFileIconProvider()
        ic = _PROV.icon(QFileInfo(exe))
        if not ic.isNull():
            return ic
    return style.standardIcon(QStyle.StandardPixmap.SP_FileIcon)


def load_qss() -> str:
    """Build a stylesheet from the current pywal palette (with a dark fallback)."""
    try:
        c = tomllib.loads(WINWAL.read_text(encoding="utf-8"))["colors"]
        bg, fg, accent = c["background"], c["foreground"], c["ansi"][5]
    except Exception:
        bg, fg, accent = "#1e1e2e", "#cdd6f4", "#a855f7"
    panel = _mix(bg, fg, 0.07)
    border = _mix(bg, fg, 0.16)
    hover = _mix(accent, fg, 0.15)
    on_accent = _mix(bg, "#000000", 0.4)
    return f"""
    QWidget {{ background: {bg}; color: {fg};
               font-family: 'Segoe UI'; font-size: 14px; }}
    #Sidebar {{ background: {panel}; border-right: 1px solid {border}; }}
    QListWidget {{ background: {panel}; border: none; padding: 6px; }}
    QListWidget::item {{ padding: 9px 12px; border-radius: 8px; }}
    QListWidget::item:selected {{ background: {accent}; color: {on_accent}; }}
    QListWidget::item:hover:!selected {{ background: {border}; }}
    #Title {{ font-size: 22px; font-weight: 600; }}
    #Hint {{ color: {border}; font-size: 15px; }}
    #Sub {{ color: {_mix(bg, fg, 0.45)}; font-size: 11px; }}
    QPushButton {{ background: {accent}; color: {on_accent}; border: none;
                   border-radius: 8px; padding: 8px 16px; font-weight: 600; }}
    QPushButton:hover {{ background: {hover}; }}
    QPushButton#Ghost {{ background: transparent; color: {fg};
                         border: 1px solid {border}; }}
    QPushButton#Ghost:hover {{ background: {panel}; }}
    QPushButton#Remove {{ background: transparent; color: {fg};
                          border: none; border-radius: 14px;
                          font-size: 16px; padding: 0; }}
    QPushButton#Remove:hover {{ background: {_mix(bg, '#ff5555', 0.5)}; }}
    #Card {{ background: {panel}; border: 1px solid {border};
             border-radius: 12px; }}
    QLineEdit, QSpinBox {{ background: {bg}; color: {fg};
                           border: 1px solid {border};
                           border-radius: 8px; padding: 6px 8px; }}
    QSpinBox {{ font-size: 16px; font-weight: 600; }}
    QLineEdit:focus, QSpinBox:focus {{ border: 1px solid {accent}; }}
    QScrollArea {{ border: none; }}
    """


def _mix(a: str, b: str, t: float) -> str:
    a, b = a.lstrip("#"), b.lstrip("#")
    ch = lambda s, i: int(s[i:i + 2], 16)
    r = [round(ch(a, i) + (ch(b, i) - ch(a, i)) * t) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(r)


class AppCard(QFrame):
    """One app: icon, editable name + detected process, workspace, remove."""

    def __init__(self, app: dict, on_change, on_remove):
        super().__init__()
        self.setObjectName("Card")
        self.app = dict(app)

        icon = QLabel()
        icon.setPixmap(app_icon(exe_of(app), self.style()).pixmap(40, 40))

        self.name = QLineEdit(app.get("name", ""))
        self.name.setPlaceholderText("Display name")
        self.name.textChanged.connect(on_change)
        sub = QLabel(f"process: {app.get('process', '?')}")
        sub.setObjectName("Sub")
        self.args = QLineEdit(args_of(app))
        self.args.setPlaceholderText("arguments (optional) — e.g. terminal: start -- nvim")
        self.args.textChanged.connect(on_change)
        col = QVBoxLayout()
        col.setSpacing(2)
        col.addWidget(self.name)
        col.addWidget(sub)
        col.addWidget(self.args)

        ws_label = QLabel("Workspace")
        self.ws = QSpinBox()
        self.ws.setRange(1, 9)
        self.ws.setValue(int(app.get("workspace", 1)))
        self.ws.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.ws.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ws.setFixedWidth(48)
        self.ws.valueChanged.connect(on_change)

        remove = QPushButton("✕")
        remove.setObjectName("Remove")
        remove.setFixedSize(28, 28)
        remove.clicked.connect(lambda: on_remove(self))

        row = QHBoxLayout(self)
        row.setContentsMargins(14, 12, 14, 12)
        row.setSpacing(14)
        row.addWidget(icon)
        row.addLayout(col, 1)
        row.addWidget(ws_label)
        row.addWidget(self.ws)
        row.addWidget(remove)

    def to_dict(self) -> dict:
        d = dict(self.app)
        d["name"] = self.name.text().strip() or self.app.get("process", "app")
        d["workspace"] = self.ws.value()
        args = self.args.text().strip()
        if d.get("exe"):          # rebuild launch from exe + args
            d["launch"] = launch_cmd(d["exe"], args)
        if args:
            d["args"] = args
        else:
            d.pop("args", None)
        return d


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Startup Setups")
        self.resize(940, 600)
        self.current: str | None = None
        self.cards: list[AppCard] = []
        self._loading = False

        # ---- sidebar
        self.setups = QListWidget()
        self.setups.currentItemChanged.connect(self.on_pick)
        self.setups.itemDoubleClicked.connect(lambda *_: self.rename_current())
        new_btn = QPushButton("New")
        new_btn.clicked.connect(self.new_setup)
        clone_btn = QPushButton("Clone")
        clone_btn.setObjectName("Ghost")
        clone_btn.clicked.connect(self.clone_current)
        del_btn = QPushButton("Delete")
        del_btn.setObjectName("Ghost")
        del_btn.clicked.connect(self.delete_current)
        sbtns = QHBoxLayout()
        sbtns.addWidget(new_btn)
        sbtns.addWidget(clone_btn)
        sbtns.addWidget(del_btn)
        side = QVBoxLayout()
        side.setContentsMargins(12, 12, 12, 12)
        side.addWidget(QLabel("Setups"))
        side.addWidget(self.setups, 1)
        side.addLayout(sbtns)
        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(240)
        sidebar.setLayout(side)

        # ---- header
        self.title = QLabel("Select a setup")
        self.title.setObjectName("Title")
        add_btn = QPushButton("＋  Add program")
        add_btn.clicked.connect(self.add_app)
        save_btn = QPushButton("Save")
        save_btn.setObjectName("Ghost")
        save_btn.clicked.connect(self.save)
        header = QHBoxLayout()
        header.addWidget(self.title)
        header.addStretch(1)
        header.addWidget(add_btn)
        header.addWidget(save_btn)

        # ---- cards area
        self.cards_box = QVBoxLayout()
        self.cards_box.setSpacing(10)
        self.cards_box.addStretch(1)
        inner = QWidget()
        inner.setLayout(self.cards_box)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(inner)
        self.hint = QLabel("Pick a setup on the left, then add programs.")
        self.hint.setObjectName("Hint")
        self.hint.setAlignment(Qt.AlignmentFlag.AlignCenter)

        right = QVBoxLayout()
        right.setContentsMargins(20, 18, 20, 18)
        right.addLayout(header)
        right.addWidget(self.hint)
        right.addWidget(scroll, 1)
        rightw = QWidget()
        rightw.setLayout(right)

        root = QHBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(sidebar)
        root.addWidget(rightw, 1)
        central = QWidget()
        central.setLayout(root)
        self.setCentralWidget(central)

        self.dirty = False
        self.refresh_setups()

    # ---- setups
    def refresh_setups(self, select: str | None = None):
        self._loading = True
        self.setups.clear()
        self.setups.addItems(list_setups())
        self._loading = False
        if select:
            items = self.setups.findItems(select, Qt.MatchFlag.MatchExactly)
            if items:
                self.setups.setCurrentItem(items[0])

    def confirm_discard(self) -> bool:
        return not self.dirty or QMessageBox.question(
            self, "Unsaved changes",
            f"Discard unsaved changes to '{self.current}'?") == QMessageBox.StandardButton.Yes

    def on_pick(self, current, previous):
        if self._loading or current is None:
            return
        if not self.confirm_discard():
            self._loading = True
            self.setups.setCurrentItem(previous)
            self._loading = False
            return
        self.load_setup(current.text())

    def load_setup(self, name: str):
        self.current = name
        self.title.setText(name)
        self.clear_cards()
        self._loading = True
        for app in read_setup(name):
            self.add_card(app)
        self._loading = False
        self.hint.setVisible(not self.cards)
        self.set_clean()

    def ask_name(self, title: str, initial: str = "") -> str | None:
        name, ok = QInputDialog.getText(
            self, title, "Setup name (letters, numbers, - _):", text=initial)
        name = name.strip()
        if not ok or not name:
            return None
        if not NAME_RE.fullmatch(name):
            QMessageBox.warning(self, "Invalid name", "Use only letters, numbers, dashes, underscores.")
            return None
        if name in list_setups():
            QMessageBox.warning(self, "Exists", f"Setup '{name}' already exists.")
            return None
        return name

    def new_setup(self):
        if not self.confirm_discard():
            return
        name = self.ask_name("New setup")
        if name:
            write_setup(name, [])
            self.refresh_setups(select=name)

    def rename_current(self):
        if self.current is None or not self.confirm_discard():
            return
        name = self.ask_name("Rename setup", initial=self.current)
        if name:
            rename_setup(self.current, name)
            self.refresh_setups(select=name)

    def clone_current(self):
        if self.current is None or not self.confirm_discard():
            return
        name = self.ask_name("Clone setup", initial=f"{self.current}-copy")
        if name:
            clone_setup(self.current, name)
            self.refresh_setups(select=name)

    def delete_current(self):
        if self.current and QMessageBox.question(
                self, "Delete", f"Delete setup '{self.current}'?") == QMessageBox.StandardButton.Yes:
            delete_setup(self.current)
            self.current = None
            self.title.setText("Select a setup")
            self.clear_cards()
            self.hint.setVisible(True)
            self.refresh_setups()

    # ---- cards
    def clear_cards(self):
        for c in self.cards:
            c.setParent(None)
        self.cards.clear()

    def add_card(self, app: dict):
        card = AppCard(app, self.set_dirty, self.remove_card)
        self.cards.append(card)
        self.cards_box.insertWidget(self.cards_box.count() - 1, card)

    def add_app(self):
        if self.current is None:
            QMessageBox.information(self, "No setup", "Select or create a setup first.")
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "Pick a program", os.environ.get("ProgramFiles", ""), "Programs (*.exe)")
        if not path:
            return
        self.add_card(app_from_exe(path))
        self.hint.setVisible(False)
        self.set_dirty()

    def remove_card(self, card: AppCard):
        self.cards.remove(card)
        card.setParent(None)
        self.hint.setVisible(not self.cards)
        self.set_dirty()

    # ---- dirty state
    def set_dirty(self, *_):
        if self._loading or self.current is None:
            return
        self.dirty = True
        self.title.setText(f"{self.current}  •")

    def set_clean(self):
        self.dirty = False
        if self.current:
            self.title.setText(self.current)

    def save(self):
        if self.current is None:
            return
        write_setup(self.current, [c.to_dict() for c in self.cards])
        self.set_clean()

    def closeEvent(self, e):
        e.accept() if self.confirm_discard() else e.ignore()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(load_qss())
    win = Editor()
    win.show()
    if "--smoke" in sys.argv:
        QTimer.singleShot(400, app.quit)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
