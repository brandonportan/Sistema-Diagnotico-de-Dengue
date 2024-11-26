import flet as ft   
import cohere
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()
serpapi_key = os.getenv("SERPAPI_KEY")
cohere_key = os.getenv("COHERE_KEY")

co = cohere.ClientV2(cohere_key)


i = 0
preguntas = [
    {
        "Pregunta": "¿Tiene el paciente fiebre?",
        "Respuesta": None,
        "TipoPregunta": 1, #? 1: Pregunta cerrada, 2: Pregunta abierta
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
    src="https://www.bing.com/images/search?view=detailV2&ccid=pvRD6ccd&id=605830166CA2D4DEC868EECD3F6166E8D8EA211A&thid=OIP.pvRD6ccdIW3z4UVBFWZ7igHaFg&mediaurl=https%3a%2f%2fstatic.vecteezy.com%2fsystem%2fresources%2fpreviews%2f013%2f799%2f075%2fnon_2x%2fperson-with-high-fever-illustration-vector.jpg&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.a6f443e9c71d216df3e1454115667b8a%3frik%3dGiHq2OhmYT%252fN7g%26pid%3dImgRaw%26r%3d0&exph=980&expw=1317&q=fiebre&simid=608021126431448113&FORM=IRPRST&ck=E5FF39C26AAA46C0F8697741156BD9F3&selectedIndex=3&itb=0"
)

def start_system_expert(page: ft.Page, regClinico):
    # Aquí va el contenido de la función `main`, pero cambiando `regClinico`
    # como parámetro recibido por esta función.
    main(page, regClinico)

def main(page: ft.Page, regClinico):
    global preg
    page.title = "Sistema Experto"    
    page.title = 'Diagnóstico de Enfermedad del Dengue'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.BLUE_GREY_800
    page.vertical_alignment =  ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.update()

    system_message = "Me ayudarás a diagnósticar la enfermedad del dengue  y su posible trataimiento, primero harás preguntas cerradas una por una, cuando tengas suficiente imformación puedes hacer dos o tres preguntas abiertas, todo con el objetivo de dar una conclusión si el paciente tiene o no dengue y que tipo de dengue, para que tengas un contexto inicial esta es información médica general del paciente:  " + regClinico.__str__() 

    container1 = ft.Container(
        width=400,
        height=400,
        bgcolor=ft.colors.BLUE_GREY_800,
        border_radius=20,
        content=ft.Column(
            [
                ft.Text("Diagnóstico de Enfermedad del Dengue", color=ft.colors.WHITE),
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
                    "content": "These are the questions: " + preguntas.__str__() + "\n if you need more information ask another question (one at a time), if you have diagnostic then finish the conversation with the explanation of the diagnostic and the possible treatment",
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

# ft.app(target=main)
