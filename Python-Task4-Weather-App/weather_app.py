import os
import requests
from datetime import datetime
from collections import defaultdict
import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv

from weather_api import (
    get_current_weather,
    get_five_day_forecast,
    get_hourly_forecast,
    get_location_from_ip
)

from weather_utils import (
    get_weather_icon,
    get_temperature_text,
    get_weather_description,
    get_openweather_icon_code
)


# Configuration

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

current_weather = None
current_unit = "C"
forecast_data = None
hourly_data = None


# Colors

BG_TOP = "#111827"
BG_BOTTOM = "#312E81"
CARD = "#1E293B"
CARD_LIGHT = "#263449"
WHITE = "#F8FAFC"
TEXT_SECONDARY = "#CBD5E1"
TEXT_MUTED = "#94A3B8"
ACCENT = "#8B5CF6"
ACCENT_LIGHT = "#A78BFA"
ERROR_BG = "#451A1A"
SUCCESS_BG = "#123524"


# Gradient background

def draw_gradient():
    """Draw the application gradient background."""

    width = max(
        root.winfo_width(),
        700
    )

    height = max(
        root.winfo_height(),
        850
    )

    gradient_canvas.delete("gradient")

    steps = 100

    top_rgb = root.winfo_rgb(BG_TOP)
    bottom_rgb = root.winfo_rgb(BG_BOTTOM)

    top_rgb = tuple(
        value // 256
        for value in top_rgb
    )

    bottom_rgb = tuple(
        value // 256
        for value in bottom_rgb
    )

    for index in range(steps):

        ratio = index / steps

        r = int(
            top_rgb[0]
            + (bottom_rgb[0] - top_rgb[0]) * ratio
        )

        g = int(
            top_rgb[1]
            + (bottom_rgb[1] - top_rgb[1]) * ratio
        )

        b = int(
            top_rgb[2]
            + (bottom_rgb[2] - top_rgb[2]) * ratio
        )

        color = f"#{r:02x}{g:02x}{b:02x}"

        y1 = int(
            height * index / steps
        )

        y2 = int(
            height * (index + 1) / steps
        )

        gradient_canvas.create_rectangle(
            0,
            y1,
            width,
            y2,
            fill=color,
            outline="",
            tags="gradient"
        )


# Glass card helper

def create_card(parent, height=None):
    """Create a styled glass-like card."""

    frame = tk.Frame(
        parent,
        bg=CARD,
        highlightthickness=1,
        highlightbackground="#475569"
    )

    if height:
        frame.configure(
            height=height
        )

        frame.pack_propagate(False)

    return frame


# Status message

def show_status(message, status_type="normal"):
    """Display a status message."""

    if status_type == "error":
        status_label.config(
            text=message,
            bg=ERROR_BG,
            fg="#FCA5A5"
        )

    elif status_type == "success":
        status_label.config(
            text=message,
            bg=SUCCESS_BG,
            fg="#86EFAC"
        )

    else:
        status_label.config(
            text=message,
            bg=CARD_LIGHT,
            fg=TEXT_SECONDARY
        )


# Clear forecasts

def clear_forecast_frames():
    """Remove existing forecast widgets."""

    for widget in hourly_frame.winfo_children():
        widget.destroy()

    for widget in daily_frame.winfo_children():
        widget.destroy()


# Display current weather

def display_weather(data):
    """Display current weather information."""

    global current_weather

    current_weather = data

    city_name = data["name"]
    country = data["sys"]["country"]

    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    condition = (
        data["weather"][0]["description"]
        .title()
    )

    icon_code = data["weather"][0]["icon"]

    location_label.config(
        text=f"{city_name}, {country}"
    )

    condition_label.config(
        text=condition
    )

    update_temperature()

    humidity_value.config(
        text=f"{humidity}%"
    )

    wind_value.config(
        text=f"{wind_speed} m/s"
    )

    icon = get_weather_icon(
        icon_code,
        (120, 120)
    )

    if icon:
        weather_icon_label.config(
            image=icon,
            text=""
        )

        weather_icon_label.image = icon

    else:
        weather_icon_label.config(
            image="",
            text="☁️"
        )


# Temperature update

def update_temperature():
    """Update temperature using the selected unit."""

    if current_weather is None:
        return

    temperature = current_weather[
        "main"
    ]["temp"]

    temperature_label.config(
        text=get_temperature_text(
            temperature,
            current_unit
        )
    )

    update_forecast_temperatures()


# Celsius

