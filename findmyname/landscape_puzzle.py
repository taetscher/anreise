import csv
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager
from word_search_generator import WordSearch

# =====================================================================
# farbkonfiguration (zentrales design-dictionary)
# =====================================================================
LAYOUT_COLORS = {
    "hintergrund": "#f4f1ea",       # eierschalenfarbe für das gesamte dokument
    "suchfeld_text": "#2d3748",     # farbe der buchstaben im rätselraster
    "titel_text": "#2d3748",        # farbe für die haupttitel
    "listen_text": "#2d3748",       # farbe für die namen in den spalten
    "regeln_text": "#2d3748",       # farbe für den text der spielregeln
    "loesung_highlight": "#e53e3e"  # farbe für die gefundenen namen auf dem lösungsblatt
}

# =====================================================================
# schriftgrössenerkennung (zentrale variablen)
# =====================================================================
LAYOUT_FONTS = {
    "titel_groesse": 12,            # einheitliche grösse für "fingsch di?" und "spielregle"
    "text_groesse": 9            # einheitliche grösse für namenslisten und spielregel-inhalt
}

RASTER_SIZE = 25  # perfekt ausgewogen für ca. 20-40 namen inklusive umlaute

# =====================================================================
# custom font configuration
# =====================================================================
font_path = "./findmyname/hello_paris_serif.ttf"

if os.path.exists(font_path):
    # register the font file globally in matplotlib
    font_manager.fontManager.addfont(font_path)
    # extract the internal font name from the file metadata
    prop = font_manager.FontProperties(fname=font_path)
    custom_font_name = prop.get_name()
    print(f"Successfully loaded custom font: '{custom_font_name}'")
else:
    print(f"Warning: '{font_path}' not found. Falling back to monospace.")
    custom_font_name = "monospace"
# =====================================================================

csv_filename = './findmyname/names.csv'
names_list = []
original_hyphen_names = {}  # speichert die originalnamen für die spätere wiederherstellung

