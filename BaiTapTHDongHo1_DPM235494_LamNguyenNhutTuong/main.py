{
  "version": 1,
    "author": "LamNguyenNhutTuongdz",
  "editor": "wokwi",
  "parts": [
    { "type": "wokwi-breadboard", "id": "bb1", "top": -89.4, "left": -534.8, "attrs": {} },
    {
      "type": "board-esp32-devkit-c-v4",
      "id": "esp",from machine import Pin, PWM, ADC
from time import sleep_ms


HANDS = {
    "gio":  (34, 13, 12, 12),   # 12 vạch giờ  -> mỗi vạch 30°
    "phut": (35, 14, 27, 60),   # 60 vạch phút -> mỗi vạch 6°
    "giay": (32, 26, 25, 60),   # 60 vạch giây -> mỗi vạch 6°
}

ADC_MAX = 4095          #ADC 12-bit của ESP32
NGUONG_LOI = 15         #đọc dưới ngưỡng này coi như không hoạt động -> số 12


#Điều khiển servo
class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin), freq=50)
        self.goc = None

    def quay(self, goc):
        goc = max(0, min(180, goc))
        if self.goc is not None and abs(goc - self.goc) < 1:
            return                          # tránh rung servo
        # xung 0.5ms..2.5ms trong chu kỳ 20ms (duty_u16: 1638..8192)
        duty = int(1638 + (goc / 180) * (8192 - 1638))
        self.pwm.duty_u16(duty)
        self.goc = goc


# Một kim = một cặp servo 
class Kim:
    def __init__(self, pin_adc, pin_a, pin_b, so_vach):
        self.adc = ADC(Pin(pin_adc))
        self.adc.atten(ADC.ATTN_11DB)       # đo đến ~3.3V
        self.A = Servo(pin_a)               # nửa phải: 12 -> 6
        self.B = Servo(pin_b)               # nửa trái: 6 -> 12
        self.so_vach = so_vach
        self.chi_so_12()

    def chi_so_12(self):
        self.A.quay(0)                      # A: 0°   = số 12
        self.B.quay(180)                    # B: 180° = số 12

    def doc_gia_tri(self):
        """Trung bình 8 lần đọc; trả None nếu biến trở lỗi."""
        try:
            tong = 0
            for _ in range(8):
                tong += self.adc.read()
            gt = tong // 8
        except Exception:
            return None
        if gt < NGUONG_LOI:
            return None                     # không hoạt động
        return gt

    def cap_nhat(self):
        gt = self.doc_gia_tri()
        if gt is None:
            self.chi_so_12()
            return 0

        vach = int(gt * self.so_vach / (ADC_MAX + 1))   # 0 .. so_vach-1
        theta = vach * 360 / self.so_vach               # góc trên mặt đồng hồ

        if theta <= 180:                    # nửa phải: servo A làm việc
            self.A.quay(theta)
            self.B.quay(180)                # B đỗ ở số 12
        else:                               # nửa trái: servo B làm việc
            self.B.quay(theta - 180)
            self.A.quay(0)                  # A đỗ ở số 12
        return vach


#  Chương trình chính
gio  = Kim(*HANDS["gio"])
phut = Kim(*HANDS["phut"])
giay = Kim(*HANDS["giay"])

while True:
    h = gio.cap_nhat()
    m = phut.cap_nhat()
    s = giay.cap_nhat()

    # 12:00:00 đúng -> cả 6 động cơ chỉ số 12
    if h == 0 and m == 0 and s == 0:
        for kim in (gio, phut, giay):
            kim.chi_so_12()

    print("Thoi gian: {:02d}:{:02d}:{:02d}".format(h if h else 12, m, s))
    sleep_ms(100)from machine import Pin, PWM, ADC
from time import sleep_ms


HANDS = {
    "gio":  (34, 13, 12, 12),   # 12 vạch giờ  -> mỗi vạch 30°
    "phut": (35, 14, 27, 60),   # 60 vạch phút -> mỗi vạch 6°
    "giay": (32, 26, 25, 60),   # 60 vạch giây -> mỗi vạch 6°
}

ADC_MAX = 4095          #ADC 12-bit của ESP32
NGUONG_LOI = 15         #đọc dưới ngưỡng này coi như không hoạt động -> số 12


#Điều khiển servo
class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin), freq=50)
        self.goc = None

    def quay(self, goc):
        goc = max(0, min(180, goc))
        if self.goc is not None and abs(goc - self.goc) < 1:
            return                          # tránh rung servo
        # xung 0.5ms..2.5ms trong chu kỳ 20ms (duty_u16: 1638..8192)
        duty = int(1638 + (goc / 180) * (8192 - 1638))
        self.pwm.duty_u16(duty)
        self.goc = goc


