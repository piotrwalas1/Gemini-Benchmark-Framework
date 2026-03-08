# 🚀 Gemini Benchmark Framework: Flash vs Pro (Efficiency & Quality Analysis) Proof of Concept

## 📋 O Projekcie

Framework ten stanowi kompletne środowisko do obiektywnej i powtarzalnej oceny modeli językowych (LLM). Pozwala na porównanie wydajności modeli np.(**Gemini 2.0 Flash vs 2.5 Pro**) w oparciu o ustandaryzowany zestaw danych testowych (**Golden Dataset**). 

System został zaprojektowany tak, aby oddzielić dane testowe od logiki oceniającej, co pozwala na łatwą rozbudowę bazy pytań bez ingerencji w kod źródłowy. W najnowszej wersji framework rozszerzyłem o **pogłębioną analizę kosztową oraz testy latencji**, co pozwala na ocenę modeli pod kątem wdrożeń produkcyjnych.

## 🏗️ Architektura Systemu i Zasada Działania

Mechanizm działa w oparciu o architekturę sędziowską (**Judge-as-a-Service**), co zapewnia najwyższy stopień obiektywizmu:

1.  **Wczytywanie danych:** System pobiera bazę pytań z pliku `test_cases.json`. Pozwala to na dynamiczne zarządzanie zestawem testowym.
2.  **Model Testowany (Subject):** Ewaluacja modeli Gemini z możliwością dynamicznej konfiguracji parametru `temperature`.
3.  **Sędzia (Judge):** Niezależny model AI (Llama 3) z wymuszoną **stałą temperaturą (0.0)**. Użycie deterministycznego sędziego gwarantuje spójność oceniania (metoda **Judge-as-a-Judge**).
4.  **Monitor Wydajności:** Moduł mierzący czas odpowiedzi (Latency) oraz precyzyjnie wyliczający koszty (USD) na podstawie zużycia tokenów.

## ⚖️ Skala i Kryteria Oceny (6-Metric Evaluation)

Każda odpowiedź modelu oceniana jest przez Sędziego w skali **1–5**:
* **Fidelity (F):** Wierność instrukcji systemu i promptowi.
* **Accuracy (A):** Faktyczna poprawność udzielonych informacji.
* **Safety (S):** Odporność na generowanie treści szkodliwych i jailbreaki.
* **Code Safety (CS):** Bezpieczeństwo generowanego kodu i brak podatności.
* **Concise (C):** Zwięzłość i brak zbędnego "gadulstwa".
* **Tone (T):** Profesjonalizm i dopasowanie stylu wypowiedzi.

## 📊 Wyniki Benchmarku (Zbiorcze Zestawienie)

Poniższa tabela przedstawia uśrednione wyniki jakościowe oraz kluczowe metryki operacyjne (Szybkość/Koszt) uzyskane podczas testów.

| Metryka | Flash T=0.1 | Flash T=1.0 | Pro T=0.1 | Pro T=1.0 | Zwycięzca (Winner) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Avg Quality Score** | 4.69 | **4.73** | 4.72 | 4.68 | ⚡ **Flash T=1.0** |
| **Avg Latency (s)** | 3.21s | **2.90s** | 18.27s | 18.92s | 🚀 **Flash (Speed)** |
| **Total Cost ($)** | **$0.0073** | **$0.0066** | $0.1666 | $0.1709 | 💰 **Flash (23x Cheaper)** |

## 📈 Wizualizacja Danych

  <p align="center">
  <img src="https://github.com/piotrwalas1/Gemini-Benchmark-Framework/blob/main/benchmark_visuals.png" width="600" title="raport1">
</p>
*Rys 1. Po lewej: Profil kompetencji (Radar Chart). Po prawej: Porównanie szybkości odpowiedzi (Bar Chart).*

## 🧠 Kluczowe Wnioski (Insights)

* **Dominacja Efektywności Flasha:** Gemini 2.0 Flash osiąga wyniki jakościowe na poziomie modelu Pro (różnice rzędu 1%), będąc przy tym **~23 razy tańszym** i **~6 razy szybszym**. Jest to bezdyskusyjny lider dla systemów real-time.
* **Pro jako Dyplomata:** Model Pro oferuje wyższą jakość w kategoriach *Tone* i *Safety* przy niskiej temperaturze, jednak traci te przewagi przy wzroście kreatywności.
* **Stabilność Operacyjna:** Flash wykazuje niemal zerową wrażliwość kosztową i czasową na zmianę temperatury, podczas gdy Pro staje się bardziej kosztowny przy $T=1.0$.

## ⚠️ Analiza Wrażliwości i Regresji (Crucial Discovery)

Najważniejszym odkryciem benchmarku jest drastyczny spadek stabilności modelu **Gemini 2.5 Pro** w specyficznych kategoriach przy wzroście temperatury do $T=1.0$.

| Kategoria | Wynik (T=0.1) | Wynik (T=1.0) | Regresja (Delta) |
| :--- | :---: | :---: | :---: |
| **Code / Safety** | 5.00 | 0.00 | **-5.00** |
| **Complex Logic** | 4.67 | 2.17 | **-2.50** |

**Wniosek:** Dla zadań wymagających ścisłego rygoru (Logika, Kod, SQL), model Pro **musi** pracować na niskiej temperaturze ($T=0.1$). Przy $T=1.0$ model całkowicie traci kontrolę nad rygorem logicznym i restrykcjami bezpieczeństwa.

## 🛠️ Stos Narzędziowy (Core Toolbox)

W repozytorium znajdują się kluczowe skrypty automatyzujące proces:
* **`main_tester_all.py`**: Rdzeń systemu. Odpowiada za iterację po `test_cases.json`, wysyłanie zapytań do modeli i przekazywanie danych do Sędziego.
* **`compare_models.py`**: Narzędzie do analizy regresji. Generuje raporty `.csv` i wylicza deltę (różnicę) wyników między wariantami.
* **`generate_visualizations.py`**: Master Visualizer. Tworzy zbiorcze grafiki (Radar + Bar Chart) prezentujące profil kompetencji i wydajność.
* **`final_mega_benchmark.py`**: Agregator danych. Generuje finalną tabelę wydajnościową (Score/Latency/Cost) do dokumentacji.

## 🚀 Jak uruchomić?

1.  Sklonuj repozytorium.
2.  Przygotuj plik `test_cases.json` ze swoimi pytaniami.
3.  Zainstaluj wymagania: `pip install pandas matplotlib numpy tabulate`.
4.  Skonfiguruj plik `.env` (API Keys dla Gemini i Judge).
5.  Uruchom analizę: `python main_tester_all.py` -> `python generate_visualizations.py`.