if os.path.exists(csv_filename):
    with open(csv_filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for idx, row in enumerate(reader, start=1):
            if row:  # skip empty rows
                name_raw = row[0].strip()
                if name_raw:
                    # umlaute umwandeln und bindestriche entfernen für den generator
                    name_clean = name_raw.lower()
                    name_clean = name_clean.replace("ä", "ae")
                    name_clean = name_clean.replace("ö", "oe")
                    name_clean = name_clean.replace("ü", "ue")
                    name_clean = name_clean.replace("-", "")
                    
                    # bombensicherer trick: wir hängen die zeilennummer an
                    name_gen = f"{name_clean}{idx}"
                    
                    names_list.append(name_gen)
                    original_hyphen_names[name_gen] = name_raw
else:
    print(f"Error: Could not find '{csv_filename}'. Please create it first.")
    exit()

# convert the list of names into a comma-separated string for the generator
names_string = ", ".join(names_list)

# =====================================================================
# brute-force-schleife: rätsel neu generieren bis alle namen passen
# =====================================================================
max_attempts = 50
puzzle = None
placed_words_generator = []
matched_clean_names = set()

print(f"\nGeneriere Rätsel (Grösse {RASTER_SIZE}). Suche nach perfektem Layout...")

for attempt in range(1, max_attempts + 1):
    puzzle = WordSearch(names_string, size=RASTER_SIZE, secret_words="Melamin, Fred, Leandro", level=3)
    puzzle.generator.chars = "abcdefghijklmnopqrstuvwxyzäöüéèàçë"
    
    placed_words_generator = [word.text.lower() for word in puzzle.placed_words if not word.secret]
    matched_clean_names = set(placed_words_generator)
    failed_count = sum(1 for clean_name in original_hyphen_names if clean_name not in matched_clean_names)
    
    if failed_count == 0:
        print(f"  → [PERFEKT] Alle Namen erfolgreich platziert im Versuch {attempt}!")
        break
    else:
        print(f"  → Versuch {attempt}: {failed_count} Namen haben nicht gepasst. Generiere neu...")
else:
    print(f"\n[WARNUNG] Nach {max_attempts} Versuchen fehlen immer noch Namen. Erhöhe RASTER_SIZE im Skript!")
# =====================================================================

# extract the matrix properties 
grid = puzzle.puzzle
size = len(grid)

# =====================================================================
# funktion zum zeichnen des pdfs (wird für rätsel und lösung wiederverwendet)
# =====================================================================
def generate_pdf(output_path, is_solution=False):
    fig, ax = plt.subplots(figsize=(29.7 / 2.54, 21.0 / 2.54), facecolor=LAYOUT_COLORS["hintergrund"])
    ax.set_facecolor(LAYOUT_COLORS["hintergrund"])
    ax.axis('off')

    grid_fontsize = max(8, 14 - (size - 15) * 0.3)

    # erstelle ein set aller koordinaten, die zu einem versteckten wort gehören
    solution_coords = set()
    if is_solution:
        for word in puzzle.placed_words:
            for coord in word.coordinates:
                solution_coords.add((coord[0], coord[1]))

    # loop through the rows to plot the puzzle characters onto the canvas
    for r in range(size):
        for c in range(size):
            char = grid[r][c].lower()
            if char.isdigit():
                char = "a"
            
            # farb- und gewichtslogik für das lösungsblatt
            if is_solution:
                if (r, c) in solution_coords:
                    char_color = LAYOUT_COLORS["loesung_highlight"]
                    char_weight = 'bold'
                else:
                    char_color = '#cbd5e0'  # füllbuchstaben ausgrauen
                    char_weight = 'normal'
            else:
                char_color = LAYOUT_COLORS["suchfeld_text"]
                char_weight = 'bold'

            ax.text(c, size - 1 - r, char, 
                    ha='center', va='center', 
                    fontsize=grid_fontsize, 
                    fontname=custom_font_name,  
                    fontweight=char_weight,
                    color=char_color)

    # spalten-berechnung und ausgabe für die rechte seite
    spaced_names = []
    for name in sorted(restored_names):
        formatted_name = "-".join([part.capitalize() for part in name.split("-")])
        spaced_names.append(" ".join(list(formatted_name)))

    midpoint = (len(spaced_names) + 1) // 2
    col1_text = "\n".join(spaced_names[:midpoint])
    col2_text = "\n".join(spaced_names[midpoint:])

    # namensspalten-titel und inhalt zeichnen (grösseneinstellungen angeglichen)
    titel_erweiterung = " (Lösig)" if is_solution else ""
    ax.text(size + 1, size - 1, f"Fingsch  Di?{titel_erweiterung}", 
            ha='left', va='top', 
            fontsize=LAYOUT_FONTS["titel_groesse"], fontname=custom_font_name, fontweight='bold', color=LAYOUT_COLORS["titel_text"])

    ax.text(size + 1, size - 2.5, col1_text, ha='left', va='top', 
            fontsize=LAYOUT_FONTS["text_groesse"], fontname=custom_font_name, color=LAYOUT_COLORS["listen_text"], linespacing=1.5)
    ax.text(size + 6, size - 2.5, col2_text, ha='left', va='top', 
            fontsize=LAYOUT_FONTS["text_groesse"], fontname=custom_font_name, color=LAYOUT_COLORS["listen_text"], linespacing=1.5)

    # aktualisierte spielregeln zeichnen (grösseneinstellungen absolut identisch zur namensliste)
    info_title = "Spielregle"
    info_text = (
        "D Näme chöi i alli 8 Himmusrichtige versteckt si:\n"
        "- West-Ost ( vo links nach rächts )\n"
        "- Ost-West ( vo rächts nach links )\n"
        "- Nord-Süd ( vo obe nach unge )\n"
        "- Süd-Nord ( vo unge nach obe )\n"
        "- Sowie diagonal ( NW, NO, SW, SO ), gäu!\n\n"
        "- Umlutte si umgformt: Ä -> AE\n"
        "- Dr H-U isch dr HU, Dr Günter isch dr Guenter\n"
        "- Aber dr Cédi blibt dr Cédi u d Noëlla isch d Noëlla\n"
        "- We zwöi glich heisse, isch ide Enderi die Gschwinderi\n\n"
        "+ Es chönnt si, dasses meh z finde gitt aus nur Die Näme"
    )
    
    # spielregeln-titel zeichnen
    ax.text(size + 1, 9, info_title, 
            ha='left', va='bottom', 
            fontsize=LAYOUT_FONTS["titel_groesse"], fontname=custom_font_name, fontweight='bold', color=LAYOUT_COLORS["titel_text"])
    
    # spielregeln-inhalt zeichnen
    ax.text(size + 1, 0, info_text, 
            ha='left', va='bottom', 
            fontsize=LAYOUT_FONTS["text_groesse"], fontname=custom_font_name, color=LAYOUT_COLORS["regeln_text"], linespacing=1.5)

    ax.set_xlim(-1, size + 12)
    ax.set_ylim(-1, size)

    plt.savefig(output_path, format='pdf', bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
# =====================================================================

# bereite die originalnamen für die anzeige vor
restored_names = []
for name in placed_words_generator:
    if name in original_hyphen_names:
        restored_names.append(original_hyphen_names[name])
    else:
        restored_names.append(name)

# 1. Generiere das normale Rätselblatt
generate_pdf("./findmyname/landscape_names_puzzle.pdf", is_solution=False)
print("→ Spieldokument gespeichert unter: ./findmyname/landscape_names_puzzle.pdf")

# 2. Generiere das Lösungsblatt
generate_pdf("./findmyname/landscape_names_solution.pdf", is_solution=True)
print("→ Lösungsdokument gespeichert unter: ./findmyname/landscape_names_solution.pdf")
