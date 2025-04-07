from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from database.models import Usuario
KV = '''
<CadastroScreen>:
    name: "cadastro"

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(20)
        padding: dp(40)
        md_bg_color: 1, 1, 1, 1

        MDLabel:
            text: "Crie sua conta"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color

        MDTextField:
            id: nome
            hint_text: "Nome"
            icon_right: "account"
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}
            mode: "rectangle"

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
            password: True
            icon_right: "lock"
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}
            mode: "rectangle"
        MDTextField:
            id: confirmar_senha
            hint_text: "Confirmar Senha"
            icon_right: "lock"
            password: True
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}
            mode: "rectangle"
        MDRaisedButton:
            text: "Cadastrar"
            md_bg_color: app.theme_cls.primary_color
            text_color: 1, 1, 1, 1
            pos_hint: {"center_x": 0.5}
            on_release: root.cadastrar()

        MDRaisedButton:
            text: "Voltar ao login"
            md_bg_color: 1, 1, 1, 1
            text_color: app.theme_cls.primary_color
            pos_hint: {"center_x": 0.5}
            on_release: root.manager.current = "login"
'''

Builder.load_string(KV)

class CadastroScreen(MDScreen):
    def cadastrar(self):
        nome = self.ids.nome.text
        email = self.ids.email.text
        senha = self.ids.senha.text
        confirmar_senha = self.ids.confirmar_senha.text

        
        if not nome or not email or not senha or not confirmar_senha:
            self.show_dialog("Preencha todos os campos.")
        else:
            # Aqui você pode conectar ao banco de dados

            
            self.show_dialog("Usuário cadastrado com sucesso!")
            self.manager.current = "login"

    def show_dialog(self, mensagem):
        dialog = MDDialog(
            title="Cadastro",
            text=mensagem,
            buttons=[],
        )
        dialog.open()