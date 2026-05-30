import os
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.gridspec as gridspec
from config import LAYOUT_COLORS, LAYOUT_FONTS, LAYOUT_SPACING, INFO_TEXT

# custom font laden und global registrieren
font_path = "./findmyname/hello_paris_serif.ttf"
if os.path.exists(font_path):
    font_manager.fontManager.addfont(font_path)
    prop = font_manager.FontProperties(fname=font_path)
    custom_font_name = prop.get_name()
else:
    print(f"Warning: '{font_path}' nicht gefunden. Nutze Ausweichschrift.")
    custom_font_name = "monospace"

def generate_pdf(output_path, puzzle, restored_names, original_hyphen_names, is_solution=False):
    grid = puzzle.puzzle
    size = len(grid)
    
    # erstelle das hauptfenster (a4 querformat)
    fig = plt.figure(figsize=(29.7 / 2.54, 21.0 / 2.54), facecolor=LAYOUT_COLORS["hintergrund"])
    
    # bootstrap-gitter-äquivalent: 1 zeile, 2 spalten (verhältnis 55% zu 45%)
    gs = gridspec.GridSpec(1, 2, width_ratios=[0.55, 0.45], 
                           wspace=LAYOUT_SPACING["spalten_abstand"], 
                           left=0.05, right=0.95, top=0.92, bottom=0.08)
    
    # --- LINKER CONTAINER (ROW 1, COL 1): DAS BUCHSTABENRASTER ---
    ax_grid = fig.add_subplot(gs[0])
    ax_grid.set_facecolor(LAYOUT_COLORS["hintergrund"])
    ax_grid.axis('off')
    
    grid_fontsize = max(8, 14 - (size - 15) * 0.3)

    # koordinaten für das lösungsblatt ermitteln
    solution_coords = set()
    if is_solution:
        for word in puzzle.words:
            if word.placed:
                for coord in word.coordinates:
                    # FIXED: extrahiert die indizes absolut sauber, egal welcher datentyp geliefert wird
                    if hasattr(coord, 'row') and hasattr(coord, 'col'):
                        solution_coords.add((coord.row, coord.col))
                    elif isinstance(coord, (tuple, list)) and len(coord) == 2:
                        solution_coords.add((coord[0], coord[1]))

    # raster zeichnen
    for r in range(size):
        for c in range(size):
            char = grid[r][c].lower()
            
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

            ax_grid.text(c, size - 1 - r, char, 
                         ha='center', va='center', 
                         fontsize=grid_fontsize, 
                         fontname=custom_font_name,  
                         fontweight=char_weight,
                         color=char_color)
            
    ax_grid.set_xlim(-0.5, size - 0.5)
    ax_grid.set_ylim(-0.5, size - 0.5)

    # --- RECHTER CONTAINER (ROW 1, COL 2): SIDEBAR (FLEXBOX BEHAVIOR) ---
    ax_text = fig.add_subplot(gs[1])
    ax_text.set_facecolor(LAYOUT_COLORS["hintergrund"])
    ax_text.axis('off')
    
    # namensspalten für die rechte seite formatieren
    spaced_names = []
    for name in sorted(restored_names):
        formatted_name = "-".join([part.capitalize() for part in name.split("-")])
        spaced_names.append(" ".join(list(formatted_name)))

    midpoint = (len(spaced_names) + 1) // 2
    col1_text = "\n".join(spaced_names[:midpoint])
    col2_text = "\n".join(spaced_names[midpoint:])

    # spielregeln definieren
    info_title = "Spielregle"
    info_text = INFO_TEXT

    # block 1: fingsch di? titel & listen
    titel1_erweiterung = " (Lösig)" if is_solution else ""
    ax_text.text(0.0, 1.0, f"Fingsch  Di?{titel1_erweiterung}", ha='left', va='top', transform=ax_text.transAxes,
                 fontsize=LAYOUT_FONTS["titel_groesse"], fontname=custom_font_name, fontweight='bold', color=LAYOUT_COLORS["titel_text"])
    
    liste_y = 1.0 - LAYOUT_SPACING["titel_zu_liste_gap"]
    
    ax_text.text(0.0, liste_y, col1_text, ha='left', va='top', transform=ax_text.transAxes,
                 fontsize=LAYOUT_FONTS["text_groesse"], fontname=custom_font_name, color=LAYOUT_COLORS["listen_text"], linespacing=1.4)
    ax_text.text(LAYOUT_SPACING["spalte2_einzug"], liste_y, col2_text, ha='left', va='top', transform=ax_text.transAxes,
                 fontsize=LAYOUT_FONTS["text_groesse"], fontname=custom_font_name, color=LAYOUT_COLORS["listen_text"], linespacing=1.4)

    # block 2: spielregeln
    ax_text.text(0.0, LAYOUT_SPACING["titel_zu_regeln_gap"], info_title, ha='left', va='bottom', transform=ax_text.transAxes,
                 fontsize=LAYOUT_FONTS["titel_groesse"], fontname=custom_font_name, fontweight='bold', color=LAYOUT_COLORS["titel_text"])
    
    ax_text.text(0.0, 0.0, info_text, ha='left', va='bottom', transform=ax_text.transAxes,
                 fontsize=LAYOUT_FONTS["text_groesse"], fontname=custom_font_name, color=LAYOUT_COLORS["regeln_text"], linespacing=1.4)

    # exportieren und speichern
    plt.savefig(output_path, format='pdf', bbox_inches='tight', facecolor=fig.get_facecolor(), dpi=300)
    plt.close()
