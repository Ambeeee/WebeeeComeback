from email.message import EmailMessage
import smtplib
import ssl

em = EmailMessage()
ssl_context = ssl.create_default_context()

padrone = "alessandro.minestrini.01@gmail.com"
Python_google_2fa = "ncrxhaohumrtrvln"

subject = {"sign up": "Benvenuto su Webeee!", "sign in": "Accesso a Webeee effettuato"}




def send_confirm(user, email, mode="sign up"):
    body = {
        "sign up": f"""
        Ciao {user}, ti diamo il benvenuto!
        Ora che sei parte dello staff, avrai dei vantaggi incredibili potendo partecipare attivamente
        alla crescita di questo sito e della sua fantastica community!

        Per effettuare il login clicca qui: https://webeee.herokuapp.com/login
        e usa questa password provvisoria: Cambiami!01 , che potrai cambiare nella tua area personale
        webeee.herokuapp.com/users/{user}
        Se hai bisogno di altro aiuto, non esitare a chiedere. Ci vediamo in rete!
        """,
        "sign in": f"""
        Ciao {user}, bentornato!
        La tua area personale: webeee.herokuapp.com/users/{user}
        """
    }
    
    em["From"] = padrone
    em["To"] = email
    em["subject"] = subject[mode]
    em.set_content(body[mode])

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context) as s:
        s.login(padrone, Python_google_2fa)
        s.sendmail(padrone, email, em.as_string())


