"""Application entry point."""

import customtkinter as ctk

from app.ui.main_window import MainWindow


def main():
    settings_theme = "dark"
    ctk.set_appearance_mode(settings_theme)
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()