{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # (UPDATED): byzantine_to_western.py with Accordion Sidebar UI\
\
import tkinter as tk\
from tkinter import ttk, filedialog, messagebox\
from music21 import stream, note, metadata, converter, midi, environment, pitch\
import os\
import tempfile\
import json\
from PIL import Image, ImageTk\
\
# Real modal interval structures (semitone steps)\
MODE_INTERVALS = \{\
    "1st Mode": [2, 2, 1, 2, 2, 2, 1],\
    "2nd Mode": [2, 1, 2, 2, 1, 2, 2],\
    "3rd Mode": [1, 3, 1, 2, 1, 3, 1],\
    "4th Mode": [2, 2, 2, 1, 2, 2, 1],\
    "Plagal 1st": [2, 1, 2, 2, 1, 2, 2],\
    "Plagal 2nd": [1, 2, 2, 1, 3, 1, 2],\
    "Grave Mode": [1, 2, 1, 2, 2, 1, 3],\
    "Plagal 4th": [2, 2, 1, 2, 2, 1, 2]\
\}\
\
MODE_BASES = \{\
    "1st Mode": 62,\
    "2nd Mode": 62,\
    "3rd Mode": 62,\
    "4th Mode": 65,\
    "Plagal 1st": 55,\
    "Plagal 2nd": 55,\
    "Grave Mode": 57,\
    "Plagal 4th": 60\
\}\
\
NEUME_MAP = \{\
    "ison": 0,\
    "oligon": 1,\
    "petaste": 2,\
    "klasma": -1,\
    "apostrophos": -1,\
    "kentemata": -2,\
    "elaphron": 1,\
    "argon": -2,\
    "apoderma": 0,\
    "bareia": -1,\
    "hyporrhoe": -2,\
    "oligon-kentema": 2\
\}\
\
def scale_degree_to_pitch(base_pitch, scale, degree):\
    pitch_value = base_pitch\
    for i in range(abs(degree)):\
        step = scale[i % len(scale)]\
        pitch_value += step if degree > 0 else -step\
    return pitch_value\
\
def convert_neumes_to_stream(neumes, default_mode, text_underlay):\
    current_mode = default_mode\
    base_pitch = MODE_BASES.get(current_mode, 60)\
    intervals = MODE_INTERVALS.get(current_mode, [2, 2, 1, 2, 2, 2, 1])\
    melody = stream.Part()\
    melody.append(metadata.Metadata(title="Byzantine Transcription"))\
    degree = 0\
\
        degree = 0\
\
    for i, entry in enumerate(neumes):\
        if isinstance(entry, dict) and "fthora" in entry:\
            current_mode = entry["fthora"]\
            base_pitch = MODE_BASES.get(current_mode, base_pitch)\
            intervals = MODE_INTERVALS.get(current_mode, intervals)\
            text = note.TextExpression(f"Mode: \{current_mode\}")\
            melody.append(text)\
            continue\
\
        symbol = entry.get("neume") if isinstance(entry, dict) else entry\
        degree += NEUME_MAP.get(symbol, 0)\
        pitch_midi = scale_degree_to_pitch(base_pitch, intervals, degree)\
        n = note.Note()\
        n.pitch.midi = pitch_midi\
        n.quarterLength = 1\
        if i < len(text_underlay):\
            n.lyric = text_underlay[i]\
        melody.append(n)\
\
    return melody\
\
class CollapsibleSection(ttk.Frame):\
    def __init__(self, parent, title, *args, **kwargs):\
        super().__init__(parent, *args, **kwargs)\
        self.show = tk.IntVar()\
        self.title_frame = ttk.Frame(self)\
        self.toggle_button = ttk.Checkbutton(\
            self.title_frame, text=title, style="Toolbutton", variable=self.show,\
            command=self.toggle)\
        self.sub_frame = ttk.Frame(self)\
        self.toggle_button.pack(side="left", fill="x")\
        self.title_frame.pack(fill="x")\
        self.sub_frame.pack(fill="x")\
        self.toggle()\
\
    def toggle(self):\
        if self.show.get():\
            self.sub_frame.pack(fill="x")\
        else:\
            self.sub_frame.forget()\
\
# Placeholder for full UI layout with sidebar\
if __name__ == '__main__':\
    root = tk.Tk()\
    root.title("Byzantine to Western Notation Converter")\
    root.geometry("1000x600")\
\
    sidebar = tk.Frame(root, width=200, bg="#f0f0f0")\
    sidebar.pack(side="left", fill="y")\
\
    main_area = tk.Frame(root)\
\
    # Live score preview canvas\
    preview_label = tk.Label(main_area, text="Western Notation Preview")\
    preview_label.pack(pady=5)\
    preview_canvas = tk.Canvas(main_area, width=600, height=200, bg="white")\
    preview_canvas.pack(pady=5)\
\
    def update_score_preview():\
        s = convert_neumes_to_stream([\{"neume": n\} if isinstance(n, str) else n for n in selected_neumes], selected_mode.get(), get_lyrics())\
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:\
            try:\
                s.write('lily.png', fp=tmp_img.name)\
                img = Image.open(tmp_img.name).resize((600, 200))\
                preview_img = ImageTk.PhotoImage(img)\
                preview_canvas.image = preview_img\
                preview_canvas.create_image(0, 0, image=preview_img, anchor="nw")\
            except Exception as e:\
                print("Preview Error:", e)\
    main_area.pack(side="right", fill="both", expand=True)\
\
    # Example accordion sections\
    modes_section = CollapsibleSection(sidebar, "Modes / Moduri")\
    modes_section.pack(fill="x", pady=5)\
\
    mode_dropdown_frame = tk.Frame(modes_section.sub_frame)\
    mode_dropdown_frame.pack(fill="x", padx=5, pady=5)\
\
    tk.Label(mode_dropdown_frame, text="Select Mode / Alege Mod:").pack(anchor="w")\
    selected_mode = tk.StringVar(value="1st Mode")\
    mode_menu = ttk.Combobox(mode_dropdown_frame, textvariable=selected_mode, values=list(MODE_INTERVALS.keys()), state="readonly")\
    mode_menu.pack(fill="x")\
\
    neume_section = CollapsibleSection(sidebar, "Neumes / Neume")\
    neume_section.pack(fill="x", pady=5)\
\
    neume_buttons_frame = tk.Frame(neume_section.sub_frame)\
    neume_buttons_frame.pack(fill="x", padx=5, pady=5)\
\
    selected_neumes = []\
\
    reorder_frame = tk.Frame(main_area)\
    reorder_frame.pack(fill="x", pady=5)\
\
    reorder_listbox = tk.Listbox(reorder_frame, height=4, selectmode="single")\
    reorder_listbox.pack(side="left", fill="x", expand=True, padx=5)\
\
    def refresh_reorder_list():\
        reorder_listbox.delete(0, tk.END)\
        for i, n in enumerate(selected_neumes):\
            label = n["neume"] if isinstance(n, dict) else n\
            reorder_listbox.insert(tk.END, f"\{i+1\}. \{label\}")\
\
    def move_up():\
        sel = reorder_listbox.curselection()\
        if sel and sel[0] > 0:\
            idx = sel[0]\
            selected_neumes[idx-1], selected_neumes[idx] = selected_neumes[idx], selected_neumes[idx-1]\
            refresh_reorder_list()\
            reorder_listbox.select_set(idx-1)\
            update_score_preview()\
\
    def move_down():\
        sel = reorder_listbox.curselection()\
        if sel and sel[0] < len(selected_neumes) - 1:\
            idx = sel[0]\
            selected_neumes[idx], selected_neumes[idx+1] = selected_neumes[idx+1], selected_neumes[idx]\
            refresh_reorder_list()\
            reorder_listbox.select_set(idx+1)\
            update_score_preview()\
\
    up_btn = tk.Button(reorder_frame, text="\uc0\u8593 ", command=move_up)\
    up_btn.pack(side="left", padx=5)\
\
    down_btn = tk.Button(reorder_frame, text="\uc0\u8595 ", command=move_down)\
    down_btn.pack(side="left", padx=5)\
\
    def add_neume(neume):\
        selected_neumes.append(neume)\
        print("Added neume:", neume)\
        refresh_reorder_list()\
        update_score_preview()\
\
    for neume_name in NEUME_MAP:\
        btn = tk.Button(\
            neume_buttons_frame,\
            text=neume_name.capitalize(),\
            width=14,\
            height=2,\
            bg="#dbeafe",\
            relief="raised",\
            command=lambda n=neume_name: add_neume(n)\
        )\
        btn.pack(pady=2, fill="x")\
\
    lyrics_section = CollapsibleSection(sidebar, "Text / Text")\
    lyrics_section.pack(fill="x", pady=5)\
\
    lyrics_textbox = tk.Text(lyrics_section.sub_frame, height=5, wrap="word")\
    lyrics_textbox.pack(fill="both", padx=5, pady=5)\
\
    def get_lyrics():\
        return lyrics_textbox.get("1.0", tk.END).strip().split()\
\
    control_section = CollapsibleSection(sidebar, "Controls / Comenzi")\
    control_section.pack(fill="x", pady=5)\
\
    export_controls_frame = tk.Frame(control_section.sub_frame)\
    export_controls_frame.pack(fill="x", padx=5, pady=5)\
\
    def preview_score():\
        s = convert_neumes_to_stream([\{"neume": n\} if isinstance(n, str) else n for n in selected_neumes], selected_mode.get(), [])\
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp:\
            try:\
                s.write('lily.pdf', fp=temp.name)\
                os.system(f'open "\{temp.name\}"')  # macOS-specific\
            except Exception as e:\
                messagebox.showerror("Error", str(e))\
\
    def export_as_pdf():\
        s = convert_neumes_to_stream([\{"neume": n\} if isinstance(n, str) else n for n in selected_neumes], selected_mode.get(), [])\
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])\
        if pdf_path:\
            try:\
                s.write('lily.pdf', fp=pdf_path)\
                messagebox.showinfo("Success", f"PDF exported to \{pdf_path\}")\
            except Exception as e:\
                messagebox.showerror("Error", str(e))\
