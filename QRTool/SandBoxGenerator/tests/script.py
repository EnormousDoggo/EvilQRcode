import ansible_runner

globalPrivate_data_dir='.'
globalPlaybook='/root/docker/EvilQRcode/QRTool/SandBoxGenerator/tests/playbook_tests.yml'
globalInventory='/root/docker/EvilQRcode/QRTool/SandBoxGenerator/tests/inventory'

def create_sandbox(url):
    return ansible_runner.run(
        private_data_dir=globalPrivate_data_dir,
        playbook=globalPlaybook,
        inventory=globalInventory,
        tags='creation_sandbox,scan',
        extravars={'url_a_tester': 'https://www.google.com/'}
        )

def display_result(result):
    # Récupère et affiche le résultat du scan
    for event in result.events:
        if event.get('event') == 'runner_on_ok':
            task = event['event_data']['task']
            if task == 'Show analysis results':
                print("✔ Résultat du scan :")
                print(event['event_data']['res']['msg'])

def kill_sandbox():
    ansible_runner.run(
        private_data_dir=globalPrivate_data_dir,
        playbook=globalPlaybook,
        inventory=globalInventory,
        tags='cleaning'
        )
    return 0


if __name__ == "__main__":
    url = "https://www.google.com/"
    result = create_sandbox(url)
    display_result(result)
    kill_sandbox()

