import sys
import requests
import time

API_KEY = "23e405c979a19e2efec0afb25836226ade27e88b6ab1523fb2459960fca1a294"  # Remplace par ta vraie clé

def scan_url(url):
    headers = {"x-apikey": API_KEY}
    data = {"url": url}

    # Envoi de l'URL à scanner
    response = requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data=data)
    if response.status_code != 200:
        print("Erreur lors de l'envoi :", response.text)
        sys.exit(1)

    analysis_id = response.json()["data"]["id"]

    # Attente avant de récupérer le rapport
    time.sleep(10)

    # Récupération du rapport
    report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    report_response = requests.get(report_url, headers=headers)
    report = report_response.json()

    # Affichage simplifié du rapport
    stats = report["data"]["attributes"]["stats"]
    print(f"URL : {url}")
    print(f"Détections : {stats['malicious']} malveillants, {stats['harmless']} inoffensifs")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python scanner.py <url>")
        sys.exit(1)

    scan_url(sys.argv[1])