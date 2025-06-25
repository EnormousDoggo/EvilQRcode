import ansible_runner
import uuid
import os

RESULTS_DIR = "results"
PLAYBOOK_DIR = "/root/containers/EvilQRcode/QRTool/SandBoxGenerator/tests/playbook_tests.yml"
INVENTORY_DIR = "/root/containers/EvilQRcode/QRTool/SandBoxGenerator/tests/inventory"
os.makedirs(RESULTS_DIR, exist_ok=True)

def create_sandbox(url):
    id_container = f"sandbox_{uuid.uuid4().hex[:8]}"
    result = ansible_runner.run(
        private_data_dir='.',
        playbook=PLAYBOOK_DIR,
        inventory=INVENTORY_DIR,
        tags='creation_sandbox,scan',
        extravars={
            'url_a_tester': url,
            'id_container': id_container
        }
    )

    # Récupère le résultat du scan
    result_file = os.path.join(RESULTS_DIR, f"{id_container}.txt")
    with open(result_file, "w", encoding="utf-8") as f:
        for event in result.events:
            if event.get('event') == 'runner_on_ok':
                task = event['event_data']['task']
                if task == 'Show analysis results':
                    msg = event['event_data']['res']['msg']
                    f.write(f"✔ Résultat du scan {url} (container: {id_container}):\n{msg}\n")
                    break

    return id_container

def display_result(id_container):
    result_file = os.path.join(RESULTS_DIR, f"{id_container}.txt")
    if os.path.exists(result_file):
        with open(result_file, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return f"Aucun résultat trouvé pour le container {id_container}."

def kill_sandbox(id_container):
    ansible_runner.run(
        private_data_dir='.',
        playbook=PLAYBOOK_DIR,
        inventory=INVENTORY_DIR,
        tags='clean',
        extravars={'id_container': id_container}
    )

if __name__ == '__main__':
    create_sandbox("pwnedme.com/")