# Một kim = một cặp servo 
class Kim:
    def __init__(self, pin_adc, pin_a, pin_b, so_vach):
        self.adc = ADC(Pin(pin_adc))
        self.adc.atten(ADC.ATTN_11DB)       # đo đến ~3.3V
        self.A = Servo(pin_a)               # nửa phải: 12 -> 6
        self.B = Servo(pin_b)               # nửa trái: 6 -> 12
        self.so_vach = so_vach
        self.chi_so_12()

    def chi_so_12(self):
        self.A.quay(0)                      # A: 0°   = số 12
        self.B.quay(180)                    # B: 180° = số 12

    def doc_gia_tri(self):
        """Trung bình 8 lần đọc; trả None nếu biến trở lỗi."""
        try:
            tong = 0
            for _ in range(8):
                tong += self.adc.read()
            gt = tong // 8
        except Exception:
            return None
        if gt < NGUONG_LOI:
            return None                     # không hoạt động
        return gt

    def cap_nhat(self):
        gt = self.doc_gia_tri()
        if gt is None:
            self.chi_so_12()
            return 0

        vach = int(gt * self.so_vach / (ADC_MAX + 1))   # 0 .. so_vach-1
        theta = vach * 360 / self.so_vach               # góc trên mặt đồng hồ

        if theta <= 180:                    # nửa phải: servo A làm việc
            self.A.quay(theta)
            self.B.quay(180)                # B đỗ ở số 12
        else:                               # nửa trái: servo B làm việc
            self.B.quay(theta - 180)
            self.A.quay(0)                  # A đỗ ở số 12
        return vach


#  Chương trình chính
gio  = Kim(*HANDS["gio"])
phut = Kim(*HANDS["phut"])
giay = Kim(*HANDS["giay"])

