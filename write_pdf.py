from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from itertools import combinations

def create_schedule_pdf_4(filename, teams=None):

    if teams is None:
        teams = ["Squadra A", "Squadra B", "Squadra C", "Squadra D"]

    assert len(teams) == 4, 'I need 4 teams exactly'

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 2 * cm, "Comabbio Cup - Schedule")

    # Subtitle
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 3 * cm, "Girone Unico")

    # Table Title
    c.setFont("Helvetica-Bold", 11)
    c.drawString(3 * cm, height - 4.5 * cm, "Classifica Girone")

    # Table Positioning
    table_top = height - 5.2 * cm
    row_height = 0.7 * cm
    num_rows = 5  # Header + 4 teams
    col_x = [3 * cm, 8 * cm, 11 * cm, 14 * cm, 17 * cm]  # Column boundaries: Squadra, Punti, GF, GS

    # Draw outer border
    table_height = row_height * num_rows
    c.rect(col_x[0], table_top - table_height, col_x[-1] - col_x[0], table_height, stroke=1, fill=0)

    # Draw horizontal lines
    for i in range(num_rows + 1):
        y = table_top - i * row_height
        c.line(col_x[0], y, col_x[-1], y)

    # Draw vertical lines
    for x in col_x:
        c.line(x, table_top, x, table_top - table_height)

    # Headers
    headers = ["Squadra", "Punti", "PF", "PS"]
    c.setFont("Helvetica-Bold", 10)
    for i, header in enumerate(headers):
        c.drawString(col_x[i] + 0.2 * cm, table_top - 0.5 * row_height, header)

    # Teams
    c.setFont("Helvetica", 10)
    for idx, team in enumerate(teams):
        y = table_top - (idx + 1.5) * row_height + 0.1 * cm
        c.drawString(col_x[0] + 0.2 * cm, y, team)

    # Match List
    match_start_y = table_top - table_height - 1 * cm
    matches = [
        "- %s vs %s" % (teams[0], teams[1]),
        "- %s vs %s" % (teams[2], teams[3]),
        "- %s vs %s" % (teams[0], teams[2]),
        "- %s vs %s" % (teams[1], teams[3]),
        "- %s vs %s" % (teams[0], teams[3]),
        "- %s vs %s" % (teams[1], teams[2]),
    ]
    c.setFont("Helvetica", 11)
    for match in matches:
        c.drawString(3 * cm, match_start_y, match)
        match_start_y -= 0.6 * cm

    # Semifinali
    match_start_y -= 0.4 * cm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(3 * cm, match_start_y, "Semifinali")
    match_start_y -= 0.6 * cm
    c.setFont("Helvetica", 11)
    c.drawString(3 * cm, match_start_y, "1. 1° vs 4°")
    match_start_y -= 0.5 * cm
    c.drawString(3 * cm, match_start_y, "2. 2° vs 3°")

    # Finali
    match_start_y -= 1 * cm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(3 * cm, match_start_y, "Finali")
    match_start_y -= 0.6 * cm
    c.setFont("Helvetica", 11)
    c.drawString(3 * cm, match_start_y, "1. Finale 3°-4° posto (Perdenti semifinali)")
    match_start_y -= 0.5 * cm
    c.drawString(3 * cm, match_start_y, "2. Finale 1°-2° posto (Vincitori semifinali)")

    c.save()


def generate_structured_round_robin(teams):
    assert len(teams) == 5, "This version supports exactly 5 teams"

    rounds = [
        [(teams[0], teams[1]), (teams[2], teams[3])],  # E rests
        [(teams[0], teams[2]), (teams[3], teams[4])],  # B rests
        [(teams[0], teams[3]), (teams[1], teams[4])],  # C rests
        [(teams[0], teams[4]), (teams[1], teams[2])],  # D rests
        [(teams[1], teams[3]), (teams[2], teams[4])],  # A rests
    ]
    rests = [teams[4], teams[1], teams[2], teams[3], teams[0]]
    return rounds, rests



def create_schedule_pdf_5(filename, teams=None):
    if teams is None:
        teams = ["Team A", "Team B", "Team C", "Team D", "Team E"]

    assert len(teams) == 5, 'I need exactly 5 teams'

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 2 * cm, "Comabbio Cup - Schedule")

    # Subtitle
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 3 * cm, "Girone Unico")

    # Table Title
    c.setFont("Helvetica-Bold", 11)
    c.drawString(3 * cm, height - 4.5 * cm, "Classifica Girone")

    # Table Positioning
    table_top = height - 5.2 * cm
    row_height = 0.7 * cm
    num_rows = 6  # Header + 5 teams
    col_x = [3 * cm, 8 * cm, 11 * cm, 14 * cm, 17 * cm]

    # Draw table borders
    table_height = row_height * num_rows
    c.rect(col_x[0], table_top - table_height, col_x[-1] - col_x[0], table_height, stroke=1, fill=0)

    # Horizontal lines
    for i in range(num_rows + 1):
        y = table_top - i * row_height
        c.line(col_x[0], y, col_x[-1], y)

    # Vertical lines
    for x in col_x:
        c.line(x, table_top, x, table_top - table_height)

    # Headers
    headers = ["Squadra", "Punti", "PF", "PS"]
    c.setFont("Helvetica-Bold", 10)
    for i, header in enumerate(headers):
        c.drawString(col_x[i] + 0.2 * cm, table_top - 0.5 * row_height, header)

    # Teams
    c.setFont("Helvetica", 10)
    for idx, team in enumerate(teams):
        y = table_top - (idx + 1.5) * row_height + 0.1 * cm
        c.drawString(col_x[0] + 0.2 * cm, y, team)

    # Structured Match Schedule
    rounds, rests = generate_structured_round_robin(teams)
    y = table_top - table_height - 1 * cm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(3 * cm, y, "Partite (Girone all'italiana)")
    y -= 0.6 * cm
    c.setFont("Helvetica", 11)
    for i, (matches, rest) in enumerate(zip(rounds, rests), start=1):
        c.drawString(3 * cm, y, f"Turno {i}:")
        y -= 0.5 * cm
        for match in matches:
            c.drawString(4 * cm, y, f"- {match[0]} vs {match[1]}")
            y -= 0.5 * cm
        c.drawString(4 * cm, y, f"(Riposa: {rest})")
        y -= 0.8 * cm

    # Semifinals
    c.setFont("Helvetica-Bold", 11)
    c.drawString(3 * cm, y, "Semifinali")
    y -= 0.6 * cm
    c.setFont("Helvetica", 11)
    c.drawString(3 * cm, y, "1. 1° vs 4°")
    y -= 0.5 * cm
    c.drawString(3 * cm, y, "2. 2° vs 3°")

    # Finals
    y -= 1 * cm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(3 * cm, y, "Finali")
    y -= 0.6 * cm
    c.setFont("Helvetica", 11)
    c.drawString(3 * cm, y, "1. Finale 3°-4° posto (Perdenti semifinali)")
    y -= 0.5 * cm
    c.drawString(3 * cm, y, "2. Finale 1°-2° posto (Vincitori semifinali)")

    c.save()

# Example usage
create_schedule_pdf_5("schedule_5_structured.pdf", ['A', 'B', 'C', 'D', 'E'])
