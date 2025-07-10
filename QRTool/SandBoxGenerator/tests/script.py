import ansible_runner
import uuid
import os

RESULTS_DIR = "results"
PLAYBOOK_DIR = "/root/containers/EvilQRcode/QRTool/SandBoxGenerator/tests/playbook_tests.yml"
INVENTORY_DIR = "/root/containers/EvilQRcode/QRTool/SandBoxGenerator/tests/inventory"
os.makedirs(RESULTS_DIR, exist_ok=True)

async def create_sandbox(url):
    id_container = f"sandbox_{uuid.uuid4().hex[:8]}"
    await ansible_runner.run(
        private_data_dir='.',
        playbook=PLAYBOOK_DIR,
        inventory=INVENTORY_DIR,
        tags='creation_sandbox,scan',
        extravars={
            'url_a_tester': url,
            'id_container': id_container
        }
    )

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