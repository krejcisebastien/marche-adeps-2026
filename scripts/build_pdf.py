import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
    PageBreak, HRFlowable, KeepTogether,
)

NAVY = colors.HexColor("#14294e")
GREEN = colors.HexColor("#2e7d32")
ORANGE = colors.HexColor("#e2672a")
BG = colors.HexColor("#f7f5ef")
BORDER = colors.HexColor("#e3ddd0")
TEXT_MUTED = colors.HexColor("#6b6b6b")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "img")
OUT = os.path.join(ROOT, "marche-adeps-2026.pdf")

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=22, textColor=NAVY, spaceAfter=2, alignment=TA_CENTER,
)
subtitle_style = ParagraphStyle(
    "SubtitleCustom", parent=styles["Normal"], fontName="Helvetica",
    fontSize=11, textColor=TEXT_MUTED, alignment=TA_CENTER, spaceAfter=14,
)
h2_style = ParagraphStyle(
    "H2Custom", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=15, textColor=NAVY, spaceBefore=6, spaceAfter=8,
)
h3_style = ParagraphStyle(
    "H3Custom", parent=styles["Heading3"], fontName="Helvetica-Bold",
    fontSize=14, textColor=NAVY, spaceAfter=8,
)
body_style = ParagraphStyle(
    "BodyCustom", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, textColor=colors.HexColor("#2b2b2b"), leading=14,
)
label_style = ParagraphStyle(
    "LabelCustom", parent=styles["Normal"], fontName="Helvetica",
    fontSize=8, textColor=TEXT_MUTED, alignment=TA_CENTER,
)
value_style = ParagraphStyle(
    "ValueCustom", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=12, textColor=NAVY, alignment=TA_CENTER,
)
caption_style = ParagraphStyle(
    "CaptionCustom", parent=styles["Normal"], fontName="Helvetica",
    fontSize=8, textColor=TEXT_MUTED, alignment=TA_CENTER, spaceBefore=3,
)

def stat_box(value, label):
    return Table(
        [[Paragraph(value, value_style)], [Paragraph(label, label_style)]],
        colWidths=[38 * mm],
        style=TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
            ("BACKGROUND", (0, 0), (-1, -1), BG),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]),
    )

def stats_row(distance, dplus, dminus, duree):
    boxes = [
        stat_box(distance, "Distance"),
        stat_box(dplus, "Dénivelé +"),
        stat_box(dminus, "Dénivelé -"),
        stat_box(duree, "Durée estim."),
    ]
    t = Table([boxes], colWidths=[39 * mm] * 4, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t

def media_row(map_path, profil_path):
    col_w = 82 * mm
    map_img = Image(map_path, width=col_w, height=col_w * 0.62)
    profil_img = Image(profil_path, width=col_w, height=col_w * 0.4)
    cell1 = [map_img, Paragraph("Carte du tracé", caption_style)]
    cell2 = [profil_img, Paragraph("Profil d'altitude", caption_style)]
    t = Table([[cell1, cell2]], colWidths=[col_w + 4, col_w + 4], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t

def parcours_block(titre, badge, distance, dplus, dminus, duree, map_file, profil_file, description):
    elements = []
    heading = titre
    if badge:
        heading = f'{titre} &nbsp;&nbsp;<font size="8" color="#2e7d32">● {badge}</font>'
    elements.append(Paragraph(heading, h3_style))
    elements.append(Spacer(1, 4))
    elements.append(stats_row(distance, dplus, dminus, duree))
    elements.append(Spacer(1, 10))
    elements.append(media_row(os.path.join(IMG, map_file), os.path.join(IMG, profil_file)))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(description, body_style))
    return elements

def build():
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=16 * mm,
        title="Marche Adeps 2026 - RCTT Thuin",
    )

    story = []

    story.append(Paragraph("Marche Adeps 2026", title_style))
    story.append(Paragraph("RCTT Thuin — Venez découvrir la Thudinie à travers ses campagnes", subtitle_style))

    story.append(HRFlowable(width="100%", thickness=1.2, color=BORDER, spaceAfter=12))

    story.append(Paragraph("Infos pratiques", h2_style))
    infos = [
        ("Date", "dimanche 2 août 2026"),
        ("Départ &amp; arrivée", "Drève des Alliés 120, 6530 Thuin"),
        ("Accueil des marcheurs", "de 8h à 18h"),
        ("Sur place", "pains saucisse et petite restauration"),
        ("Organisation", "RCTT Thuin ASBL (Club de Tennis de Table de Thuin), Points Verts Adeps"),
        ("Contacts", "Sébastien Krejci — 0491 02 83 66 · Jean-François Mabille — 0477 98 76 02"),
    ]
    info_rows = [[Paragraph(f"<b>{k} :</b>", body_style), Paragraph(v, body_style)] for k, v in infos]
    info_table = Table(info_rows, colWidths=[45 * mm, 119 * mm])
    info_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Les parcours", h2_style))
    story.append(Paragraph(
        "Trois boucles au départ de Thuin, à travers bois, campagnes et bords de Sambre.",
        body_style,
    ))
    story.append(Spacer(1, 10))

    story.append(KeepTogether(parcours_block(
        "Parcours 5 km", "Accessible aux poussettes",
        "5,68 km", "+23 m", "-22 m", "1h28",
        "map-5km.jpg", "profil-5km.jpg",
        "Boucle familiale et très plate au départ du Gibet, idéale en poussette. "
        "Parcours court à travers les campagnes proches de Thuin, sans difficulté particulière.",
    )))

    story.append(PageBreak())

    story.append(KeepTogether(parcours_block(
        "Parcours 10 km", None,
        "10,87 km", "+95 m", "-96 m", "2h58",
        "map-10km.jpg", "profil-10km.jpg",
        "Boucle vallonnée à travers les bois de Reumont, de Pê et du Grand Bon Dieu, "
        "avec deux montées bien marquées vers le 3e et le 6e kilomètre. "
        "Un bon compromis nature et effort modéré.",
    )))

    story.append(PageBreak())

    story.append(KeepTogether(parcours_block(
        "Parcours 20 km", None,
        "20,3 km", "+250 m", "-249 m", "5h19",
        "map-20km.jpg", "profil-20km.jpg",
        "La plus longue et la plus vallonnée des trois boucles : elle pousse jusqu'aux bois de "
        "la Grattière et de l'Ermitage au nord-est avant de retrouver les bois de Reumont, "
        "dè Pê et du Grand Bon Dieu à l'ouest. Plusieurs montées marquées, notamment "
        "vers le 14e et le 16e kilomètre.",
    )))

    doc.build(story)
    print(f"PDF written to {OUT}")

if __name__ == "__main__":
    build()
