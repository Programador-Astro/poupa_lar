from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.card import MDCard
import random

Builder.load_string('''
<HomeScreen>:
    name: "home"

    MDBoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: "Bem-vindo ao PoupaLar"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Primary"

        MDCard:
            orientation: "vertical"
            padding: dp(16)
            size_hint_y: None
            height: dp(100)
            md_bg_color: app.theme_cls.primary_light
            elevation: 2
            radius: [12, 12, 12, 12]

            MDBoxLayout:
                spacing: dp(10)

                MDIcon:
                    icon: "warehouse"
                    theme_text_color: "Primary"

                MDLabel:
                    id: resumo_label
                    text: ""
                    theme_text_color: "Primary"
                    font_style: "Body1"

            MDBoxLayout:
                spacing: dp(10)

                MDIcon:
                    icon: "alert"
                    theme_text_color: "Error"

                MDLabel:
                    id: alerta_label
                    text: ""
                    theme_text_color: "Error"
                    font_style: "Body2"

        MDCard:
            orientation: "vertical"
            padding: dp(16)
            size_hint_y: None
            height: dp(100)
            elevation: 2
            radius: [12, 12, 12, 12]

            MDLabel:
                text: "Dica do dia:"
                theme_text_color: "Primary"
                font_style: "Subtitle1"

            MDLabel:
                id: dica_label
                text: ""
                font_style: "Body2"
                theme_text_color: "Secondary"

    MDFloatingActionButtonSpeedDial:
        id: speed_dial
        icon: "plus"
        root_button_anim: True
        hint_animation: True
        callback: root.callback_speed_dial
        data: {}
        pos_hint: {"x": 0.85, "y": 0.02}
''')

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dicas = [
            "Compare preços antes de comprar.",
            "Use o estoque antes que expire.",
            "Planeje as compras da semana.",
            "Avalie onde está gastando mais.",
            "Produtos de limpeza rendem mais em embalagens grandes!"
        ]

    def on_enter(self):
        self.ids.resumo_label.text = "Total de produtos: 35"
        self.ids.alerta_label.text = "4 produtos abaixo do mínimo"
        self.ids.dica_label.text = random.choice(self.dicas)

        self.ids.speed_dial.data = {
            "plus": "Adicionar item",
            "magnify": "Buscar produto",
            "cash": "Melhor preço"
        }

    def callback_speed_dial(self, instance, icon_name):
        print(f"Você clicou em: {icon_name}")
