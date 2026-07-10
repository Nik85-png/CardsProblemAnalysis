"""Generate two tiny test CSVs for quick verification of upload/revert/badge/Excel features.

Run:  py test_datasets/generate.py

Output:
  test_datasets/test_small.csv        — 8 rows, all 4 conditions, mix success/fail
  test_datasets/test_b_conditions.csv — 6 rows, only KQB + KQJB (tests Excel regen)
"""

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Minimal column list — just the ones the app actually reads.
# Extra columns can stay empty.
HEADER = [
    "participant", "Trials per task", "Task", "condition", "Trials2correct", "trialN",
    "trial_ends",
    "movement_codes",
    "final_card_positions_1",
    "final_card_position_codes_1",
    "row_overall_correct_1", "col_overall_correct_1", "overall_correct",
    "downTimes", "upTimes",
]

# Add move_0..move_50 + their downTime/upTime columns (empty — not needed for processing)
for i in range(51):
    HEADER.append(f"move_{i}")
    HEADER.append(f"move_{i}_downTime")
    HEADER.append(f"move_{i}_upTime")


def make_row(participant, condition, trial_n, overall_correct, moves_list, final_list):
    """Build a CSV row with realistic-looking movement/final-position strings."""
    moves_str = str(moves_list) if moves_list else "[]"
    # For final_card_position_codes_1, the app reads it for blank-pattern analysis.
    # It should be a list of tokens like "queen_spades_dA1" etc.
    final_str = str(final_list) if final_list else "[]"

    # Use first and last token from final_list for row/col_overall_correct placeholders
    row_val = 1 if overall_correct == 1 else 0
    col_val = 1 if overall_correct == 1 else 0

    row = {
        "participant": participant,
        "Trials per task": "", "Task": "1",
        "condition": condition,
        "Trials2correct": "1" if overall_correct == 1 else "0",
        "trialN": trial_n,
        "trial_ends": "submit",
        "movement_codes": moves_str,
        "final_card_positions_1": "",
        "final_card_position_codes_1": final_str,
        "row_overall_correct_1": row_val,
        "col_overall_correct_1": col_val,
        "overall_correct": overall_correct,
        "downTimes": "", "upTimes": "",
    }
    return row


def write_csv(name, rows):
    path = HERE / name
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"  Wrote {path}  ({len(rows)} rows)")


# ─── DATASET 1: All 4 conditions, success + fail mix ────────────────────────

ds1 = [
    # Participant 101, KQJB, 2 trials: one success, one fail
    make_row(101, "KQJB", 0, 1,
             ["queen_spades_cA1", "king_diamonds_cA2", "jack_diamonds_cA3",
              "queen_clubs_cB2", "king_hearts_cB3", "jack_hearts_cB4",
              "queen_diamonds_cC3", "king_clubs_cC4", "jack_clubs_cC5",
              "queen_hearts_cD4", "king_spades_cD5", "jack_spades_cD6"],
             ["queen_spades_cA1", "king_diamonds_cA2", "jack_diamonds_cA3",
              "queen_clubs_cB2", "king_hearts_cB3", "jack_hearts_cB4",
              "queen_diamonds_cC3", "king_clubs_cC4", "jack_clubs_cC5",
              "queen_hearts_cD4", "king_spades_cD5", "jack_spades_cD6"]),
    make_row(101, "KQJB", 1, 0,
             ["queen_spades_cA1", "queen_clubs_cOff Grid", "jack_diamonds_cB2"],
             ["queen_spades_cA1", "jack_diamonds_cB2"]),

    # Participant 102, KQB, 2 trials: success + fail
    make_row(102, "KQB", 0, 1,
             ["queen_diamonds_bB1", "queen_clubs_bC2", "queen_spades_bD3",
              "king_clubs_bC1", "king_hearts_bD2", "king_diamonds_bE3"],
             ["queen_diamonds_bB1", "queen_clubs_bC2", "queen_spades_bD3",
              "king_clubs_bC1", "king_hearts_bD2", "king_diamonds_bE3"]),
    make_row(102, "KQB", 1, 0,
             ["queen_diamonds_bB1", "king_clubs_bOff Grid", "blank_bC3"],
             ["queen_diamonds_bB1", "blank_bC3"]),

    # Participant 103, KQ, 2 trials: success + fail
    make_row(103, "KQ", 0, 1,
             ["queen_spades_aA1", "king_diamonds_aA2",
              "queen_clubs_aB2", "king_hearts_aB3",
              "queen_diamonds_aC3", "king_clubs_aC4"],
             ["queen_spades_aA1", "king_diamonds_aA2",
              "queen_clubs_aB2", "king_hearts_aB3",
              "queen_diamonds_aC3", "king_clubs_aC4"]),
    make_row(103, "KQ", 1, 0,
             ["queen_spades_aA1", "king_hearts_aOff Grid"],
             ["queen_spades_aA1"]),

    # Participant 104, KQJ, 2 trials: success + fail
    make_row(104, "KQJ", 0, 1,
             ["queen_spades_dA1", "king_diamonds_dA2", "jack_diamonds_dA3",
              "queen_clubs_dB2", "king_hearts_dB3", "jack_hearts_dB4",
              "queen_diamonds_dC3", "king_clubs_dC4", "jack_clubs_dC5"],
             ["queen_spades_dA1", "king_diamonds_dA2", "jack_diamonds_dA3",
              "queen_clubs_dB2", "king_hearts_dB3", "jack_hearts_dB4",
              "queen_diamonds_dC3", "king_clubs_dC4", "jack_clubs_dC5"]),
    make_row(104, "KQJ", 1, 0,
             ["jack_diamonds_dA1", "jack_hearts_dOff Grid"],
             ["jack_diamonds_dA1"]),
]

