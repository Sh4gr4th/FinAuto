import tkinter as tk
import subprocess

def run_comdirect():
    try:
        subprocess.run(["python", r"c:\Users\dkron\Coding\Python\FinAuto\comdirect.py"], check=True)
        status_label.config(text="Comdirect-Skript erfolgreich ausgeführt!", fg="green")
    except subprocess.CalledProcessError:
        status_label.config(text="Fehler beim Ausführen des Comdirect-Skripts.", fg="red")

def run_amex():
    try:
        subprocess.run(["python", r"c:\Users\dkron\Coding\Python\FinAuto\amex.py"], check=True)
        status_label.config(text="Amex-Skript erfolgreich ausgeführt!", fg="green")
    except subprocess.CalledProcessError:
        status_label.config(text="Fehler beim Ausführen des Amex-Skripts.", fg="red")

# GUI erstellen
root = tk.Tk()
root.title("FinAuto Skript-Runner")

# Buttons
comdirect_button = tk.Button(root, text="Comdirect", command=run_comdirect, width=20, height=2)
comdirect_button.pack(pady=10)

amex_button = tk.Button(root, text="Amex", command=run_amex, width=20, height=2)
amex_button.pack(pady=10)

# Statusanzeige
status_label = tk.Label(root, text="", font=("Arial", 10))
status_label.pack(pady=20)

# GUI starten
root.mainloop()
