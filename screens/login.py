from kivymd.uix.screen import MDScreen 
from kivymd.uix.button import MDRaisedButton  
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.clock import Clock

from database.connection import db
from database.models import Usuario

KV = '''
<LoginScreen>:
    name: "login"
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(20)
        padding: dp(40)
        md_bg_color: 1, 1, 1, 1

        MDLabel:
            text: "PoupaLar"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color

        MDTextField:
            id: email
            hint_text: "E-mail"
            icon_right: "email"
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}
            mode: "rectangle"

        MDTextField:
            id: senha
            hint_text: "Senha"
            icon_right: "lock"
            password: True
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}
            mode: "rectangle"
        
        MDRaisedButton:
            text: "Entrar"
            md_bg_color: app.theme_cls.primary_color
            text_color: 1, 1, 1, 1
            pos_hint: {"center_x": 0.5}
            on_release: root.login()

        MDTextButton:
            text: "Não tem uma conta? Cadastre-se"
            pos_hint: {"center_x": 0.5}
            on_release: root.manager.current = "cadastro"
'''

Builder.load_string(KV)

class LoginScreen(MDScreen):
    def login(self):
        email = self.ids.email.text
        senha = self.ids.senha.text
        usuario = db.query(Usuario).filter_by(email=email).first()
        
        if usuario and usuario.senha_hash == senha:
            if usuario.email_confirmado == False:
                self.manager.current = 'verificacao'
                return
            self.manager.current = "home"
            Clock.schedule_once(self.mostrar_boas_vindas, 0.5)
        else:
            self.show_error("E-mail ou senha incorretos")

    def show_error(self, mensagem):
        MDDialog(
            title="Erro de login",
            text=mensagem,
            buttons=[],
        ).open()

    def mostrar_boas_vindas(self, *args):
        dialog = MDDialog(
            title="Bem-vindo ao PoupaLar! 🏡",
            text=(
                "Olá!\n\n"
                "Aqui estão algumas dicas rápidas:\n"
                "• Cadastre os produtos que você tem em casa 🧼\n"
                "• Defina o estoque mínimo para receber alertas 📦\n"
                "• Compare preços dos mercados e economize 💰\n\n"
                "Aproveite o app!"
            ),
            buttons=[
                MDRaisedButton(
                    text="Começar",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()