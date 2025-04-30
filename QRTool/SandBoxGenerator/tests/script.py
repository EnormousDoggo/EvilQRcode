import ansible_runner

def run_playbook(playbook_path, inventory_path=None, extravars=None):
    result = ansible_runner.run(
        private_data_dir='.',
        playbook=playbook_path,
        inventory=inventory_path,
        extravars=extravars
    )

    print("Statut de l'exécution :", result.status)  # "successful", "failed", etc.
    print("Code de retour :", result.rc)
    for event in result.events:
        print(event['event'], event.get('stdout', ''))

# Exemple d'utilisation
run_playbook(
    playbook_path='/home/gitlab-runner/workspace-ansible/qr-code/tests/playbook_tests.yml',
    inventory_path='/home/gitlab-runner/workspace-ansible/qr-code/tests/inventory',
    extravars={'url_a_tester': 'https://www.google.com/'}
)
