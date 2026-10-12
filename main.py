from flask import Flask, request
import requests

app = Flask(__name__)

CLIENT_ID = "1542165228765323385"
CLIENT_SECRET = "chN5xAeMqICo2S21hBnWSS38Gthc9Hqj"
REDIRECT_URI = "https://verif-discord-1.onrender.com/callback"
WEBHOOK_URL = "https://discord.com/api/webhooks/1559330325631471736/b9wQSa_sZbnWj2yHhVETwWpdqGkAbHUz5_ruTdDdu61DMG1REygNEs4c1MR4cN2gWp_4"

@app.route("/")
def home():
    return "Serveur de vérification en ligne"

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Erreur : pas de code"

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_res = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    token_json = token_res.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return "Erreur token"

    user_res = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user = user_res.json()

    embed = {
        "embeds": [{
            "title": "Nouvelle vérification",
            "color": 0x5865F2,
            "fields": [
                {"name": "Pseudo", "value": user.get("username", "Inconnu"), "inline": True},
                {"name": "ID", "value": str(user.get("id", "???")), "inline": True},
                {"name": "Email", "value": user.get("email", "Non fourni"), "inline": False},
                {"name": "Vérifié", "value": "Oui" if user.get("verified") else "Non", "inline": True}
            ]
        }]
    }
    requests.post(WEBHOOK_URL, json=embed)

    return "<h2>Vérification réussie ✅</h2><p>Tu peux fermer cette page.</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
