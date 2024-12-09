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
paciente = {}

i = 0
preguntas = [
    {
        "nPregunta": i+1,
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
    global paciente
    # Llamar directamente a main, usando el objeto `page` proporcionado
    paciente = regClinico
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

    system_message = "Me ayudarás a diagnósticar la enfermedad del dengue  y su posible tratamiento, primero harás preguntas cerradas una por una, si necesitas mas información puedes hacer hasta dos preguntas abiertas, todo con el objetivo de dar una conclusión si el paciente tiene o no dengue y que tipo de dengue, para que tengas un contexto inicial esta es información médica general del paciente:  " + regClinico.__str__() 

    container1 = ft.Container(
        width=400,
        height=400,
        bgcolor=ft.colors.BLUE_GREY_800,
        border_radius=20,
        content=ft.Column(
            [
                ft.Text("Diagnóstico de Enfermedad del Dengue, paciente: ", color=ft.colors.WHITE),
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
                        ft.TextButton(
                            "Concluir",
                            on_click=lambda e: conclusion(e),
                        ) 
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
        
        # Registrar la respuesta
        preguntas[i]['Respuesta'] = res
        
        # Crear mensaje para la IA
        mensaje_usuario = (
            "Estas son las preguntas previas: " + preguntas.__str__() + 
            "\nSi necesitas más información haz otra pregunta. Si nPregunta = 12, da una conclusión con TipoPregunta: 3 basándote en las preguntas dadas."
        )
        
        # Solicitar respuesta a la IA
        res = co.chat(
            model="command-r-plus-08-2024",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "system", "content": "Estructura tu respuesta en un JSON con la estructura indicada. No reinicies el contador de preguntas."},
                {"role": "user", "content": mensaje_usuario},
            ],
            response_format={
                "type": "json_object",
                "schema": {
                    "type": "object",
                    "properties": {
                        "nPregunta": {"type": "number"},
                        "Pregunta": {"type": "string"},
                        "Respuesta": {"type": "string"},
                        "TipoPregunta": {"type": "number"},
                        "imagen": {"type": "string"},
                    },
                    "required": ["nPregunta", "Pregunta", "TipoPregunta"],
                },
            }
        )

        # Procesar la respuesta recibida
        try:
            jsonContent = json.loads(res.message.content[0].text)
            if 'nPregunta' in jsonContent and 'TipoPregunta' in jsonContent:
                if jsonContent['nPregunta'] != i + 1:
                    raise ValueError("El contador de preguntas no coincide con el esperado.")
                
                preguntas.append(jsonContent)
                i += 1
                
                # Actualizar control de UI
                preg.value = preguntas[i]["Pregunta"]
                preg.update()

                # Actualizar imagen
                new_image_link = get_image_link(0, preguntas[i]["Pregunta"])
                if new_image_link:
                    image.src = new_image_link
                    image.update()
            else:
                raise ValueError("El JSON recibido está incompleto o mal formateado.")
        except Exception as ex:
            print(f"Error procesando la respuesta de la IA: {ex}")


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

    #función para consultar a la ia que haga una conclusión en base a las preguntas
    def conclusion(e):
        global preguntas        
        print('\n')
        print(preguntas)
        print('\n')
        # Preguntar a la IA
        res = co.chat(
            model="command-r-plus-08-2024",
            messages=[
                {"role": "system", "content": system_message},
                {
                    "role": "user","content":"Concluye si el paciente tiene dengue o no tiene dengue en base a estas preguntas " + preguntas.__str__(),
                },
            ]
        )
        print(res.message.content[0].text)
        preg.value = res.message.content[0].text
        preg.update()
# ft.app(target=main)
