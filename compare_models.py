import json
import pandas as pd
import os

def load_category_scores(filepath):
    if not os.path.exists(filepath):
        print(f"Błąd: Brak pliku {filepath}")
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    rows = []
    for entry in data:
        avg = sum(entry['scores'].values()) / len(entry['scores'])
        rows.append({'category': entry['category'], 'score': avg})
    return pd.DataFrame(rows).groupby('category').mean()

def run_advanced_comparison():
    files = {
        'Flash_01': 'gemini-2.0-flash-0.1-0305-2114.json',
        'Flash_10': 'gemini-2.0-flash-1-0305-2104.json',
        'Pro_01': 'models-gemini-2.5-pro-0.1-0306-1719.json',
        'Pro_10': 'models-gemini-2.5-pro-1-0306-1820.json'
    }

    results = {}
    for label, path in files.items():
        df = load_category_scores(path)
        if df is not None:
            results[label] = df['score']

    if not results: return

    comp = pd.DataFrame(results)
    comp['Delta_Flash_Temp'] = comp['Flash_10'] - comp['Flash_01']
    comp['Delta_Pro_Temp'] = comp['Pro_10'] - comp['Pro_01']
    comp['Delta_Pro_vs_Flash_01'] = comp['Pro_01'] - comp['Flash_01']

   
    comp = comp.sort_values(by='Delta_Pro_Temp', ascending=True)

    output_filename = "advanced_comparison_report.csv"
    
   
    top_regressions = comp[['Pro_01', 'Pro_10', 'Delta_Pro_Temp']].head(10).round(3)
    header_text = "--- TOP REGRESJE W MODELU PRO (Największe spadki jakości) ---\n"
    header_text += top_regressions.to_string() + "\n\n"
    header_text += "--- PEŁNE DANE PORÓWNAWCZE ---\n"

   
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(header_text)
        comp.to_csv(f)

    print(f">>> Zaawansowany raport wygenerowany: {output_filename}")
    print("\n" + header_text)

if __name__ == "__main__":
    run_advanced_comparison()