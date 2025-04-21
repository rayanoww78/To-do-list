import threading
import AI
import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
import psycopg2

# Connexion PostgreSQL
params = {
    'user': 'postgres',
    'password': 'RAYANDU98',
    'host': 'localhost',
    'port': 5432,
}
conn = psycopg2.connect(**params)
cursor = conn.cursor()
cursor.execute('SET search_path TO todolist;')

# Variable globale pour l'utilisateur connecté

utilisateur_connecte_id = 0
# --- Interface principale ---
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("📝 To-Do List")
app.geometry("600x600")
app.protocol("WM_DELETE_WINDOW", lambda: quitter_application())
app.withdraw()

# --- Fonctions ---
def connexion():
    global utilisateur_connecte_id
    username = entry_user.get().strip()
    password = entry_pass.get().strip()
    if username == "" or password == "":
        messagebox.showwarning("Champ vide", "Vous avez oublié de mettre votre nom d'utilisateur ou votre mot de passe !")
        return
    cursor.execute("SELECT id_user FROM personne WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    print(user)
    if user is None:
        messagebox.showwarning("Mauvais identifiants", "Nom d'utilisateur ou mot de passe incorrect !")
    else:
        utilisateur_connecte_id = user[0]
        messagebox.showinfo("Connexion réussie", f"Bienvenue {username} !")
        login_window.destroy()
        app.deiconify()
        afficher_taches()

def inscription():
    username = entry_user.get().strip()
    mdp = entry_pass.get().strip()
    if username == "" or mdp == "":
        messagebox.showwarning("Champ vide", "Veuillez remplir tous les champs.")
        return
    cursor.execute("SELECT * FROM personne WHERE username = %s", (username,))
    lst = cursor.fetchall()
    for row in lst:
        if row[0] == username:
            messagebox.showwarning("Problème utilisateur","Veuillez choisir un autre nom d'utilisateur")
            return
        if row[1] == mdp:
            messagebox.showwarning("Problème mot de passe","Veuillez choisir un autre mot de passe ")
            return
    if cursor.fetchone():
        messagebox.showwarning("Erreur", "Ce nom d'utilisateur existe déjà.")
    else:
        cursor.execute("INSERT INTO personne(username, password) VALUES (%s, %s)", (username, mdp))
        conn.commit()
        messagebox.showinfo("Inscription réussie", "Compte créé avec succès !")

def afficher_taches(filtre=""):
    for widget in scroll_frame.winfo_children():
        widget.destroy()

    if filtre:
        cursor.execute("SELECT * FROM todo WHERE id_user = %s AND LOWER(tache) LIKE %s ORDER BY id", (utilisateur_connecte_id, f"%{filtre.lower()}%"))
    else:
        cursor.execute("SELECT * FROM todo WHERE id_user = %s ORDER BY id", (utilisateur_connecte_id,))
    taches = cursor.fetchall()

    for id, texte, terminee,id_u in taches:
        ligne = ctk.CTkFrame(scroll_frame)
        ligne.pack(fill="x", pady=2, padx=5)

        var = ctk.StringVar(value="on" if terminee else "off")
        case = ctk.CTkCheckBox(
            ligne,
            text=texte,
            variable=var,
            onvalue="on",
            offvalue="off",
            command=lambda v=var, i=id: marquer_tache(i, v),
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color="green" if terminee else "#1f2937"
        )
        case.pack(side="left", padx=10, pady=2, anchor="w")

        btn_sup = ctk.CTkButton(
            ligne, text="🗑", width=30, fg_color="red",
            command=lambda i=id: supprimer_tache(i)
        )
        btn_sup.pack(side="right", padx=3)

        btn_AI = ctk.CTkButton(ligne, text = "IA suggestion", width=20, fg_color="blue", command=lambda i=id: IAReponse(i))
        btn_AI.pack(side="right", padx=4)

def ajouter_tache():
    texte = entry.get().strip()
    if texte == "":
        messagebox.showwarning("Champ vide", "Tu dois écrire une tâche !")
        return
    cursor.execute("INSERT INTO todo (tache, id_user) VALUES (%s, %s)", (texte, utilisateur_connecte_id,))
    conn.commit()
    entry.delete(0, ctk.END)
    afficher_taches()

def supprimer_tache(id):
    cursor.execute("DELETE FROM todo WHERE id = %s AND id_user = %s", (id, utilisateur_connecte_id))
    conn.commit()
    afficher_taches()

def marquer_tache(id, variable):
    terminee = variable.get() == "on"
    cursor.execute("UPDATE todo SET terminee = %s WHERE id = %s AND id_user = %s", (terminee, id, utilisateur_connecte_id))
    conn.commit()
    afficher_taches()

def IAReponse(id):
    cursor.execute("SELECT tache FROM todo WHERE id = (%s)",(id,))
    tache = cursor.fetchone()
    messagebox.showinfo("Suggestion de l'IA",AI.repondre(tache[0]))
    conn.commit()
    afficher_taches()

def lancer_recherche():
    filtre = champ_recherche.get().strip()
    afficher_taches(filtre)

def reinitialiser_recherche():
    champ_recherche.delete(0, ctk.END)
    afficher_taches()

def quitter_application():
    if messagebox.askokcancel("Quitter", "Tu es sûr de vouloir quitter ?"):
        messagebox.showinfo("À bientôt 👋", "Merci d’avoir utilisé la To-Do List 💼\n Created by RAYAN EL AMJAD")
        app.destroy()

def quitter_connexion():
    if messagebox.askokcancel("Quitter", "Tu es sûr de vouloir quitter ?"):
        messagebox.showinfo("À bientôt 👋", "Merci d’avoir utilisé la To-Do List 💼\n Created by RAYAN EL AMJAD")
        login_window.destroy()

# --- Fenêtre de login ---
login_window = ctk.CTk()
login_window.title("Connexion")
login_window.geometry("500x400")
login_window.protocol("WM_DELETE_WINDOW", quitter_connexion)

frame_login = ctk.CTkFrame(login_window, corner_radius=10)
frame_login.pack(padx=20, pady=30)

ctk.CTkLabel(frame_login, text="Nom d'utilisateur :", font=ctk.CTkFont(size=14), text_color="#1f2937").pack(pady=5)
entry_user = ctk.CTkEntry(frame_login, text_color="#1f2937")
entry_user.pack(pady=5)

ctk.CTkLabel(frame_login, text="Mot de passe :", font=ctk.CTkFont(size=14), text_color="#1f2937").pack(pady=5)
entry_pass = ctk.CTkEntry(frame_login, show="*", text_color="#1f2937")
entry_pass.pack(pady=5)

btn_login = ctk.CTkButton(frame_login, text="Se connecter", command=connexion, text_color="white")
btn_login.pack(pady=10)

btn_signup = ctk.CTkButton(frame_login, text="S'inscrire", command=inscription, text_color="white")
btn_signup.pack(pady=5)

# --- Widgets app principale ---
label = ctk.CTkLabel(app, text="📝 Ma To-Do List", font=ctk.CTkFont(size=22, weight="bold"), text_color="#1f2937")
label.pack(pady=15)

entry = ctk.CTkEntry(app, width=400, placeholder_text="Nouvelle tâche", text_color="#1f2937")
entry.pack(pady=5)

btn_ajouter = ctk.CTkButton(app, text="➕ Ajouter une tâche", command=ajouter_tache, text_color="white")
btn_ajouter.pack(pady=5)

recherche_frame = ctk.CTkFrame(app)
recherche_frame.pack(pady=10)

champ_recherche = ctk.CTkEntry(recherche_frame, width=300, placeholder_text="Rechercher une tâche...", text_color="#1f2937")
champ_recherche.pack(side="left", padx=5)

btn_rechercher = ctk.CTkButton(recherche_frame, text="🔍 Rechercher", command=lancer_recherche, text_color="white")
btn_rechercher.pack(side="left", padx=5)

btn_reset = ctk.CTkButton(recherche_frame, text="🔁 Tout afficher", command=reinitialiser_recherche, text_color="white")
btn_reset.pack(side="left", padx=5)

scroll_frame = ctk.CTkScrollableFrame(app, width=500, height=300)
scroll_frame.pack(pady=10)

login_window.mainloop()
app.mainloop()