from machine import Pin, SPI, PWM # type: ignore
import framebuf # type: ignore
import time
import network
import urequests
import math
import utime

# Konfiguracja Wi-Fi
SSID = 'biuro'
PASSWORD = '8521Morek14'

namessid = ["biuro", "Hotspot1", "Wojtek"]
router_positions = [(0, 0), (0, 10), (10, 0)]
A = -40  # Przykładowa wartość RSSI w odległości 1 metra
n = 2  # Przykładowy współczynnik tłumienia
disc = 0

# Konfiguracja ThingSpeak
CHANNEL_ID = '2553609'
READ_API_KEY = 'ZSALT2L6973X8QNU'
THINGSPEAK_URL = 'https://api.thingspeak.com/channels/{}/feeds/last.json?api_key={}'.format(CHANNEL_ID, READ_API_KEY)

BL = 13
DC = 7
RST = 12
MOSI = 11
SCK = 10
CS = 9

delay = 0

led_pin = machine.Pin(15, machine.Pin.OUT)


def blink_led(pin, duration=0.5, times=2):
    for _ in range(times):
        pin.value(1)  # Włączenie diody LED
        utime.sleep(0.8)
        pin.value(0)  # Wyłączenie diody LED
        utime.sleep(0.2)
        pin.value(1)  # Włączenie diody LED
        utime.sleep(0.8)
        pin.value(0)  # Wyłączenie diody LED
        utime.sleep(0.2)
        pin.value(1)  # Włączenie diody LED
        utime.sleep(0.2)
        pin.value(0)
        utime.sleep(1)


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Łączenie z siecią WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Połączono z siecią WiFi:', ssid)

def get_data_from_thingspeak():
    try:
        response = urequests.get(THINGSPEAK_URL)
        data = response.json()
        response.close()
        return data
    except Exception as e:
        print('Błąd podczas pobierania danych z ThingSpeak:', e)
        return None

def main():
    connect_wifi(SSID, PASSWORD)
    return
        
def calculate_distance(rssi):
    """Oblicz odległość na podstawie RSSI."""
    return 10 ** ((A - rssi) / (10 * n))

def scan_networks():
    wlan = network.WLAN(network.STA_IF)  # Używamy trybu stacji (klienta)
    wlan.active(True)  # Aktywujemy interfejs Wi-Fi

    networks = wlan.scan()  # Skanujemy dostępne sieci Wi-Fi

    distances = [None, None, None]  # Lista na odległości do znanych routerów

    for net in networks:
        ssid = net[0].decode('utf-8')  # SSID (nazwa sieci)
        rssi = net[3]  # RSSI (siła sygnału)

        if ssid in namessid:
            index = namessid.index(ssid)
            distances[index] = calculate_distance(rssi)
            print(f'SSID: {ssid}, RSSI: {rssi}, Distance: {distances[index]:.2f} meters')

    return distances

def calculate_position(router_positions, distances):
    """Oblicz pozycję na podstawie pozycji routerów i odległości."""
    if None in distances:
        return None  # Jeśli którejś z odległości brakuje, nie możemy obliczyć pozycji

    x1, y1 = router_positions[0]
    x2, y2 = router_positions[1]
    x3, y3 = router_positions[2]

    d1, d2, d3 = distances

    # Wyznaczanie współrzędnych metodą triangulacji
    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    C = d1**2 - d2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2 * (x3 - x2)
    E = 2 * (y3 - y2)
    F = d2**2 - d3**2 - x2**2 + x3**2 - y2**2 + y3**2

    if (E * A - B * D) == 0:
        return None  # Unikamy dzielenia przez zero

    y = (C * D - A * F) / (E * A - B * D)
    if A != 0:
        x = (C - B * y) / A
    elif D != 0:
        x = (F - E * y) / D
    else:
        return None

    return (x, y)

def degrees_from_tangent(tangent_value):
    # Obliczanie arcustangensa (kąta w radianach)
    angle_radians = math.atan(tangent_value)
    # Konwersja kąta z radianów na stopnie
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees


