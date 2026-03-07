# 🚀 Gemini Benchmark Framework: Flash vs Pro (Multi-Metric Analysis)

## 📋 O Projekcie
Framework ten stanowi kompletne środowisko do obiektywnej i powtarzalnej oceny modeli językowych (LLM). Pozwala na porównanie wydajności modeli (np. Gemini Flash vs Pro lub Grok) w oparciu o ustandaryzowany zestaw danych testowych (**Golden Dataset**).

System został zaprojektowany tak, aby oddzielić dane testowe od logiki oceniającej, co pozwala na łatwą rozbudowę bazy pytań bez ingerencji w kod źródłowy.

---

## 🏗️ Architektura Systemu i Zasada Działania

Mechanizm **Main Tester** działa w oparciu o architekturę sędziowską, co zapewnia najwyższy stopień obiektywizmu:

1. **Wczytywanie danych:** System pobiera bazę pytań testowych z zewnętrznego pliku `test_cases.json`. Pozwala to na dynamiczne zarządzanie zestawem testowym.
2. **Model Testowany (Subject):** Model poddawany ewaluacji (np. Gemini lub Grok) z możliwością dynamicznej konfiguracji parametru `temperature`. Umożliwia to badanie wpływu losowości i kreatywności na stabilność odpowiedzi.
3. **Sędzia (Judge):** Niezależny model AI z ustawioną **stałą temperaturą (0.0)**. Użycie deterministycznego sędziego gwarantuje spójność oceniania i minimalizuje wariancję w punktacji (metoda *Judge-as-a-Judge*).



---

## ⚖️ Skala i Kryteria Oceny

Każda odpowiedź modelu oceniana jest przez Sędziego w skali **1–5**:
* **1** – Odpowiedź całkowicie błędna lub niebezpieczna.
* **5** – Odpowiedź idealna, wyczerpująca i bezpieczna.

### Kluczowe Kategorie Oceny (6-Metric Evaluation):
* **Fidelity (F):** Wierność instrukcji systemu i promptowi.
* **Relevance (R):** Trafność merytoryczna względem zadanego pytania.
* **Safety (S):** Odporność na generowanie treści szkodliwych i jailbreaki.
* **Tone (T):** Profesjonalizm i dopasowanie stylu wypowiedzi.
* **Context (C):** Zdolność utrzymania kontekstu i spójności logicznej.
* **Accuracy (A):** Faktyczna poprawność udzielonych informacji.

---

## 📊 Wyniki Benchmarku (Zbiorcze Zestawienie)

Poniższy wykres oraz tabela przedstawiają uśrednione wyniki uzyskane podczas testów porównawczych we wszystkich 6 kategoriach.

| Metryka | Flash T=0.1 | Flash T=1.0 | Pro T=0.1 | Pro T=1.0 | Zwycięzca (Winner) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Accuracy** | **4.86** | 4.83 | 4.73 | 4.73 | ⚡ Flash T0.1 |
| **Fidelity** | 4.76 | **4.81** | 4.69 | 4.64 | ⚡ Flash T1.0 |
| **Context** | **4.90** | **4.90** | 4.81 | 4.81 | ⚡ Flash T=0.1 / T=1.0 |
| **Relevance** | **4.90** | **4.90** | 4.83 | 4.83 | ⚡ Flash T=0.1 / T=1.0 |
| **Safety** | 4.59 | 4.68 | **4.80** | 4.71 | 🛡️ Pro T0.1 |
| **Tone** | 4.20 | 4.22 | **4.31** | 4.30 | 🛡️ Pro T0.1 |

 <p align="center">
  <img src="https://github.com/piotrwalas1/Gemini-Benchmark-Framework/blob/main/radar_4_variants.png" width="600" title="raport1">
</p>

---

## 🧠 Kluczowe Wnioski (Insights)

* **Stabilność Flasha:** Model Flash wykazuje niemal perfekcyjne wyniki w kategoriach **Context** i **Relevance** (4.90), co czyni go idealnym do zadań wymagających ścisłego trzymania się tematu.
* **Pro jako Dyplomata:** Model Pro oferuje wyższą jakość w kategoriach **Tone** i **Safety**. Jest to model bezpieczniejszy i lepiej brzmiący, choć nieco mniej wierny instrukcjom przy wyższych temperaturach.
* **Czułość na Temperaturę:** Niska temperatura ($T=0.1$) drastycznie poprawia stabilność logiczną modelu Pro, redukując tendencję do "przegadywania" odpowiedzi.
### ⚠️ Analiza wrażliwości modelu Pro na temperaturę
Najważniejszym odkryciem benchmarku jest drastyczny spadek jakości modelu **Gemini 2.5 Pro** przy wzroście temperatury do $T=1.0$ w zadaniach wymagających ścisłego rozumowania.

| Kategoria | Wynik (T=0.1) | Wynik (T=1.0) | Regresja (Delta) |
| :--- | :---: | :---: | :---: |
| **Complex Logic** | **4.67** | 2.17 | <span style="color:red">**-2.50**</span> |
| **Red Teaming / SQL** | 4.83 | 4.33 | -0.50 |
| **Safety** | 4.83 | 4.33 | -0.50 |
| **Hallucination** | 4.00 | 3.58 | -0.42 |

**Wniosek:** Model Pro przy wyższej temperaturze traci zdolność do utrzymania rygoru logicznego. W kategorii `Complex Logic` model przestał dostarczać poprawne odpowiedzi, co sugeruje, że dla zadań deterministycznych (logika, kod, SQL) model ten **musi** pracować na niskiej temperaturze ($T=0.1$). Flash w tym samym czasie wykazał niemal zerową wrażliwość na ten parametr.
---

## 🛠️ Stos Narzędziowy (Toolbox)

W repozytorium znajdują się skrypty analizujące:
* `main_tester_all.py`: Rdzeń systemu. Odpowiada za iterację po zestawie `test_cases.json`, wysyłanie zapytań do testowanego modelu, a następnie przekazywanie par (Pytanie + Odpowiedź) do Sędziego w celu wystawienia ocen. Wyniki zapisuje w formacie JSON.
* `final_mega_benchmark.py`: Generowanie tabelarycznych zestawień zbiorczych.
* `model_profile_4v.py`: Analiza profilowa wymiarów jakościowych.
* `generate_radar_chart_4v.py`: Wizualizacja danych na wykresach radarowych.
* `compare_models.py`: Narzędzie do analizy regresji i wyliczania delty wyników.

---

## 🚀 Jak uruchomić?

1. Sklonuj repozytorium.
2. Przygotuj plik `test_cases.json` ze swoimi pytaniami.
3. Zainstaluj wymagania: `pip install pandas matplotlib numpy`.
4. Uruchom analizę zbiorczą: `python scripts/final_mega_benchmark.py`.
