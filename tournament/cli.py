from tournament.fixtures import generate_fixtures, record_result
from tournament.standings import compute_standings, get_champion, is_league_complete
from tournament.storage import load_league, save_league
from tournament.teams import list_teams, register_team, team_names_by_id
from tournament.validation import ValidationError, parse_score_text
from tournament.fixtures import generate_fixtures, record_result, simulate_demo_fixtures

DEFAULT_SAVE_FILE = "league.json"
DEMO_SEED = 42

MENU = """
=== TournamentLab ===
 1) Register team
 2) List teams
 3) Generate schedule
 4) List fixtures
 5) Record result
 6) Show standings
 7) Save
 8) Load
 9) Show champion
 10) Simulate League
 0) Quit"""


def format_standings(rows, complete):
    label = "FINAL" if complete else "IN PROGRESS"
    header = f"{'#':>2} {'Team':<30} {'P':>2} {'W':>2} {'D':>2} {'L':>2} {'GF':>3} {'GA':>3} {'GD':>4} {'Pts':>3}"
    lines = [f"League table ({label})", header, "-" * len(header)]
    for position, row in enumerate(rows, start=1):
        lines.append(
            f"{position:>2} {row['name']:<30} {row['played']:>2} {row['wins']:>2} "
            f"{row['draws']:>2} {row['losses']:>2} {row['goals_for']:>3} "
            f"{row['goals_against']:>3} {row['goal_diff']:>+4} {row['points']:>3}"
        )
    return "\n".join(lines)


def format_fixtures(teams, fixtures):
    names = team_names_by_id(teams)
    lines = []
    for fixture in fixtures:
        home = names[fixture["home_id"]]
        away = names[fixture["away_id"]]
        if fixture["status"] == "played":
            result = f"played {fixture['home_score']}-{fixture['away_score']}"
        else:
            result = "pending"
        lines.append(f"{fixture['id']}  {home} vs {away}  [{result}]")
    return "\n".join(lines)


def action_register(state):
    if state["fixtures"]:
        print("Error: teams cannot be added after the schedule is generated.")
        return
    team = register_team(state["teams"], input("Team name: "))
    print(f"Registered {team['name']} as {team['id']}.")


def action_list_teams(state):
    if not state["teams"]:
        print("No teams registered yet.")
    for line in list_teams(state["teams"]):
        print(line)


def action_generate(state):
    state["fixtures"] = generate_fixtures(state["teams"], state["fixtures"])
    print(f"Generated {len(state['fixtures'])} fixtures.")


def action_list_fixtures(state):
    if not state["fixtures"]:
        print("No fixtures yet. Generate the schedule first.")
        return
    print(format_fixtures(state["teams"], state["fixtures"]))


def action_record(state):
    if not state["fixtures"]:
        print("Error: no fixtures yet. Generate the schedule first.")
        return
    fixture_id = input("Fixture ID (e.g. M001): ").strip().upper()
    home = parse_score_text(input("Home score: "))
    away = parse_score_text(input("Away score: "))
    record_result(state["fixtures"], fixture_id, home, away)
    print(f"Recorded {fixture_id}: {home}-{away}.")


def action_standings(state):
    if not state["teams"]:
        print("No teams registered yet.")
        return
    rows = compute_standings(state["teams"], state["fixtures"])
    print(format_standings(rows, is_league_complete(state["fixtures"])))


def action_save(state):
    path = input(f"Save to [{DEFAULT_SAVE_FILE}]: ").strip() or DEFAULT_SAVE_FILE
    save_league(path, state["teams"], state["fixtures"])
    print(f"Saved to {path}.")


def action_load(state):
    path = input(f"Load from [{DEFAULT_SAVE_FILE}]: ").strip() or DEFAULT_SAVE_FILE
    teams, fixtures = load_league(path)
    state["teams"] = teams
    state["fixtures"] = fixtures
    print(f"Loaded {len(teams)} teams and {len(fixtures)} fixtures from {path}.")


def action_champion(state):
    champion = get_champion(state["teams"], state["fixtures"])
    if champion is None:
        print("No champion yet: the league is in progress.")
    else:
        print(f"Champion: {champion['name']} with {champion['points']} points!")


def action_simulate(state):
    if not state["fixtures"]:
        print("Error: no fixtures yet. Generate the schedule first.")
        return
    answer = input(
        f"This fills ALL pending games with fake scores (seed {DEMO_SEED}). "
        "Type YES to confirm: "
    )
    if answer.strip() != "YES":
        print("Cancelled. Nothing was changed.")
        return
    state["fixtures"] = simulate_demo_fixtures(state["fixtures"], DEMO_SEED)
    print("Demo scores filled in.")

ACTIONS = {
    "1": action_register,
    "2": action_list_teams,
    "3": action_generate,
    "4": action_list_fixtures,
    "5": action_record,
    "6": action_standings,
    "7": action_save,
    "8": action_load,
    "9": action_champion,
    "10": action_simulate,
}



def run():
    state = {"teams": [], "fixtures": []}
    try:
        while True:
            print(MENU)
            choice = input("Choose: ").strip()
            if choice == "0":
                break
            action = ACTIONS.get(choice)
            if action is None:
                print(f"'{choice}' is not a menu option. Try again.")
                continue
            try:
                action(state)
            except ValidationError as problem:
                print(f"Error: {problem}")
    except (EOFError, KeyboardInterrupt):
        print()
    print("Goodbye!")