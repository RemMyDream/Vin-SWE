"""Read-only PowerPoint text-fit audit for the generated lecture deck."""
import json
import sys
from pathlib import Path
import win32com.client

deck = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "COMP5320_Agentic_Security.pptx"
app = win32com.client.DispatchEx("PowerPoint.Application")
issues = []
checked = 0
try:
    pres = app.Presentations.Open(str(deck), True, False, False)
    def check(shape, slide_no, label, width=None, height=None):
        global checked
        if not shape.HasTextFrame or not shape.TextFrame.HasText:
            return
        checked += 1
        tf = shape.TextFrame2
        tr = tf.TextRange
        aw = (shape.Width if width is None else width) - tf.MarginLeft - tf.MarginRight
        ah = (shape.Height if height is None else height) - tf.MarginTop - tf.MarginBottom
        # Whole-range BoundWidth can include the trailing space from soft wrapping,
        # even beyond the widest line. Check visible glyphs on each rendered line.
        visible_width = max((tr.GetLines(i, 1).TrimText().BoundWidth
                             for i in range(1, tr.Lines.Count + 1)), default=0)
        over_x, over_y = visible_width - aw, tr.BoundHeight - ah
        if over_x > 1.5 or over_y > 1.5:
            issues.append(dict(slide=slide_no, shape=label, text=tr.Text[:160],
                               over_x_pt=round(over_x, 2), over_y_pt=round(over_y, 2)))
    for slide in pres.Slides:
        for shape in slide.Shapes:
            if shape.HasTable:
                table = shape.Table
                for r in range(1, table.Rows.Count + 1):
                    for c in range(1, table.Columns.Count + 1):
                        check(table.Cell(r, c).Shape, slide.SlideIndex, f"{shape.Name}[{r},{c}]",
                              table.Columns(c).Width, table.Rows(r).Height)
            else:
                check(shape, slide.SlideIndex, shape.Name)
    pres.Close()
finally:
    app.Quit()
print(json.dumps(dict(checked=checked, tolerance_pt=1.5, issues=issues), indent=2, ensure_ascii=True))
