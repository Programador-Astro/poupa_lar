# utils/email_utils.py
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email_verificacao(destinatario, codigo):
    email_origem = "programadordavisf@gmail.com"
    senha = "vsag tvkt popy yknu"

    assunto = "Código de Verificação - PoupaLar"
    corpo = f"""
    <html>
        <body>
            <h2>Bem-vindo ao PoupaLar!</h2>
            <p>Seu código de verificação é:</p>
            <h1>{codigo}</h1>
            <p>Insira esse código no app para confirmar seu e-mail.</p>
        </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = assunto
    msg["From"] = email_origem
    msg["To"] = destinatario
    parte_html = MIMEText(corpo, "html")
    msg.attach(parte_html)

    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as servidor:
        servidor.login(email_origem, senha)
        servidor.sendmail(email_origem, destinatario, msg.as_string())
        print("E-mail enviado com sucesso!")