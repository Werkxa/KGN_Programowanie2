# -*- coding: utf-8 -*-
"""Reużywalny framework do budowy notatek PDF (reportlab + czcionki Unicode)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Preformatted,
    Table, TableStyle, PageBreak, HRFlowable, KeepTogether, ListFlowable, ListItem)
import xml.sax.saxutils as su

FONT_DIR = ("/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/"
            "site-packages/matplotlib/mpl-data/fonts/ttf/")
pdfmetrics.registerFont(TTFont("DJ",   FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DJB",  FONT_DIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DJI",  FONT_DIR + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DJM",  FONT_DIR + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("DJMB", FONT_DIR + "DejaVuSansMono-Bold.ttf"))
registerFontFamily("DJ", normal="DJ", bold="DJB", italic="DJI", boldItalic="DJB")

C_PRIMARY = colors.HexColor("#1a3c6e")
C_ACCENT  = colors.HexColor("#0b7285")
C_CODE_BG = colors.HexColor("#f4f6f8")
C_CODE_BORDER = colors.HexColor("#c8d0d8")
C_NOTE_BG = colors.HexColor("#fff8e1")
C_NOTE_BORDER = colors.HexColor("#f0c75e")
C_FORM_BG = colors.HexColor("#eef4fb")
C_GREY = colors.HexColor("#555555")
C_DEF_BG = colors.HexColor("#e8f5e9")
C_DEF_BORDER = colors.HexColor("#66bb6a")


class Notebook:
    def __init__(self, footer="Notatka"):
        self.story = []
        self.footer = footer
        self.cm = cm
        s = getSampleStyleSheet()
        self.ST_TITLE = ParagraphStyle("T", fontName="DJB", fontSize=25, leading=31,
                                       textColor=C_PRIMARY, alignment=TA_CENTER, spaceAfter=6)
        self.ST_SUB = ParagraphStyle("S", fontName="DJ", fontSize=13, leading=18,
                                     textColor=C_GREY, alignment=TA_CENTER)
        self.ST_H1 = ParagraphStyle("H1", fontName="DJB", fontSize=16, leading=21,
                                    textColor=colors.white, leftIndent=6)
        self.ST_PART = ParagraphStyle("PART", fontName="DJB", fontSize=20, leading=26,
                                      textColor=colors.white, alignment=TA_CENTER)
        self.ST_H2 = ParagraphStyle("H2", fontName="DJB", fontSize=12.5, leading=16,
                                    textColor=C_PRIMARY, spaceBefore=11, spaceAfter=5)
        self.ST_H3 = ParagraphStyle("H3", fontName="DJB", fontSize=10.8, leading=14,
                                    textColor=C_ACCENT, spaceBefore=7, spaceAfter=3)
        self.ST_BODY = ParagraphStyle("B", fontName="DJ", fontSize=9.6, leading=14.2,
                                      alignment=TA_JUSTIFY, spaceAfter=6,
                                      textColor=colors.HexColor("#1d1d1d"))
        self.ST_BULLET = ParagraphStyle("BU", parent=self.ST_BODY, leftIndent=12,
                                        spaceAfter=2, alignment=TA_LEFT)
        self.ST_CODE = ParagraphStyle("C", fontName="DJM", fontSize=7.4, leading=10.1,
                                      textColor=colors.HexColor("#11181c"))
        self.ST_CODECAP = ParagraphStyle("CC", fontName="DJI", fontSize=8, leading=11,
                                         textColor=C_GREY, spaceBefore=4, spaceAfter=1)
        self.ST_OUT = ParagraphStyle("O", fontName="DJM", fontSize=7.4, leading=10.1,
                                     textColor=C_ACCENT)
        self.ST_FORM = ParagraphStyle("F", fontName="DJI", fontSize=10.5, leading=15,
                                      alignment=TA_CENTER, textColor=C_PRIMARY)
        self.ST_NOTE = ParagraphStyle("N", fontName="DJ", fontSize=9.1, leading=13.3,
                                      textColor=colors.HexColor("#5f4b00"), alignment=TA_LEFT)
        self.ST_DEF = ParagraphStyle("D", fontName="DJ", fontSize=9.3, leading=13.6,
                                     textColor=colors.HexColor("#1b3a1d"), alignment=TA_LEFT)
        self.ST_TOC = ParagraphStyle("TO", fontName="DJ", fontSize=10.3, leading=17, textColor=C_PRIMARY)
        self.ST_TOCB = ParagraphStyle("TOB", fontName="DJB", fontSize=11, leading=19, textColor=C_ACCENT)
        self.ST_TBL = ParagraphStyle("TB", fontName="DJ", fontSize=8.5, leading=11.2)
        self.ST_TBLB = ParagraphStyle("TBB", fontName="DJB", fontSize=8.7, leading=11.2, textColor=colors.white)
        self.W = 16.6 * cm

    def esc(self, t):
        return (su.escape(t).replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
                .replace("&lt;i&gt;", "<i>").replace("&lt;/i&gt;", "</i>"))

    def part(self, text):
        self.story.append(PageBreak())
        self.story.append(Spacer(1, 6 * cm))
        tbl = Table([[Paragraph(self.esc(text).replace("\n", "<br/>"), self.ST_PART)]],
                    colWidths=[self.W])
        tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), C_ACCENT),
                                 ("TOPPADDING", (0, 0), (-1, -1), 16),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 16)]))
        self.story.append(tbl)
        self.story.append(PageBreak())

    def h1(self, text, num=None):
        label = f"{num}. {text}" if num else text
        tbl = Table([[Paragraph(self.esc(label), self.ST_H1)]], colWidths=[self.W])
        tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), C_PRIMARY),
                                 ("TOPPADDING", (0, 0), (-1, -1), 6),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
        self.story += [Spacer(1, 6), tbl, Spacer(1, 7)]

    def h2(self, text):
        self.story.append(Paragraph(self.esc(text), self.ST_H2))

    def h3(self, text):
        self.story.append(Paragraph(self.esc(text), self.ST_H3))

    def p(self, text):
        self.story.append(Paragraph(self.esc(text), self.ST_BODY))

    def bullets(self, items):
        self.story.append(ListFlowable(
            [ListItem(Paragraph(self.esc(it), self.ST_BULLET), value="•", leftIndent=10)
             for it in items],
            bulletType="bullet", start="•", leftIndent=12, bulletFontName="DJ",
            bulletFontSize=8, spaceAfter=6))

    def _boxed(self, flow, bg, border=None, pad=6):
        box = Table([[f] for f in flow] if False else [[flow[0]]], colWidths=[self.W])
        # build a single cell containing all flowables via inner table
        inner = Table([[f] for f in flow], colWidths=[self.W - 16])
        inner.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                   ("TOPPADDING", (0, 0), (-1, -1), 1),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
        box = Table([[inner]], colWidths=[self.W])
        sty = [("BACKGROUND", (0, 0), (-1, -1), bg),
               ("LEFTPADDING", (0, 0), (-1, -1), 8),
               ("RIGHTPADDING", (0, 0), (-1, -1), 8),
               ("TOPPADDING", (0, 0), (-1, -1), pad),
               ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]
        if border:
            sty.append(("BOX", (0, 0), (-1, -1), 0.7, border))
        box.setStyle(TableStyle(sty))
        return box

    def code(self, src, caption=None, out=None):
        src = src.rstrip("\n")
        box = Table([[Preformatted(src, self.ST_CODE)]], colWidths=[self.W])
        box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), C_CODE_BG),
                                 ("BOX", (0, 0), (-1, -1), 0.6, C_CODE_BORDER),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 7),
                                 ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                                 ("TOPPADDING", (0, 0), (-1, -1), 6),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
        if caption:
            self.story.append(Paragraph(self.esc(caption), self.ST_CODECAP))
        self.story.append(box)
        if out is not None:
            obox = Table([[Preformatted("Wynik:\n" + out.rstrip("\n"), self.ST_OUT)]],
                         colWidths=[self.W])
            obox.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f0f7f9")),
                                      ("LINEBEFORE", (0, 0), (-1, -1), 2, C_ACCENT),
                                      ("LEFTPADDING", (0, 0), (-1, -1), 7),
                                      ("TOPPADDING", (0, 0), (-1, -1), 4),
                                      ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
            self.story.append(obox)
        self.story.append(Spacer(1, 6))

    def formula(self, text):
        box = Table([[Paragraph(self.esc(text), self.ST_FORM)]], colWidths=[self.W])
        box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), C_FORM_BG),
                                 ("TOPPADDING", (0, 0), (-1, -1), 7),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
        self.story += [box, Spacer(1, 6)]

    def note(self, text, title="Uwaga"):
        inner = Paragraph(f"<b>{self.esc(title)}:</b> " + self.esc(text), self.ST_NOTE)
        self.story.append(self._boxed([inner], C_NOTE_BG, C_NOTE_BORDER))
        self.story.append(Spacer(1, 7))

    def definition(self, text, title="Definicja"):
        inner = Paragraph(f"<b>{self.esc(title)}:</b> " + self.esc(text), self.ST_DEF)
        self.story.append(self._boxed([inner], C_DEF_BG, C_DEF_BORDER))
        self.story.append(Spacer(1, 7))

    def table(self, header, rows, widths=None):
        data = [[Paragraph(self.esc(c), self.ST_TBLB) for c in header]]
        for r in rows:
            data.append([Paragraph(self.esc(c), self.ST_TBL) for c in r])
        n = len(header)
        widths = widths or [self.W / n] * n
        t = Table(data, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), C_ACCENT),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef3f7")]),
            ("GRID", (0, 0), (-1, -1), 0.4, C_CODE_BORDER),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        self.story += [t, Spacer(1, 8)]

    def spacer(self, h=6):
        self.story.append(Spacer(1, h))

    def rule(self):
        self.story.append(HRFlowable(width="100%", thickness=0.6, color=C_CODE_BORDER,
                                     spaceBefore=4, spaceAfter=8))

    def pagebreak(self):
        self.story.append(PageBreak())

    def title_page(self, title, subtitle, tagline, intro):
        self.story.append(Spacer(1, 3.0 * cm))
        self.story.append(Paragraph(title, self.ST_TITLE))
        self.story.append(Spacer(1, 4))
        self.story.append(Paragraph(subtitle, self.ST_SUB))
        self.story.append(Spacer(1, 12))
        self.story.append(HRFlowable(width="55%", thickness=1.4, color=C_ACCENT, hAlign="CENTER"))
        self.story.append(Spacer(1, 14))
        self.story.append(Paragraph(tagline, ParagraphStyle("x", parent=self.ST_SUB, fontSize=11)))
        self.story.append(Spacer(1, 1.8 * cm))
        self.story.append(Paragraph(intro, ParagraphStyle("i", parent=self.ST_BODY,
                                    alignment=TA_CENTER, fontSize=10, textColor=C_GREY)))
        self.story.append(PageBreak())

    def toc(self, items):
        self.h1("Spis treści")
        for it in items:
            style = self.ST_TOCB if it.startswith("CZĘŚĆ") else self.ST_TOC
            self.story.append(Paragraph(self.esc(it), style))
        self.story.append(PageBreak())

    def build(self, path):
        def on_page(canvas, doc):
            canvas.saveState()
            w, h = A4
            canvas.setStrokeColor(C_CODE_BORDER)
            canvas.setLineWidth(0.5)
            canvas.line(2 * cm, 1.3 * cm, w - 2 * cm, 1.3 * cm)
            canvas.setFont("DJ", 8)
            canvas.setFillColor(C_GREY)
            canvas.drawString(2 * cm, 1.0 * cm, self.footer)
            canvas.drawRightString(w - 2 * cm, 1.0 * cm, f"str. {doc.page}")
            canvas.restoreState()

        doc = BaseDocTemplate(path, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                              topMargin=1.8 * cm, bottomMargin=1.7 * cm, title=self.footer)
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="m")
        doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=on_page)])
        doc.build(self.story)
