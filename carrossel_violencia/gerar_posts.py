# -*- coding: utf-8 -*-
"""
Carrossel Instagram - Violência contra Médicos
SINMEVAÇO - Design Profissional
1080x1080px - Fonte Quicksand
"""

import os
import sys
import subprocess
import urllib.request

def install_packages():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pillow', '-q'])

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    install_packages()
    from PIL import Image, ImageDraw, ImageFont

# Diretórios
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(WORK_DIR, "posts_png")
FONT_DIR = os.path.join(WORK_DIR, "fonts")

# URL da logo
LOGO_URL = "https://storage.googleapis.com/msgsndr/0Def8kzJShLPuKrPk5Jw/media/6949c4f879fc965317e1ca2c.jpeg"
LOGO_PATH = os.path.join(WORK_DIR, "logo_sinmevaco.jpg")

# Cores sólidas
VERDE = (27, 122, 74)
VERDE_ESCURO = (18, 85, 52)
VERDE_CLARO = (144, 238, 144)
VERMELHO = (220, 53, 53)
LARANJA = (255, 152, 0)
BRANCO = (255, 255, 255)
CINZA_BG = (248, 249, 250)
PRETO = (33, 37, 41)
CINZA = (108, 117, 125)
CINZA_CLARO = (173, 181, 189)

# Quicksand font URLs - usando fontsource CDN
QUICKSAND_URLS = {
    'regular': 'https://cdn.jsdelivr.net/fontsource/fonts/quicksand@latest/latin-400-normal.ttf',
    'medium': 'https://cdn.jsdelivr.net/fontsource/fonts/quicksand@latest/latin-500-normal.ttf',
    'semibold': 'https://cdn.jsdelivr.net/fontsource/fonts/quicksand@latest/latin-600-normal.ttf',
    'bold': 'https://cdn.jsdelivr.net/fontsource/fonts/quicksand@latest/latin-700-normal.ttf',
}

def download_file(url, path):
    """Baixa arquivo da URL"""
    if not os.path.exists(path):
        print(f"  Baixando: {os.path.basename(path)}...")
        try:
            urllib.request.urlretrieve(url, path)
            return True
        except Exception as e:
            print(f"  Erro ao baixar: {e}")
            return False
    return True

def setup_fonts():
    """Baixa fontes Quicksand se necessário"""
    os.makedirs(FONT_DIR, exist_ok=True)
    for weight, url in QUICKSAND_URLS.items():
        path = os.path.join(FONT_DIR, f"Quicksand-{weight.capitalize()}.ttf")
        download_file(url, path)

def download_logo():
    """Baixa logo se necessário"""
    if not os.path.exists(LOGO_PATH):
        print("  Baixando logo...")
        try:
            urllib.request.urlretrieve(LOGO_URL, LOGO_PATH)
            return True
        except Exception as e:
            print(f"  Erro ao baixar logo: {e}")
            return False
    return True

def get_font(size, bold=False):
    """Retorna fonte Quicksand"""
    if bold:
        font_path = os.path.join(FONT_DIR, "Quicksand-Bold.ttf")
    else:
        font_path = os.path.join(FONT_DIR, "Quicksand-Regular.ttf")

    try:
        return ImageFont.truetype(font_path, size)
    except:
        # Fallback para fontes do sistema
        fallbacks = [
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ]
        for f in fallbacks:
            try:
                return ImageFont.truetype(f, size)
            except:
                pass
        return ImageFont.load_default()

def get_font_medium(size):
    """Retorna fonte Quicksand Medium"""
    font_path = os.path.join(FONT_DIR, "Quicksand-Medium.ttf")
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return get_font(size, False)

def get_font_semibold(size):
    """Retorna fonte Quicksand SemiBold"""
    font_path = os.path.join(FONT_DIR, "Quicksand-Semibold.ttf")
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return get_font(size, True)