while True:
    h = gio.cap_nhat()
    m = phut.cap_nhat()
    s = giay.cap_nhat()

    # 12:00:00 đúng -> cả 6 động cơ chỉ số 12
    if h == 0 and m == 0 and s == 0:
        for kim in (gio, phut, giay):
            kim.chi_so_12()

    print("Thoi gian: {:02d}:{:02d}:{:02d}".format(h if h else 12, m, s))
    sleep_ms(100)
      "top": -105.6,
      "left": 196.84,
      "attrs": { "env": "micropython-20231227-v1.22.0" }
    },
    { "type": "wokwi-potentiometer", "id": "pot_gio", "top": -260.5, "left": -38.6, "attrs": {} },
    {
      "type": "wokwi-potentiometer",
      "id": "pot_phut",
      "top": -260.5,
      "left": -115.4,
      "attrs": {}
    },
    {
      "type": "wokwi-potentiometer",
      "id": "pot_giay",
      "top": -260.5,
      "left": -192.2,
      "attrs": {}
    },
    {
      "type": "wokwi-servo",
      "id": "sv_giay_b",
      "top": 236.2,
      "left": -555.8,
      "rotate": 90,
      "attrs": {}
    },
    {
      "type": "wokwi-servo",
      "id": "sv_giay_a",
      "top": 236.2,
      "left": -459.8,
      "rotate": 90,
      "attrs": {}
    },
    {
      "type": "wokwi-servo",
      "id": "sv_phut_b",
      "top": 236.2,
      "left": -315.8,
      "rotate": 90,
      "attrs": {}
    },
    {
      "type": "wokwi-servo",
      "id": "sv_phut_a",
      "top": 236.2,
      "left": -229.4,
      "rotate": 90,
      "attrs": {}
    },
    {
      "type": "wokwi-servo",
      "id": "sv_gio_b",
      "top": 236.2,
      "left": -75.8,
      "rotate": 90,
      "attrs": {}
    },
    {
      "type": "wokwi-servo",
      "id": "sv_gio_a",
      "top": 236.2,
      "left": 1,
      "rotate": 90,
      "attrs": {}
    }
  ],
  "connections": [
    [ "esp:TX", "$serialMonitor:RX", "", [] ],
    [ "esp:RX", "$serialMonitor:TX", "", [] ],
    [ "esp:3V3", "bb1:tp.50", "red", [ "h-67.05", "v-57.6" ] ],
    [ "pot_gio:VCC", "bb1:tp.45", "red", [ "v0" ] ],
    [ "pot_gio:GND", "bb1:tn.43", "black", [ "v0" ] ],
    [ "pot_phut:GND", "bb1:tn.36", "black", [ "v0" ] ],
    [ "pot_phut:VCC", "bb1:tp.38", "red", [ "v0" ] ],
    [ "pot_giay:VCC", "bb1:tp.31", "red", [ "v0" ] ],
    [ "pot_giay:GND", "bb1:tn.30", "black", [ "v0" ] ],
    [ "pot_giay:SIG", "bb1:38t.a", "purple", [ "v0" ] ],
    [ "pot_phut:SIG", "bb1:46t.a", "blue", [ "v0" ] ],
    [ "esp:32", "bb1:38t.d", "green", [ "h-19.05", "v9.6", "h9.6" ] ],
    [ "esp:35", "bb1:46t.c", "blue", [ "h-28.65", "v9.6" ] ],
    [ "pot_gio:SIG", "bb1:54t.a", "green", [ "v0" ] ],
    [ "esp:34", "bb1:54t.b", "green", [ "h-38.25", "v9.6" ] ],
    [ "esp:5V", "bb1:bp.50", "red", [ "h0" ] ],
    [ "esp:GND.2", "bb1:tn.48", "black", [ "v-38.4", "h-248.8" ] ],
    [ "esp:GND.3", "bb1:bn.50", "black", [ "h9.6", "v134.4" ] ],
    [ "sv_giay_b:V+", "bb1:bp.3", "red", [ "v0" ] ],
    [ "sv_giay_a:V+", "bb1:bp.11", "red", [ "v0" ] ],
    [ "sv_phut_b:V+", "bb1:bp.24", "red", [ "v0" ] ],
    [ "bb1:bn.4", "sv_giay_b:GND", "black", [ "v0" ] ],
    [ "sv_giay_a:GND", "bb1:bn.12", "black", [ "v0" ] ],
    [ "sv_phut_b:GND", "bb1:bn.25", "black", [ "v0" ] ],
    [ "sv_phut_a:V+", "bb1:bp.31", "red", [ "v0" ] ],
    [ "sv_phut_a:GND", "bb1:bn.32", "black", [ "v0" ] ],
    [ "sv_gio_b:V+", "bb1:bp.41", "red", [ "v-48", "h-38.5", "v-67.2" ] ],
    [ "sv_gio_b:GND", "bb1:bn.42", "black", [ "v-57.6", "h-38.4" ] ],
    [ "sv_giay_b:PWM", "bb1:4b.j", "orange", [ "v0" ] ],
    [ "esp:25", "bb1:4t.e", "orange", [ "v0" ] ],
    [ "bb1:4b.f", "bb1:4t.e", "orange", [ "v0" ] ],
    [ "sv_giay_a:PWM", "bb1:14b.j", "yellow", [ "v0" ] ],
    [ "esp:26", "bb1:14b.f", "yellow", [ "h0" ] ],
    [ "sv_phut_b:PWM", "bb1:29b.j", "cyan", [ "v0" ] ],
    [ "esp:27", "bb1:29b.f", "cyan", [ "h0" ] ],
    [ "sv_phut_a:PWM", "bb1:38b.j", "magenta", [ "v0" ] ],
    [ "esp:14", "bb1:38b.f", "magenta", [ "h0" ] ],
    [ "sv_gio_b:PWM", "bb1:50b.j", "gold", [ "v-38.4", "h-38.6" ] ],
    [ "esp:12", "bb1:50b.g", "gold", [ "v0" ] ],
    [ "sv_gio_a:GND", "bb1:bn.48", "black", [ "v-57.6", "h-48" ] ],
    [ "sv_gio_a:V+", "bb1:bp.47", "red", [ "v-48", "h-0.1" ] ],
    [ "sv_gio_a:PWM", "bb1:57b.j", "green", [ "v-38.4", "h-48.2" ] ],
    [ "esp:13", "bb1:57b.i", "green", [ "h0" ] ]
  ],
  "dependencies": {}
}