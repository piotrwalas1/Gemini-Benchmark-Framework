import json
import pandas as pd
import os

def load_benchmark_data(filepath):
    if not os.path.exists(filepath):
        print(f"Błąd: Brak pliku {filepath}")
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    

    results_list = data.get("results", [])
    
    rows = []
    for entry in results_list:
        
        avg_score = sum(entry['scores'].values()) / len(entry['scores'])
        
        rows.append({
            'category': entry['category'],
            'score': avg_score,
            'latency': entry['metrics'].get('latency', 0),
            'cost': entry['metrics'].get('cost_usd', 0)
        })
    
    df = pd.DataFrame(rows)
    
    return df.groupby('category').mean()

def run_advanced_comparison():
    
    files = {
        'Flash_01': 'results-models-gemini-2.0-flash-0.1-0308-1241.json',
        'Flash_10': 'results-models-gemini-2.0-flash-1.0-0308-1225.json',
        'Pro_01': 'results-models-gemini-2.5-pro-0.1-0308-1310.json',
        'Pro_10': 'results-models-gemini-2.5-pro-1.0-0308-1207.json'
    }

    
    scores = {}
    latencies = {}
    costs = {}

    for label, path in files.items():
        df = load_benchmark_data(path)
        if df is not None:
            scores[label] = df['score']
            latencies[label] = df['latency']
            costs[label] = df['cost']

    if not scores:
        print("Nie znaleziono danych do porównania.")
        return

    comp = pd.DataFrame(scores)
    
    # Obliczamy delty (regresje)
    comp['Delta_Pro_Temp'] = comp['Pro_10'] - comp['Pro_01']
    comp['Delta_Flash_Temp'] = comp['Flash_10'] - comp['Flash_01']
    
    # Sortujemy po największym spadku w modelu Pro
    comp = comp.sort_values(by='Delta_Pro_Temp', ascending=True)

    # Obliczamy globalne statystyki dla raportu tekstowego
    report_filename = "advanced_comparison_report.csv"
    
    
    header = "=== KOMPLEKSOWY RAPORT PORÓWNAWCZY LLM ===\n\n"
    
    header += "--- ANALIZA REGRESJI (Top spadki jakości przy T=1.0) ---\n"
    header += comp[['Pro_01', 'Pro_10', 'Delta_Pro_Temp']].head(10).round(3).to_string() + "\n\n"
    
    header += "--- EFEKTYWNOŚĆ OPERACYJNA (Średnie) ---\n"
    stats = []
    for label in files.keys():
        if label in scores:
            stats.append({
                'Model_Variant': label,
                'Avg_Score': scores[label].mean(),
                'Avg_Latency_Sec': latencies[label].mean(),
                'Avg_Cost_USD': costs[label].mean()
            })
    stats_df = pd.DataFrame(stats).round(4)
    header += stats_df.to_string(index=False) + "\n\n"
    
    header += "--- PEŁNE DANE KATEGORII ---\n"

    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(header)
        comp.to_csv(f)

    print(f"Sukces! Raport wygenerowany: {report_filename}")
    print("\n" + header)

if __name__ == "__main__":
    run_advanced_comparison()