import json
import os

def get_value(data_dict, keys_to_try):
    """Pomocnicza funkcja do szukania danych pod różnymi nazwami kluczy."""
    for key in keys_to_try:
        if key in data_dict:
            return data_dict[key]
    return "Nie znaleziono danych (sprawdź klucze w JSON)"

def export_discrepancies(file_flash, file_pro, output_file, threshold=1.0):
    base_path = os.path.dirname(os.path.abspath(__file__))
    path_flash = os.path.join(base_path, file_flash)
    path_pro = os.path.join(base_path, file_pro)
    path_output = os.path.join(base_path, output_file)

    if not os.path.exists(path_flash) or not os.path.exists(path_pro):
        print(f"BŁĄD: Nie znaleziono plików JSON.")
        return

    with open(path_flash, 'r', encoding='utf-8') as f:
        data_flash = json.load(f)
    with open(path_pro, 'r', encoding='utf-8') as f:
        data_pro = json.load(f)

    report = ["="*80, "EKSPORT BŁĘDÓW I PORÓWNANIE ODPOWIEDZI", "="*80 + "\n"]


    prompt_keys = ['prompt', 'input', 'question', 'zapytanie']
    response_keys = ['response', 'output', 'answer', 'model_response', 'odpowiedz']

    found_count = 0
    for f_test, p_test in zip(data_flash, data_pro):
        f_avg = sum(f_test['scores'].values()) / len(f_test['scores'])
        p_avg = sum(p_test['scores'].values()) / len(p_test['scores'])
        diff = f_avg - p_avg

        if diff >= threshold:
            found_count += 1
            report.append(f"PRZYPADEK NR {found_count} | KATEGORIA: {f_test.get('category', 'n/a')}")
            report.append(f"ŚREDNIA OCENA -> FLASH: {f_avg:.2f} | PRO: {p_avg:.2f} | RÓŻNICA: -{diff:.2f}")
            
            
            prompt_text = get_value(f_test, prompt_keys)
            flash_resp = get_value(f_test, response_keys)
            pro_resp = get_value(p_test, response_keys)

            report.append(f"\n[TREŚĆ ZAPYTANIA]:\n{prompt_text}")
            report.append(f"\n[PEŁNA ODPOWIEDŹ FLASH (LEPSZA)]:\n{flash_resp}")
            report.append(f"\n[PEŁNA ODPOWIEDŹ PRO (SŁABSZA)]:\n{pro_resp}")
            report.append("\n" + "-"*80 + "\n")

    with open(path_output, 'w', encoding='utf-8') as out:
        out.write("\n".join(report))
    
    print(f"Zakończono! Znaleziono {found_count} rażących różnic.")
    print(f"Wyniki zapisano w: {output_file}")

if __name__ == "__main__":
    export_discrepancies(
        'gemini-2.0-flash-1-0305-2104.json', 
        'models-gemini-2.5-pro-1-0306-1820.json', 
        'analiza_bledow_v2.txt'
    )