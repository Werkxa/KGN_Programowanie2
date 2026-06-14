# -*- coding: utf-8 -*-
"""Generator obszernej notatki PDF: SQL, pandas, numpy, sklearn, ML.
Buduje plik Notatka_Programowanie2.pdf na podstawie repozytorium KGN_Programowanie2.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Preformatted,
    Table, TableStyle, PageBreak, HRFlowable, KeepTogether, ListFlowable, ListItem
)
import xml.sax.saxutils as su

# ----------------------------------------------------------------------------
# Czcionki Unicode (obsługa polskich znaków)
# ----------------------------------------------------------------------------
FONT_DIR = "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/matplotlib/mpl-data/fonts/ttf/"
pdfmetrics.registerFont(TTFont("DJ",  FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DJB", FONT_DIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DJI", FONT_DIR + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DJM", FONT_DIR + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("DJMB", FONT_DIR + "DejaVuSansMono-Bold.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DJ", normal="DJ", bold="DJB", italic="DJI", boldItalic="DJB")

# Kolory motywu
C_PRIMARY = colors.HexColor("#1a3c6e")   # granat
C_ACCENT  = colors.HexColor("#0b7285")   # morski
C_CODE_BG = colors.HexColor("#f4f6f8")
C_CODE_BORDER = colors.HexColor("#c8d0d8")
C_NOTE_BG = colors.HexColor("#fff8e1")
C_NOTE_BORDER = colors.HexColor("#f0c75e")
C_FORM_BG = colors.HexColor("#eef4fb")
C_GREY = colors.HexColor("#555555")

# ----------------------------------------------------------------------------
# Style
# ----------------------------------------------------------------------------
styles = getSampleStyleSheet()

ST_TITLE = ParagraphStyle("MTitle", fontName="DJB", fontSize=26, leading=32,
                          textColor=C_PRIMARY, alignment=TA_CENTER, spaceAfter=6)
ST_SUB = ParagraphStyle("MSub", fontName="DJ", fontSize=13, leading=18,
                        textColor=C_GREY, alignment=TA_CENTER, spaceAfter=4)
ST_H1 = ParagraphStyle("H1", fontName="DJB", fontSize=17, leading=22,
                       textColor=colors.white, spaceBefore=2, spaceAfter=2,
                       leftIndent=6)
ST_H2 = ParagraphStyle("H2", fontName="DJB", fontSize=13, leading=17,
                       textColor=C_PRIMARY, spaceBefore=12, spaceAfter=5)
ST_H3 = ParagraphStyle("H3", fontName="DJB", fontSize=11, leading=15,
                       textColor=C_ACCENT, spaceBefore=8, spaceAfter=3)
ST_BODY = ParagraphStyle("Body", fontName="DJ", fontSize=9.7, leading=14.5,
                         alignment=TA_JUSTIFY, spaceAfter=6, textColor=colors.HexColor("#1d1d1d"))
ST_BULLET = ParagraphStyle("Bullet", parent=ST_BODY, leftIndent=14, bulletIndent=2,
                           spaceAfter=2, alignment=TA_LEFT)
ST_CODE = ParagraphStyle("Code", fontName="DJM", fontSize=7.6, leading=10.4,
                         textColor=colors.HexColor("#11181c"))
ST_CODECAP = ParagraphStyle("CodeCap", fontName="DJI", fontSize=8, leading=11,
                            textColor=C_GREY, spaceBefore=4, spaceAfter=1)
ST_FORM = ParagraphStyle("Form", fontName="DJI", fontSize=10.5, leading=15,
                         alignment=TA_CENTER, textColor=C_PRIMARY)
ST_NOTE = ParagraphStyle("Note", fontName="DJ", fontSize=9.2, leading=13.5,
                         textColor=colors.HexColor("#5f4b00"), alignment=TA_LEFT)
ST_TOC = ParagraphStyle("Toc", fontName="DJ", fontSize=10.5, leading=18, textColor=C_PRIMARY)
ST_TABLE = ParagraphStyle("Tbl", fontName="DJ", fontSize=8.6, leading=11.5)
ST_TABLEB = ParagraphStyle("TblB", fontName="DJB", fontSize=8.8, leading=11.5, textColor=colors.white)

# ----------------------------------------------------------------------------
# Pomocnicze konstruktory flowable
# ----------------------------------------------------------------------------
story = []

def esc(t):
    return su.escape(t).replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>") \
                       .replace("&lt;i&gt;", "<i>").replace("&lt;/i&gt;", "</i>")

def h1(text, num=None):
    label = f"{num}. {text}" if num else text
    tbl = Table([[Paragraph(esc(label), ST_H1)]], colWidths=[16.6*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_PRIMARY),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(Spacer(1, 6))
    story.append(tbl)
    story.append(Spacer(1, 7))

def h2(text):
    story.append(Paragraph(esc(text), ST_H2))

def h3(text):
    story.append(Paragraph(esc(text), ST_H3))

def p(text):
    story.append(Paragraph(esc(text), ST_BODY))

def bullets(items):
    flow = []
    for it in items:
        flow.append(Paragraph(esc(it), ST_BULLET, bulletText="•"))
    story.append(ListFlowable(
        [ListItem(Paragraph(esc(it), ST_BULLET), value="•", leftIndent=10) for it in items],
        bulletType="bullet", start="•", leftIndent=12, bulletFontName="DJ",
        bulletFontSize=8, spaceBefore=0, spaceAfter=6))

def code(src, caption=None):
    src = src.rstrip("\n")
    inner = Preformatted(src, ST_CODE)
    box = Table([[inner]], colWidths=[16.6*cm])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_CODE_BG),
        ("BOX", (0,0), (-1,-1), 0.6, C_CODE_BORDER),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    flow = []
    if caption:
        flow.append(Paragraph(esc(caption), ST_CODECAP))
    flow.append(box)
    flow.append(Spacer(1, 6))
    story.append(KeepTogether(flow) if len(src.splitlines()) <= 26 else None) if False else None
    for f in flow:
        story.append(f)

def formula(text):
    box = Table([[Paragraph(esc(text), ST_FORM)]], colWidths=[16.6*cm])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_FORM_BG),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    story.append(box)
    story.append(Spacer(1, 6))

def note(text, title="Uwaga"):
    inner = Paragraph(f"<b>{esc(title)}:</b> " + esc(text), ST_NOTE)
    box = Table([[inner]], colWidths=[16.6*cm])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_NOTE_BG),
        ("BOX", (0,0), (-1,-1), 0.7, C_NOTE_BORDER),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(box)
    story.append(Spacer(1, 7))

def table(header, rows, widths=None):
    data = [[Paragraph(esc(c), ST_TABLEB) for c in header]]
    for r in rows:
        data.append([Paragraph(esc(c), ST_TABLE) for c in r])
    n = len(header)
    if widths is None:
        widths = [16.6*cm/n]*n
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), C_ACCENT),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#eef3f7")]),
        ("GRID", (0,0), (-1,-1), 0.4, C_CODE_BORDER),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

def spacer(h=6):
    story.append(Spacer(1, h))

def rule():
    story.append(HRFlowable(width="100%", thickness=0.6, color=C_CODE_BORDER,
                            spaceBefore=4, spaceAfter=8))

# ============================================================================
#  STRONA TYTUŁOWA
# ============================================================================
story.append(Spacer(1, 3.2*cm))
story.append(Paragraph("Programowanie 2", ST_TITLE))
story.append(Spacer(1, 4))
story.append(Paragraph("Obszerna notatka do nauki od podstaw", ST_SUB))
story.append(Spacer(1, 10))
story.append(HRFlowable(width="55%", thickness=1.4, color=C_ACCENT, hAlign="CENTER"))
story.append(Spacer(1, 14))
story.append(Paragraph("SQL &bull; pandas &bull; NumPy &bull; scikit-learn &bull; uczenie maszynowe &bull; sieci neuronowe",
                       ParagraphStyle("x", parent=ST_SUB, fontSize=11)))
story.append(Spacer(1, 2.0*cm))
story.append(Paragraph("Materiał opracowany na podstawie repozytorium <b>KGN_Programowanie2</b> "
                       "(laboratoria i wykłady). Notatka prowadzi czytelnika od zupełnych podstaw, "
                       "tłumacząc każde pojęcie krok po kroku i ilustrując je komentowanymi przykładami kodu.",
                       ParagraphStyle("intro", parent=ST_BODY, alignment=TA_CENTER, fontSize=10,
                                      textColor=C_GREY)))
story.append(PageBreak())

# ============================================================================
#  SPIS TREŚCI
# ============================================================================
h1("Spis treści")
toc_items = [
    "1. Podstawy języka SQL",
    "2. SQL w praktyce pakietu pandas",
    "3. pandas: Series, DataFrame, loc/iloc, informacje o tabeli",
    "4. NumPy: kształt obiektu ndarray i jego zmiana",
    "5. NumPy: broadcasting, wektoryzacja, wydajność, axis",
    "6. NumPy: referencje (widoki) kontra kopie",
    "7. Czyszczenie i standaryzacja danych",
    "8. Klasyfikacja i regresja w scikit-learn",
    "9. Uczenie z nadzorem i bez nadzoru",
    "10. Miary błędu: MSE, RMSE, MAE, accuracy, FP/FN",
    "11. Przeuczenie (overfitting) i jak mu zapobiegać",
    "12. Podział danych: zbiór treningowy i testowy",
    "13. Perceptron i funkcje aktywacji",
    "14. Wsteczna propagacja błędu (backpropagation)",
]
for it in toc_items:
    story.append(Paragraph(it, ST_TOC))
story.append(PageBreak())

# ============================================================================
#  WSTRZYKNIĘCIE TREŚCI Z PLIKÓW content_part*.py
# ============================================================================
api = dict(h1=h1, h2=h2, h3=h3, p=p, bullets=bullets, code=code, formula=formula,
           note=note, table=table, spacer=spacer, rule=rule, cm=cm)

import content_part1, content_part2, content_part3
content_part1.build(api)
story.append(PageBreak())
content_part2.build(api)
story.append(PageBreak())
content_part3.build(api)

# ============================================================================
#  SZABLON STRONY (nagłówek/stopka z numeracją)
# ============================================================================
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    # stopka
    canvas.setStrokeColor(C_CODE_BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 1.3*cm, w-2*cm, 1.3*cm)
    canvas.setFont("DJ", 8)
    canvas.setFillColor(C_GREY)
    canvas.drawString(2*cm, 1.0*cm, "Programowanie 2 — notatka do nauki")
    canvas.drawRightString(w-2*cm, 1.0*cm, f"str. {doc.page}")
    canvas.restoreState()

doc = BaseDocTemplate(
    "Notatka_Programowanie2.pdf", pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.7*cm,
    title="Programowanie 2 - notatka", author="KGN_Programowanie2")
frame = Frame(doc.leftMargin, doc.bottomMargin,
              doc.width, doc.height, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=on_page)])

doc.build(story)
print("OK: zapisano Notatka_Programowanie2.pdf")
