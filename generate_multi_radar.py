import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def generate_radar_4v():
    files = {
        'Flash T0.1': ('gemini-2.0-flash-0.1-0305-2114.json', '#1f77b4'), 
        'Flash T1.0': ('gemini-2.0-flash-1-0305-2104.json', '#a0cbe8'),  
        'Pro T0.1': ('models-gemini-2.5-pro-0.1-0306-1719.json', '#ff7f0e'), 
        'Pro T1.0': ('models-gemini-2.5-pro-1-0306-1820.json', '#ffbb78')   
    }

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    for label, (path, color) in files.items():
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                df = pd.DataFrame([x['scores'] for x in data]).mean()
                
                categories = list(df.index)
                values = df.tolist()
                values += values[:1] 
                
                angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
                angles += angles[:1]
                
                ax.plot(angles, values, linewidth=2, label=label, color=color)
                ax.fill(angles, values, color=color, alpha=0.05)
        except FileNotFoundError:
            continue

    plt.xticks(angles[:-1], categories)
    plt.title('Porównanie 4 wariantów: Model + Temperatura', size=15, y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.savefig('radar_4_variants.png')
    print("Wykres radarowy zapisany jako: radar_4_variants.png")

if __name__ == "__main__":
    generate_radar_4v()