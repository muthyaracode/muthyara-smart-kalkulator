# Muthyara Smart Calculator

A portable Windows desktop calculator built with Python 3.11+ and CustomTkinter.

## Run from source

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Build the portable executable

Run `build.bat` with the Python 3.11 Windows Launcher target available (`py -3.11`). The executable is written to `dist\Muthyara Smart Calculator.exe`. User settings and calculation history are stored in a `data` folder beside the executable, with a Local AppData fallback when that location is read-only.

## Tests

```powershell
python -m unittest discover -s tests -t . -v
```

The calculation engine uses an AST whitelist and `decimal.Decimal`; it never evaluates expressions with `eval()`.

# muthyara-smart-kalkulator