import json
import pandas as pd
import os


FILES = {
    'Flash_T01': 'results-models-gemini-2.0-flash-0.1-0308-1241.json',
    'Flash_T10': 'results-models-gemini-2.0-flash-1.0-0308-1225.json',
    'Pro_T01': 'results-models-gemini-2.5-pro-0.1-0308-1310.json',
    'Pro_T10': 'results-models-gemini-2.5-pro-1.0-0308-1207.json'
}

def get_summary_metrics(filepath):
    """Pobiera uśrednione dane z pliku JSON."""
    if not os.path.exists(filepath):
        return None
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    meta = data.get("metadata", {})
    results = data.get("results", [])
    
    
    all_scores = []
    for r in results:
        
        row_avg = sum(r['scores'].values()) / len(r['scores'])
        all_scores.append(row_avg)
    
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
    
    return {
        "Avg Score": round(avg_score, 2),
        "Avg Latency (s)": round(meta.get("avg_latency", 0), 2),
        "Total Cost ($)": round(meta.get("total_estimated_cost_usd", 0), 4)
    }

def generate_final_report():
    summary_data = []
    
    for label, path in FILES.items():
        metrics = get_summary_metrics(path)
        if metrics:
            metrics["Model Variant"] = label
            summary_data.append(metrics)
    
    if not summary_data:
        print("❌ BŁĄD: Nie znaleziono żadnych plików wynikowych JSON!")
        return

   
    df_summary = pd.DataFrame(summary_data)[["Model Variant", "Avg Score", "Avg Latency (s)", "Total Cost ($)"]]
    
    try:
        
        markdown_table = df_summary.to_markdown(index=False)
        
        print("\n" + "="*50)
        print("📊 GOTOWA TABELA DO README.md")
        print("="*50 + "\n")
        print(markdown_table)
        print("\n" + "="*50)
        print("👉 Skopiuj powyższą tabelę i wklej ją do sekcji 'Results' w swoim README.")

    except ImportError:
        print("\n❌ BRAKUJĄCA BIBLIOTEKA: tabulate")
        print("-" * 30)
        print("Aby wyświetlić tabelę, zainstaluj bibliotekę w swoim venv:")
        print("Wpisz w terminalu: .\\venv\\Scripts\\pip install tabulate")
        print("-" * 30)
        print("\nSurowe dane (Pandas):\n")
        print(df_summary)

if __name__ == "__main__":
    generate_final_report()