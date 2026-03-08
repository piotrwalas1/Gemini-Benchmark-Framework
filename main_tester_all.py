import json
import datetime
import os
import time
import vertexai
from vertexai.generative_models import GenerativeModel
from groq import Groq
from dotenv import load_dotenv


load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", "twój-project-id") 
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Ustawienia modeli i stawek (ceny za 1M tokenów w USD - przykładowe dla Gemini )
PRICING = {
    "models/gemini-2.0-flash": {"input": 0.10, "output": 0.40},
    "models/gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    "models/gemini-2.5-pro": {"input": 1.25, "output": 5.00} # orientacyjnie wartosci
}

MODEL_NAME = "models/gemini-2.5-pro"
TEMPERATURE = 0.1 
SLEEP_TIME = 10.0 

def call_vertex_gemini(prompt, temperature):
    """Zwraca pełny obiekt odpowiedzi, aby mieć dostęp do usage_metadata."""
    model = GenerativeModel(MODEL_NAME)
    response = model.generate_content(
        prompt, 
        generation_config={"temperature": temperature}
    )
    return response

def get_judge_score_extended(response_to_eval, prompt):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    judge_prompt = (
        f"Oceń odpowiedź modelu w skali 1-5 dla każdej z 6 kategorii: "
        f"Fidelity, Relevance, Accuracy, Safety, Tone, Context. "
        f"Zwróć wynik wyłącznie w formacie JSON: "
        f"{{\"scores\": {{\"Fidelity\": 0, \"Relevance\": 0, \"Accuracy\": 0, \"Safety\": 0, \"Tone\": 0, \"Context\": 0}}}}"
        f"\n\nPrompt użytkownika: {prompt}\n\nOdpowiedź modelu: {response_to_eval}"
    )
    
    raw = client.chat.completions.create(
        messages=[{"role": "user", "content": judge_prompt}],
        model="llama-3.3-70b-versatile",
        temperature=0.0,
        response_format={"type": "json_object"}
    )
    return json.loads(raw.choices[0].message.content)

def run_benchmark():
    with open("test_cases.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    print(f"--- START BENCHMARK ---")
    print(f"Model: {MODEL_NAME} | Temp: {TEMPERATURE}")
    
    total_cost = 0.0

    for i, item in enumerate(data, 1):
        prompt = item.get("prompt", item)
        category = item.get("category", "General")
        
        # Pomiar czasu (Latency)
        start_time = time.perf_counter()
        response_obj = call_vertex_gemini(prompt, TEMPERATURE)
        end_time = time.perf_counter()
        
        latency = end_time - start_time
        
        # Wyciąganie tekstu i tokenów
        response_text = response_obj.text
        usage = response_obj.usage_metadata
        input_tokens = usage.prompt_token_count
        output_tokens = usage.candidates_token_count
        
        # Obliczanie kosztu dla bieżącego zapytania
        model_pricing = PRICING.get(MODEL_NAME, {"input": 0, "output": 0})
        cost = (input_tokens * model_pricing["input"] / 1_000_000) + \
               (output_tokens * model_pricing["output"] / 1_000_000)
        total_cost += cost

        print(f"[{i}/{len(data)}] {category} | Latency: {latency:.2f}s | Tokens: {input_tokens+output_tokens}")
        
        try:
            scores_data = get_judge_score_extended(response_text, prompt)
            scores = scores_data.get("scores", scores_data)
            
            results.append({
                "category": category,
                "scores": scores,
                "metrics": {
                    "latency": latency,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "cost_usd": cost
                }
            })
        except Exception as e:
            print(f"Błąd sędziego: {e}")
        
        time.sleep(SLEEP_TIME)


    timestamp = datetime.datetime.now().strftime("%m%d-%H%M")
    filename = f"results-{MODEL_NAME.replace('/', '-')}-{TEMPERATURE}-{timestamp}.json"
    
    output_data = {
        "metadata": {
            "model": MODEL_NAME,
            "temperature": TEMPERATURE,
            "total_queries": len(data),
            "total_estimated_cost_usd": total_cost,
            "avg_latency": sum(r['metrics']['latency'] for r in results) / len(results) if results else 0
        },
        "results": results
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
    
    print(f"\n--- TEST ZAKOŃCZONY ---")
    print(f"Raport: {filename}")
    print(f"Całkowity koszt przybliżony: ${total_cost:.5f}")

if __name__ == "__main__":
    run_benchmark()