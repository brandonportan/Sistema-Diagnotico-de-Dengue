import flet as ft

def main(page: ft.Page):
    # Contenedor para el diagrama 
    diagram_container = ft.Container(
        width=page.width * 0.35,
        height=page.height * 0.7,
        bgcolor="lightgray",  # Fondo del contenedor para diferenciarlo
        content=ft.ListView(  # Usamos ListView con desplazamiento
            spacing=10,
            expand=True,  # Expandir para llenar el contenedor disponible
            auto_scroll=True,  # Habilitar desplazamiento automático
        ),
    )

    counter = 0

    # Agregar la primera figura cilíndrica al inicio
    diagram_container.content.controls.append(
        ft.Container(
            width=diagram_container.width * 0.3,  # 30% del ancho del contenedor
            height=60,
            border_radius=30,
            bgcolor="lightblue",
            content=ft.Text("Diagrama", text_align="center"),
            alignment=ft.alignment.center,
        )
    )

    # Función para agregar elementos al diagrama con lógica para "Sí" o "No"
    def add_element(choice):
        nonlocal counter
        counter += 1

        # Flecha y texto correspondiente
        arrow_color = "green" if choice == "yes" else "red"
        arrow_text = "Sí" if choice == "yes" else "No"
        arrow_alignment = ft.Row(
            controls=[
                ft.Text(arrow_text, size=20) if choice == "no" else ft.Container(width=20),
                ft.Text("↓", size=30, color=arrow_color),  # Flecha con color
                ft.Text(arrow_text, size=20) if choice == "yes" else ft.Container(width=20),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
        diagram_container.content.controls.append(arrow_alignment)

        # Cuadrado con número ajustado al 30% del ancho del contenedor
        diagram_container.content.controls.append(
            ft.Container(
                width=diagram_container.width * 0.3,  # 30% del ancho del contenedor
                height=80,
                bgcolor="lightgreen",
                content=ft.Text(str(counter - 1), size=24, text_align="center"),
                alignment=ft.alignment.center,
            )
        )

        # Actualizamos la página
        page.update()

    # Botones para "Sí" y "No"
    yes_button = ft.ElevatedButton("Sí", on_click=lambda e: add_element("yes"))
    no_button = ft.ElevatedButton("No", on_click=lambda e: add_element("no"))

    # Contenedor con la imagen
    image_container = ft.Container(
        image_src='https://media.gettyimages.com/id/139289970/es/foto/aedes-aegypti.jpg?s=1024x1024&w=gi&k=20&c=wjoYQF_aEKh72eN_Iu0dqXUyvmwIJaxUc5FlS0IvZwc=',  # Replace with your image URL
        image_fit=ft.ImageFit.COVER,  # Scale the image to cover the container
        expand=True,  # Fill the container with the image

        width=page.width * 0.2,  # 20% del ancho de la página
        height=page.width * 0.2,  # Hacerlo cuadrado
        alignment=ft.alignment.center,
    )

    # Layout principal
    page.add(
        ft.Row(
            [
                # Columna principal con el diagrama y botones
                ft.Column(
                    [
                        ft.Container(height=50),  # Espacio para mover el diagrama hacia abajo
                        diagram_container,  # Contenedor con el diagrama
                        ft.Row(
                            [yes_button, no_button],  # Botones fuera del contenedor
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                # Contenedor de imagen al lado derecho
                ft.Container(
                    content=image_container,
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(right=100),  
                    expand=False,  # No expandir horizontalmente
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar verticalmente
        )
    )

# Ejecutar la aplicación
ft.app(target=main)
