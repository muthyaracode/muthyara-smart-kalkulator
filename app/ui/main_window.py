"""Main window and interaction flow for the desktop calculator."""

from decimal import Decimal

import customtkinter as ctk

from app.core.evaluator import ExpressionError, evaluate
from app.core.formatter import format_decimal
from app.core.units import UNIT_CATEGORIES, UNIT_FACTORS, convert_value
from app.utils.settings import append_history, clear_history, load_history, load_settings, save_settings


class MainWindow(ctk.CTk):
    def __init__(self):
        self.settings = load_settings()
        ctk.set_appearance_mode(self.settings.get("theme", "dark"))
        ctk.set_default_color_theme("blue")
        super().__init__()
        self.title("Muthyara Smart Calculator")
        window = self.settings.get("window", {})
        self.geometry("{}x{}".format(window.get("width", 400), window.get("height", 640)))
        self.minsize(340, 520)
        self.configure(fg_color=("#F5F6FA", "#14161B"))
        self.attributes("-topmost", bool(self.settings.get("always_on_top", False)))

        self.expression = ""
        self.memory = Decimal(0)
        self.last_result = None
        self.history = load_history()
        self.history_visible = False
        self.mode = self.settings.get("mode", "standard")
        self.converter_category = "Panjang"
        self.converter_from = "Meter"
        self.converter_to = "Kilometer"

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build_header()
        self.shell = ctk.CTkFrame(self, fg_color="transparent")
        self.shell.grid(row=1, column=0, sticky="nsew", padx=16, pady=(4, 16))
        self.shell.bind("<Configure>", self._layout_panels)
        self._build_calculator()
        self._build_converter()
        self._build_history_panel()
        self._set_mode(self.mode)
        self.bind_all("<KeyPress>", self._global_keypress, add="+")
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 4))
        header.grid_columnconfigure(0, weight=1)
        self.mode_picker = ctk.CTkSegmentedButton(
            header,
            values=["Standar", "Ilmiah", "Konversi"],
            command=self._mode_selected,
            font=("Segoe UI", 14),
            selected_color=("#6C4BF0", "#7C5CFF"),
            selected_hover_color=("#5B3FD1", "#9B82FF"),
        )
        self.mode_picker.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ctk.CTkButton(header, text="◷", width=38, command=self._toggle_history, font=("Segoe UI", 18), fg_color="transparent", text_color=("#353844", "#F2F3F7"), hover_color=("#E0E3EE", "#2F3440")).grid(row=0, column=1, padx=2)
        ctk.CTkButton(header, text="◐", width=38, command=self._toggle_theme, font=("Segoe UI", 18), fg_color="transparent", text_color=("#353844", "#F2F3F7"), hover_color=("#E0E3EE", "#2F3440")).grid(row=0, column=2, padx=2)
        ctk.CTkButton(header, text="⚙", width=38, command=self._open_settings, font=("Segoe UI", 17), fg_color="transparent", text_color=("#353844", "#F2F3F7"), hover_color=("#E0E3EE", "#2F3440")).grid(row=0, column=3, padx=(2, 0))

    def _build_calculator(self):
        self.calculator = ctk.CTkFrame(self.shell, fg_color="transparent")
        self.calculator.grid(row=0, column=0, sticky="nsew")
        self.calculator.grid_columnconfigure(0, weight=1)
        self.calculator.grid_rowconfigure(1, weight=1)

        display = ctk.CTkFrame(self.calculator, corner_radius=16, fg_color=("#FFFFFF", "#1C1F26"))
        display.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        display.grid_columnconfigure(0, weight=1)
        self.expression_entry = ctk.CTkEntry(display, height=44, border_width=0, fg_color="transparent", justify="right", font=("Segoe UI", 20), placeholder_text="0")
        self.expression_entry.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 0))
        self.expression_entry.bind("<KeyRelease>", self._typed_expression)
        self.expression_entry.bind("<Return>", self._calculate_event)
        self.expression_entry.bind("<Escape>", self._clear_event)
        self.expression_entry.bind("<Control-c>", self._copy_event)
        self.preview_label = ctk.CTkLabel(display, text="", anchor="e", text_color=("#6B7080", "#8A90A2"), font=("Segoe UI", 13))
        self.preview_label.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 2))
        self.result_label = ctk.CTkLabel(display, text="0", anchor="e", font=("Segoe UI", 38, "bold"), text_color=("#1B1D24", "#F2F3F7"), cursor="hand2")
        self.result_label.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 15))
        self.result_label.bind("<Button-1>", self._copy_event)

        self.key_area = ctk.CTkFrame(self.calculator, fg_color="transparent")
        self.key_area.grid(row=1, column=0, sticky="nsew")
        self.key_area.grid_columnconfigure(tuple(range(4)), weight=1, uniform="keycol")
        self.key_area.grid_rowconfigure(2, weight=1)
        memory_row = ctk.CTkFrame(self.key_area, fg_color="transparent")
        memory_row.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 6))
        for index, (label, action) in enumerate((("MC", self._memory_clear), ("MR", self._memory_recall), ("M+", lambda: self._memory_change(1)), ("M−", lambda: self._memory_change(-1)))):
            ctk.CTkButton(memory_row, text=label, command=action, height=30, fg_color="transparent", text_color=("#6B7080", "#B9BDCA"), hover_color=("#E0E3EE", "#2F3440"), font=("Segoe UI", 13)).grid(row=0, column=index, sticky="ew", padx=2)
            memory_row.grid_columnconfigure(index, weight=1)

        self.scientific_keys = ctk.CTkFrame(self.key_area, fg_color="transparent")
        self.scientific_keys.grid_columnconfigure(tuple(range(3)), weight=1, uniform="sci")
        scientific = (("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("log", "log("), ("ln", "ln("), ("√", "sqrt("), ("x²", "**2"), ("xʸ", "**"), ("n!", "!"), ("π", "π"), ("e", "e"), ("( )", "()"))
        for index, (label, value) in enumerate(scientific):
            button = self._make_key(self.scientific_keys, label, lambda item=value: self._insert(item), style="operator", height=36)
            button.grid(row=index // 6, column=index % 6, sticky="nsew", padx=3, pady=3)
        for index in range(6):
            self.scientific_keys.grid_columnconfigure(index, weight=1, uniform="scicol")
        self._show_scientific(False)

        keypad = ctk.CTkFrame(self.key_area, fg_color="transparent")
        keypad.grid(row=2, column=0, columnspan=4, sticky="nsew")
        keypad.grid_columnconfigure(tuple(range(4)), weight=1, uniform="keypad")
        for row in range(5):
            keypad.grid_rowconfigure(row, weight=1, uniform="keyrow")
        keys = (("C", "()", "%", "÷"), ("7", "8", "9", "×"), ("4", "5", "6", "−"), ("1", "2", "3", "+"), ("±", "0", ",", "="))
        for row, labels in enumerate(keys):
            for column, label in enumerate(labels):
                style = "equal" if label == "=" else "danger" if label == "C" else "operator" if label in {"()", "%", "÷", "×", "−", "+"} else "number"
                button = self._make_key(keypad, label, lambda item=label: self._press(item), style)
                button.grid(row=row, column=column, sticky="nsew", padx=4, pady=4)

    def _make_key(self, parent, label, command, style="number", height=54):
        colors = {
            "number": (("#EDEFF5", "#262A33"), ("#DDE0E9", "#363B47"), ("#1B1D24", "#F2F3F7")),
            "operator": (("#E0E3EE", "#2F3440"), ("#D2D6E2", "#414756"), ("#353844", "#F2F3F7")),
            "danger": (("#FCE8E8", "#3B292E"), ("#F8D8D8", "#523139"), ("#C63F4B", "#FF8A91")),
            "equal": (("#6C4BF0", "#7C5CFF"), ("#5B3FD1", "#9B82FF"), ("#FFFFFF", "#FFFFFF")),
        }
        background, hover, foreground = colors[style]
        return ctk.CTkButton(parent, text=label, command=command, height=height, corner_radius=12, font=("Segoe UI", 18), fg_color=background, hover_color=hover, text_color=foreground)

    def _build_converter(self):
        self.converter = ctk.CTkFrame(self.shell, corner_radius=16, fg_color=("#FFFFFF", "#1C1F26"))
        self.converter.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.converter, text="Konverter satuan", font=("Segoe UI", 21, "bold"), anchor="w").grid(row=0, column=0, sticky="ew", padx=20, pady=(22, 14))
        self.category_menu = ctk.CTkOptionMenu(self.converter, values=UNIT_CATEGORIES, command=self._category_changed, height=40)
        self.category_menu.grid(row=1, column=0, sticky="ew", padx=20, pady=6)
        self.converter_input = ctk.CTkEntry(self.converter, height=48, font=("Segoe UI", 20), placeholder_text="Nilai")
        self.converter_input.insert(0, "1")
        self.converter_input.grid(row=2, column=0, sticky="ew", padx=20, pady=(14, 6))
        self.converter_input.bind("<KeyRelease>", lambda event: self._convert())
        self.unit_row = ctk.CTkFrame(self.converter, fg_color="transparent")
        self.unit_row.grid(row=3, column=0, sticky="ew", padx=20, pady=12)
        self.unit_row.grid_columnconfigure(0, weight=1)
        self.from_menu = ctk.CTkOptionMenu(self.unit_row, values=[], command=lambda value: self._set_unit("from", value))
        self.from_menu.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ctk.CTkButton(self.unit_row, text="⇄", width=44, command=self._swap_units, font=("Segoe UI", 20), fg_color="transparent").grid(row=0, column=1, padx=4)
        self.to_menu = ctk.CTkOptionMenu(self.unit_row, values=[], command=lambda value: self._set_unit("to", value))
        self.to_menu.grid(row=0, column=2, sticky="ew", padx=(6, 0))
        self.unit_row.grid_columnconfigure(2, weight=1)
        self.convert_result = ctk.CTkLabel(self.converter, text="", font=("Segoe UI", 30, "bold"), anchor="e", wraplength=330)
        self.convert_result.grid(row=4, column=0, sticky="ew", padx=20, pady=(20, 10))
        self.category_menu.set(self.converter_category)
        self._set_category_units()

    def _build_history_panel(self):
        self.history_panel = ctk.CTkFrame(self.shell, corner_radius=16, fg_color=("#FFFFFF", "#1C1F26"))
        self.history_panel.grid_columnconfigure(0, weight=1)
        header = ctk.CTkFrame(self.history_panel, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Riwayat", font=("Segoe UI", 17, "bold"), anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="Hapus", width=58, command=self._clear_history, fg_color="transparent", text_color=("#6B7080", "#B9BDCA")).grid(row=0, column=1)
        self.history_list = ctk.CTkScrollableFrame(self.history_panel, fg_color="transparent")
        self.history_list.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 10))
        self.history_panel.grid_rowconfigure(1, weight=1)
        self._refresh_history()

    def _layout_panels(self, event=None):
        width = self.winfo_width()
        show_side_panel = self.history_visible and width >= 720
        self.shell.grid_columnconfigure(0, weight=3 if self.history_visible and width >= 720 else 1)
        self.shell.grid_columnconfigure(1, weight=2 if self.history_visible and width >= 720 else 0)
        if self.mode == "converter":
            self.calculator.grid_forget()
            self.converter.grid(row=0, column=0, columnspan=1 if show_side_panel else 2, sticky="nsew")
        else:
            self.converter.grid_forget()
            self.calculator.grid(row=0, column=0, columnspan=2 if not self.history_visible or width < 720 else 1, sticky="nsew")
        if not self.history_visible:
            self.history_panel.grid_forget()
            self.history_panel.place_forget()
        elif width >= 720:
            self.history_panel.place_forget()
            self.history_panel.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        else:
            self.history_panel.grid_forget()
            self.history_panel.place(relx=0.06, rely=0.04, relwidth=0.88, relheight=0.90)

    def _mode_selected(self, label):
        self._set_mode({"Standar": "standard", "Ilmiah": "scientific", "Konversi": "converter"}[label])

    def _set_mode(self, mode):
        self.mode = mode if mode in {"standard", "scientific", "converter"} else "standard"
        label = {"standard": "Standar", "scientific": "Ilmiah", "converter": "Konversi"}[self.mode]
        self.mode_picker.set(label)
        if self.mode == "converter":
            self.calculator.grid_forget()
            self.converter.grid(row=0, column=0, columnspan=2, sticky="nsew")
            self.shell.grid_rowconfigure(0, weight=1)
            self._convert()
        else:
            self.converter.grid_forget()
            self.calculator.grid(row=0, column=0, sticky="nsew")
            self.shell.grid_rowconfigure(0, weight=1)
            self._show_scientific(self.mode == "scientific")
        self.settings["mode"] = self.mode
        self._layout_panels()

    def _show_scientific(self, visible):
        if visible:
            self.scientific_keys.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 4))
            self.key_area.grid_rowconfigure(2, weight=2)
        else:
            self.scientific_keys.grid_forget()
            self.key_area.grid_rowconfigure(2, weight=1)

    def _press(self, label):
        if label == "C":
            self._clear()
        elif label == "=":
            self._calculate()
        elif label == "±":
            text = self.expression_entry.get()
            self._set_expression("-(" + text + ")" if text and not text.startswith("-(") else text[2:-1] if text.startswith("-(") and text.endswith(")") else "-")
        elif label == "()":
            self._insert("()")
            self.expression_entry.icursor(max(0, self.expression_entry.index("insert") - 1))
        else:
            self._insert("%" if label == "%" else {"÷": "÷", "×": "×", "−": "−", ",": ","}.get(label, label))

    def _insert(self, text):
        try:
            start = self.expression_entry.index("sel.first")
            end = self.expression_entry.index("sel.last")
            self.expression_entry.delete(start, end)
        except Exception:
            pass
        self.expression_entry.insert("insert", text)
        self.expression_entry.focus_set()
        self._typed_expression()

    def _set_expression(self, text):
        self.expression_entry.delete(0, "end")
        self.expression_entry.insert(0, text)
        self.expression_entry.icursor("end")
        self.expression_entry.focus_set()
        self._typed_expression()

    def _typed_expression(self, event=None):
        self.expression = self.expression_entry.get()
        self.last_result = None
        candidate = self.expression
        candidate += ")" * max(0, candidate.count("(") - candidate.count(")"))
        try:
            value = evaluate(candidate, self.settings.get("angle_unit", "deg"))
            rendered = format_decimal(value, self.settings.get("decimal_separator", ","))
            self.preview_label.configure(text="Pratinjau")
            self._set_result_label(rendered)
        except ExpressionError as error:
            if "dibagi nol" in str(error):
                self.preview_label.configure(text=str(error), text_color=("#E04848", "#FF6B6B"))
            else:
                self.preview_label.configure(text="", text_color=("#6B7080", "#8A90A2"))
            self.result_label.configure(text="")
        else:
            self.preview_label.configure(text_color=("#6B7080", "#8A90A2"))

    def _calculate(self):
        candidate = self.expression_entry.get()
        candidate += ")" * max(0, candidate.count("(") - candidate.count(")"))
        try:
            value = evaluate(candidate, self.settings.get("angle_unit", "deg"))
            self.last_result = value
            rendered = format_decimal(value, self.settings.get("decimal_separator", ","))
            self._set_result_label(rendered)
            self.preview_label.configure(text="Hasil", text_color=("#6B7080", "#8A90A2"))
            self.history = append_history(self.history, self.expression_entry.get(), format(value, "f"))
            self._refresh_history()
        except ExpressionError as error:
            self.last_result = None
            self.result_label.configure(text=str(error), font=("Segoe UI", 20, "bold"), text_color=("#E04848", "#FF6B6B"))
            self.preview_label.configure(text="")

    def _set_result_label(self, text):
        font_size = max(18, 38 - max(0, len(text) - 12))
        self.result_label.configure(text=text, font=("Segoe UI", font_size, "bold"), text_color=("#1B1D24", "#F2F3F7"))

    def _calculate_event(self, event):
        self._calculate()
        return "break"

    def _clear(self):
        self._set_expression("")
        self.result_label.configure(text="0", font=("Segoe UI", 38, "bold"), text_color=("#1B1D24", "#F2F3F7"))
        self.preview_label.configure(text="")

    def _clear_event(self, event):
        self._clear()
        return "break"

    def _global_keypress(self, event):
        if event.keysym == "Return" or event.char == "=":
            self._calculate()
            return "break"
        if event.keysym == "Escape":
            self._clear()
            return "break"
        if event.keysym == "BackSpace":
            self.after_idle(self._typed_expression)
        if event.state & 0x4 and event.keysym.lower() == "h":
            self._toggle_history()
            return "break"
        if event.state & 0x4 and event.keysym.lower() == "t":
            self._toggle_theme()
            return "break"
        if event.state & 0x4 and event.keysym in {"1", "2", "3"}:
            self._set_mode({"1": "standard", "2": "scientific", "3": "converter"}[event.keysym])
            return "break"
        if event.state & 0x4 and event.keysym.lower() == "c":
            self._copy_result()
            return "break"

    def _copy_event(self, event=None):
        self._copy_result()
        return "break"

    def _copy_result(self):
        text = self.result_label.cget("text")
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            original = self.preview_label.cget("text")
            self.preview_label.configure(text="Tersalin")
            self.after(1200, lambda: self.preview_label.configure(text=original) if self.preview_label.winfo_exists() else None)

    def _toggle_theme(self):
        self.settings["theme"] = "light" if self.settings.get("theme", "dark") == "dark" else "dark"
        ctk.set_appearance_mode(self.settings["theme"])

    def _set_theme(self, value):
        self.settings["theme"] = {"Sistem": "system", "Terang": "light", "Gelap": "dark"}[value]
        ctk.set_appearance_mode(self.settings["theme"])

    def _toggle_history(self):
        self.history_visible = not self.history_visible
        self._layout_panels()

    def _refresh_history(self):
        if not hasattr(self, "history_list"):
            return
        for child in self.history_list.winfo_children():
            child.destroy()
        if not self.history:
            ctk.CTkLabel(self.history_list, text="Belum ada perhitungan", text_color=("#6B7080", "#8A90A2")).grid(row=0, column=0, pady=20)
            return
        for index, item in enumerate(self.history):
            row = ctk.CTkFrame(self.history_list, fg_color="transparent")
            row.grid(row=index, column=0, sticky="ew", pady=3)
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkButton(row, text=item.get("expr", ""), anchor="w", command=lambda expr=item.get("expr", ""): self._set_expression(expr), fg_color="transparent", hover_color=("#EDEFF5", "#262A33"), text_color=("#6B7080", "#8A90A2"), font=("Segoe UI", 13)).grid(row=0, column=0, sticky="ew")
            result = item.get("result", "0")
            try:
                display_result = format_decimal(Decimal(result), self.settings.get("decimal_separator", ","))
            except Exception:
                display_result = result
            ctk.CTkButton(row, text="= " + display_result, anchor="e", command=lambda value=result: self._set_expression(value.replace(".", ",")), fg_color="transparent", hover_color=("#EDEFF5", "#262A33"), font=("Segoe UI", 15, "bold")).grid(row=1, column=0, sticky="ew")

    def _clear_history(self):
        self.history = []
        clear_history()
        self._refresh_history()

    def _memory_clear(self):
        self.memory = Decimal(0)

    def _memory_recall(self):
        self._insert(format(self.memory, "f").replace(".", ","))

    def _memory_change(self, direction):
        try:
            value = evaluate(self.expression_entry.get(), self.settings.get("angle_unit", "deg"))
            self.memory += value if direction > 0 else -value
        except ExpressionError:
            pass

    def _category_changed(self, category):
        self.converter_category = category
        self._set_category_units()
        self._convert()

    def _set_category_units(self):
        units = list(UNIT_FACTORS[self.converter_category])
        self.converter_from = units[0]
        self.converter_to = units[1] if len(units) > 1 else units[0]
        self.from_menu.configure(values=units)
        self.to_menu.configure(values=units)
        self.from_menu.set(self.converter_from)
        self.to_menu.set(self.converter_to)

    def _set_unit(self, direction, unit):
        if direction == "from":
            self.converter_from = unit
        else:
            self.converter_to = unit
        self._convert()

    def _swap_units(self):
        self.converter_from, self.converter_to = self.converter_to, self.converter_from
        self.from_menu.set(self.converter_from)
        self.to_menu.set(self.converter_to)
        self._convert()

    def _convert(self):
        if not hasattr(self, "converter_input"):
            return
        try:
            raw = self.converter_input.get().strip().replace(" ", "")
            if "," in raw:
                raw = raw.replace(".", "").replace(",", ".")
            value = float(raw)
            result = convert_value(value, self.converter_category, self.converter_from, self.converter_to)
            rendered = format_decimal(Decimal(str(result)), self.settings.get("decimal_separator", ","))
            self.convert_result.configure(text=rendered or "0")
        except (ValueError, ArithmeticError):
            self.convert_result.configure(text="-")

    def _open_settings(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Pengaturan")
        dialog.geometry("320x360")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(dialog, text="Pengaturan", font=("Segoe UI", 20, "bold")).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 14))
        ctk.CTkLabel(dialog, text="Tema", anchor="w").grid(row=1, column=0, sticky="ew", padx=20)
        theme = ctk.CTkSegmentedButton(dialog, values=["Sistem", "Terang", "Gelap"], command=self._set_theme)
        theme.set({"system": "Sistem", "light": "Terang", "dark": "Gelap"}.get(self.settings.get("theme", "dark"), "Gelap"))
        theme.grid(row=2, column=0, sticky="ew", padx=20, pady=(5, 12))
        ctk.CTkLabel(dialog, text="Satuan sudut", anchor="w").grid(row=3, column=0, sticky="ew", padx=20)
        angle = ctk.CTkSegmentedButton(dialog, values=["Derajat", "Radian"], command=lambda value: self._set_angle(value))
        angle.set("Derajat" if self.settings.get("angle_unit", "deg") == "deg" else "Radian")
        angle.grid(row=4, column=0, sticky="ew", padx=20, pady=(5, 12))
        pin = ctk.CTkSwitch(dialog, text="Selalu di atas", command=lambda: self._set_topmost(pin.get()))
        pin.select() if self.settings.get("always_on_top") else None
        pin.grid(row=5, column=0, sticky="w", padx=20, pady=8)
        ctk.CTkLabel(dialog, text="Muthyara Smart Calculator  ·  v1.0", text_color=("#6B7080", "#8A90A2")).grid(row=6, column=0, padx=20, pady=(8, 16))

    def _set_angle(self, value):
        self.settings["angle_unit"] = "deg" if value == "Derajat" else "rad"
        self._typed_expression()

    def _set_topmost(self, enabled):
        self.settings["always_on_top"] = bool(enabled)
        self.attributes("-topmost", bool(enabled))

    def _on_close(self):
        self.settings["window"] = {"width": self.winfo_width(), "height": self.winfo_height()}
        save_settings(self.settings)
        self.destroy()