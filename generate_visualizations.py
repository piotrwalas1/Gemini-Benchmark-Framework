import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

FILES = {
    'Flash_T01': 'results-models-gemini-2.0-flash-0.1-0308-1241.json',
    'Flash_T10': 'results-models-gemini-2.0-flash-1.0-0308-1225.json',
    'Pro_T01': 'results-models-gemini-2.5-pro-0.1-0308-1310.json',
    'Pro_T10': 'results-models-gemini-2.5-pro-1.0-0308-1207.json'
}

def load_all_metrics():
    data_summary = []
    category_scores = {}

    for label, path in FILES.items():
        if not os.path.exists(path): continue
        with open(path, 'r', encoding='utf-8') as f:
            d = json.load(f)
        
        # 1. Dane do słupków (Efektywność)
        meta = d.get("metadata", {})
        results = d.get("results", [])
        avg_s = sum(sum(r['scores'].values())/len(r['scores']) for r in results)/len(results)
        
        data_summary.append({
            'Model': label,
            'Score': avg_s,
            'Latency': meta.get("avg_latency", 0),
            'Cost': meta.get("total_estimated_cost_usd", 0)
        })

        # 2. Dane do radaru (Kategorie)
        df_cat = pd.DataFrame([{'cat': r['category'], 's': sum(r['scores'].values())/len(r['scores'])} for r in results])
        category_scores[label] = df_cat.groupby('cat')['s'].mean()

    return pd.DataFrame(data_summary), category_scores

def create_plots():
    df_eff, cat_scores = load_all_metrics()
    
    # --- WYKRES 1: RADAR CHART (JAKOŚĆ) ---
    categories = list(cat_scores['Flash_T01'].index)
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    fig = plt.figure(figsize=(16, 8))
    ax1 = plt.subplot(121, polar=True)
    
    for label, scores in cat_scores.items():
        values = scores.tolist()
        values += values[:1]
        ax1.plot(angles, values, label=label, linewidth=2)
        ax1.fill(angles, values, alpha=0.05)
    
    plt.xticks(angles[:-1], categories, size=8)
    ax1.set_title("Profil Jakościowy (Radar)", y=1.1)
    ax1.legend(loc='upper right', bbox_to_anchor=(0.1, 1.1))

    # --- WYKRES 2: BAR CHART (LATENCY) ---
    ax2 = plt.subplot(122)
    colors = ['#66b3ff','#2980b9','#ffcc99','#e67e22']
    bars = ax2.bar(df_eff['Model'], df_eff['Latency'], color=colors)
    ax2.set_ylabel('Średnia Latencja (sekundy)')
    ax2.set_title('Porównanie Szybkości Odpowiedzi')
    
    # Dodanie etykiet nad słupkami
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5, f'{height:.1f}s', ha='center')

    plt.tight_layout()
    plt.savefig("benchmark_visuals.png")
    print("✅ Sukces: Wygenerowano benchmark_visuals.png")
    plt.show()

if __name__ == "__main__":
    create_plots()