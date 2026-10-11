# 🚪 Extel Umii pour Home Assistant

Basé sur l'excellent travail de [Jason Pretavoine](https://github.com/jasonpretavoine)  
Repository original: [https://github.com/jasonpretavoine/Extel-HomeAssistant](https://github.com/jasonpretavoine/Extel-HomeAssistant)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Cette intégration personnalisée permet de piloter les portails motorisés des marques **Extel** et **Avidsen** utilisant l'application **Umii** directement depuis Home Assistant.

---

## ✨ Caractéristiques

* **Contrôle Complet** : Ouverture, Fermeture et Arrêt (Stop).
* **Ouverture Piéton** : Un bouton dédié pour l'ouverture partielle (`HALF-OPEN`).
* **Retour d'État** : Suivi en temps réel de l'état du portail (Ouvert/Fermé).
* **Multi-Appareils** : Détection et installation automatique de tous les portails liés à votre compte.

---

## ⚠️ Avertissement

> [!IMPORTANT]
> Cette intégration est un projet communautaire **non-officiel**. Elle n'est ni affiliée, ni approuvée par **Extel** ou **Avidsen**. L'utilisation de cette intégration se fait à vos propres risques et périls.
> Pour fonctionner, il est maintenant recommandé d'utiliser le **deviceId** généré par l'application mobile.  
>De plus, le **UserAgent** attendu par **Umii** possède une version.  
>Il faut donc récupérer ces 2 informations en examinant les trames envoyées par l'application iOS ou Android (voir explications plus bas).  

---

## 🚀 Installation

### Méthode 1 : HACS (Recommandé)

1.  Assurez-vous que [HACS](https://hacs.xyz/) est installé.
2.  Allez dans **HACS** > **Intégrations**.
3.  Cliquez sur les **3 points** en haut à droite et choisissez **Dépôts personnalisés**.
4.  Collez l'URL de ce dépôt : `https://github.com/Yohan-Janolin/HA-Integration_Extel-Umii-Portal`.
5.  Sélectionnez la catégorie **Intégration** et cliquez sur **Ajouter**.
6.  Cherchez **Extel Umii** dans la liste et cliquez sur **Télécharger**.
7.  **Redémarrez Home Assistant**.

### Méthode 2 : Manuelle

1.  Téléchargez le dossier `custom_components/extel_umii`.
2.  Copiez-le dans le dossier `custom_components` de votre installation Home Assistant.
3.  **Redémarrez Home Assistant**.

---

## ⚙️ Configuration

1.  Allez dans **Paramètres** > **Appareils et services**.
2.  Cliquez sur **Ajouter une intégration** en bas à droite.
3.  Recherchez **Extel Portail**.
4.  Entrez vos identifiants Umii (Email, Mot de passe).
5.  Suivez la procédure ci-dessous pour obtenir votre deviceToken et l'UA

>     Sur iOS (iPhone)
>
>    La méthode la plus simple est d'utiliser l'application Proxyman pour iOS (disponible sur l'App Store, gratuite) .
>
>    1. Préparation de Proxyman
>
>        Installez Proxyman – Capture HTTPS depuis l'App Store.  
>        Ouvrez l'application et activez l'interception. iOS vous demandera d'autoriser une configuration VPN – acceptez.  
>        Suivez les instructions dans l'app pour télécharger et installer le certificat Proxyman (via Safari sur http://proxy.man/ssl).  
>        Étape cruciale : Allez dans **Réglages** → **Général** → **À propos** → **Réglages de confiance des certificats** et activez le switch pour le certificat Proxyman .  
>        Sans cette étape, le HTTPS ne sera pas déchiffré.  
>
>    2. Capture de la requête
>
>       Dans Proxyman, lancez la capture.  
>       Fermez complètement l'application Umii (pas juste la mettre en arrière-plan), puis rouvrez-la.  
>       Déconnectez-vous puis reconnectez-vous dans Umii pour forcer une nouvelle requête de login.  
>       Dans Proxyman, cherchez la requête POST https://umii.avidsen.one/services/dain/login.  
>   
>    3. Extraction des valeurs
>
>       User-Agent (UA) : Dans les Headers de cette requête, copiez la valeur complète du champ User-Agent. Elle ressemble à : Umii/106 CFNetwork/3896.100.1.2.1 Darwin/27.0.0.  
>       Device Token : Dans le Body de cette même requête, copiez la valeur du champ deviceToken. C'est une longue chaîne de caractères (souvent commençant par des lettres et >des  chiffres, incluant un :).  
>       ⚠️ Important : N'oubliez pas de désactiver le VPN Proxyman et de supprimer le certificat une fois vos tests terminés, pour éviter tout risque de sécurité .  


>    📱 Sur Android
>   
>    **A VENIR -- PAS D'APPAREIL ANDROID SOUS LA MAIN** 

5.  Sélectionnez votre portail dans la liste proposée.

---

## 🛠️ Entités créées

| Nom de l'entité | Type | Description |
| :--- | :--- | :--- |
| `cover.portail_jardin` | **Cover** | Contrôle principal : Ouverture, Fermeture et Arrêt (Stop). |
| `button.ouverture_pieton` | **Button** | Déclenche l'ouverture partielle (HALF-OPEN) du portail. |


---

## 🤝 Contribution

Si vous souhaitez améliorer cette intégration ou signaler un bug :
1.  Ouvrez une **Issue** pour signaler un problème.
2.  Soumettez une **Pull Request** pour proposer des changements.

---

## 📄 Licence

Ce projet est distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
