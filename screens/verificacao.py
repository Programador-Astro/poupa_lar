from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from kivy.lang import Builder
from database.connection import db
from database.models import Usuario

verificacao_kv = """
<VerificacaoScreen>:
    name: "verificacao"

    MDBoxLayout:
        orientation: "vertical"
        padding: dp(30)
        spacing: dp(20)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: None, None
        size: dp(300), dp(300)

        MDLabel:
            text: "Verifique seu e-mail"
            halign: "center"
            font_style: "H6"

        MDTextField:
            id: codigo_input
            hint_text: "Digite o código de verificação"
            mode: "rectangle"
            max_text_length: 6
            

        MDRaisedButton:
            text: "Verificar"
            pos_hint: {"center_x": 0.5}
            on_release: root.verificar_codigo()
"""

Builder.load_string(verificacao_kv)

class VerificacaoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.usuario_email = None  # recebe o email do cadastro
        
    def verificar_codigo(self):
        codigo_digitado = self.ids.codigo_input.text.strip()
        if not codigo_digitado:
            toast("Digite o código de verificação")
            return

        self.usuario = db.query(Usuario).filter_by(email=self.usuario_email).first()
        print(f'========================={self.usuario.codigo_verificacao}')
        if self.usuario and self.usuario.codigo_verificacao == codigo_digitado:
            self.usuario.verificado = True
            db.commit()
            toast("Email verificado com sucesso!")
            self.manager.current = "login"  # ou outra tela
        else:
            
            toast(f"Código incorreto")