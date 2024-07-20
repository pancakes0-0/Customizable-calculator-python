import customtkinter as ctk
import tkinter as tk
from tkinter import colorchooser


class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculator")
        self.geometry("300x450")

        self.result_var = tk.StringVar()
        self.accent_color = "#1F6AA5"
        self.bg_opacity = 1.0
        self.tile_color = "#2B2B2B"
        self.output_bg_color = "#1E1E1E"
        self.text_color = "#FFFFFF"

        self.calculator_frame = ctk.CTkFrame(self)
        self.settings_frame = ctk.CTkFrame(self)

        self.create_calculator_widgets()
        self.create_settings_widgets()

        self.show_calculator()

    def create_calculator_widgets(self):
        self.calculator_frame.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Settings button
        self.settings_button = ctk.CTkButton(self.calculator_frame, text="Settings", width=80, height=30,
                                             command=self.show_settings, fg_color=self.tile_color,
                                             text_color=self.text_color)
        self.settings_button.place(relx=0.7, rely=0.02)

        # Result display
        self.result_entry = ctk.CTkEntry(self.calculator_frame, textvariable=self.result_var, font=("Arial", 24),
                                         justify="right")
        self.result_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=(40, 10), sticky="nsew")

        # Buttons
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        self.button_frame = ctk.CTkFrame(self.calculator_frame)
        self.button_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        row_val = 0
        col_val = 0

        self.calc_buttons = []
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            btn = ctk.CTkButton(self.button_frame, text=button, command=cmd, width=50, height=50,
                                corner_radius=10)
            btn.grid(row=row_val, column=col_val, padx=5, pady=5)
            self.calc_buttons.append(btn)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        # Clear button
        self.clear_button = ctk.CTkButton(self.button_frame, text="C", command=self.clear, width=50, height=50,
                                          corner_radius=10)
        self.clear_button.grid(row=row_val, column=col_val, padx=5, pady=5)
        self.calc_buttons.append(self.clear_button)

    def create_settings_widgets(self):
        self.settings_frame.grid(row=0, column=0, sticky="nsew")

        # Back arrow
        self.back_button = ctk.CTkButton(self.settings_frame, text="←", width=50, height=30,
                                         command=self.show_calculator, fg_color=self.tile_color,
                                         text_color=self.text_color)
        self.back_button.place(relx=0.05, rely=0.05)

        # Color settings
        ctk.CTkButton(self.settings_frame, text="Background Color", command=lambda: self.choose_color("accent")).pack(
            pady=10)
        ctk.CTkButton(self.settings_frame, text="Tile Color", command=lambda: self.choose_color("tile")).pack(pady=10)
        ctk.CTkButton(self.settings_frame, text="Output Background", command=lambda: self.choose_color("output")).pack(
            pady=10)
        ctk.CTkButton(self.settings_frame, text="Text Color", command=lambda: self.choose_color("text")).pack(pady=10)
    def show_calculator(self):
        self.settings_frame.grid_remove()
        self.calculator_frame.grid()
        self.apply_colors()

    def show_settings(self):
        self.calculator_frame.grid_remove()
        self.settings_frame.grid()
        self.apply_colors()

    def click(self, key):
        if key == '=':
            try:
                result = eval(self.result_var.get())
                self.result_var.set(result)
            except:
                self.result_var.set("Error")
        else:
            current = self.result_var.get()
            self.result_var.set(current + key)

    def clear(self):
        self.result_var.set("")

    def choose_color(self, element):
        color = colorchooser.askcolor()[1]
        if color:
            if element == "accent":
                self.accent_color = color
            elif element == "tile":
                self.tile_color = color
            elif element == "output":
                self.output_bg_color = color
            elif element == "text":
                self.text_color = color
            self.apply_colors()

    def change_opacity(self, value):
        self.bg_opacity = value
        self.apply_colors()

    def apply_colors(self):
        accent_color_with_opacity = self.apply_opacity(self.accent_color)
        self.configure(fg_color=accent_color_with_opacity)
        self.calculator_frame.configure(fg_color=accent_color_with_opacity)
        self.settings_frame.configure(fg_color=accent_color_with_opacity)

        for button in self.calc_buttons:
            button.configure(fg_color=self.tile_color, text_color=self.text_color)

        self.result_entry.configure(fg_color=self.output_bg_color, text_color=self.text_color)
        self.settings_button.configure(fg_color=self.tile_color, text_color=self.text_color)
        self.back_button.configure(fg_color=self.tile_color, text_color=self.text_color)
        self.button_frame.configure(fg_color=accent_color_with_opacity)

        # Update settings frame buttons
        for child in self.settings_frame.winfo_children():
            if isinstance(child, ctk.CTkButton):
                child.configure(fg_color=self.tile_color, text_color=self.text_color)
            elif isinstance(child, ctk.CTkLabel):
                child.configure(text_color=self.text_color)

    def apply_opacity(self, hex_color):
        rgb = tuple(int(hex_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        rgb_with_opacity = [int(x * self.bg_opacity + 255 * (1 - self.bg_opacity)) for x in rgb]
        return '#{:02x}{:02x}{:02x}'.format(*rgb_with_opacity)


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()