import json
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTION = """Sei un assistente che analizza partite di calcio GIÀ GIOCATE.
Ricevi una domanda dell'utente e un elenco di partite in formato JSON.

Regole:
- Usa i dati presenti nel JSON, se non trovi qualcosa cerca sul web..
- Se un dato richiesto non è presente, cercalo sul web invece di inventarlo.
- Rispondi in italiano, in modo diretto e sintetico.
- Non menzionare il JSON nelle risposte all'utente.
- NON USARE "*".
- Sii gentile con l'utente.
- Puoi anche fare ricerche sul web per controllare che i dati siano corretti.
Struttura di ogni partita nel JSON:
- "home_team" / "away_team": squadre (casa/trasferta)
- "match_date": data della partita (già disputata)
- "home_goals" / "away_goals": gol segnati, risultato finale
- "matchday": giornata di campionato
- "season": stagione
"""


MAX_RETRIES = 3


def process_chat(question: str, matches: list[dict]) -> str:  #type:ignore
    if not matches:
        return "Non ci sono partite disponibili con i filtri selezionati."

    matches_json = json.dumps(matches, indent=2, ensure_ascii=False)

    prompt = f"""
Domanda: {question}

Sono state trovate {len(matches)} partite.

JSON dei match:
{matches_json}
"""

    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.2,
                    # tools=[types.Tool(google_search=types.GoogleSearch())],
                ),
            )
            return response.text
        except errors.ServerError:
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(2 ** attempt)