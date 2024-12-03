import flet as ft
import json
import diagnostico

global data 

def main(page: ft.Page):
    global data
    page.title = "Formulario de Diagnóstico"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = "adaptive"
    # Diccionario para almacenar los datos
    data = {
        "nombres": "",
        "apellidos": "", 
        "residencia_viajes": "",
        "contacto_dengue": False,
        "antecedentes_dengue": False,
        "enfermedades_cronicas": False,
        "tipos_enfermedades_cronicas": {
            "diabetes": False,
            "hipertension": False,
            "enfermedad_cardiaca": False,
            "otros": "",
        },
        "agua_potable_control_mosquitos": False,
        "medicamentos_usados": "",
        "problemas_respiratorios_desHidratacion": False,
    }

    # Funciones para manejar los cambios
    def on_change(e, key):
        data[key] = e.control.value

    def on_toggle(e, key):
        data[key] = e.control.value
        # Mostrar u ocultar las opciones de enfermedades crónicas
        if key == "enfermedades_cronicas":
            enfermedades_container.visible = e.control.value
            page.update()

    def on_checkbox_change(e, key):        
        data["tipos_enfermedades_cronicas"][key] = e.control.value

    def guardar_json(e):        
        with open("diagnostico.json", "w") as file:
            json.dump(data, file, indent=4)
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Datos guardados correctamente"),
            open=True,
        )
        page.update()
        # Llamar el otro formulario y pasar la información del paciente
        print(data)
        diagnostico.start_system_expert(page, data)


    # Contenedor para opciones de enfermedades crónicas
    enfermedades_container = ft.Container(
        visible=False,
        content=ft.Column(
            controls=[
                ft.Checkbox(
                    label="Diabetes",
                    on_change=lambda e: on_checkbox_change(e, "diabetes"),
                ),
                ft.Checkbox(
                    label="Hipertensión",
                    on_change=lambda e: on_checkbox_change(e, "hipertension"),
                ),
                ft.Checkbox(
                    label="Enfermedades cardíacas",
                    on_change=lambda e: on_checkbox_change(e, "enfermedad_cardiaca"),
                ),
                ft.TextField(
                    label="Otros (especificar)",
                    on_change=lambda e: on_change(e, "tipos_enfermedades_cronicas.otros"),
                ),
            ]
        ),
    )

    # Formulario
    form = ft.Container(
        padding=ft.Padding(120, 0, 120, 0),
        content=ft.Column(
            adaptive= True,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Formulario de Diagnóstico", size=24, weight=ft.FontWeight.BOLD)
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.TextField(
                            label="Nombres",
                            border_color=ft.colors.BLUE_GREY_700,
                            on_change=lambda e: on_change(e, "nombres"),
                        ),
                        ft.TextField(
                            label="Apellidos",
                            border_color=ft.colors.BLUE_GREY_700,
                            on_change=lambda e: on_change(e, "apellidos"),
                        ),
                    ],
                ),
                ft.Dropdown(
                    label="Sexo",
                    options=[
                        ft.dropdown.Option("Masculino"),
                        ft.dropdown.Option("Femenino"),
                        ft.dropdown.Option("Otro"),
                    ],
                    on_change=lambda e: on_change(e, "sexo"),
                ),
                ft.TextField(
                    label="¿Dónde reside o ha viajado recientemente (últimos 14 días)?",
                    border_color=ft.colors.BLUE_GREY_700,
                    on_change=lambda e: on_change(e, "residencia_viajes"),
                ),
                ft.Switch(
                    label="¿Ha estado en contacto con alguien diagnosticado con dengue?",
                    on_change=lambda e: on_toggle(e, "contacto_dengue"),
                ),
                ft.Switch(
                    label="¿Tiene antecedentes de haber tenido dengue previamente?",
                    on_change=lambda e: on_toggle(e, "antecedentes_dengue"),
                ),
                ft.Switch(
                    label="¿Tiene enfermedades crónicas como diabetes, hipertensión o enfermedades cardíacas?",
                    on_change=lambda e: on_toggle(e, "enfermedades_cronicas"),
                ),
                enfermedades_container,
                ft.Switch(
                    label="¿Tiene acceso a agua potable y control de mosquitos en su hogar?",
                    on_change=lambda e: on_toggle(e, "agua_potable_control_mosquitos"),
                ),
                ft.TextField(
                    label="¿Ha usado algún medicamento para la fiebre o dolor en los últimos días?",
                    border_color=ft.colors.BLUE_GREY_700,
                    on_change=lambda e: on_change(e, "medicamentos_usados"),
                ),
                ft.Switch(
                    label="¿Ha tenido problemas para respirar o signos de deshidratación?",
                    on_change=lambda e: on_toggle(e, "problemas_respiratorios_desHidratacion"),
                ),
                ft.ElevatedButton(
                    text="Guardar Datos",
                    on_click=guardar_json,
                    bgcolor=ft.colors.GREEN,
                    color=ft.colors.WHITE,
                ),
            ],
        ),
    )

    page.add(form)
    page.update()


ft.app(main)