def rounded_rect(draw, box, radius, fill):
    """Retângulo arredondado sólido"""
    x1, y1, x2, y2 = box
    r = min(radius, (y2-y1)//2, (x2-x1)//2)
    draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
    draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)
    draw.ellipse([x1, y1, x1+2*r, y1+2*r], fill=fill)
    draw.ellipse([x2-2*r, y1, x2, y1+2*r], fill=fill)
    draw.ellipse([x1, y2-2*r, x1+2*r, y2], fill=fill)
    draw.ellipse([x2-2*r, y2-2*r, x2, y2], fill=fill)

def add_logo(img, x, y, size):
    """Adiciona logo circular"""
    try:
        logo = Image.open(LOGO_PATH)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')

        # Redimensionar
        logo.thumbnail((size, size), Image.Resampling.LANCZOS)
        lw, lh = logo.size

        # Máscara circular
        circle_size = min(lw, lh)
        mask = Image.new('L', (circle_size, circle_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, circle_size-1, circle_size-1], fill=255)

        # Recortar em círculo
        logo_cropped = logo.crop((
            (lw - circle_size) // 2,
            (lh - circle_size) // 2,
            (lw + circle_size) // 2,
            (lh + circle_size) // 2
        ))

        output = Image.new('RGBA', (circle_size, circle_size), (0, 0, 0, 0))
        output.paste(logo_cropped, (0, 0))
        output.putalpha(mask)

        paste_x = x - circle_size // 2
        paste_y = y - circle_size // 2
        img.paste(output, (paste_x, paste_y), output)
    except Exception as e:
        print(f"Erro logo: {e}")

def add_logo_corner(img, x, y, size):
    """Adiciona logo no canto circular"""
    try:
        logo = Image.open(LOGO_PATH)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        logo.thumbnail((size, size), Image.Resampling.LANCZOS)
        lw, lh = logo.size

        circle_size = min(lw, lh)
        mask = Image.new('L', (circle_size, circle_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, circle_size-1, circle_size-1], fill=255)

        logo_cropped = logo.crop((
            (lw - circle_size) // 2,
            (lh - circle_size) // 2,
            (lw + circle_size) // 2,
            (lh + circle_size) // 2
        ))

        output = Image.new('RGBA', (circle_size, circle_size), (0, 0, 0, 0))
        output.paste(logo_cropped, (0, 0))
        output.putalpha(mask)

        img.paste(output, (x, y), output)
    except Exception as e:
        print(f"Erro logo: {e}")

def center_text(draw, text, y, font, color, width=1080):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, y), text, font=font, fill=color)

def page_dots(draw, current, total, x, y, active_color, inactive_color):
    for i in range(total):
        px = x + i * 20
        if i == current - 1:
            rounded_rect(draw, [px, y, px+28, y+8], 4, active_color)
        else:
            draw.ellipse([px+8, y, px+16, y+8], fill=inactive_color)

# ============================================================================
# SLIDE 1 - CAPA
# ============================================================================
def slide1_capa():
    img = Image.new('RGB', (1080, 1080), VERDE)
    draw = ImageDraw.Draw(img)

    # Faixa decorativa superior
    draw.rectangle([0, 0, 1080, 8], fill=VERDE_CLARO)

    # Badge ALERTA
    rounded_rect(draw, [800, 50, 1030, 100], 25, VERMELHO)
    f = get_font(18, True)
    draw.text((915, 65), "ALERTA", font=f, fill=BRANCO, anchor="mm")

    # Logo centralizada
    add_logo(img, 540, 220, 200)

    # VIOLÊNCIA - título principal
    f = get_font(90, True)
    center_text(draw, "VIOLÊNCIA", 420, f, BRANCO)

    # Box destaque
    rounded_rect(draw, [120, 530, 960, 640], 16, VERDE_ESCURO)
    f = get_font(75, True)
    center_text(draw, "CONTRA MÉDICOS", 545, f, VERDE_CLARO)

    # Subtítulo
    f = get_font_medium(28)
    center_text(draw, "A categoria precisa de proteção.", 700, f, BRANCO)
    f = get_font(28, True)
    center_text(draw, "Sua voz é fundamental!", 745, f, BRANCO)

    # Localização
    rounded_rect(draw, [350, 830, 730, 885], 28, VERDE_ESCURO)
    f = get_font(24, True)
    draw.text((540, 848), "Ipatinga e Região", font=f, fill=BRANCO, anchor="mm")

    # Rodapé
    draw.line([50, 1000, 1030, 1000], fill=VERDE_ESCURO, width=2)
    f = get_font_medium(16)
    draw.text((50, 1025), "Arraste para saber mais", font=f, fill=VERDE_CLARO)
    draw.text((280, 1025), ">>>", font=f, fill=VERDE_CLARO)

    # Indicadores
    page_dots(draw, 1, 6, 880, 1027, BRANCO, VERDE_ESCURO)

    return img

