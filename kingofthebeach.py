import random
from itertools import combinations, chain
from collections import defaultdict

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generate_schedule_pdf_kob(filename, players, schedule):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("Comabbio Cup - Gloria & Disagio", styles['Title']))
    elements.append(Spacer(1, 12))

    # Annotatable Player Points Table
    elements.append(Paragraph("Players", styles['Heading2']))
    
    header = ["Player"] + [f"R{i+1}" for i in range(len(schedule))]
    table_data = [header]
    for player in players:
        row = [player] + ["" for _ in schedule]
        table_data.append(row)

    points_table = Table(table_data, colWidths=[100] + [35] * len(schedule))
    points_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWHEIGHT', (0,1), (-1,-1), 20),
    ]))
    elements.append(points_table)

    # Rounds
    for i, rnd in enumerate(schedule):
        elements.append(Paragraph(f"Round {i + 1}", styles['Heading2']))
        match_data = [["Team 1", " ", "Team 2"]]

        for team1, team2 in rnd["matches"]:
            team1_str = " & ".join(team1)
            team2_str = " & ".join(team2)
            match_data.append([team1_str, " ", team2_str])

        match_table = Table(match_data, colWidths=[150, 30, 150])
        match_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ]))
        elements.append(match_table)

        # Resting players
        if rnd["rest"]:
            rest_line = "Riposa: " + ", ".join(rnd["rest"])
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(rest_line, styles['Normal']))

        elements.append(Spacer(1, 18))

    doc.build(elements)

def reorder_rounds_no_consecutive_rests(rounds):
    def backtrack(path, used_indices, last_rest_set):
        if len(path) == len(rounds):
            return path

        for i, rnd in enumerate(rounds):
            if i in used_indices:
                continue
            current_rest = set(rnd['rest'])

            # Check no one rests twice in a row
            if last_rest_set and not current_rest.isdisjoint(last_rest_set):
                continue

            result = backtrack(
                path + [rnd],
                used_indices | {i},
                current_rest
            )
            if result:
                return result  # Found valid ordering

        return None  # Dead end, trigger backtracking

    return backtrack([], set(), set())

def schedule_tournament(players):
    if len(players) < 4:
        raise ValueError("At least 4 players required")

    all_possible_pairs = set(combinations(players, 2))
    used_pairs = set()
    player_match_count = defaultdict(int)
    rounds = []
    player_partners = defaultdict(set)
    rested_last_round = set()

    def can_pair(p1, p2):
        return p2 not in player_partners[p1]

    while True:
        available_players = set(players)
        round_matches = []
        used_this_round = set()

        # Try to form all valid teams (no reused partners)
        valid_teams = [pair for pair in all_possible_pairs if pair not in used_pairs and can_pair(*pair)]
        random.shuffle(valid_teams)
        
        teams = []
        used_in_teams = set()

        for team in valid_teams:
            if team[0] in used_in_teams or team[1] in used_in_teams:
                continue
            teams.append(team)
            used_in_teams.update(team)
            used_pairs.add(team)
            player_partners[team[0]].add(team[1])
            player_partners[team[1]].add(team[0])
            if len(used_in_teams) >= len(players) - len(players) % 4:
                break
            
        # Pair teams into matches
        team_matches = []
        used_players = set()
        i = 0
        while i < len(teams) - 1:
            t1 = teams[i]
            t2 = teams[i + 1]
            if set(t1).isdisjoint(set(t2)):
                team_matches.append((t1, t2))
                used_players.update(t1)
                used_players.update(t2)
                i += 2
            else:
                i += 1

        if not team_matches:
            break

        # Track player match count
        for t1, t2 in team_matches:
            for p in t1 + t2:
                player_match_count[p] += 1

        resting_players = list(set(players) - used_players)
        rounds.append({
            'matches': team_matches,
            'rest': resting_players
        })

        # Stop if no more valid unique pairs or teams can be made
        if len(used_pairs) >= len(all_possible_pairs):
            break

    return rounds, player_match_count

# Example usage:
players = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Giulia"]
if len(players) % 4 in (0, 1):
    exp_matches = len(players) - 1
else:
    exp_matches = len(players) - 2

while True:
    schedule, match_counts = schedule_tournament(players)
    if min(match_counts.values()) == exp_matches:
        break

schedule_ordered = reorder_rounds_no_consecutive_rests(schedule)
if schedule_ordered is None:
    schedule_ordered = schedule
for i, round_data in enumerate(schedule_ordered):
    print(f"\nRound {i+1}:")
    for t1, t2 in round_data['matches']:
        print(f"  Match: {t1} - {t2}")
    if round_data['rest']:
        print(f"  Resting: {', '.join(round_data['rest'])}")

print("\nMatch count per player:")
for p in players:
    print(f"  {p}: {match_counts[p]} matches")


generate_schedule_pdf("tournament_schedule.pdf", players, schedule_ordered)