def set_celsius():
    """Switch temperature display to Celsius."""

    global current_unit

    current_unit = "C"

    celsius_button.config(
        relief="sunken",
        bg=ACCENT
    )

    fahrenheit_button.config(
        relief="flat",
        bg=CARD_LIGHT
    )

    update_temperature()


# Fahrenheit

def set_fahrenheit():
    """Switch temperature display to Fahrenheit."""

    global current_unit

    current_unit = "F"

    celsius_button.config(
        relief="flat",
        bg=CARD_LIGHT
    )

    fahrenheit_button.config(
        relief="sunken",
        bg=ACCENT
    )

    update_temperature()


# Hourly forecast

def display_hourly_forecast():
    """Display the next six hourly forecasts."""

    for widget in hourly_frame.winfo_children():
        widget.destroy()

    if not hourly_data:
        return

    times = hourly_data[
        "hourly"
    ]["time"]

    temperatures = hourly_data[
        "hourly"
    ]["temperature_2m"]

    weather_codes = hourly_data[
        "hourly"
    ]["weather_code"]

    is_day_values = hourly_data[
        "hourly"
    ]["is_day"]

    for index in range(
        min(6, len(times))
    ):

        forecast_time = datetime.fromisoformat(
            times[index]
        )

        time_text = forecast_time.strftime(
            "%I %p"
        ).lstrip("0")

        temperature = temperatures[index]

        weather_code = weather_codes[index]

        is_day = is_day_values[index]

        icon_code = get_openweather_icon_code(
            weather_code,
            is_day
        )

        card = tk.Frame(
            hourly_frame,
            bg=CARD_LIGHT,
            highlightthickness=1,
            highlightbackground="#475569",
            width=100,
            height=150
        )

        card.grid(
            row=0,
            column=index,
            padx=4,
            pady=5
        )

        card.grid_propagate(False)

        time_label = tk.Label(
            card,
            text=time_text,
            font=("Segoe UI", 10, "bold"),
            bg=CARD_LIGHT,
            fg=TEXT_SECONDARY
        )

        time_label.pack(
            pady=(10, 2)
        )

        icon = get_weather_icon(
            icon_code,
            (50, 50)
        )

        icon_label = tk.Label(
            card,
            bg=CARD_LIGHT
        )

        icon_label.pack()

        if icon:
            icon_label.config(
                image=icon
            )

            icon_label.image = icon

        temperature_label = tk.Label(
            card,
            text=get_temperature_text(
                temperature,
                current_unit
            ),
            font=("Segoe UI", 11, "bold"),
            bg=CARD_LIGHT,
            fg=WHITE
        )

        temperature_label.pack(
            pady=2
        )

        condition = get_weather_description(
            weather_code
        )

        condition_label = tk.Label(
            card,
            text=condition,
            font=("Segoe UI", 7),
            bg=CARD_LIGHT,
            fg=TEXT_MUTED,
            wraplength=85
        )

        condition_label.pack()


# Five-day forecast

def display_daily_forecast(forecast_list):
    """Display the five-day forecast."""

    daily_data = defaultdict(list)

    for item in forecast_list:

        date = datetime.fromtimestamp(
            item["dt"]
        ).date()

        daily_data[date].append(
            item
        )

    dates = list(
        daily_data.keys()
    )[:5]

    for index, date in enumerate(dates):

        items = daily_data[date]

        selected_item = min(
            items,
            key=lambda item: abs(
                datetime.fromtimestamp(
                    item["dt"]
                ).hour - 12
            )
        )

        temperature = selected_item[
            "main"
        ]["temp"]

        icon_code = selected_item[
            "weather"
        ][0]["icon"]

        condition = selected_item[
            "weather"
        ][0]["description"].title()

        day_name = date.strftime(
            "%a"
        )

        card = tk.Frame(
            daily_frame,
            bg=CARD_LIGHT,
            highlightthickness=1,
            highlightbackground="#475569",
            width=110,
            height=170
        )

        card.grid(
            row=0,
            column=index,
            padx=5,
            pady=5
        )

        card.grid_propagate(False)

        day_label = tk.Label(
            card,
            text=day_name,
            font=("Segoe UI", 11, "bold"),
            bg=CARD_LIGHT,
            fg=TEXT_SECONDARY
        )

        day_label.pack(
            pady=(10, 3)
        )

        icon = get_weather_icon(
            icon_code,
            (55, 55)
        )

        icon_label = tk.Label(
            card,
            bg=CARD_LIGHT
        )

        icon_label.pack()

        if icon:
            icon_label.config(
                image=icon
            )

            icon_label.image = icon

        temperature_label = tk.Label(
            card,
            text=get_temperature_text(
                temperature,
                current_unit
            ),
            font=("Segoe UI", 12, "bold"),
            bg=CARD_LIGHT,
            fg=WHITE
        )

        temperature_label.pack(
            pady=3
        )

        condition_label = tk.Label(
            card,
            text=condition,
            font=("Segoe UI", 7),
            bg=CARD_LIGHT,
            fg=TEXT_MUTED,
            wraplength=90
        )

        condition_label.pack()


