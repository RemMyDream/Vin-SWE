"""Embed permitted presentation fonts and export the final PDF with PowerPoint."""
from pathlib import Path
import zipfile
import win32com.client

deck = Path(__file__).resolve().parent.parent / "COMP5320_Agentic_Security.pptx"
pdf = deck.with_suffix(".pdf")
embedded = Path(__file__).resolve().parent / "assets" / "agentic-security-embedded.pptx"
app = win32com.client.DispatchEx("PowerPoint.Application")
pres = None
try:
    app.DisplayAlerts = 1
    pres = app.Presentations.Open(str(deck), False, False, False)
    # Save to a new path: saving an unchanged presentation over itself can skip embedding.
    pres.Saved = False
    pres.SaveAs(str(embedded), 24, -1)
    pres.SaveAs(str(pdf), 32)
finally:
    if pres:
        pres.Close()
    app.Quit()
embedded.replace(deck)
with zipfile.ZipFile(deck) as package:
    fonts = [n for n in package.namelist() if n.startswith("ppt/fonts/")]
print(f"Exported {pdf.name}; embedded font parts: {len(fonts)}")
