"""Small drawing kit on top of python-pptx for the COMP5320 Chapter 9 deck.

All coordinates are inches; colours are 6-digit hex strings without '#'.
Design tokens live in C / FONT / MONO so the visual design can be tuned in one place.
"""
from __future__ import annotations

import copy
from pathlib import Path

from lxml import etree
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE, PP_PLACEHOLDER
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ICON_DIR = Path(__file__).resolve().parent / "assets" / "icons"

# ---------------------------------------------------------------- design tokens
C = dict(
    navy="114984", navy_dark="0B3260", navy_mid="4F79A8", navy_tint="E7EEF7", navy_soft="BFD2E8",
    red="CA1F27", red_dark="9C161D", red_tint="FBE9EA", red_soft="F2B8BB",
    ink="1F2937", muted="536376", line="D1D9E2", card="F3F5F7", white="FFFFFF",
    green="1E7B4F", green_tint="E5F3EB", amber="B7791F", amber_tint="FCF3E2",
    code_bg="15233B", code_fg="DCE4F0", code_dim="8FA2BD", code_red="FF9BA0", code_green="8FD9A8",
)
FONT = "Montserrat Medium"
HEAD_FONT = "Poppins"
MONO = "Consolas"
FONT_DIR = Path(__file__).resolve().parent / "assets" / "fonts"

# icon colour names produced by make_icons.js
ICON_COLOR = {"FFFFFF": "white", C["navy"]: "navy", C["red"]: "red", C["ink"]: "ink",
              C["muted"]: "slate", C["green"]: "green", C["amber"]: "amber"}

# content grid (template: navy title band 0-1.21in, red bar from 7.25in)
X0, X1 = 0.92, 12.42
CW = X1 - X0
SLIDE_W, SLIDE_H = 13.333, 7.5

ALIGN = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}
ANCHOR = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}

SHAPES = {
    "rect": MSO_SHAPE.RECTANGLE, "round": MSO_SHAPE.ROUNDED_RECTANGLE, "oval": MSO_SHAPE.OVAL,
    "chevron": MSO_SHAPE.CHEVRON, "pentagon": MSO_SHAPE.PENTAGON, "rarrow": MSO_SHAPE.RIGHT_ARROW,
    "darrow": MSO_SHAPE.DOWN_ARROW, "uarrow": MSO_SHAPE.UP_ARROW, "tri": MSO_SHAPE.ISOSCELES_TRIANGLE,
    "rtri": MSO_SHAPE.RIGHT_TRIANGLE, "trap": MSO_SHAPE.TRAPEZOID, "hex": MSO_SHAPE.HEXAGON,
    "wedge": MSO_SHAPE.ROUNDED_RECTANGULAR_CALLOUT, "plaque": MSO_SHAPE.PLAQUE,
}


def rgb(hex_):
    return RGBColor.from_string(hex_)


# ---------------------------------------------------------------- text
def _apply_run(run, size, color, bold, italic, font, underline=False):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.name = HEAD_FONT if bold and font == FONT else font
    if underline:
        f.underline = True
    f.color.rgb = rgb(color)