# ============================================================================
# SLIDE 2 - O PROBLEMA
# ============================================================================
def slide2_problema():
    img = Image.new('RGB', (1080, 1080), CINZA_BG)
    draw = ImageDraw.Draw(img)

    # Barra verde
    draw.rectangle([0, 0, 1080, 12], fill=VERDE)

    # Logo pequena no canto
    add_logo_corner(img, 40, 25, 75)

    # Página
    f = get_font(22, True)
    draw.text((950, 60), "02", font=f, fill=VERMELHO)
    draw.text((985, 60), "/ 06", font=f, fill=VERDE)

    # Badge
    rounded_rect(draw, [50, 140, 250, 190], 25, VERMELHO)
    f = get_font(16, True)
    draw.text((150, 157), "O PROBLEMA", font=f, fill=BRANCO, anchor="mm")

    # Título
    f = get_font(56, True)
    draw.text((50, 220), "Por que isso é", font=f, fill=PRETO)
    draw.text((50, 290), "alarmante?", font=f, fill=VERMELHO)

    # Linha verde
    draw.rectangle([50, 375, 56, 445], fill=VERDE)
    f = get_font_medium(22)
    draw.text((75, 385), "A violência contra médicos não é um problema", font=f, fill=CINZA)
    draw.text((75, 415), "isolado. É uma crise que afeta toda a categoria.", font=f, fill=CINZA)

    # Card 117%
    rounded_rect(draw, [50, 480, 1030, 620], 16, BRANCO)
    draw.rectangle([50, 480, 62, 620], fill=VERMELHO)

    draw.ellipse([90, 515, 160, 585], fill=(255, 230, 230))
    draw.polygon([(125, 530), (150, 575), (100, 575)], fill=VERMELHO)
    f = get_font(24, True)
    draw.text((125, 560), "!", font=f, fill=BRANCO, anchor="mm")

    f = get_font(58, True)
    draw.text((180, 510), "117%", font=f, fill=VERMELHO)
    f = get_font(34, True)
    draw.text((370, 525), "de aumento", font=f, fill=PRETO)
    f = get_font_medium(22)
    draw.text((180, 580), "Agressões cresceram nos últimos 5 anos", font=f, fill=CINZA)

    # Card 64%
    rounded_rect(draw, [50, 645, 1030, 785], 16, BRANCO)
    draw.rectangle([50, 645, 62, 785], fill=LARANJA)

    draw.ellipse([90, 680, 160, 750], fill=(255, 240, 220))
    draw.polygon([(125, 695), (150, 740), (100, 740)], fill=LARANJA)
    f = get_font(24, True)
    draw.text((125, 725), "!", font=f, fill=BRANCO, anchor="mm")

    f = get_font(58, True)
    draw.text((180, 675), "64%", font=f, fill=LARANJA)
    f = get_font(34, True)
    draw.text((340, 690), "dos médicos", font=f, fill=PRETO)
    f = get_font_medium(22)
    draw.text((180, 745), "Já sofreram violência no ambiente de trabalho", font=f, fill=CINZA)

    # Box verde
    rounded_rect(draw, [50, 815, 1030, 960], 16, VERDE)
    f = get_font(16, True)
    draw.text((540, 840), "AS PRINCIPAIS OCORRÊNCIAS:", font=f, fill=VERDE_CLARO, anchor="mm")

    # Tags
    tags = ["Ameaças", "Agressões Físicas", "Destruição", "Coerção"]
    positions = [145, 355, 580, 790]
    f = get_font(18, True)
    for tag, px in zip(tags, positions):
        w = len(tag) * 10 + 40
        rounded_rect(draw, [px - w//2, 875, px + w//2, 920], 22, VERDE_ESCURO)
        draw.text((px, 890), tag, font=f, fill=BRANCO, anchor="mm")

    # Rodapé
    draw.line([50, 990, 1030, 990], fill=CINZA_CLARO, width=1)
    page_dots(draw, 2, 6, 50, 1020, VERMELHO, CINZA_CLARO)
    f = get_font(16, True)
    draw.text((1030, 1025), "SINMEVAÇO", font=f, fill=VERDE, anchor="rm")

    return img

# ============================================================================
# SLIDE 3 - A RESPOSTA
# ============================================================================
def slide3_resposta():
    img = Image.new('RGB', (1080, 1080), VERDE)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, 1080, 8], fill=VERDE_CLARO)

    # Logo pequena no canto
    add_logo_corner(img, 40, 40, 80)

    # Página
    f = get_font(22, True)
    draw.text((950, 70), "03", font=f, fill=VERDE_CLARO)
    draw.text((985, 70), "/ 06", font=f, fill=BRANCO)

    # Badge
    rounded_rect(draw, [50, 160, 260, 210], 25, VERDE_CLARO)
    f = get_font(16, True)
    draw.text((155, 177), "A RESPOSTA", font=f, fill=VERDE_ESCURO, anchor="mm")

    # Título
    f = get_font(52, True)
    draw.text((50, 250), "O CFM aprovou a", font=f, fill=BRANCO)

    # Box resolução
    rounded_rect(draw, [50, 330, 800, 420], 16, VERDE_CLARO)
    f = get_font(52, True)
    draw.text((425, 358), "Resolução 2.444/2025", font=f, fill=VERDE_ESCURO, anchor="mm")

    # Texto
    f = get_font_medium(28)
    center_text(draw, "que obriga todas as unidades de saúde,", 470, f, BRANCO)
    center_text(draw, "públicas e privadas, a garantir", 510, f, BRANCO)

    f = get_font(30, True)
    center_text(draw, "segurança integral ao médico", 565, f, VERDE_CLARO)

    f = get_font_medium(28)
    center_text(draw, "no exercício da profissão.", 615, f, BRANCO)

    # Box destaque
    rounded_rect(draw, [140, 700, 940, 890], 20, VERDE_ESCURO)
    draw.rounded_rectangle([140, 700, 940, 890], radius=20, outline=VERDE_CLARO, width=3)

    f = get_font(48, True)
    draw.text((540, 760), "NÃO É SUGESTÃO.", font=f, fill=LARANJA, anchor="mm")
    draw.text((540, 830), "É NORMA.", font=f, fill=VERDE_CLARO, anchor="mm")

    # Rodapé
    draw.line([50, 1000, 1030, 1000], fill=VERDE_ESCURO, width=2)
    page_dots(draw, 3, 6, 50, 1030, VERDE_CLARO, VERDE_ESCURO)
    f = get_font(16, True)
    draw.text((1030, 1035), "SINMEVAÇO", font=f, fill=BRANCO, anchor="rm")

    return img

