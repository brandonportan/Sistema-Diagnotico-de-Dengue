import flet as ft   
import cohere
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()
serpapi_key = os.getenv("SERPAPI_KEY")
cohere_key = os.getenv("COHERE_KEY")

co = cohere.ClientV2(cohere_key)
system_message = "You are helping me in the diagnosis of a not working printer your goal is to give a possible solution (just one) by asking closed questions (just one), i am going to give you a map of asked questions and their answers so you have context of the problem"

i = 0
preguntas = [
    {
        "Pregunta": "¿Enciende su impresora?",
        "Respuesta": None,
        "imagen": None
    }
]
preg = ft.Text(
        value=preguntas[i]["Pregunta"],
        color=ft.colors.WHITE,
        size=20,
        weight=ft.FontWeight.BOLD
    )
image = ft.Image(
    src="https://th.bing.com/th/id/R.682cc010a568bf4e0b2fa550208be220?rik=oAke0b8wKem8lg&pid=ImgRaw&r=0"
)

def main(page: ft.Page):
    global preg
    page.title = "My app"    
    page.title = 'Aplicacion Tienda'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.BLUE_GREY_800
    page.vertical_alignment =  ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.update()

    container1 = ft.Container(
        width=400,
        height=400,
        bgcolor=ft.colors.BLUE_GREY_800,
        border_radius=20,
        content=ft.Column(
            [
                ft.Text("Prueba Consumo de API", color=ft.colors.WHITE),
                preg,
                ft.Row(
                    controls=[
                        ft.TextButton(
                            "Si",
                            on_click=lambda e: respuesta(e, "Si"),
                        ),
                        ft.TextButton(
                            "No",
                            on_click=lambda e: respuesta(e, "No"),
                        ),   
                    ]
                ),
                ft.Container(
                    content=image
                )
            ]
        )
    )
    page.add(container1)

    def respuesta(e, res):
        global preg, i, preguntas, image    
            
        print(preguntas)
        preguntas[i]["Respuesta"] = res
        print(preguntas)
        
        # Preguntar a la IA
        res = co.chat(
            model="command-r-plus-08-2024",
            messages=[
                {"role": "system", "content": system_message},
                {
                    "role": "user",
                    "content": "These are the questions: " + preguntas.__str__() + "\n if you need more information ask another question (one at a time), if you have a solution or a diagnostic then finish the conversation",
                },
            ],
        )
        print(res.message.content[0].text)
        preguntas.append({"Pregunta": res.message.content[0].text, "Respuesta": None})
        print(preguntas)
        i = i + 1
        
        # Actualiza el valor de la pregunta y refresca el control
        preg.value = preguntas[i]["Pregunta"]
        preg.update()

        # Actualiza la imagen con el nuevo enlace
        new_image_link = get_image_link(0, preguntas[i]["Pregunta"])
        if new_image_link:
            image.src = new_image_link
            image.update()

    def get_image_link(pageNumber, query):
        global serpapi_key
        params = {
            "q": query,  # Término de búsqueda
            "hl": "es",  # Idioma español
            "gl": "us",  # País
            "api_key": serpapi_key,  # API key
            "tbm": "isch",  # Tipo de búsqueda (imágenes)
            "ijn": pageNumber,  # Número de la página
        }

        # Realiza la búsqueda
        query = GoogleSearch(params)
        data = query.get_dictionary()

        # Extraer el enlace de la primera imagen
        if 'images_results' in data and len(data['images_results']) > 0:
            first_image_link = data['images_results'][0].get('original')
            print("Link de la primera imagen:", first_image_link)
            return first_image_link
        else:
            print("No se encontraron resultados de imágenes.")
            return None

ft.app(target=main)