# Display forecasts

def display_forecasts():
    """Display hourly and daily forecasts."""

    clear_forecast_frames()

    if hourly_data:
        display_hourly_forecast()

    if forecast_data:

        forecast_list = forecast_data.get(
            "list",
            []
        )

        if forecast_list:
            display_daily_forecast(
                forecast_list
            )

    update_scroll_region()


# Forecast temperature update

def update_forecast_temperatures():
    """Update forecast temperatures after unit change."""

    if hourly_data or forecast_data:
        display_forecasts()


# Reset weather card

def reset_weather_display():
    """Reset weather information while loading."""

    location_label.config(
        text="Loading weather..."
    )

    temperature_label.config(
        text="--°C"
    )

    condition_label.config(
        text="Please wait..."
    )

    humidity_value.config(
        text="--"
    )

    wind_value.config(
        text="--"
    )

    weather_icon_label.config(
        image="",
        text="🌤"
    )

    weather_icon_label.image = None


# Get weather

def get_weather():
    """Fetch weather and forecast information."""

    global forecast_data
    global hourly_data

    location = city_entry.get().strip()

    if not location:

        show_status(
            "⚠ Please enter a city or PIN code.",
            "error"
        )

        return

    if not API_KEY:

        show_status(
            "⚠ OpenWeatherMap API key not found.",
            "error"
        )

        return

    reset_weather_display()

    show_status(
        "Fetching weather data...",
        "normal"
    )

    get_weather_button.config(
        state="disabled"
    )

    location_button.config(
        state="disabled"
    )

    root.update_idletasks()

    try:

        current_data = get_current_weather(
            location,
            API_KEY
        )

        display_weather(
            current_data
        )

        latitude = current_data[
            "coord"
        ]["lat"]

        longitude = current_data[
            "coord"
        ]["lon"]

        hourly_data = get_hourly_forecast(
            latitude,
            longitude
        )

        forecast_data = get_five_day_forecast(
            latitude,
            longitude,
            API_KEY
        )

        display_forecasts()

        show_status(
            "✓ Weather updated successfully.",
            "success"
        )

    except ValueError as error:

        show_status(
            f"⚠ {error}",
            "error"
        )

    except TimeoutError as error:

        show_status(
            f"⚠ {error}",
            "error"
        )

    except ConnectionError as error:

        show_status(
            f"⚠ {error}",
            "error"
        )

    except requests.exceptions.RequestException:

        show_status(
            "⚠ Unable to connect to the weather service.",
            "error"
        )

    except Exception:

        show_status(
            "⚠ Unable to retrieve weather data.",
            "error"
        )

    finally:

        get_weather_button.config(
            state="normal"
        )

        location_button.config(
            state="normal"
        )


# Automatic location

def use_my_location():
    """Detect approximate location using IP address."""

    show_status(
        "Detecting your approximate location...",
        "normal"
    )

    get_weather_button.config(
        state="disabled"
    )

    location_button.config(
        state="disabled"
    )

    root.update_idletasks()

    try:

        city = get_location_from_ip()

        city_entry.delete(
            0,
            tk.END
        )

        city_entry.insert(
            0,
            city
        )

        get_weather()

    except TimeoutError as error:

        show_status(
            f"⚠ {error}",
            "error"
        )

    except ConnectionError as error:

        show_status(
            f"⚠ {error}",
            "error"
        )

    except requests.exceptions.RequestException:

        show_status(
            "⚠ Unable to detect your location.",
            "error"
        )

    except Exception:

        show_status(
            "⚠ Unable to detect your location.",
            "error"
        )

    finally:

        get_weather_button.config(
            state="normal"
        )

        location_button.config(
            state="normal"
        )


# Scroll functions

def update_scroll_region():
    """Update the scrollable area."""

    scrollable_frame.update_idletasks()

    main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )


def on_mousewheel(event):
    """Scroll the application."""

    main_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


# Button hover effects

def button_enter(button):
    """Apply button hover effect."""

    button.config(
        bg=ACCENT_LIGHT
    )


def button_leave(button):
    """Remove button hover effect."""

    button.config(
        bg=ACCENT
    )


# Main window

