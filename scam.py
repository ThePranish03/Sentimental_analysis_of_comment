# scam_detection_pretty.py
# Requires: pandas, tabulate
# pip install pandas tabulate

import re
from collections import Counter
import pandas as pd
from tabulate import tabulate

def normalize_words(text):
    """
    Lowercase and extract word tokens (letters, numbers, underscores).
    """
    return re.findall(r"\b\w+\b", text.lower())

def detect_scam_counts(sentences, scam_keywords):
    scam_set = sorted({w.lower() for w in scam_keywords})
    rows = []
    global_counter = Counter()

    for s in sentences:
        tokens = normalize_words(s)
        counts = Counter(tok for tok in tokens if tok in scam_set)

        row = {"Sentence": s}
        for k in scam_set:
            row[k] = counts.get(k, 0)
        row["Total"] = sum(counts.values())
        row["Unique"] = len([k for k, v in counts.items() if v > 0])
        rows.append(row)
        global_counter.update(counts)

    df_per_sentence = pd.DataFrame(rows)
    cols = ["Sentence"] + scam_set + ["Total", "Unique"]
    df_per_sentence = df_per_sentence[cols]

    summary_rows = [{"Word": w, "Total_Count": global_counter.get(w, 0)} for w in scam_set]
    df_summary = pd.DataFrame(summary_rows).sort_values("Total_Count", ascending=False).reset_index(drop=True)

    return df_per_sentence, df_summary

if __name__ == "__main__":
    scam_keywords = [
        "win", "winner", "prize", "congratulations", "click", "urgent", "lottery",
        "transfer", "bank", "limited", "offer", "free", "claim", "password", "verified"
    ]

    sentences = [
        "Congratulations! You are a WINNER. Click here to claim your prize.",
        "This is an urgent message from your bank: transfer required to verify account.",
        "Limited time offer — get a free trial now.",
        "Your password is secure. No action needed.",
        "You have won the lottery! Claim your prize prize now.",
        "Hello friend, let's meet tomorrow for lunch."
    ]

    df_per_sentence, df_summary = detect_scam_counts(sentences, scam_keywords)

    # Pretty print tables
    print("\n📌 Scam Word Counts per Sentence:\n")
    print(tabulate(df_per_sentence, headers="keys", tablefmt="grid", showindex=False))

    print("\n📊 Summary of Scam Words (all sentences):\n")
    print(tabulate(df_summary, headers="keys", tablefmt="fancy_grid", showindex=False))

    # Save clean CSVs
    df_per_sentence.to_csv("scam_counts_per_sentence.csv", index=False)
    df_summary.to_csv("scam_counts_summary.csv", index=False)
    print("\n✅ Results saved as 'scam_counts_per_sentence.csv' and 'scam_counts_summary.csv'")
