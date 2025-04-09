from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from database.models import Casa
from database.connection import db
import requests

Builder.load_string('''
<CadastroCasaScreen>:
    name: "cadastro_casa"

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
            max_text_length: 9  # Inclui hífen quando formatado
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
            text: "Proximo"
            md_bg_color: app.theme_cls.primary_color
            text_color: 1, 1, 1, 1
            pos_hint: {"center_x": 0.5}
            on_press: root.salvar_casa()


''')
#           on_release: root.manager.current = "cadastro_usuario"
class CadastroCasaScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flag_casa = False  # define logo a variável


   
    def salvar_casa(self):
        #Verificando os dados
        if self.flag_casa == True:
            print('tudo certo')
            nova_casa = Casa(codigo='123', nome='minha_casa',
                            uf= self.ids.estado_field.text,
                            cidade= self.ids.cidade_field.text,
                            cep = self.ids.cep_field.text,
                            endereco = self.ids.rua_field.text,
                            numero = self.ids.numero_field.text,
                            complemento = self.ids.complemento_field.text
                            )
            if nova_casa:
                print('Criando uma nova casa!')
                db.add(nova_casa)
                db.commit()
                
             
              
        if self.flag_casa == False:
            print('Deu error')
        


    def formatar_cep(self, cep):
        # Remove qualquer caractere que não seja dígito
        cep_numeros = ''.join(filter(str.isdigit, cep))[:8]

        if len(cep_numeros) == 8:
            cep_formatado = f"{cep_numeros[:5]}-{cep_numeros[5:]}"
            self.ids.cep_field.text = cep_formatado
            self.buscar_cep(cep_formatado)
        else:
            self.ids.status_label.text = "CEP inválido. Deve conter 8 dígitos."
            self.flag_casa = False
            return self.flag_casa

    def buscar_cep(self, cep):
        cep = ''.join(filter(str.isdigit, cep))  # remove o hífen pra API
        if len(cep) != 8:
            self.ids.status_label.text = "CEP inválido. Deve conter 8 dígitos."
            self.flag_casa = False
            return self.flag_casa

        url = f"https://viacep.com.br/ws/{cep}/json/"
        try:
            response = requests.get(url)
            data = response.json()

            if "erro" in data:
                self.ids.status_label.text = "CEP não encontrado."
                self.ids.rua_field.text = ""
                self.ids.cidade_field.text = ""
                self.ids.estado_field.text = ""
                self.flag_casa = False
                return self.flag_casa
            else:
                self.ids.rua_field.text = data.get("logradouro", "")
                self.ids.cidade_field.text = data.get("localidade", "")
                self.ids.estado_field.text = data.get("uf", "")
                self.ids.status_label.text = "Endereço carregado com sucesso!"
                self.flag_casa = True
                return self.flag_casa
        except Exception as e:
            self.ids.status_label.text = f"Erro: {e}"

    