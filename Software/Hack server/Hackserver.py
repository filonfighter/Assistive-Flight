import requests


def send_to_thingspeak(value, channel_id, write_key):
    # Tworzenie URL-a zapytania
    url = f"https://api.thingspeak.com/update?api_key={write_key}&field1={value}"

    try:
        # Wysłanie zapytania HTTP GET do Thingspeak
        response = requests.get(url)

        # Sprawdzenie czy zapytanie zostało pomyślnie przetworzone
        if response.status_code == 200:
            print("Dane wysłane pomyślnie do Thingspeak.")
        else:
            print("Wystąpił problem podczas wysyłania danych do Thingspeak.")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    # Ustawienia kanału Thingspeak
    channel_id = "2553609"
    write_key = "QGIU9SDZRRQQRG4O"

    # Wartość do wysłania na Thingspeak
    value_to_send = 93# Tutaj możesz wpisać dowolną wartość, którą chcesz wysłać

    # Wysłanie wartości do Thingspeak
    send_to_thingspeak(value_to_send, channel_id, write_key)
