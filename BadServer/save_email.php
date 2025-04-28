<?php
if (isset($_POST['email'])) {
    $email = filter_var($_POST['email'], FILTER_SANITIZE_EMAIL); // Nettoyage du champ
    if (filter_var($email, FILTER_VALIDATE_EMAIL)) { // Vérifie si l'email est valide
        file_put_contents('emails.txt', $email . PHP_EOL, FILE_APPEND | LOCK_EX);
        echo "Merci pour votre inscription !";
    } else {
        echo "Email invalide.";
    }
} else {
    echo "Aucun email reçu.";
}
?>