class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 135
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    black = 0x0000

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
    
    def draw_thick_line(self, x0, y0, length, angle, color, thickness):
        """Draw a thick line at a given angle."""
        for i in range(thickness):
            x1 = x0 + length * math.cos(angle) + i
            y1 = y0 + length * math.sin(angle) + i
            self.line(round(x0), round(y0), round(x1), round(y1), color)
            
    def clear(self):
        """Wyczyść ekran, zapełniając cały bufor kolorem czarnym."""
        self.fill(0x0000)  # Czarny kolor

    def draw_thick_arrow(self, x, y, length, angle, color, thickness):
        """Draw a thick arrow."""
        for i in range(thickness):
            x0 = x - length * math.cos(angle) / 2 + i
            y0 = y - length * math.sin(angle) / 2 + i
            x1 = x + length * math.cos(angle) / 2 + i
            y1 = y + length * math.sin(angle) / 2 + i
            self.draw_thick_line(x0, y0, length, angle, color, thickness)  # shaft
            self.draw_thick_line(x1, y1, length / 3, angle - 5 * math.pi / 6, color, thickness)  # arrowhead
            self.draw_thick_line(x1, y1, length / 3, angle + 5 * math.pi / 6, color, thickness)  # arrowhead

BB = 0;    
    
if __name__=='__main__':
    LCD = LCD_1inch14()
    main()
    angle = 0  # initialize angle

    while(1):
        LCD.fill(LCD.black)
        distances = scan_networks()  # Skanuj dostępne sieci Wi-Fi i oblicz odległości
        if None not in distances:
            position = calculate_position(router_positions, distances)
            if position:
                print(f"Estimated position: {position}")
                x, y = position
                if y > 5:
                    tga = y - 5
                    tga = tga / x
                    anglea = degrees_from_tangent(tga)
                    print(f"Kąt A: {anglea} stopni")
                    disc = y-5
                    disc = disc**2 + x**2
                    disc = disc**0.5
                elif y < 5:
                    tgb = 5 - y
                    tgb = tgb / x
                    angleb = degrees_from_tangent(tgb)
                    anglea = 180 - angleb
                    print(f"Kąt B: {angleb} stopni")
                    print(f"Kąt A: {anglea} stopni")
                    disc = 5 - y
                    disc = disc**2 + x**2
                    disc = disc**0.5
            else:
                print("Error calculating position.")
        else:
            print("Not all routers found.")
        data = get_data_from_thingspeak()
        if data and 'field1' in data:
            field1_value = data['field1']
            print('Wartość pola field1:', field1_value)
            # Tutaj możesz umieścić kod do przetwarzania wartości pola field1
        times = int(field1_value)
        if times > 0:
            LCD.clear()
            led_pin.value(0)
            print("Bardziej cool")
            times2 = str(times)
            text = times2
            text_width = len(text) * 8  # assuming each character is 8 pixels wide
            LCD.text(text, round((LCD.width - text_width) / 2), 70, LCD.blue)
            #LCD.show()
            text = "Remaining time to enter:"
            text_width = len(text) * 8  # assuming each character is 8 pixels wide
            LCD.text(text, round((LCD.width - text_width) / 2), 40, LCD.blue)
            #LCD.show()
            text = "minutes"
            text_width = len(text) * 8  # assuming each character is 8 pixels wide
            LCD.text(text, round((LCD.width - text_width) / 2), 80, LCD.blue)
            text = "Flight delayed"
            text_width = len(text) * 8  # assuming each character is 8 pixels wide
            if delay == 1:
                LCD.text(text, round((LCD.width - text_width) / 2), 100, LCD.red)
            LCD.show()
            time.sleep(0.1)
            BB == 0
            
            
        elif times <= 0:
            print("cool")
            if BB == 0:
                blink_led(led_pin)
                BB == 1
                
            text = "Go to: Gate 1"
            text_width = len(text) * 8  # assuming each character is 8 pixels wide
            LCD.text(text, round((LCD.width - text_width) / 2), 10, LCD.blue)
            disc2 = str(disc)
            disc2 = disc2[:-6]
            text = "Distance: "
            print(disc2)
            text_width = len(text) * 8  # assuming each character is 8 pixels wide
            LCD.text(text, round((LCD.width - text_width) / 4), 120, LCD.blue)
            text = disc2
            text_width = len(text) * 8  # assuming each character is 8 pixels wide
            LCD.text(text, round((LCD.width - text_width) / 2), 120, LCD.blue)
            text =" Meters"
            text_width = len(text) * 8  # assuming each character is 8 pixels wide
            LCD.text(text, round((LCD.width - text_width) / 1.5), 120, LCD.blue)
            LCD.draw_thick_arrow(round(LCD.width / 2), round(LCD.height / 2), 75, angle, LCD.blue, 3)
            LCD.show()
            time.sleep(0.1)
            
        
        angle += math.pi / 30  # rotate by 6 degrees
        