# ─── DATASET 2: ONLY KQB + KQJB — specifically to test Excel regeneration ───

ds2 = [
    # Participant 201, KQJB, success
    make_row(201, "KQJB", 0, 1,
             ["queen_spades_cA1", "queen_clubs_cB2", "queen_diamonds_cC3",
              "queen_hearts_cD4", "king_diamonds_cA2", "king_hearts_cB3",
              "king_clubs_cC4", "king_spades_cD5", "jack_diamonds_cA3",
              "jack_hearts_cB4", "jack_clubs_cC5", "jack_spades_cD6"],
             ["queen_spades_cA1", "queen_clubs_cB2", "queen_diamonds_cC3",
              "queen_hearts_cD4", "king_diamonds_cA2", "king_hearts_cB3",
              "king_clubs_cC4", "king_spades_cD5", "jack_diamonds_cA3",
              "jack_hearts_cB4", "jack_clubs_cC5", "jack_spades_cD6"]),
    # Participant 201, KQJB, fail
    make_row(201, "KQJB", 1, 0,
             ["queen_hearts_cA1", "king_spades_cB2", "jack_spades_cC3"],
             ["queen_hearts_cA1", "king_spades_cB2", "jack_spades_cC3"]),

    # Participant 202, KQB, success
    make_row(202, "KQB", 0, 1,
             ["queen_diamonds_bB1", "queen_clubs_bC2", "queen_spades_bD3",
              "king_clubs_bC1", "king_hearts_bD2", "king_diamonds_bB3"],
             ["queen_diamonds_bB1", "queen_clubs_bC2", "queen_spades_bD3",
              "king_clubs_bC1", "king_hearts_bD2", "king_diamonds_bB3"]),
    # Participant 202, KQB, fail (includes a blank card)
    make_row(202, "KQB", 1, 0,
             ["queen_diamonds_bB1", "queen_clubs_bOff Grid", "blank_bC2"],
             ["queen_diamonds_bB1", "blank_bC2"]),

    # Participant 203, KQJB, success
    make_row(203, "KQJB", 0, 1,
             ["queen_spades_cA1", "king_diamonds_cB1", "jack_diamonds_cC1",
              "queen_clubs_cA3", "king_hearts_cB3", "jack_hearts_cC3",
              "queen_diamonds_cA5", "king_clubs_cB5", "jack_clubs_cC5",
              "queen_hearts_cA7", "king_spades_cB7", "jack_spades_cC7"],
             ["queen_spades_cA1", "king_diamonds_cB1", "jack_diamonds_cC1",
              "queen_clubs_cA3", "king_hearts_cB3", "jack_hearts_cC3",
              "queen_diamonds_cA5", "king_clubs_cB5", "jack_clubs_cC5",
              "queen_hearts_cA7", "king_spades_cB7", "jack_spades_cC7"]),
    # Participant 203, KQB, fail
    make_row(203, "KQB", 1, 0,
             ["king_diamonds_bA1", "queen_hearts_bOff Grid"],
             ["king_diamonds_bA1"]),
]


# ─── Write both ─────────────────────────────────────────────────────────────

print("Generating test datasets...\n")
write_csv("test_small.csv", ds1)
write_csv("test_b_conditions.csv", ds2)

print("\nDone! Checklist:")
print("  ✓ test_small.csv       — Upload it → badge shows, all 4 conditions in tabs")
print("  ✓ test_b_conditions.csv — Upload it → Excel regenerates with only KQB/KQJB")
print("  ✓ Then click Revert    → badge hides, original data back")
