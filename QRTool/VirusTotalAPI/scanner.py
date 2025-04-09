import sys
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("VT_API_KEY")
if not API_KEY:
    raise ValueError("Clé API manquante.")

def scan_url(url):
    headers = {"x-apikey": API_KEY}
    data = {"url": url}

    # Envoi de l'URL à scanner
    response = requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data=data)
    if response.status_code != 200:
        print("Erreur lors de l'envoi :", response.text)
        sys.exit(1) 
    analysis_id = response.json()["data"]["id"]

    # Attente pour récupérer le rapport
    report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    timeout = 60  # Temps maximum d'attente en secondes
    elapsed_time = 0  # Temps écoulé

    while elapsed_time < timeout:
        report_response = requests.get(report_url, headers=headers)
        report = report_response.json()

        # Vérifie si l'analyse est terminée
        status = report["data"]["attributes"]["status"]
        if status == "completed":
            break

        print(f"Analyse en cours, attente de 15 secondes...")
        time.sleep(15)
        elapsed_time += 15

    if elapsed_time >= timeout:
        print("Temps d'attente dépassé. L'analyse n'est pas terminée.")
        sys.exit(1)

    # Affichage simplifié du rapport
    stats = report["data"]["attributes"]["stats"]
    print(f"URL : {url}")
    print(f"Détections : {stats['malicious']} malveillants, {stats['harmless']} inoffensifs")
    return stats

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python scanner.py <url>")
        sys.exit(1)

    scan_url(sys.argv[1])