# Marche Adeps 2026 — RCTT Thuin

Site statique pour la Marche Adeps du dimanche 2 août 2026, organisée par le RCTT Thuin ASBL.
Présente les parcours proposés (carte, profil d'altitude, descriptif) avec téléchargement du GPX correspondant.

## Structure

- `index.html` — page principale
- `css/style.css` — styles
- `img/` — affiche, cartes et profils d'altitude (générés via Openrunner)
- `gpx/` — traces GPX téléchargeables
- `js/lightbox.js` — zoom plein écran au clic sur les cartes/profils

## Déploiement (Render)

Ce repo (`marche-adeps-2026`) contient un `render.yaml` (Blueprint) qui déclare un site statique
(`marche-adeps-2026`).

1. Pousser ce repo sur GitHub.
2. Sur [render.com](https://dashboard.render.com), **New > Blueprint**, sélectionner ce repo.
3. Render détecte `render.yaml` et crée le service statique automatiquement.
4. L'URL publique sera `https://marche-adeps-2026.onrender.com` (ou un nom disponible proche si celui-ci est déjà pris).

Le QR code dans `img/qr-code.png` pointe vers cette URL — à régénérer si le nom du service change
(remplacer l'URL encodée dans la requête vers `api.qrserver.com` et retélécharger l'image).