# ============================================================================
# SLIDE 4 - EXIGÊNCIAS
# ============================================================================
def slide4_exigencias():
    img = Image.new('RGB', (1080, 1080), VERDE)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, 1080, 8], fill=VERDE_CLARO)

    # Logo pequena no canto
    add_logo_corner(img, 40, 40, 80)

    # Página
    f = get_font(22, True)
    draw.text((950, 70), "04", font=f, fill=VERDE_CLARO)
    draw.text((985, 70), "/ 06", font=f, fill=BRANCO)

    # Badge
    rounded_rect(draw, [50, 160, 245, 210], 25, VERDE_ESCURO)
    draw.rounded_rectangle([50, 160, 245, 210], radius=25, outline=VERDE_CLARO, width=2)
    f = get_font(16, True)
    draw.text((147, 177), "O QUE EXIGE", font=f, fill=BRANCO, anchor="mm")

    # Título
    f = get_font(48, True)
    draw.text((50, 250), "O que a Resolução", font=f, fill=VERDE_CLARO)
    draw.text((50, 315), "determina?", font=f, fill=BRANCO)

    # Cards
    items = [
        ("1", "Controle de acesso", "às unidades de saúde"),
        ("2", "Vigilância presencial e contínua", "Não apenas segurança patrimonial"),
        ("3", "Videomonitoramento", "em áreas comuns das unidades"),
        ("4", "Protocolos de resposta", "Ações imediatas em casos de agressão"),
    ]

    y = 410
    for num, titulo, desc in items:
        rounded_rect(draw, [50, y, 1030, y+130], 16, VERDE_ESCURO)

        draw.ellipse([80, y+30, 150, y+100], fill=VERDE_CLARO)
        f = get_font(36, True)
        draw.text((115, y+55), num, font=f, fill=VERDE_ESCURO, anchor="mm")

        f = get_font(28, True)
        draw.text((175, y+35), titulo, font=f, fill=BRANCO)
        f = get_font_medium(22)
        draw.text((175, y+80), desc, font=f, fill=VERDE_CLARO)

        y += 150

    # Rodapé
    draw.line([50, 1000, 1030, 1000], fill=VERDE_ESCURO, width=2)
    page_dots(draw, 4, 6, 50, 1030, VERDE_CLARO, VERDE_ESCURO)
    f = get_font(16, True)
    draw.text((1030, 1035), "SINMEVAÇO", font=f, fill=BRANCO, anchor="rm")

    return img

