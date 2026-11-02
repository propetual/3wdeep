#!/usr/bin/env python3
"""
3wdeep humanizer - Native Linux Desktop GUI
Built with GTK 4 & Libadwaita

Features:
- Native Wayland / X11 rendering with automatic dark/light theme
- Drag and drop text & file support (.txt, .md, .toml)
- Dynamic Pack Discovery: scans packs/*.toml with zero hardcoded packs
- Live metrics: Density %, Sentence Rhythm / Burstiness, and replacement stats
- One-click copy, sample text loader, and pack creation
- Inline buzzword highlighting (orange = filler, yellow = cliché)
"""

import os
import re
import sys
import math
import tomllib
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, Gdk, GObject

# Import core humanizer components
from humanizer import TextHumanizer, FILLERS_TO_PRUNE, REPLACEMENTS_MAP, CONTRACTIONS_MAP

PACKS_DIR = Path(__file__).parent / "packs"

# ── BACKGROUND IMAGE ──────────────────────────────────────────────────────────
# Drop your exported GIMP image into the project folder and update this path.
# Supported formats: PNG, JPG, WebP.  Set to None to disable.
#
# BACKGROUND_IMAGE = Path(__file__).parent / "background.png"
BACKGROUND_IMAGE = None
# ─────────────────────────────────────────────────────────────────────────────

APP_CSS = """
window {
    /* background-image: url("file:///home/geldof/Downloads/databaise/background.png"); */
    /* background-size: cover; */
    /* background-position: center; */
}

textview.input-view text {
    background-color: transparent;
}
"""



# DYNAMIC PACK LOADER (ZERO HARDCODING)


