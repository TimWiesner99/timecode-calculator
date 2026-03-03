"""
Desktop application for timecode calculator using customtkinter.
"""

import customtkinter as ctk
from timecode import add_timecodes, apply_to_all

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

FRAMERATES = ["23.976", "24", "25", "29.97", "30", "50", "60"]
DEFAULT_FRAMERATE = "25"

SUCCESS_COLOR = "#28a745"
ERROR_COLOR = "#dc3545"

MODE_HINTS = {
    "Frames": "Format: HH:MM:SS:FF  \u2014  e.g. 00:01:30:12",
    "Decimal": "Format: HH:MM:SS,mmm  \u2014  e.g. 00:01:30,500",
    "Simple": "Format: HH:MM:SS  \u2014  e.g. 00:01:30",
}

MODE_MAP = {"Frames": "frames", "Decimal": "decimal", "Simple": "simple"}

OFFSET_PLACEHOLDERS = {
    "Frames": "00:00:10:00",
    "Decimal": "00:00:10,000",
    "Simple": "00:00:10",
}


class TimecodeCalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Timecode Calculator")
        self.geometry("580x750")
        self.minsize(520, 650)

        self._build_ui()

    # ------------------------------------------------------------------ #
    #  UI construction
    # ------------------------------------------------------------------ #

    def _build_ui(self):
        # Title
        ctk.CTkLabel(
            self, text="Timecode Calculator",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(pady=(20, 10))

        # --- Header frame (mode, framerate, hint) using grid -----------
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(padx=30, fill="x", pady=(0, 5))
        self.header.columnconfigure(0, weight=1)

        # Row 0 – mode selector
        self.mode_var = ctk.StringVar(value="Frames")
        self.mode_selector = ctk.CTkSegmentedButton(
            self.header,
            values=["Frames", "Decimal", "Simple"],
            variable=self.mode_var,
            command=self._on_mode_change,
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        self.mode_selector.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        # Row 1 – framerate
        self.framerate_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        self.framerate_frame.grid(row=1, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(
            self.framerate_frame, text="Framerate:",
            font=ctk.CTkFont(size=13),
        ).pack(side="left", padx=(0, 8))

        self.framerate_var = ctk.StringVar(value=DEFAULT_FRAMERATE)
        self.framerate_menu = ctk.CTkOptionMenu(
            self.framerate_frame,
            values=FRAMERATES,
            variable=self.framerate_var,
            width=100,
        )
        self.framerate_menu.pack(side="left")

        # Row 2 – format hint
        self.hint_label = ctk.CTkLabel(
            self.header, text=MODE_HINTS["Frames"],
            font=ctk.CTkFont(size=12), text_color="gray", anchor="w",
        )
        self.hint_label.grid(row=2, column=0, sticky="w")

        # --- Tabview ------------------------------------------------
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=(0, 20), fill="both", expand=True)

        self._build_sum_tab()
        self._build_add_to_all_tab()

    # ---- Sum tab ---------------------------------------------------

    def _build_sum_tab(self):
        tab = self.tabview.add("Sum")

        ctk.CTkLabel(
            tab, text="Timecodes (one per line):",
            font=ctk.CTkFont(size=13, weight="bold"), anchor="w",
        ).pack(fill="x", pady=(5, 4))

        self.sum_input = ctk.CTkTextbox(
            tab, font=ctk.CTkFont(family="Courier New", size=13), height=200,
        )
        self.sum_input.pack(fill="both", expand=True, pady=(0, 8))
        self.sum_input.bind("<Control-Return>", lambda e: self._calculate_sum())
        self.sum_input.bind("<Command-Return>", lambda e: self._calculate_sum())

        ctk.CTkButton(
            tab, text="Calculate Sum",
            font=ctk.CTkFont(size=14, weight="bold"), height=40,
            command=self._calculate_sum,
        ).pack(fill="x", pady=(0, 10))

        # Result area (hidden until calculation)
        self.sum_result_frame = ctk.CTkFrame(tab)

        self.sum_result_label = ctk.CTkLabel(
            self.sum_result_frame, text="",
            font=ctk.CTkFont(family="Courier New", size=28, weight="bold"),
            text_color=SUCCESS_COLOR,
        )
        self.sum_result_label.pack(pady=10)

        self.sum_copy_btn = ctk.CTkButton(
            self.sum_result_frame, text="Copy to Clipboard",
            command=self._copy_sum_result,
            fg_color="gray", hover_color="darkgray",
        )
        self.sum_copy_btn.pack(fill="x", padx=10, pady=(0, 10))

        # Error label (hidden until error)
        self.sum_error_label = ctk.CTkLabel(
            tab, text="", text_color=ERROR_COLOR,
            font=ctk.CTkFont(size=12), wraplength=450, anchor="w", justify="left",
        )

    # ---- Add to All tab -------------------------------------------

    def _build_add_to_all_tab(self):
        tab = self.tabview.add("Add to All")

        # Operation selector
        op_frame = ctk.CTkFrame(tab, fg_color="transparent")
        op_frame.pack(fill="x", pady=(5, 8))

        ctk.CTkLabel(
            op_frame, text="Operation:",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(side="left", padx=(0, 10))

        self.operation_var = ctk.StringVar(value="Add")
        ctk.CTkSegmentedButton(
            op_frame, values=["Add", "Subtract"],
            variable=self.operation_var, width=200,
        ).pack(side="left")

        # Offset input
        ctk.CTkLabel(
            tab, text="Offset timecode:",
            font=ctk.CTkFont(size=13, weight="bold"), anchor="w",
        ).pack(fill="x", pady=(0, 4))

        self.offset_input = ctk.CTkEntry(
            tab, font=ctk.CTkFont(family="Courier New", size=13),
            placeholder_text=OFFSET_PLACEHOLDERS["Frames"], height=36,
        )
        self.offset_input.pack(fill="x", pady=(0, 10))

        # Timecodes input
        ctk.CTkLabel(
            tab, text="Timecodes (one per line):",
            font=ctk.CTkFont(size=13, weight="bold"), anchor="w",
        ).pack(fill="x", pady=(0, 4))

        self.ata_input = ctk.CTkTextbox(
            tab, font=ctk.CTkFont(family="Courier New", size=13), height=150,
        )
        self.ata_input.pack(fill="both", expand=True, pady=(0, 8))
        self.ata_input.bind("<Control-Return>", lambda e: self._calculate_add_to_all())
        self.ata_input.bind("<Command-Return>", lambda e: self._calculate_add_to_all())

        ctk.CTkButton(
            tab, text="Calculate",
            font=ctk.CTkFont(size=14, weight="bold"), height=40,
            command=self._calculate_add_to_all,
        ).pack(fill="x", pady=(0, 10))

        # Result area (hidden until calculation)
        self.ata_result_frame = ctk.CTkFrame(tab)

        self.ata_result_text = ctk.CTkTextbox(
            self.ata_result_frame,
            font=ctk.CTkFont(family="Courier New", size=13), height=150,
        )
        self.ata_result_text.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        self.ata_copy_btn = ctk.CTkButton(
            self.ata_result_frame, text="Copy to Clipboard",
            command=self._copy_ata_result,
            fg_color="gray", hover_color="darkgray",
        )
        self.ata_copy_btn.pack(fill="x", padx=10, pady=(0, 10))

        # Error label (hidden until error)
        self.ata_error_label = ctk.CTkLabel(
            tab, text="", text_color=ERROR_COLOR,
            font=ctk.CTkFont(size=12), wraplength=450, anchor="w", justify="left",
        )

    # ------------------------------------------------------------------ #
    #  Event handlers
    # ------------------------------------------------------------------ #

    def _on_mode_change(self, value):
        self.hint_label.configure(text=MODE_HINTS[value])

        if value == "Frames":
            self.framerate_frame.grid()
        else:
            self.framerate_frame.grid_remove()

        self.offset_input.configure(placeholder_text=OFFSET_PLACEHOLDERS[value])

    # ------------------------------------------------------------------ #
    #  Calculations
    # ------------------------------------------------------------------ #

    def _get_mode_and_fps(self):
        mode = MODE_MAP[self.mode_var.get()]
        framerate = round(float(self.framerate_var.get()))
        return mode, framerate

    def _calculate_sum(self):
        self.sum_result_frame.pack_forget()
        self.sum_error_label.pack_forget()

        timecodes = self.sum_input.get("1.0", "end").strip()
        if not timecodes:
            self._show_sum_error("Please enter at least one timecode")
            return

        mode, framerate = self._get_mode_and_fps()
        try:
            result = add_timecodes(timecodes, mode=mode, framerate=framerate)
            self.sum_result_label.configure(text=result)
            self.sum_result_frame.pack(fill="x", pady=(0, 10))
            self.sum_copy_btn.configure(text="Copy to Clipboard", fg_color="gray")
        except ValueError as e:
            self._show_sum_error(str(e))
        except Exception as e:
            self._show_sum_error(f"Error: {e}")

    def _calculate_add_to_all(self):
        self.ata_result_frame.pack_forget()
        self.ata_error_label.pack_forget()

        offset = self.offset_input.get().strip()
        if not offset:
            self._show_ata_error("Please enter an offset timecode")
            return

        timecodes = self.ata_input.get("1.0", "end").strip()
        if not timecodes:
            self._show_ata_error("Please enter at least one timecode")
            return

        mode, framerate = self._get_mode_and_fps()
        operation = self.operation_var.get().lower()

        try:
            results = apply_to_all(
                timecodes, offset,
                operation=operation, mode=mode, framerate=framerate,
            )
            self.ata_result_text.configure(state="normal")
            self.ata_result_text.delete("1.0", "end")
            self.ata_result_text.insert("1.0", "\n".join(results))
            self.ata_result_text.configure(state="disabled")
            self.ata_result_frame.pack(fill="both", expand=True, pady=(0, 10))
            self.ata_copy_btn.configure(text="Copy to Clipboard", fg_color="gray")
        except ValueError as e:
            self._show_ata_error(str(e))
        except Exception as e:
            self._show_ata_error(f"Error: {e}")

    # ------------------------------------------------------------------ #
    #  Helpers
    # ------------------------------------------------------------------ #

    def _show_sum_error(self, message):
        self.sum_error_label.configure(text=message)
        self.sum_error_label.pack(fill="x", pady=(0, 5))

    def _show_ata_error(self, message):
        self.ata_error_label.configure(text=message)
        self.ata_error_label.pack(fill="x", pady=(0, 5))

    def _copy_sum_result(self):
        text = self.sum_result_label.cget("text")
        self.clipboard_clear()
        self.clipboard_append(text)
        self.sum_copy_btn.configure(text="Copied!", fg_color=SUCCESS_COLOR)
        self.after(2000, lambda: self.sum_copy_btn.configure(
            text="Copy to Clipboard", fg_color="gray",
        ))

    def _copy_ata_result(self):
        self.ata_result_text.configure(state="normal")
        text = self.ata_result_text.get("1.0", "end").strip()
        self.ata_result_text.configure(state="disabled")
        self.clipboard_clear()
        self.clipboard_append(text)
        self.ata_copy_btn.configure(text="Copied!", fg_color=SUCCESS_COLOR)
        self.after(2000, lambda: self.ata_copy_btn.configure(
            text="Copy to Clipboard", fg_color="gray",
        ))


def main():
    app = TimecodeCalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
