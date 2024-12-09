import flet as ft
import cohere
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
import json

load_dotenv()
serpapi_key = os.getenv("SERPAPI_KEY")
cohere_key = os.getenv("COHERE_KEY")

co = cohere.ClientV2(cohere_key)

# Datos de ejemplo para regClinico
regClinico = {
    'nombre': 'Juan Pérez',
    'edad': 35,
    'sexo': 'Masculino',
    'historia_clinica': 'Sin antecedentes médicos relevantes'
}

# Inicialización de las preguntas
i = 0
preguntas = [
    {
        "nPregunta": i + 1,
        "Pregunta": "¿Tiene el paciente fiebre?",
        "Respuesta": None,
        "TipoPregunta": 1,  # 1: Pregunta cerrada, 2: Pregunta abierta
        "imagen": None
    }
]

# Definir el texto de la primera pregunta
preg = ft.Text(
    'Diagnostico de Dengue',
    color=ft.colors.WHITE,
    size=20,
    weight=ft.FontWeight.BOLD
)


# Imagen asociada a la pregunta (inicial)
image = ft.Image(
    src='https://media.gettyimages.com/id/139289970/es/foto/aedes-aegypti.jpg?s=1024x1024&w=gi&k=20&c=wjoYQF_aEKh72eN_Iu0dqXUyvmwIJaxUc5FlS0IvZwc=',  # Inicialmente no hay imagen
    width=350,
    height=350
)

def start_system_expert(page: ft.Page, regClinico):
    global paciente
    paciente = regClinico  # Asignamos regClinico a paciente
    main(page, regClinico)  # Llamamos la función main pasando regClinico

def main(page: ft.Page, regClinico):
    global preg, preguntas, i
    page.title = "Sistema Experto"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.BLUE_GREY_800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.update()

    system_message = "Me ayudarás a diagnósticar la enfermedad del dengue y su posible tratamiento. " + str(regClinico)

    # Contenedor para el diagrama
    diagram_container = ft.Container(
        width=page.width * 0.5,  # Contenedor que ocupa el 50% de la página
        height=page.height * 0.7,
        bgcolor="lightgray",
        content=ft.ListView(
            spacing=10,
            expand=True,
            auto_scroll=True,
        ),
    )

    counter = 0
    diagram_container.content.controls.append(
        ft.Container(
            width=diagram_container.width * 0.3,
            height=60,
            border_radius=30,
            bgcolor="lightblue",
            content=ft.Text(preguntas[0]["Pregunta"], text_align="center"),
            alignment=ft.alignment.center,
        )
    )

    # Función para agregar elementos al diagrama
    def add_element(choice):
        nonlocal counter
        counter += 1
        arrow_color = "green" if choice == "yes" else "red"
        arrow_text = "Sí" if choice == "yes" else "No"
        arrow_alignment = ft.Row(
            controls=[
                ft.Text(arrow_text, size=20) if choice == "no" else ft.Container(width=20),
                ft.Text("↓", size=30, color=arrow_color),
                ft.Text(arrow_text, size=20) if choice == "yes" else ft.Container(width=20),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
        diagram_container.content.controls.append(arrow_alignment)
        
        # Crear el recuadro con la pregunta dentro
        diagram_container.content.controls.append(
            ft.Container(
                width=diagram_container.width * 0.3,
                height=80,
                bgcolor="lightgreen",
                content=ft.Text(str(preguntas[i]["Pregunta"]), size=20, text_align="center"),
                alignment=ft.alignment.center,
            )
        )
        page.update()

    def respuesta(e, res):
        global preg, i, preguntas, image
        preguntas[i]['Respuesta'] = res
        res = co.chat(
            model="command-r-plus-08-2024",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": "Estas son las preguntas previas " + str(preguntas) + "\n si necesitas más información haz otra pregunta. Si nPregunta = 12, da la conclusión."},
            ],
            response_format={"type": "json_object", "schema": {"type": "object", "properties": {"nPregunta": {"type": "number"}, "Pregunta": {"type": "string"}, "Respuesta": {"type": "string"}, "TipoPregunta": {"type": "number"}, "imagen": {"type": "string"}}, "required": ["nPregunta", "Pregunta", "TipoPregunta"]}}
        )
        jsonContent = json.loads(res.message.content[0].text)
        preguntas.append(jsonContent)
        i += 1
        page.update()
        add_element(res)

        # Buscar imagen en internet
        new_image_link = get_image_link(0, preguntas[i]["Pregunta"])
        if new_image_link:
            image.src = new_image_link
            image.update()

    def get_image_link(pageNumber, query):
        global serpapi_key
        params = {"q": query, "hl": "es", "gl": "us", "api_key": serpapi_key, "tbm": "isch", "ijn": pageNumber}
        query = GoogleSearch(params)
        data = query.get_dictionary()
        if 'images_results' in data and len(data['images_results']) > 0:
            return data['images_results'][0].get('original')
        else:
            return None

    def conclusion(e):
        global preguntas
        res = co.chat(
            model="command-r-plus-08-2024",
            messages=[{"role": "system", "content": system_message}, {"role": "user", "content": "Concluye si el paciente tiene dengue o no en base a estas preguntas " + str(preguntas)}]
        )
        preg.value = res.message.content[0].text
        page.update()

    # Contenedor principal de la interfaz
    container1 = ft.Container(
        width=page.width,
        height=page.height,
        bgcolor=ft.colors.BLUE_GREY_800,
        border_radius=20,
        content=ft.Row(
            [
                # Columna para el diagrama
                ft.Column(
                    [
                        preg,
                        diagram_container,
                        ft.Row(
                            controls=[
                                ft.TextButton("Sí", on_click=lambda e: respuesta(e, "Sí")),
                                ft.TextButton("No", on_click=lambda e: respuesta(e, "No")),
                                ft.TextButton("Concluir", on_click=lambda e: conclusion(e)),
                            ]
                        )
                    ],
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                # Columna para la imagen
                ft.Column(
                    [
                        ft.Container(content=image),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    width=page.width * 0.4,  # Ajusta el tamaño del contenedor de la imagen
                    height=page.height * 0.7,  # Ajusta la altura del contenedor de la imagen
                ),
            ]
        )
    )

    page.add(container1)

# Ejecutar la aplicación pasando regClinico
ft.app(target=lambda page: start_system_expert(page, regClinico))