# ============================================================================
# SLIDE 5 - PROTEÇÃO
# ============================================================================
def slide5_protecao():
    img = Image.new('RGB', (1080, 1080), CINZA_BG)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, 1080, 12], fill=VERDE)

    # Logo pequena no canto
    add_logo_corner(img, 40, 25, 75)

    # Página
    f = get_font(22, True)
    draw.text((950, 60), "05", font=f, fill=VERDE)
    draw.text((985, 60), "/ 06", font=f, fill=VERDE)

    # Badge
    rounded_rect(draw, [50, 140, 230, 190], 25, VERDE)
    f = get_font(16, True)
    draw.text((140, 157), "PROTEÇÃO", font=f, fill=BRANCO, anchor="mm")

    # Título
    f = get_font(52, True)
    draw.text((50, 220), "Proteção ao", font=f, fill=PRETO)
    draw.text((50, 290), "Médico Vítima", font=f, fill=VERDE)

    # Card 1 - destaque
    rounded_rect(draw, [50, 380, 1030, 490], 16, VERDE)
    draw.ellipse([85, 405, 145, 465], fill=VERDE_ESCURO)
    f = get_font(28, True)
    draw.text((115, 428), "✓", font=f, fill=BRANCO, anchor="mm")
    f = get_font(26, True)
    draw.text((170, 410), "Protocolos imediatos", font=f, fill=BRANCO)
    f = get_font_medium(20)
    draw.text((170, 450), "de resposta a agressões", font=f, fill=VERDE_CLARO)

    # Cards 2-4
    cards = [
        ("Suporte psicológico e jurídico", "ao médico vítima"),
        ("Notificação obrigatória", "ao CRM e às autoridades"),
        ("Possibilidade de remanejamento", "do médico de setor após agressão"),
    ]

    y = 520
    for titulo, desc in cards:
        rounded_rect(draw, [50, y, 1030, y+115], 16, BRANCO)
        draw.ellipse([85, y+27, 145, y+87], fill=VERDE)

        f = get_font(26, True)
        draw.text((170, y+30), titulo, font=f, fill=PRETO)
        f = get_font_medium(20)
        draw.text((170, y+70), desc, font=f, fill=CINZA)

        y += 135

    # Rodapé
    draw.line([50, 940, 1030, 940], fill=CINZA_CLARO, width=1)
    page_dots(draw, 5, 6, 50, 970, VERDE, CINZA_CLARO)
    f = get_font(16, True)
    draw.text((1030, 975), "SINMEVAÇO", font=f, fill=VERDE, anchor="rm")

    return img

