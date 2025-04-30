import ansible_runner

# Étape 1 : Exécute uniquement les tâches de scan
result = ansible_runner.run(
    private_data_dir='.',
    playbook='/home/gitlab-runner/workspace-ansible/qr-code/tests/playbook_tests.yml',
    inventory='/home/gitlab-runner/workspace-ansible/qr-code/tests/inventory',
    tags='creation_sandbox,scan',
    extravars={'url_a_tester': 'https://www.google.com/'}
)

# Récupère et affiche le résultat du scan
for event in result.events:
    if event.get('event') == 'runner_on_ok':
        task = event['event_data']['task']
        if task == 'Show analysis results':
            print("✔ Résultat du scan :")
            print(event['event_data']['res']['msg'])

# Étape 2 : Exécute ensuite le nettoyage
ansible_runner.run(
    private_data_dir='.',
    playbook='/home/gitlab-runner/workspace-ansible/qr-code/tests/playbook_tests.yml',
    inventory='/home/gitlab-runner/workspace-ansible/qr-code/tests/inventory',
    tags='cleaning'
)