root = tk.Tk()

root.title(
    "Weather App"
)

root.geometry(
    "760x900"
)

root.minsize(
    700,
    750
)

root.configure(
    bg=BG_TOP
)


# Gradient canvas

gradient_canvas = tk.Canvas(
    root,
    bg=BG_TOP,
    highlightthickness=0
)

gradient_canvas.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)


root.bind(
    "<Configure>",
    lambda event: draw_gradient()
)


# Main scrollable canvas

main_canvas = tk.Canvas(
    root,
    bg=BG_TOP,
    highlightthickness=0
)

main_canvas.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)


scrollbar = ttk.Scrollbar(
    root,
    orient="vertical",
    command=main_canvas.yview
)

scrollbar.place(
    relx=0.985,
    rely=0.04,
    relheight=0.92
)

main_canvas.configure(
    yscrollcommand=scrollbar.set
)


# Scrollable frame

scrollable_frame = tk.Frame(
    main_canvas,
    bg=BG_TOP
)

canvas_window = main_canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="n",
    width=720
)


scrollable_frame.bind(
    "<Configure>",
    lambda event: update_scroll_region()
)


def update_canvas_width(event):
    """Keep content centered and sized correctly."""

    width = max(
        event.width - 40,
        680
    )

    main_canvas.itemconfig(
        canvas_window,
        width=width
    )


main_canvas.bind(
    "<Configure>",
    update_canvas_width
)


main_canvas.bind_all(
    "<MouseWheel>",
    on_mousewheel
)


# Header

header = tk.Frame(
    scrollable_frame,
    bg=BG_TOP
)

header.pack(
    fill="x",
    pady=(35, 15)
)


title_label = tk.Label(
    header,
    text="🌤 Weather",
    font=("Segoe UI", 30, "bold"),
    bg=BG_TOP,
    fg=WHITE
)

title_label.pack()


subtitle_label = tk.Label(
    header,
    text="Beautiful weather information at a glance",
    font=("Segoe UI", 11),
    bg=BG_TOP,
    fg=TEXT_SECONDARY
)

subtitle_label.pack(
    pady=(3, 0)
)


# Search card

search_card = create_card(
    scrollable_frame
)

search_card.pack(
    fill="x",
    padx=25,
    pady=10
)


search_inner = tk.Frame(
    search_card,
    bg=CARD
)

search_inner.pack(
    fill="x",
    padx=20,
    pady=18
)


search_title = tk.Label(
    search_inner,
    text="Search Location",
    font=("Segoe UI", 12, "bold"),
    bg=CARD,
    fg=WHITE
)

search_title.pack(
    anchor="w",
    pady=(0, 8)
)


search_row = tk.Frame(
    search_inner,
    bg=CARD
)

search_row.pack(
    fill="x"
)


city_entry = tk.Entry(
    search_row,
    font=("Segoe UI", 12),
    bg="#334155",
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    bd=0
)

city_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=11,
    padx=(0, 10)
)


get_weather_button = tk.Button(
    search_row,
    text="Search",
    font=("Segoe UI", 11, "bold"),
    bg=ACCENT,
    fg=WHITE,
    activebackground=ACCENT_LIGHT,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=20,
    pady=9,
    command=get_weather
)

get_weather_button.pack(
    side="right"
)


get_weather_button.bind(
    "<Enter>",
    lambda event: button_enter(
        get_weather_button
    )
)

get_weather_button.bind(
    "<Leave>",
    lambda event: button_leave(
        get_weather_button
    )
)


location_button = tk.Button(
    search_inner,
    text="📍  Use My Location",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_LIGHT,
    fg=TEXT_SECONDARY,
    activebackground="#334155",
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=15,
    pady=7,
    command=use_my_location
)

location_button.pack(
    pady=(12, 0)
)


status_label = tk.Label(
    search_inner,
    text="Enter a city or PIN code to get started.",
    font=("Segoe UI", 9),
    bg=CARD_LIGHT,
    fg=TEXT_SECONDARY,
    padx=12,
    pady=7
)

status_label.pack(
    fill="x",
    pady=(12, 0)
)


# Main weather card

weather_card = create_card(
    scrollable_frame
)

weather_card.pack(
    fill="x",
    padx=25,
    pady=15
)


location_label = tk.Label(
    weather_card,
    text="Enter a location",
    font=("Segoe UI", 22, "bold"),
    bg=CARD,
    fg=WHITE
)

location_label.pack(
    pady=(22, 3)
)


condition_label = tk.Label(
    weather_card,
    text="Current Weather",
    font=("Segoe UI", 11),
    bg=CARD,
    fg=TEXT_SECONDARY
)