# ============================================================================
# SLIDE 6 - FECHAMENTO
# ============================================================================
def slide6_fechamento():
    img = Image.new('RGB', (1080, 1080), VERDE)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, 1080, 8], fill=VERDE_CLARO)

    # Logo grande centralizada
    add_logo(img, 540, 150, 200)

    # Título
    f = get_font(60, True)
    center_text(draw, "Nenhum Médico", 380, f, BRANCO)
    center_text(draw, "Pode Trabalhar", 455, f, BRANCO)
    center_text(draw, "com Medo!", 530, f, VERDE_CLARO)

    # Subtítulo
    f = get_font_medium(26)
    center_text(draw, "A Resolução 2.444 é um marco e nós", 630, f, BRANCO)
    f = get_font(26, True)
    center_text(draw, "vamos cobrar seu cumprimento.", 670, f, VERDE_CLARO)

    # WhatsApp
    rounded_rect(draw, [280, 750, 800, 810], 30, VERDE_ESCURO)
    draw.ellipse([305, 762, 345, 802], fill=(37, 211, 102))
    f = get_font(20, True)
    draw.text((325, 775), "W", font=f, fill=BRANCO, anchor="mm")
    f = get_font(26, True)
    draw.text((540, 772), "(31) 99717-8316", font=f, fill=BRANCO, anchor="mm")

    # Hashtags
    hashtags = ["#UniãoFazAForça", "#MedicinaValeDoAço", "#SindicatoForte"]
    positions = [250, 540, 850]
    f = get_font(15, True)
    for tag, px in zip(hashtags, positions):
        w = len(tag) * 9 + 30
        rounded_rect(draw, [px - w//2, 860, px + w//2, 900], 20, VERDE_ESCURO)
        draw.text((px, 873), tag, font=f, fill=BRANCO, anchor="mm")

    # Rodapé
    draw.line([50, 1000, 1030, 1000], fill=VERDE_ESCURO, width=2)
    f = get_font_medium(14)
    draw.text((50, 1030), "Sindicato dos Médicos do Vale do Aço", font=f, fill=VERDE_CLARO)
    page_dots(draw, 6, 6, 880, 1032, BRANCO, VERDE_ESCURO)

    return img

# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 50)
    print("CARROSSEL INSTAGRAM - SINMEVAÇO")
    print("Violência contra Médicos")
    print("=" * 50)

    print("\nPreparando recursos...")
    setup_fonts()

    if not download_logo():
        print("ERRO: Não foi possível baixar a logo")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    slides = [
        ("01_capa", slide1_capa),
        ("02_problema", slide2_problema),
        ("03_resposta", slide3_resposta),
        ("04_exigencias", slide4_exigencias),
        ("05_protecao", slide5_protecao),
        ("06_fechamento", slide6_fechamento),
    ]

    print("\nGerando posts...")
    for name, func in slides:
        print(f"  {name}...", end=" ")
        try:
            img = func()
            path = os.path.join(OUTPUT_DIR, f"{name}.png")
            img.save(path, 'PNG')
            print("OK")
        except Exception as e:
            print(f"ERRO: {e}")

    print(f"\nPronto! Arquivos em: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