def extract_replacements_from_toml(data: dict) -> Dict[str, str]:
    """Recursively extracts all key-value string replacements from any TOML structure."""
    replacements = {}
    def recurse(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k.lower() in ('pack_metadata', 'metadata', 'pack'):
                    continue
                if isinstance(v, str):
                    replacements[k.lower()] = v
                elif isinstance(v, dict):
                    recurse(v)
    recurse(data)
    return replacements

def discover_packs() -> List[Dict]:
    """Scans packs/ directory and returns metadata for all available TOML packs."""
    PACKS_DIR.mkdir(exist_ok=True)
    packs = []
    for toml_path in sorted(PACKS_DIR.glob("*.toml")):
        try:
            content = toml_path.read_text(encoding="utf-8")
            data = tomllib.loads(content)
            
            # Extract metadata if available, or generate from filename
            meta = data.get("pack_metadata") or data.get("pack") or {}
            pack_name = meta.get("name") or toml_path.stem.replace("_", " ").title()
            pack_desc = meta.get("description") or f"Custom pack from {toml_path.name}"
            
            reps = extract_replacements_from_toml(data)
            packs.append({
                "path": toml_path,
                "filename": toml_path.name,
                "name": pack_name,
                "description": pack_desc,
                "replacements": reps,
                "count": len(reps)
            })
        except Exception as e:
            print(f"Error parsing pack {toml_path}: {e}")
    return packs


# MAIN APPLICATION WINDOW

class HumanizerWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="3W-DEEP!")
        self.set_default_size(1000, 680)

        # Load CSS (background image + highlight colours)
        css_provider = Gtk.CssProvider()
        css_provider.load_from_string(APP_CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        # State
        self.active_packs: Dict[str, bool] = {}
        self.discovered_packs = discover_packs()
        
        self.rebuild_engine()

        # Build UI layout
        self.toast_overlay = Adw.ToastOverlay.new()
        self.set_content(self.toast_overlay)

        main_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.toast_overlay.set_child(main_box)

        # 1. Header Bar
        self.header_bar = Adw.HeaderBar.new()
        main_box.append(self.header_bar)

        # Packs Menu Button (Dynamic Popover)
        self.packs_menu_button = Gtk.MenuButton.new()
        self.packs_menu_button.set_icon_name("package-x-generic-symbolic")
        self.packs_menu_button.set_tooltip_text("Dynamic Language & Cultural Packs")
        self.header_bar.pack_start(self.packs_menu_button)
        self.setup_packs_popover()

        # Load Sample Button
        sample_btn = Gtk.Button.new_with_label("Sample Text")
        sample_btn.set_tooltip_text("Load sample AI text to test")
        sample_btn.connect("clicked", self.on_load_sample)
        self.header_bar.pack_start(sample_btn)

        # Clear Button
        clear_btn = Gtk.Button.new_with_label("Clear")
        clear_btn.set_tooltip_text("Clear all text fields")
        clear_btn.connect("clicked", self.on_clear_text)
        self.header_bar.pack_start(clear_btn)

        # 2. Metrics Bar (Banner)
        self.metrics_bar = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 16)
        self.metrics_bar.set_margin_top(8)
        self.metrics_bar.set_margin_bottom(8)
        self.metrics_bar.set_margin_start(16)
        self.metrics_bar.set_margin_end(16)
        self.metrics_bar.add_css_class("toolbar")
        main_box.append(self.metrics_bar)

        self.ai_density_label = Gtk.Label.new("Density: 0.0%")
        self.ai_density_label.add_css_class("title-4")
        self.metrics_bar.append(self.ai_density_label)

        self.burstiness_label = Gtk.Label.new("rhythm: Waiting for input")
        self.burstiness_label.add_css_class("dim-label")
        self.metrics_bar.append(self.burstiness_label)

        self.edits_label = Gtk.Label.new("buzzwords: 0")
        self.edits_label.add_css_class("dim-label")
        self.metrics_bar.append(self.edits_label)

        # 3. Main Split View (Input Left, Output Right)
        split_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 12)
        split_box.set_hexpand(True)
        split_box.set_vexpand(True)
        split_box.set_margin_start(16)
        split_box.set_margin_end(16)
        split_box.set_margin_bottom(12)
        main_box.append(split_box)

        # Left Column: Raw Input
        left_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 6)
        left_box.set_hexpand(True)
        split_box.append(left_box)

        input_title = Gtk.Label.new("ORIGINAL TEXT (Drag & Drop Text or Files Here)")
        input_title.set_halign(Gtk.Align.START)
        input_title.add_css_class("heading")
        left_box.append(input_title)

        input_scroller = Gtk.ScrolledWindow.new()
        input_scroller.set_vexpand(True)
        input_scroller.add_css_class("card")
        left_box.append(input_scroller)

        self.input_text_view = Gtk.TextView.new()
        self.input_text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.input_text_view.set_left_margin(12)
        self.input_text_view.set_right_margin(12)
        self.input_text_view.set_top_margin(12)
        self.input_text_view.set_bottom_margin(12)
        self.input_buffer = self.input_text_view.get_buffer()
        self.input_buffer.connect("changed", self.on_text_changed)

        # ── Highlight tags (applied by apply_highlights()) ─────────────────
        tag_table = self.input_buffer.get_tag_table()

        filler_tag = Gtk.TextTag.new("filler")
        filler_tag.set_property("background", "#ff9800")   # orange  – throat-clearing
        filler_tag.set_property("foreground", "#000000")
        filler_tag.set_property("weight", 700)
        tag_table.add(filler_tag)

        buzzword_tag = Gtk.TextTag.new("buzzword")
        buzzword_tag.set_property("background", "#ffd600")  # yellow  – AI cliché
        buzzword_tag.set_property("foreground", "#000000")
        buzzword_tag.set_property("weight", 700)
        tag_table.add(buzzword_tag)
        # ──────────────────────────────────────────────────────────────────
        input_scroller.set_child(self.input_text_view)

        # Setup Drag & Drop on Input View
        self.setup_drop_targets(self.input_text_view)

        # Right Column: Humanized Output
        right_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 6)
        right_box.set_hexpand(True)
        split_box.append(right_box)

        output_header = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 8)
        right_box.append(output_header)

        output_title = Gtk.Label.new("OUTPUT")
        output_title.add_css_class("heading")
        output_header.append(output_title)

        copy_btn = Gtk.Button.new_with_label("Copy Clean Text")
        copy_btn.set_halign(Gtk.Align.END)
        copy_btn.set_hexpand(True)
        copy_btn.add_css_class("suggested-action")
        copy_btn.connect("clicked", self.on_copy_output)
        output_header.append(copy_btn)

        output_scroller = Gtk.ScrolledWindow.new()
        output_scroller.set_vexpand(True)
        output_scroller.add_css_class("card")
        right_box.append(output_scroller)

        self.output_text_view = Gtk.TextView.new()
        self.output_text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.output_text_view.set_left_margin(12)
        self.output_text_view.set_right_margin(12)
        self.output_text_view.set_top_margin(12)
        self.output_text_view.set_bottom_margin(12)
        self.output_buffer = self.output_text_view.get_buffer()
        output_scroller.set_child(self.output_text_view)

        # 4. Bottom Control Bar
        bottom_bar = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 12)
        bottom_bar.set_margin_start(16)
        bottom_bar.set_margin_end(16)
        bottom_bar.set_margin_bottom(16)
        main_box.append(bottom_bar)

        self.scan_btn = Gtk.Button.new_with_label(" Scan ")
        self.scan_btn.connect("clicked", self.on_scan_clicked)
        bottom_bar.append(self.scan_btn)

        self.humanize_btn = Gtk.Button.new_with_label("Humanize")
        self.humanize_btn.add_css_class("suggested-action")
        self.humanize_btn.connect("clicked", self.on_humanize_clicked)
        bottom_bar.append(self.humanize_btn)

    
    # ENGINE & PACK MANAGEMENT
    

    def rebuild_engine(self):
        """Rebuilds the TextHumanizer instance by combining core rules + active packs."""
        merged_replacements = {}
        for p in self.discovered_packs:
            if self.active_packs.get(p["filename"], False):
                merged_replacements.update(p["replacements"])
        self.engine = TextHumanizer(custom_replacements=merged_replacements)

    def setup_packs_popover(self):
        """Builds the dynamic popover menu for all discovered TOML packs."""
        popover = Gtk.Popover.new()
        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 8)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        popover.set_child(box)

        title = Gtk.Label.new("Active Language & Dialect Packs")
        title.add_css_class("heading")
        box.append(title)

        if not self.discovered_packs:
            empty_lbl = Gtk.Label.new("No .toml packs found in packs/\nDrop any TOML file there to load.")
            empty_lbl.add_css_class("dim-label")
            box.append(empty_lbl)
        else:
            for p in self.discovered_packs:
                fname = p["filename"]
                check = Gtk.CheckButton.new_with_label(f"{p['name']} ({p['count']} rules)")
                check.set_active(self.active_packs.get(fname, False))
                check.set_tooltip_text(p["description"])
                
                def on_toggle(btn, fn=fname):
                    self.active_packs[fn] = btn.get_active()
                    self.rebuild_engine()
                    self.run_analysis(auto_humanize=False)
                    self.show_toast(f"Updated pack: {fn}")

                check.connect("toggled", on_toggle)
                box.append(check)

        box.append(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL))

        # Actions to manage packs
        btn_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 6)
        box.append(btn_box)

        new_pack_btn = Gtk.Button.new_with_label("+ New Pack")
        new_pack_btn.connect("clicked", self.on_create_new_pack)
        btn_box.append(new_pack_btn)

        open_folder_btn = Gtk.Button.new_with_label("Open Folder")
        open_folder_btn.connect("clicked", self.on_open_packs_folder)
        btn_box.append(open_folder_btn)

        self.packs_menu_button.set_popover(popover)

    def on_create_new_pack(self, btn):
        """Creates a starter TOML pack with zero preset locks."""
        pack_id = f"custom_pack_{len(self.discovered_packs) + 1}.toml"
        target_path = PACKS_DIR / pack_id
        if not target_path.exists():
            template = (
                f'# Custom Dialect & Jargon Pack\n'
                f'[pack_metadata]\n'
                f'name = "Custom Dialect Pack"\n'
                f'description = "Add your custom jargon and local slang here"\n\n'
                f'[replacements]\n'
                f'"commercial cafeteria meal" = "local lunch spot"\n'
                f'"severe transit delay" = "traffic gridlock"\n'
            )
            target_path.write_text(template, encoding="utf-8")
        
        self.show_toast(f"Created {target_path.name} in packs/")
        self.discovered_packs = discover_packs()
        self.setup_packs_popover()
        self.on_open_packs_folder(None)

    def on_open_packs_folder(self, btn):
        """Opens packs/ in user's default file manager."""
        try:
            subprocess.Popen(["xdg-open", str(PACKS_DIR)])
        except Exception as e:
            self.show_toast(f"Could not open folder: {e}")

    
    # DRAG & DROP HANDLING  
    
    def setup_drop_targets(self, widget):
        """Attaches file drop target to the input text view."""
        file_drop = Gtk.DropTarget.new(Gdk.FileList, Gdk.DragAction.COPY)
        file_drop.connect("drop", self.on_file_dropped)
        widget.add_controller(file_drop)

    def on_file_dropped(self, target, file_list, x, y):
        """Handles dropping .txt, .md, or .toml files directly into the window."""
        files = file_list.get_files()
        if not files:
            return False
        
        gfile = files[0]
        path = gfile.get_path()
        if path:
            try:
                content = Path(path).read_text(encoding="utf-8", errors="ignore")
                self.input_buffer.set_text(content)
                self.show_toast(f"Loaded file: {Path(path).name}")
                self.run_analysis(auto_humanize=True)
                return True
            except Exception as e:
                self.show_toast(f"Failed to read file: {e}")
        return False

    
    # ANALYSIS & REWRITING
    

    def get_input_text(self) -> str:
        start = self.input_buffer.get_start_iter()
        end = self.input_buffer.get_end_iter()
        return self.input_buffer.get_text(start, end, True)

    def on_text_changed(self, buffer):
        pass

    def apply_highlights(self, raw: str):
        """Clears old highlights then re-applies orange (filler) and yellow (buzzword) tags."""
        buf = self.input_buffer
        start_iter = buf.get_start_iter()
        end_iter   = buf.get_end_iter()

        # Wipe all previous highlight tags
        buf.remove_tag_by_name("filler",   start_iter, end_iter)
        buf.remove_tag_by_name("buzzword", start_iter, end_iter)

        flagged = self.engine.scan_buzzwords(raw)
        for item in flagged:
            span_start, span_end = item["span"]
            it_start = buf.get_iter_at_offset(span_start)
            it_end   = buf.get_iter_at_offset(span_end)
            tag_name = "filler" if item["type"] == "Throat-Clearing Filler" else "buzzword"
            buf.apply_tag_by_name(tag_name, it_start, it_end)

    def run_analysis(self, auto_humanize: bool = False):
        raw = self.get_input_text()
        if not raw.strip():
            self.ai_density_label.set_text("AI Density: 0.0%")
            self.burstiness_label.set_text("Cadence: Empty text")
            self.edits_label.set_text("Edits Flagged: 0")
            # Clear highlights too
            s = self.input_buffer.get_start_iter()
            e = self.input_buffer.get_end_iter()
            self.input_buffer.remove_tag_by_name("filler",   s, e)
            self.input_buffer.remove_tag_by_name("buzzword", s, e)
            return

        res = self.engine.humanize(raw)
        self.ai_density_label.set_text(f"Density: {res['ai_density_score']}")
        self.burstiness_label.set_text(f"Rhythm (SD {res['burstiness_index']}): {res['cadence_feedback'].split('(')[0].strip()}")
        self.edits_label.set_text(f"Buzzwords: {res['total_edits']}")

        # ── Apply inline highlights on input pane ──────────────────────────
        self.apply_highlights(raw)
        # ──────────────────────────────────────────────────────────────────

        if auto_humanize:
            self.output_buffer.set_text(res['humanized'])

    def on_scan_clicked(self, btn):
        self.run_analysis(auto_humanize=False)
        self.show_toast("Scanned text and updated metrics.")

    def on_humanize_clicked(self, btn):
        raw = self.get_input_text()
        if not raw.strip():
            self.show_toast("Please enter or drop text first.")
            return
        res = self.engine.humanize(raw)
        self.output_buffer.set_text(res['humanized'])
        self.run_analysis(auto_humanize=True)
        self.show_toast(f"Humanized text ({res['total_edits']} edits performed)!")

    def on_copy_output(self, btn):
        start = self.output_buffer.get_start_iter()
        end = self.output_buffer.get_end_iter()
        clean_text = self.output_buffer.get_text(start, end, True)
        if not clean_text.strip():
            self.show_toast("Output is empty.")
            return
        
        display = Gdk.Display.get_default()
        if display:
            clipboard = display.get_clipboard()
            clipboard.set(clean_text)
            self.show_toast("✓ Copied clean text to clipboard!")

    def on_load_sample(self, btn):
        sample = (
            "It is important to note that tsunamis, as a subset of marine geohazards, occupy a uniquely challenging position within the global disaster risk reduction landscape due to their capacity to generate catastrophic impact across vast geographical distances within compressed timeframes. In order to operationalize an effective early warning and community response ecosystem, it is essential that governments, scientific institutions, and civil society organizations align their respective mandates around a shared framework of preparedness, communication, and adaptive action. At the end of the day, the margin between a warning and a tragedy is measured not in meters but in minutes."
"Moving forward, the integration of deep-ocean pressure sensor networks, satellite telemetry, and AI-assisted wave propagation modeling represents a transformative leap in the technical capacity of the global tsunami early warning infrastructure. To that end, it is worth noting that the human dimension of disaster response — community trust, behavioral compliance, and last-mile communication — remains the most critical and underinvested component of any comprehensive resilience strategy. It goes without saying that technology alone is insufficient without the cultural and institutional scaffolding to translate data into decisive action."
"Needless to say, the compounding effects of sea-level rise and increased seismic activity in subduction zone regions demand that we fundamentally rethink our assumptions about coastal risk exposure and the long-term viability of current settlement patterns. The key takeaway is that tsunami resilience is not a technical problem with a technical solution — it is a holistic, multi-generational challenge that requires the full mobilization of scientific, governmental, and community resources. Going forward, the imperative to do the needful is not merely a bureaucratic obligation — it is, quite literally, a matter of life and death."
        )
        self.input_buffer.set_text(sample)
        self.run_analysis(auto_humanize=True)
        self.show_toast("Loaded sample AI draft.")

    def on_clear_text(self, btn):
        self.input_buffer.set_text("")
        self.output_buffer.set_text("")
        self.run_analysis(auto_humanize=False)
        self.show_toast("Cleared.")

    def show_toast(self, message: str):
        toast = Adw.Toast.new(message)
        toast.set_timeout(3)
        self.toast_overlay.add_toast(toast)



# APPLICATION ENTRYPOINT


class DeAIApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="org.sovereign.deai",
            flags=Gio.ApplicationFlags.NON_UNIQUE
        )
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = HumanizerWindow(app)
        self.win.present()

if __name__ == "__main__":
    app = DeAIApplication()
    app.run([])