\
    tk.Button(export_controls_frame, text="Preview Score", command=preview_score).pack(fill="x", pady=2)\
    tk.Button(export_controls_frame, text="Export as PDF", command=export_as_pdf).pack(fill="x", pady=2)\
\
    def export_as_musicxml():\
        lyrics = get_lyrics()\
        s = convert_neumes_to_stream([\{"neume": n\} if isinstance(n, str) else n for n in selected_neumes], selected_mode.get(), lyrics)\
        xml_path = filedialog.asksaveasfilename(defaultextension=".musicxml", filetypes=[("MusicXML Files", "*.musicxml")])\
        if xml_path:\
            try:\
                s.write('musicxml', fp=xml_path)\
                messagebox.showinfo("Success", f"MusicXML exported to \{xml_path\}")\
            except Exception as e:\
                messagebox.showerror("Error", str(e))\
    tk.Button(export_controls_frame, text="Export as MusicXML", command=export_as_musicxml).pack(fill="x", pady=2)\
\
    def play_midi():\
        lyrics = get_lyrics()\
        s = convert_neumes_to_stream([\{"neume": n\} if isinstance(n, str) else n for n in selected_neumes], selected_mode.get(), lyrics)\
        mf = midi.translate.streamToMidiFile(s)\
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mid")\
        mf.open(temp.name, 'wb')\
        mf.write()\
        mf.close()\
        os.system(f"open \{temp.name\}")  # macOS default MIDI player\
\
    tk.Button(export_controls_frame, text="Play MIDI", command=play_midi).pack(fill="x", pady=2)\
\
    def save_project():\
        data = \{\
            "neumes": selected_neumes,\
            "mode": selected_mode.get(),\
            "lyrics": get_lyrics()\
        \}\
        path = filedialog.asksaveasfilename(defaultextension=".byzproj", filetypes=[("Byzantine Project", "*.byzproj")])\
        if path:\
            with open(path, 'w') as f:\
                json.dump(data, f)\
            messagebox.showinfo("Saved", f"Project saved to \{path\}")\
\
    def load_project():\
        path = filedialog.askopenfilename(filetypes=[("Byzantine Project", "*.byzproj")])\
        if path:\
            with open(path, 'r') as f:\
                data = json.load(f)\
            selected_neumes.clear()\
            selected_neumes.extend(data["neumes"])\
            selected_mode.set(data["mode"])\
            lyrics_textbox.delete("1.0", tk.END)\
            lyrics_textbox.insert("1.0", ' '.join(data["lyrics"]))\
            messagebox.showinfo("Loaded", f"Project loaded from \{path\}")\
\
    tk.Button(export_controls_frame, text="Save Project", command=save_project).pack(fill="x", pady=2)\
    tk.Button(export_controls_frame, text="Load Project", command=load_project).pack(fill="x", pady=2)\
\
    root.mainloop()\
}