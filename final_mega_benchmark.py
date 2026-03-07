import json
import pandas as pd
import os

def load_avg_scores(filepath):
    if not os.path.exists(filepath):
        print(f"Brak pliku: {filepath}")
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    rows = []
    for entry in data:
        avg = sum(entry['scores'].values()) / len(entry['scores'])
        rows.append({'category': entry['category'], 'score': avg})
    return pd.DataFrame(rows).set_index('category')

def run_mega_comparison():
    files = {
        'Flash_T0.1': 'gemini-2.0-flash-0.1-0305-2114.json',
        'Flash_T1.0': 'gemini-2.0-flash-1-0305-2104.json',
        'Pro_T0.1': 'models-gemini-2.5-pro-0.1-0306-1719.json',
        'Pro_T1.0': 'models-gemini-2.5-pro-1-0306-1820.json'
    }

    results = {}
    for label, path in files.items():
        df = load_avg_scores(path)
        if df is not None:
            results[label] = df['score']

    final_df = pd.DataFrame(results)
    
    final_df['Best_Config'] = final_df.idxmax(axis=1)
    
    final_df.to_csv("mega_benchmark_4_variants.csv")
    print("Zapisano: mega_benchmark_4_variants.csv")

if __name__ == "__main__":
    run_mega_comparison()