condition_label.pack()


weather_icon_label = tk.Label(
    weather_card,
    text="🌤",
    font=("Segoe UI Emoji", 60),
    bg=CARD,
    fg=WHITE
)

weather_icon_label.pack(
    pady=5
)


temperature_label = tk.Label(
    weather_card,
    text="--°C",
    font=("Segoe UI", 45, "bold"),
    bg=CARD,
    fg=WHITE
)

temperature_label.pack()


# Details

details_frame = tk.Frame(
    weather_card,
    bg=CARD
)

details_frame.pack(
    pady=18
)


humidity_box = tk.Frame(
    details_frame,
    bg=CARD_LIGHT,
    width=170,
    height=70
)

humidity_box.grid(
    row=0,
    column=0,
    padx=7
)

humidity_box.grid_propagate(False)


humidity_title = tk.Label(
    humidity_box,
    text="💧  Humidity",
    font=("Segoe UI", 9),
    bg=CARD_LIGHT,
    fg=TEXT_MUTED
)

humidity_title.pack(
    pady=(10, 0)
)


humidity_value = tk.Label(
    humidity_box,
    text="--",
    font=("Segoe UI", 12, "bold"),
    bg=CARD_LIGHT,
    fg=WHITE
)

humidity_value.pack()


wind_box = tk.Frame(
    details_frame,
    bg=CARD_LIGHT,
    width=170,
    height=70
)

wind_box.grid(
    row=0,
    column=1,
    padx=7
)

wind_box.grid_propagate(False)


wind_title = tk.Label(
    wind_box,
    text="💨  Wind Speed",
    font=("Segoe UI", 9),
    bg=CARD_LIGHT,
    fg=TEXT_MUTED
)

wind_title.pack(
    pady=(10, 0)
)


wind_value = tk.Label(
    wind_box,
    text="--",
    font=("Segoe UI", 12, "bold"),
    bg=CARD_LIGHT,
    fg=WHITE
)

wind_value.pack()


# Unit toggle

unit_frame = tk.Frame(
    weather_card,
    bg=CARD
)

unit_frame.pack(
    pady=(0, 22)
)


celsius_button = tk.Button(
    unit_frame,
    text="°C",
    font=("Segoe UI", 10, "bold"),
    bg=ACCENT,
    fg=WHITE,
    activebackground=ACCENT_LIGHT,
    activeforeground=WHITE,
    relief="sunken",
    bd=0,
    padx=15,
    pady=6,
    command=set_celsius
)

celsius_button.grid(
    row=0,
    column=0
)


fahrenheit_button = tk.Button(
    unit_frame,
    text="°F",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_LIGHT,
    fg=TEXT_SECONDARY,
    activebackground="#334155",
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    padx=15,
    pady=6,
    command=set_fahrenheit
)

fahrenheit_button.grid(
    row=0,
    column=1
)


# Hourly section

hourly_section = create_card(
    scrollable_frame
)

hourly_section.pack(
    fill="x",
    padx=25,
    pady=10
)


hourly_title = tk.Label(
    hourly_section,
    text="Next 6 Hours",
    font=("Segoe UI", 16, "bold"),
    bg=CARD,
    fg=WHITE
)

hourly_title.pack(
    anchor="w",
    padx=18,
    pady=(18, 8)
)


hourly_frame = tk.Frame(
    hourly_section,
    bg=CARD
)

hourly_frame.pack(
    padx=10,
    pady=(0, 15)
)


# Daily section

daily_section = create_card(
    scrollable_frame
)

daily_section.pack(
    fill="x",
    padx=25,
    pady=10
)


daily_title = tk.Label(
    daily_section,
    text="5-Day Forecast",
    font=("Segoe UI", 16, "bold"),
    bg=CARD,
    fg=WHITE
)

daily_title.pack(
    anchor="w",
    padx=18,
    pady=(18, 8)
)


daily_frame = tk.Frame(
    daily_section,
    bg=CARD
)

daily_frame.pack(
    padx=10,
    pady=(0, 15)
)


# Footer

footer = tk.Label(
    scrollable_frame,
    text="Powered by OpenWeatherMap & Open-Meteo",
    font=("Segoe UI", 9),
    bg=BG_TOP,
    fg=TEXT_MUTED
)

footer.pack(
    pady=(15, 30)
)


# Keyboard shortcut

city_entry.bind(
    "<Return>",
    lambda event: get_weather()
)


# Start

city_entry.focus()

root.update_idletasks()

draw_gradient()

root.mainloop()