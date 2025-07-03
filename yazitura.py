import tkinter as tk
from PIL import Image, ImageTk
import random

# --- Arayüz Renkleri ve Fontları ---
BG_COLOR = "#2c3e50"         # Koyu Mavi-Gri Arkaplan
FRAME_COLOR = "#34495e"      # Bir Ton Açık Mavi-Gri Frame
TEXT_COLOR = "#ecf0f1"       # Neredeyse Beyaz Metin
ACCENT_COLOR = "#3498db"     # Vurgu için Parlak Mavi
ACCENT_HOVER_COLOR = "#2980b9" # Vurgu Üzerine Gelme Rengi
WIN_COLOR = "#2ecc71"        # Yeşil (Kazanma)
LOSE_COLOR = "#e74c3c"       # Kırmızı (Kaybetme)
FONT_NORMAL = ("Segoe UI", 12)
FONT_BOLD = ("Segoe UI Bold", 14)
FONT_TITLE = ("Segoe UI Black", 22)


# --- Pencere Kurulumu ---
pencere = tk.Tk()
pencere.title("Yazı Tura")
pencere.geometry("400x600")
pencere.resizable(False, False)
pencere.config(bg=BG_COLOR)

# --- Değişkenler ---
# Sadece kullanıcının tahminini tutmak için bir değişken yeterli.
tahmin = tk.StringVar(value="Yazı")

# --- Görseller ---
# Lütfen bu dosya yollarının kendi bilgisayarınızda doğru olduğundan emin olun.
try:
    yazi_path = r"C:\Users\Dembaba\Desktop\çalışmalar\python denemelik\yazitura\yazi.png"
    tura_path = r"C:\Users\Dembaba\Desktop\çalışmalar\python denemelik\yazitura\tura.png"

    yazi_img_orig = Image.open(yazi_path).resize((200, 200))
    tura_img_orig = Image.open(tura_path).resize((200, 200))
except FileNotFoundError:
    print("Hata: Resim dosyaları bulunamadı. Lütfen dosya yollarını kontrol edin.")
    # Dosyalar bulunamazsa programın çökmemesi için geçici görseller oluşturalım
    yazi_img_orig = Image.new("RGB", (200, 200), "skyblue")
    tura_img_orig = Image.new("RGB", (200, 200), "salmon")
    from PIL import ImageDraw, ImageFont
    draw_yazi = ImageDraw.Draw(yazi_img_orig)
    draw_tura = ImageDraw.Draw(tura_img_orig)
    try:
        font = ImageFont.truetype("arialbd.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
    draw_yazi.text((55, 75), "YAZI", fill="black", font=font)
    draw_tura.text((55, 75), "TURA", fill="black", font=font)

def create_edge_image(height=8, width=200):
    return Image.new("RGBA", (width, height), (192, 192, 192, 255))

edge_img = create_edge_image()

yazi_tk = ImageTk.PhotoImage(yazi_img_orig)
tura_tk = ImageTk.PhotoImage(tura_img_orig)
edge_tk = ImageTk.PhotoImage(edge_img)

current_img_orig = yazi_img_orig
current_img_tk = yazi_tk

# --- Frame'ler ---
# Frame'lere arkaplan rengi vererek temayı uygula
orta_frame = tk.Frame(pencere, bg=BG_COLOR)
orta_frame.pack(expand=True, pady=(30, 10))

alt_frame = tk.Frame(pencere, bg=BG_COLOR)
alt_frame.pack(pady=20, padx=20, fill='x')

# --- Widget'lar (Arayüze uygun şekilde stillendirildi) ---
img_label = tk.Label(orta_frame, bg=BG_COLOR)
img_label.pack(expand=True)

sonuc_label = tk.Label(alt_frame, text="SONUÇ", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR)
sonuc_label.pack(pady=20)

# Tahmin seçimi
tahmin_frame = tk.Frame(alt_frame, bg=BG_COLOR)
tahmin_frame.pack(pady=10)
tk.Label(tahmin_frame, text="Tahminin:", font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR).pack(side=tk.LEFT, padx=10)

# Radiobutton'ları daha şık hale getirelim
radio_style = {"variable": tahmin, "font": FONT_NORMAL, "bg": BG_COLOR, "fg": TEXT_COLOR,
               "activebackground": BG_COLOR, "activeforeground": ACCENT_COLOR,
               "selectcolor": FRAME_COLOR}
tk.Radiobutton(tahmin_frame, text="Yazı", value="Yazı", **radio_style).pack(side=tk.LEFT)
tk.Radiobutton(tahmin_frame, text="Tura", value="Tura", **radio_style).pack(side=tk.LEFT)

# Ana buton (daha şık bir görünümle)
buton = tk.Button(alt_frame, text="Parayı At!", font=FONT_BOLD,
                  bg=ACCENT_COLOR, fg="white", relief=tk.FLAT,
                  activebackground=ACCENT_HOVER_COLOR, activeforeground="white",
                  command=lambda: animate_flip(), width=15, pady=5)
buton.pack(pady=25)

# --- Buton Hover Efektleri ---
def on_enter(e):
    buton.config(bg=ACCENT_HOVER_COLOR)
def on_leave(e):
    buton.config(bg=ACCENT_COLOR)

buton.bind("<Enter>", on_enter)
buton.bind("<Leave>", on_leave)

# --- FONKSİYONLAR ---
def animate_flip(step=0, max_steps=20):
    global current_img_orig, current_img_tk

    # Animasyon sırasında butonu ve radiobuttonları devre dışı bırak
    if step == 0:
        buton.config(state=tk.DISABLED, bg=FRAME_COLOR) # Buton rengini soluklaştır
        for widget in tahmin_frame.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.config(state=tk.DISABLED)
        sonuc_label.config(text="...", fg=TEXT_COLOR)

    # Animasyon döngüsü (oranları değiştirerek daha hızlı bir dönüş efekti)
    phase = step % 8
    if phase in [0, 7]:
        img_tk = current_img_tk
    elif phase in [1, 6]:
        w, h = current_img_orig.size
        squeezed = current_img_orig.resize((w, int(h * 0.6)))
        img_tk = ImageTk.PhotoImage(squeezed)
    elif phase in [2, 5]:
        w, h = current_img_orig.size
        squeezed = current_img_orig.resize((w, int(h * 0.2)))
        img_tk = ImageTk.PhotoImage(squeezed)
    else: # phase 3 veya 4
        img_tk = edge_tk

    img_label.config(image=img_tk)
    img_label.image = img_tk

    if step < max_steps:
        pencere.after(40, animate_flip, step + 1, max_steps)
    else:
        # Animasyon bitti, sonucu belirle
        sonuc = random.choice(["Yazı", "Tura"])
        current_img_orig = yazi_img_orig if sonuc == "Yazı" else tura_img_orig
        current_img_tk = yazi_tk if sonuc == "Yazı" else tura_tk
        img_label.config(image=current_img_tk)
        img_label.image = current_img_tk

        # Sonucu göster
        if sonuc == tahmin.get():
            sonuc_label.config(text=f"KAZANDIN! ({sonuc})", fg=WIN_COLOR)
        else:
            sonuc_label.config(text=f"KAYBETTİN! ({sonuc})", fg=LOSE_COLOR)

        # Butonu ve radiobuttonları tekrar aktif et
        buton.config(state=tk.NORMAL, bg=ACCENT_COLOR)
        for widget in tahmin_frame.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.config(state=tk.NORMAL)


# --- Başlangıç Ayarları ---
img_label.config(image=yazi_tk)
img_label.image = yazi_tk

pencere.mainloop()