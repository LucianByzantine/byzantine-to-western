# Byzantine to Western Notation Converter

This is a Python desktop application (Tkinter-based) that helps transcribe Byzantine psaltic notation into Western staff notation in real time.

## ✨ Features

- Add neumes via sidebar buttons
- Select musical mode (echos)
- Real-time conversion to Western notation
- Text underlay support
- In-app live visual preview
- Export to PDF and MusicXML
- MIDI playback
- Save/Load `.byzproj` projects
- Drag-and-drop reorder of neumes

## 🛠 Requirements

- Python 3.9+
- music21
- pillow
- LilyPond (for PDF/MIDI preview/export)

## 🔧 Installation

```bash
pip install music21 pillow
brew install lilypond  # on macOS
```

## ▶️ Running

```bash
python3 byzantine_to_western.py
```

## 📦 To package as .app (macOS)

```bash
pip install py2app
python3 setup.py py2app
```

## 📀 Create DMG (macOS)

```bash
brew install create-dmg
create-dmg dist/byzantine_to_western.app
```
