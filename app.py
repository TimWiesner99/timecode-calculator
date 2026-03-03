"""
Tkinter desktop application for timecode calculator.
"""

import tkinter as tk
from tkinter import ttk
from timecode import add_timecodes

# Color constants matching the original design
PURPLE_START = "#667eea"
PURPLE_END = "#764ba2"
SUCCESS_GREEN = "#28a745"
ERROR_RED = "#dc3545"
ERROR_BG = "#f8d7da"
ERROR_TEXT = "#721c24"
RESULT_BG = "#f8f9fa"
LIGHT_GRAY = "#f0f0f0"
DARK_TEXT = "#333333"
MID_TEXT = "#666666"
WHITE = "#ffffff"

MODE_CONFIG = {
    "frames": {
        "subtitle": "Add timecodes in HH:MM:SS:FF format",
        "placeholder": "00:00:10:00\n00:00:15:12\n00:01:05:08",
        "hint": "Format: HH:MM:SS:FF \u2014 paste timecodes from Excel, one per line",
        "examples": [
            ("00:00:10:00", "10 seconds"),
            ("00:01:30:12", "1 minute, 30 seconds, 12 frames"),
            ("01:15:45:23", "1 hour, 15 minutes, 45 seconds, 23 frames"),
        ],
        "show_framerate": True,
    },
    "decimal": {
        "subtitle": "Add timecodes in HH:MM:SS,mmm format",
        "placeholder": "00:00:10,000\n00:00:15,500\n00:01:05,080",
        "hint": "Format: HH:MM:SS,mmm (milliseconds) \u2014 as used in SRT subtitle files",
        "examples": [
            ("00:00:10,000", "10 seconds"),
            ("00:01:30,500", "1 minute, 30.5 seconds"),
            ("01:15:45,250", "1 hour, 15 minutes, 45.25 seconds"),
        ],
        "show_framerate": False,
    },
    "simple": {
        "subtitle": "Add timecodes in HH:MM:SS format",
        "placeholder": "00:00:10\n00:00:15\n00:01:05",
        "hint": "Format: HH:MM:SS \u2014 hours, minutes, and seconds only",
        "examples": [
            ("00:00:10", "10 seconds"),
            ("00:01:30", "1 minute, 30 seconds"),
            ("01:15:45", "1 hour, 15 minutes, 45 seconds"),
        ],
        "show_framerate": False,
    },
}

FRAMERATES = ["23.976", "24", "25", "29.97", "30", "50", "60"]
DEFAULT_FRAMERATE = "25"


class TimecodeCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timecode Calculator")
        self.root.configure(bg=PURPLE_START)
        self.root.minsize(500, 600)

        self.current_mode = "frames"
        self._placeholder_active = False

        self._build_ui()
        self._set_mode("frames")

        # Center the window on screen
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"+{x}+{y}")

    def _build_ui(self):
        # Outer frame with purple gradient background
        self.outer = tk.Frame(self.root, bg=PURPLE_START, padx=20, pady=20)
        self.outer.pack(fill=tk.BOTH, expand=True)

        # White container card
        self.container = tk.Frame(self.outer, bg=WHITE, padx=30, pady=30)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(
            self.container, text="Timecode Calculator",
            font=("Helvetica", 20, "bold"), fg=DARK_TEXT, bg=WHITE
        ).pack(pady=(0, 5))

        # Mode switcher frame
        mode_frame = tk.Frame(self.container, bg=LIGHT_GRAY, padx=4, pady=4)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        mode_frame.columnconfigure(0, weight=1)
        mode_frame.columnconfigure(1, weight=1)
        mode_frame.columnconfigure(2, weight=1)

        self.mode_buttons = {}
        for i, (mode, label) in enumerate([
            ("frames", "Frames"),
            ("decimal", "Decimal"),
            ("simple", "Simple"),
        ]):
            btn = tk.Button(
                mode_frame, text=label,
                font=("Helvetica", 12, "bold"),
                relief=tk.FLAT, cursor="hand2", bd=0,
                command=lambda m=mode: self._set_mode(m),
            )
            btn.grid(row=0, column=i, sticky="ew", padx=2, pady=2)
            self.mode_buttons[mode] = btn

        # Subtitle
        self.subtitle_label = tk.Label(
            self.container, text="", font=("Helvetica", 11),
            fg=MID_TEXT, bg=WHITE, wraplength=400
        )
        self.subtitle_label.pack(pady=(0, 10))

        # Framerate selector
        self.framerate_frame = tk.Frame(self.container, bg=WHITE)
        self.framerate_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            self.framerate_frame, text="Framerate (fps):",
            font=("Helvetica", 11, "bold"), fg=DARK_TEXT, bg=WHITE
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.framerate_var = tk.StringVar(value=DEFAULT_FRAMERATE)
        self.framerate_combo = ttk.Combobox(
            self.framerate_frame, textvariable=self.framerate_var,
            values=FRAMERATES, state="readonly", width=8,
            font=("Helvetica", 11)
        )
        self.framerate_combo.pack(side=tk.LEFT)

        # Input label
        tk.Label(
            self.container, text="Timecodes (one per line):",
            font=("Helvetica", 11, "bold"), fg=DARK_TEXT, bg=WHITE,
            anchor="w"
        ).pack(fill=tk.X, pady=(5, 4))

        # Text input
        text_frame = tk.Frame(self.container, bg="#ddd", bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 4))

        self.text_input = tk.Text(
            text_frame, font=("Courier New", 12), wrap=tk.WORD,
            height=10, relief=tk.FLAT, padx=8, pady=8,
        )
        self.text_input.pack(fill=tk.BOTH, expand=True)
        self.text_input.bind("<Control-Return>", lambda e: self._calculate())
        self.text_input.bind("<Command-Return>", lambda e: self._calculate())
        self.text_input.bind("<FocusIn>", self._on_text_focus_in)
        self.text_input.bind("<FocusOut>", self._on_text_focus_out)

        # Hint label
        self.hint_label = tk.Label(
            self.container, text="", font=("Helvetica", 10),
            fg=MID_TEXT, bg=WHITE, anchor="w", wraplength=400
        )
        self.hint_label.pack(fill=tk.X, pady=(0, 10))

        # Calculate button
        self.calc_btn = tk.Button(
            self.container, text="Calculate Sum",
            font=("Helvetica", 13, "bold"), fg=WHITE, bg=PURPLE_START,
            activebackground=PURPLE_END, activeforeground=WHITE,
            relief=tk.FLAT, cursor="hand2", pady=8,
            command=self._calculate,
        )
        self.calc_btn.pack(fill=tk.X, pady=(0, 15))

        # Result section (hidden initially)
        self.result_frame = tk.Frame(self.container, bg=RESULT_BG, padx=15, pady=15)

        # Green left border simulation
        self.result_border = tk.Frame(self.result_frame, bg=SUCCESS_GREEN, width=4)
        self.result_border.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        result_inner = tk.Frame(self.result_frame, bg=RESULT_BG)
        result_inner.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            result_inner, text="Result:", font=("Helvetica", 14, "bold"),
            fg=DARK_TEXT, bg=RESULT_BG, anchor="w"
        ).pack(fill=tk.X, pady=(0, 5))

        self.result_value = tk.Label(
            result_inner, text="", font=("Courier New", 28, "bold"),
            fg=SUCCESS_GREEN, bg=WHITE, pady=15,
        )
        self.result_value.pack(fill=tk.X, pady=(0, 8))

        self.copy_btn = tk.Button(
            result_inner, text="Copy to Clipboard",
            font=("Helvetica", 11, "bold"), fg=DARK_TEXT, bg=LIGHT_GRAY,
            activebackground="#e0e0e0", relief=tk.FLAT, cursor="hand2",
            pady=6, command=self._copy_to_clipboard,
        )
        self.copy_btn.pack(fill=tk.X)

        # Error section (hidden initially)
        self.error_label = tk.Label(
            self.container, text="", font=("Helvetica", 11),
            fg=ERROR_TEXT, bg=ERROR_BG, anchor="w", padx=12, pady=10,
            wraplength=400, justify=tk.LEFT,
        )

        # Examples section
        sep = ttk.Separator(self.container, orient=tk.HORIZONTAL)
        sep.pack(fill=tk.X, pady=(15, 10))

        tk.Label(
            self.container, text="Example timecodes:",
            font=("Helvetica", 12, "bold"), fg=DARK_TEXT, bg=WHITE, anchor="w"
        ).pack(fill=tk.X, pady=(0, 5))

        self.examples_frame = tk.Frame(self.container, bg=WHITE)
        self.examples_frame.pack(fill=tk.X)

    def _set_mode(self, mode):
        self.current_mode = mode
        config = MODE_CONFIG[mode]

        self.subtitle_label.config(text=config["subtitle"])
        self.hint_label.config(text=config["hint"])

        # Update mode button styling
        for m, btn in self.mode_buttons.items():
            if m == mode:
                btn.config(bg=PURPLE_START, fg=WHITE)
            else:
                btn.config(bg=LIGHT_GRAY, fg=MID_TEXT)

        # Show/hide framerate
        if config["show_framerate"]:
            self.framerate_frame.pack(fill=tk.X, pady=(0, 10))
            # Re-order: make sure framerate_frame is before input label
            self.framerate_frame.pack_configure(after=self.subtitle_label)
        else:
            self.framerate_frame.pack_forget()

        # Clear input and set placeholder
        self.text_input.delete("1.0", tk.END)
        self._show_placeholder()

        # Hide result and error
        self.result_frame.pack_forget()
        self.error_label.pack_forget()

        # Update examples
        for w in self.examples_frame.winfo_children():
            w.destroy()
        for tc, desc in config["examples"]:
            row = tk.Frame(self.examples_frame, bg=WHITE)
            row.pack(fill=tk.X, pady=2)
            tk.Label(
                row, text=tc, font=("Courier New", 11),
                fg=PURPLE_START, bg=LIGHT_GRAY, padx=4, pady=1,
            ).pack(side=tk.LEFT, padx=(0, 8))
            tk.Label(
                row, text=f"\u2014 {desc}", font=("Helvetica", 10),
                fg=MID_TEXT, bg=WHITE,
            ).pack(side=tk.LEFT)

    def _show_placeholder(self):
        config = MODE_CONFIG[self.current_mode]
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert("1.0", config["placeholder"])
        self.text_input.config(fg="#999999")
        self._placeholder_active = True

    def _on_text_focus_in(self, event=None):
        if self._placeholder_active:
            self.text_input.delete("1.0", tk.END)
            self.text_input.config(fg="#000000")
            self._placeholder_active = False

    def _on_text_focus_out(self, event=None):
        content = self.text_input.get("1.0", tk.END).strip()
        if not content:
            self._show_placeholder()

    def _calculate(self):
        # Hide previous results/errors
        self.result_frame.pack_forget()
        self.error_label.pack_forget()

        # Get input
        if self._placeholder_active:
            self._show_error("Please enter at least one timecode")
            return

        timecodes = self.text_input.get("1.0", tk.END).strip()
        if not timecodes:
            self._show_error("Please enter at least one timecode")
            return

        framerate = round(float(self.framerate_var.get()))

        try:
            result = add_timecodes(timecodes, mode=self.current_mode, framerate=framerate)
            self._show_result(result)
        except ValueError as e:
            self._show_error(str(e))
        except Exception as e:
            self._show_error(f"An error occurred: {e}")

    def _show_result(self, result):
        self.error_label.pack_forget()
        self.result_value.config(text=result)
        self.result_frame.pack(fill=tk.X, pady=(0, 10))
        self.copy_btn.config(text="Copy to Clipboard", bg=LIGHT_GRAY, fg=DARK_TEXT)

    def _show_error(self, message):
        self.result_frame.pack_forget()
        self.error_label.config(text=message)
        self.error_label.pack(fill=tk.X, pady=(0, 10))

    def _copy_to_clipboard(self):
        text = self.result_value.cget("text")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

        # Visual feedback
        self.copy_btn.config(text="Copied!", bg=SUCCESS_GREEN, fg=WHITE)
        self.root.after(
            2000,
            lambda: self.copy_btn.config(
                text="Copy to Clipboard", bg=LIGHT_GRAY, fg=DARK_TEXT
            ),
        )


def main():
    root = tk.Tk()
    TimecodeCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
