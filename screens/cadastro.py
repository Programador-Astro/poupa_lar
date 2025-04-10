from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.snackbar import Snackbar

from database.models import Casa, Usuario
from database.connection import db

import uuid
import re
import requests
from funcs_internas import *



Builder.load_string('''
<CadastroScreen>:
    name: "cadastro"

    MDScreenManager:
        id: screen_manager

        MDScreen:
            name: "casa"

            MDBoxLayout:
                orientation: "vertical"
                padding: "24dp"
                spacing: "16dp"

                MDLabel:
                    text: "Primeiro, vamos cadastrar sua CASA!"
                    halign: "center"
                    font_style: "H5"

                MDTextField:
                    id: cep_field
                    hint_text: "Digite o CEP"
                    max_text_length: 9
                    input_filter: "int"
                    on_focus: if not self.focus: root.formatar_cep(self.text)
                    on_text_validate: root.buscar_cep(self.text)
                    mode: "rectangle"

                MDTextField:
                    id: rua_field
                    hint_text: "Rua"
                    readonly: True
                    disabled: True
                    mode: "rectangle"

                MDBoxLayout:
                    spacing: "12dp"

                    MDTextField:
                        id: cidade_field
                        hint_text: "Cidade"
                        readonly: True
                        disabled: True
                        mode: "rectangle"

                    MDTextField:
                        id: estado_field
                        hint_text: "Estado"
                        readonly: True
                        disabled: True
                        mode: "rectangle"

                MDTextField:
                    id: numero_field
                    hint_text: "Número"
                    mode: "rectangle"

                MDTextField:
                    id: complemento_field
                    hint_text: "Complemento"
                    mode: "rectangle"

                MDLabel:
                    id: status_label
                    text: ""
                    halign: "center"
                    theme_text_color: "Hint"

                MDRaisedButton:
                    text: "Próximo"
                    md_bg_color: app.theme_cls.primary_color
                    text_color: 1, 1, 1, 1
                    pos_hint: {"center_x": 0.5}
                    on_release: root.ir_para_usuario()

        MDScreen:
            name: "usuario"

            MDBoxLayout:
                orientation: "vertical"
                padding: "24dp"
                spacing: "16dp"

                MDLabel:
                    text: "Agora vamos cadastrar seus dados"
                    halign: "center"
                    font_style: "H5"
                MDTextField:
                    id: usuario_field
                    hint_text: "Usuario"
                    mode: "rectangle"
                MDTextField:
                    id: senha_field
                    hint_text: "Senha"
                    password: True
                    mode: "rectangle"

                MDTextField:
                    id: confirmar_senha_field
                    hint_text: "Confirmar Senha"
                    password: True
                    mode: "rectangle"

                MDTextField:
                    id: nome_field
                    hint_text: "Nome Completo"
                    mode: "rectangle"

                MDTextField:
                    id: email_field
                    hint_text: "E-mail"
                    mode: "rectangle"

                
                MDRaisedButton:
                    text: "Cadastrar"
                    md_bg_color: app.theme_cls.primary_color
                    text_color: 1, 1, 1, 1
                    pos_hint: {"center_x": 0.5}
                    on_release: root.cadastrar_usuario()

                MDRaisedButton:
                    text: "Voltar"
                    md_bg_color: 1, 1, 1, 1
                    text_color: app.theme_cls.primary_color
                    pos_hint: {"center_x": 0.5}
                    on_release: root.voltar_para_casa()
''')

class CadastroScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flag_casa = False#Serve pra verificar se a casa pode ser criada sem problemas
        self.nova_casa = None
        
    def formatar_cep(self, cep):
        cep_numeros = ''.join(filter(str.isdigit, cep))[:8]
        if len(cep_numeros) == 8:
            cep_formatado = f"{cep_numeros[:5]}-{cep_numeros[5:]}"
            self.ids.cep_field.text = cep_formatado
            self.buscar_cep(cep_formatado)
        else:
            self.ids.status_label.text = "CEP inválido. Deve conter 8 dígitos."
            self.flag_casa = False

    def buscar_cep(self, cep):
        cep = ''.join(filter(str.isdigit, cep))
        if len(cep) != 8:
            self.ids.status_label.text = "CEP inválido. Deve conter 8 dígitos."
            self.flag_casa = False
            return

        url = f"https://viacep.com.br/ws/{cep}/json/"
        try:
            response = requests.get(url)
            data = response.json()

            if "erro" in data:
                self.ids.status_label.text = "CEP não encontrado."
                self.flag_casa = False
            else:
                self.ids.rua_field.text = data.get("logradouro", "")
                self.ids.cidade_field.text = data.get("localidade", "")
                self.ids.estado_field.text = data.get("uf", "")
                self.ids.status_label.text = "Endereço carregado!"
                self.flag_casa = True
        except Exception as e:
            self.ids.status_label.text = f"Erro: {e}"
            self.flag_casa = False

    def ir_para_usuario(self):
        if not self.flag_casa:
            self.ids.status_label.text = "Preencha o endereço corretamente."
            return

        self.nova_casa = Casa(
            codigo="1",
            nome="Minha Casa",
            uf=self.ids.estado_field.text,
            cidade=self.ids.cidade_field.text,
            cep=self.ids.cep_field.text,
            endereco=self.ids.rua_field.text,
            numero=self.ids.numero_field.text,
            complemento=self.ids.complemento_field.text
        )

        self.ids.screen_manager.current = "usuario"

    def voltar_para_casa(self):
        self.ids.screen_manager.current = "casa"

    def cadastrar_usuario(self):
        codigo_verificacao = str(uuid.uuid4())[:6]
        usuario   = self.ids.usuario_field.text
        nome      = self.ids.nome_field.text
        email     = self.ids.email_field.text.strip()
        senha     = self.ids.senha_field.text
        confirmar = self.ids.confirmar_senha_field.text
        codigo_verificacao = codigo_verificacao
        email_confirmado = False

        
        #VALIDAÇÃO DO EMAIL
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            self.mensagem("E-mail inválido.")
            return
        # Verifica se já existe um usuário com este e-mail
        email_existe = db.query(Usuario).filter_by(email=email).first()
        if email_existe:
            self.mensagem("Este e-mail já está em uso.")
            return
        
        
        
        
        #Fim validação EMAIL






        if not usuario or not nome or not email or not senha or not confirmar:
            self.mensagem("Preencha todos os campos.")
            return

        if senha != confirmar:
            self.mensagem("Senhas não coincidem.")
            return

        if not self.nova_casa:
            self.mensagem("Erro: casa não criada.")
            return

        # Adiciona casa e usuário ao banco
        db.add(self.nova_casa)
        db.flush()

        novo_usuario = Usuario(
            usuario    = usuario,
            nome       = nome,
            email      = email,
            senha_hash = senha,
            casa_id    =  self.nova_casa.id,
            codigo_verificacao = codigo_verificacao,
            email_confirmado = email_confirmado,
        )

        db.add(novo_usuario)
        db.commit()

        self.mensagem("Cadastro concluído com sucesso!")
        self.manager.current = "login"

    def mensagem(self, texto):
        MDDialog(title="Cadastro", text=texto, buttons=[]).open()