def _bullet(p, char="•", indent=0.22, color=None):
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(int(Inches(indent))))
    pPr.set("indent", str(-int(Inches(indent))))
    for tag in ("a:buClr", "a:buFont", "a:buChar", "a:buNone", "a:buAutoNum"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    if color:
        bc = etree.SubElement(pPr, qn("a:buClr"))
        etree.SubElement(bc, qn("a:srgbClr")).set("val", color)
    etree.SubElement(pPr, qn("a:buFont")).set("typeface", FONT)
    etree.SubElement(pPr, qn("a:buChar")).set("char", char)


def fill_tf(tf, paras, size=14, color=None, bold=False, italic=False, font=FONT, align="l",
            anchor="t", margin=0.0, space_after=0, line_spacing=None, wrap=True, bullet=False):
    """paras: str | (text, opts) | list of paragraphs. A paragraph is str, a list of runs,
    or dict(runs=..., bullet=, align=, size=, space_after=, space_before=, color=, b=, line_spacing=).
    A run is str or (text, dict(b=, i=, color=, size=, font=, u=))."""
    color = color or C["ink"]
    tf.word_wrap = wrap
    # Preserve complete Latin/code words; never split a word to fill a narrow box.
    tf._txBody.bodyPr.set("latinLnBrk", "0")
    tf._txBody.bodyPr.set("eaLnBrk", "0")
    tf.auto_size = MSO_AUTO_SIZE.NONE
    if margin is not None:
        if isinstance(margin, (tuple, list)):
            l, t, r, b = margin
        else:
            l = t = r = b = margin
        tf.margin_left, tf.margin_top = Inches(l), Inches(t)
        tf.margin_right, tf.margin_bottom = Inches(r), Inches(b)
    if anchor is not None:
        tf.vertical_anchor = ANCHOR[anchor]
    if isinstance(paras, (str, tuple)):
        paras = [paras]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        popts = para if isinstance(para, dict) else {}
        runs = popts.get("runs", "") if isinstance(para, dict) else para
        if isinstance(runs, (str, tuple)):
            runs = [runs]
        p.alignment = ALIGN[popts.get("align", align)]
        sa = popts.get("space_after", space_after)
        if sa:
            p.space_after = Pt(sa)
        sb = popts.get("space_before", 0)
        if sb:
            p.space_before = Pt(sb)
        ls = popts.get("line_spacing", line_spacing)
        if ls:
            # values < 4 are multiples (1.1 = 110%); larger values are exact points
            p.line_spacing = Pt(ls) if ls >= 4 else float(ls)
        psize = popts.get("size", size)
        pcolor = popts.get("color", color)
        pbold = popts.get("b", bold)
        for r in runs:
            if isinstance(r, str):
                r = (r, {})
            t, o = r
            run = p.add_run()
            run.text = t
            _apply_run(run, o.get("size", psize), o.get("color", pcolor), o.get("b", pbold),
                       o.get("i", popts.get("i", italic)), o.get("font", popts.get("font", font)), o.get("u", False))
        if popts.get("bullet", bullet):
            _bullet(p, popts.get("bullet_char", "•"), popts.get("indent", 0.2), popts.get("bullet_color"))
    return tf


def text(s, x, y, w, h, paras, size=14, color=None, bold=False, italic=False, font=FONT, align="l",
         anchor="t", margin=0.0, space_after=0, line_spacing=None, wrap=True, bullet=False, name=None):
    # Allow a small glyph-overhang margin inside the existing card gutters.
    if wrap and name not in ("Lead", "Eyebrow", "Source"):
        w += min(0.05, max(0, X1 - x - w))
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    fill_tf(tb.text_frame, paras, size, color, bold, italic, font, align, anchor, margin,
            space_after, line_spacing, wrap, bullet)
    return tb


# ---------------------------------------------------------------- shapes
def _no_effects(sp):
    spPr = sp._element.spPr
    if spPr.find(qn("a:effectLst")) is None:
        ln = spPr.find(qn("a:ln"))
        eff = etree.Element(qn("a:effectLst"))
        if ln is not None:
            ln.addnext(eff)
        else:
            spPr.append(eff)


def set_alpha(sp, opacity_pct):
    """opacity_pct: 0 (clear) .. 100 (solid) for a solid fill."""
    sf = sp.fill._xPr.find(qn("a:solidFill"))
    if sf is None or len(sf) == 0:
        return
    clr = sf[0]
    for a in clr.findall(qn("a:alpha")):
        clr.remove(a)
    etree.SubElement(clr, qn("a:alpha")).set("val", str(int(opacity_pct * 1000)))


def box(s, x, y, w, h, fill=None, line=None, lw=1.0, shape="rect", radius=0.12, dash=False,
        alpha=None, paras=None, size=14, color=None, bold=False, align="c", anchor="m", margin=0.08,
        space_after=0, line_spacing=None, name=None, adj=None):
    sp = s.shapes.add_shape(SHAPES[shape], Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        sp.name = name
    if shape == "round":
        # Absolute corner treatment, capped to avoid pill-like tall/small cards.
        sp.adjustments[0] = min(radius, 0.055 / max(min(w, h), 0.1))
    if adj:
        for i, v in enumerate(adj):
            sp.adjustments[i] = v
    if fill:
        sp.fill.solid()
        sp.fill.fore_color.rgb = rgb(fill)
        if alpha is not None:
            set_alpha(sp, alpha)
    else:
        sp.fill.background()
    if line:
        sp.line.color.rgb = rgb(line)
        sp.line.width = Pt(lw)
        if dash:
            sp.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    else:
        sp.line.fill.background()
    _no_effects(sp)
    tf = sp.text_frame
    if paras is not None:
        fill_tf(tf, paras, size, color or C["ink"], bold, False, FONT, align, anchor, margin,
                space_after, line_spacing, True, False)
    else:
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0)
    return sp


def icon(s, name, color, x, y, size):
    cname = ICON_COLOR.get(color, color)
    return s.shapes.add_picture(str(ICON_DIR / f"{name}-{cname}.png"), Inches(x), Inches(y),
                                Inches(size), Inches(size))


def icon_circle(s, name, x, y, d, fill, icon_color="FFFFFF", scale=0.56, line=None, lw=1.5):
    c = box(s, x, y, d, d, fill=fill, shape="oval", line=line, lw=lw)
    isz = d * scale
    icon(s, name, icon_color, x + (d - isz) / 2, y + (d - isz) / 2, isz)
    return c


def badge(s, label, x, y, d=0.36, fill=None, color="FFFFFF", size=12):
    return box(s, x, y, d, d, fill=fill or C["red"], shape="oval", paras=[(str(label), {"b": True})],
               size=size, color=color, margin=0, align="c", anchor="m")


def arrow(s, x1, y1, x2, y2, color=None, w=1.75, head="end", dash=False, kind="straight"):
    kinds = {"straight": MSO_CONNECTOR.STRAIGHT, "elbow": MSO_CONNECTOR.ELBOW, "curve": MSO_CONNECTOR.CURVE}
    c = s.shapes.add_connector(kinds[kind], Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color or C["muted"])
    c.line.width = Pt(w)
    if dash:
        c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    ln = c.line._get_or_add_ln()
    if head in ("start", "both"):
        he = etree.SubElement(ln, qn("a:headEnd"))
        he.set("type", "triangle"); he.set("w", "med"); he.set("len", "med")
    if head in ("end", "both"):
        te = etree.SubElement(ln, qn("a:tailEnd"))
        te.set("type", "triangle"); te.set("w", "med"); te.set("len", "med")
    return c


def line(s, x1, y1, x2, y2, color=None, w=1.0, dash=False):
    return arrow(s, x1, y1, x2, y2, color=color, w=w, head="none", dash=dash)


def picture_alpha(pic, opacity_pct):
    blip = pic._element.find(".//" + qn("a:blip"))
    etree.SubElement(blip, qn("a:alphaModFix")).set("amt", str(int(opacity_pct * 1000)))


# ---------------------------------------------------------------- composite blocks
def eyebrow(s, label, color=None):
    return text(s, X0, 1.36, CW, 0.26, [(label.upper(), {"b": True})], size=11, color=color or C["red"],
                name="Eyebrow")


def lead(s, sentence, size=20, y=1.62, h=0.5):
    # Measure the actual heading face; Poppins is wider than the previous default.
    from PIL import ImageFont
    face = ImageFont.truetype(str(FONT_DIR / "poppins" / "Poppins-Bold.ttf"), 200)
    measured = face.getlength(sentence) / 10
    size = min(size, max(17, min(20, (CW * 72 - 6) * 20 / measured)))
    return text(s, X0, y, CW, h, [(sentence, {"b": True})], size=size, color=C["navy"],
                wrap=False, name="Lead")


def footnote(s, note, w=CW):
    return text(s, X0, 6.86, w, 0.32, note, size=9.5, color=C["muted"], anchor="m", name="Source")


def code_panel(s, x, y, w, h, lines, size=12, title=None, hl=(), hl_color=None, hl_alpha=30,
               pad=0.18, spacing=1.42, add_hl=None):
    """lines: list of str or list of runs [(text, {color})]. hl: indices of lines to highlight."""
    box(s, x, y, w, h, fill=C["code_bg"], shape="round", radius=0.035, name="Code panel")
    ty = y + pad
    if title:
        text(s, x + pad, y + 0.1, w - 2 * pad, 0.3, [(title, {"color": C["code_dim"]})], size=size - 1,
             font=MONO)
        ty = y + 0.48
    lh = size * spacing / 72.0
    for i in hl:
        box(s, x + 0.07, ty + i * lh - 0.015, w - 0.14, lh + 0.03, fill=hl_color or C["red"],
            alpha=hl_alpha, name="Highlight")
    for (i, col) in (add_hl or []):
        box(s, x + 0.07, ty + i * lh - 0.015, w - 0.14, lh + 0.03, fill=col, alpha=hl_alpha,
            name="Highlight")
    paras = []
    for ln_ in lines:
        runs = ln_ if isinstance(ln_, list) else [ln_ if ln_ else " "]
        paras.append({"runs": runs, "line_spacing": size * spacing})
    text(s, x + pad, ty, w - 2 * pad, h - (ty - y) - 0.05, paras, size=size, color=C["code_fg"],
         font=MONO, wrap=False)
    return lh


def card(s, x, y, w, h, fill=None, line=None, radius=0.06, name=None):
    return box(s, x, y, w, h, fill=fill or C["card"], line=line, shape="round", radius=radius, name=name)


def chip(s, x, y, w, h, label, fill=None, color=None, size=11, bold=True, line=None, radius=0.07,
         align="c"):
    return box(s, x, y, w, h, fill=fill or C["navy_tint"], line=line, shape="round", radius=radius,
               paras=[(label, {"b": bold})], size=size, color=color or C["navy"], margin=(0.08, 0, 0.08, 0),
               align=align)


# ---------------------------------------------------------------- table
NO_STYLE_TABLE = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"


def _cell_border(cell, sides, color, w_pt):
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        for el in tcPr.findall(qn(tag)):
            tcPr.remove(el)
    for idx, side in enumerate(("L", "R", "T", "B")):
        ln = etree.Element(qn(f"a:ln{side}"))
        if side in sides:
            ln.set("w", str(int(Pt(w_pt))))
            ln.set("cmpd", "sng")
            sf = etree.SubElement(ln, qn("a:solidFill"))
            etree.SubElement(sf, qn("a:srgbClr")).set("val", color)
        else:
            ln.set("w", "0")
            etree.SubElement(ln, qn("a:noFill"))
        tcPr.insert(idx, ln)


def table(s, x, y, col_w, rows, row_h=0.42, size=12, header_size=12, header_fill=None,
          header_color="FFFFFF", fills=None, colors=None, bold_cols=(), border=None, aligns=None,
          margin=(0.06, 0.04, 0.06, 0.04), name=None):
    """rows[0] is the header. Cells may be str or a list of runs."""
    nrows, ncols = len(rows), len(rows[0])
    heights = row_h if isinstance(row_h, (list, tuple)) else [row_h] * nrows
    gf = s.shapes.add_table(nrows, ncols, Inches(x), Inches(y), Inches(sum(col_w)), Inches(sum(heights)))
    if name:
        gf.name = name
    tbl = gf.table
    tblPr = gf._element.graphic.graphicData.tbl.tblPr
    sid = tblPr.find(qn("a:tableStyleId"))
    if sid is None:
        sid = etree.SubElement(tblPr, qn("a:tableStyleId"))
    sid.text = NO_STYLE_TABLE
    tbl.first_row = False
    tbl.horz_banding = False
    for j, cw in enumerate(col_w):
        tbl.columns[j].width = Inches(cw)
    for i, rh in enumerate(heights):
        tbl.rows[i].height = Inches(rh)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            hdr = i == 0
            fill = (header_fill or C["navy"]) if hdr else (fills[i][j] if fills else "FFFFFF")
            col = header_color if hdr else (colors[i][j] if colors else C["ink"])
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(fill)
            _cell_border(cell, "B", border or C["line"], 0.75)
            cell.margin_left, cell.margin_top = Inches(margin[0]), Inches(margin[1])
            cell.margin_right, cell.margin_bottom = Inches(margin[2]), Inches(margin[3])
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            al = aligns[j] if aligns else "l"
            runs = val if isinstance(val, list) else [val]
            fill_tf(cell.text_frame, [{"runs": runs}], size=header_size if hdr else size, color=col,
                    bold=hdr or (j in bold_cols), align=al, anchor=None, margin=None)
    return gf


# ---------------------------------------------------------------- chart
def bar_chart(s, x, y, w, h, cats, vals, colors, number_format='0.0"%"', horizontal=True,
              max_val=None, label_size=13, cat_size=12, series_name="Value", gap=55):
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series(series_name, vals)
    kind = XL_CHART_TYPE.BAR_CLUSTERED if horizontal else XL_CHART_TYPE.COLUMN_CLUSTERED
    gf = s.shapes.add_chart(kind, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    ch.has_legend = False
    ch.has_title = False
    ch.font.name = FONT
    ch.font.size = Pt(cat_size)
    ch.font.color.rgb = rgb(C["ink"])
    plot = ch.plots[0]
    plot.gap_width = gap
    plot.vary_by_categories = False
    ser = plot.series[0]
    for i, col in enumerate(colors):
        pt = ser.points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = rgb(col)
        pt.format.line.fill.background()
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format = number_format
    dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(label_size)
    dl.font.bold = True
    dl.font.name = FONT
    dl.font.color.rgb = rgb(C["ink"])
    va = ch.value_axis
    va.has_major_gridlines = False
    va.visible = False
    va.minimum_scale = 0
    if max_val:
        va.maximum_scale = max_val
    ca = ch.category_axis
    ca.tick_labels.font.size = Pt(cat_size)
    ca.tick_labels.font.name = FONT
    ca.tick_labels.font.color.rgb = rgb(C["ink"])
    ca.format.line.color.rgb = rgb(C["line"])
    ca.has_major_gridlines = False
    if horizontal:
        ca.reverse_order = True
    return gf


def grouped_bar_chart(s, x, y, w, h, cats, series, colors, number_format='0.0"%"', horizontal=False,
                      max_val=None, label_size=12, cat_size=11, legend=True, gap=70, overlap=-12):
    """series: list of (name, values). One colour per series."""
    from pptx.enum.chart import XL_LEGEND_POSITION
    cd = CategoryChartData()
    cd.categories = cats
    for name, vals in series:
        cd.add_series(name, vals)
    kind = XL_CHART_TYPE.BAR_CLUSTERED if horizontal else XL_CHART_TYPE.COLUMN_CLUSTERED
    gf = s.shapes.add_chart(kind, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    ch.has_title = False
    ch.font.name = FONT
    ch.font.size = Pt(cat_size)
    ch.font.color.rgb = rgb(C["ink"])
    ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.BOTTOM
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(cat_size)
        ch.legend.font.name = FONT
    plot = ch.plots[0]
    plot.gap_width = gap
    plot.overlap = overlap
    for ser, col in zip(plot.series, colors):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = rgb(col)
        ser.format.line.fill.background()
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format = number_format
    dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(label_size)
    dl.font.bold = True
    dl.font.name = FONT
    dl.font.color.rgb = rgb(C["ink"])
    va = ch.value_axis
    va.has_major_gridlines = False
    va.visible = False
    va.minimum_scale = 0
    if max_val:
        va.maximum_scale = max_val
    ca = ch.category_axis
    ca.tick_labels.font.size = Pt(cat_size)
    ca.tick_labels.font.name = FONT
    ca.tick_labels.font.color.rgb = rgb(C["ink"])
    ca.format.line.color.rgb = rgb(C["line"])
    ca.has_major_gridlines = False
    return gf


# ---------------------------------------------------------------- slide plumbing
def add_slide_number(slide):
    number = len(slide.part.package.presentation_part.presentation.slides)
    text(slide, 12.08, 7.05, 0.22, 0.17, str(number), size=9.5,
         color=C["muted"], font=FONT, align="r", wrap=False, name="Slide number")


def delete_slide(prs, index):
    sldIdLst = prs.slides._sldIdLst
    sld = list(sldIdLst)[index]
    prs.part.drop_rel(sld.get(qn("r:id")))
    sldIdLst.remove(sld)


def layout_by_name(prs, master_idx, name):
    for lay in prs.slide_masters[master_idx].slide_layouts:
        if lay.name == name:
            return lay
    raise KeyError(name)


def set_notes(slide, notes):
    if notes:
        slide.notes_slide.notes_text_frame.text = notes
