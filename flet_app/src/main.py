import flet as ft
import serial

from devices import arduino
from routes import about, error404, root
from utils import elements
from utils.config import TEXT_SIZE


def build_main_view(page: ft.Page) -> ft.View:
    def _send_command(command) -> None:
        try:
            if not client.port:
                client.port = arduino.find_port()

            if not client.active:
                client.connect()

            client.write(command)

        except (serial.SerialException, OSError) as e:
            print(f"Критична помилка порту: {e}")
            client.close()

    client = page.session.store.get("client")

    on_button = ft.IconButton(
        ft.Icons.PLAY_ARROW_ROUNDED, on_click=lambda e: _send_command("ON")
    )
    off_button = ft.IconButton(
        ft.Icons.STOP_ROUNDED, on_click=lambda e: _send_command("OFF")
    )
    else_button = ft.IconButton(
        ft.Icons.REPEAT, on_click=lambda e: _send_command("bad_command")
    )

    buttons = [
        on_button,
        off_button,
        else_button,
    ]

    controller = ft.Row(
        controls=buttons,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.title = root.TITLE
    return ft.View(
        route=root.ROUTE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(root.TITLE),
            # ft.Text(""),
            ft.Image(
                src="/images/logo-1024x1024.png",  # Посилання на картинку
                width=400,
                height=400,
            ),
            # ft.Text(""),
            ft.Text("Обери гру, дію:", size=TEXT_SIZE),
            # ft.Text(""),
            controller,
            ft.Text(""),
            about.button(page),
        ],
    )


async def main(page: ft.Page):
    page.title = root.TITLE
    page.theme_mode = ft.ThemeMode.DARK
    page.route = root.ROUTE

    async def route_change():
        page.views.clear()
        page.views.append(build_main_view(page))

        match page.route:
            case about.ROUTE:
                page.views.append(about.build_view(page))
            case _:
                if page.route != root.ROUTE:
                    page.views.append(error404.build_view(page))

        page.update()

    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    async def _init() -> None:
        client = arduino.ArduinoClient(arduino.find_port())
        page.session.store.set("client", client)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    await _init()
    await route_change()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
