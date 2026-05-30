# farbkonfiguration für das gesamte layout
LAYOUT_COLORS = {
    "hintergrund": "#f4f1ea",       # eierschalenfarbe für das gesamte dokument
    "suchfeld_text": "#2d3748",     # farbe der buchstaben im rätselraster
    "titel_text": "#2d3748",        # farbe für die haupttitel
    "listen_text": "#2d3748",       # farbe für die namen in den spalten
    "regeln_text": "#2d3748",       # farbe für den text der spielregeln
    "loesung_highlight": "#e53e3e"  # farbe für die gefundenen namen auf dem lösungsblatt
}

# einheitliche schriftgrössen
LAYOUT_FONTS = {
    "titel_groesse": 14,            # grösse für "fingsch di?" und "spielregle"
    "text_groesse": 10.5            # grösse für namenslisten und spielregel-inhalt
}

# =====================================================================
# flexible abstands-konfiguration (wie bootstrap/css)
# =====================================================================
LAYOUT_SPACING = {
    "spalten_abstand": 0.09,        # gutter zwischen buchstabenraster und sidebar
    "titel_zu_liste_gap": 0.06,     # margin-top zwischen titel 1 und namensliste (standard: 6%)
    "titel_zu_regeln_gap": 0.28,    # vertikale platzierung des spielregel-titels (von unten gemessen)
    "spalte2_einzug": 0.34          # horizontaler x-versatz für die zweite namensspalte (48%)
}

# schiwerigkeitsgrad
DIFFICULTY = 3

# easter eggs
EASTER_EGGS = [
    "Melyamin",
    "Fred",
    "Lazy",
    "Leandro",
    "ElTorro",
    "Stöfe",
    "Schoggitiger",
    "Dohus"
]

# grösse des rätselfelds
RASTER_SIZE = 30


INFO_TEXT = (
        "Wörter chöi i alli 8 Himmusrichtige versteckt si:\n"
        "- West-Ost ( vo links nach rächts ) aber oh Ost-West ( vo rächts nach links )\n"
        "- Nord-Süd ( vo obe nach unge ) und oh Süd-Nord ( vo unge nach obe )\n"
        "- Sowie diagonal ( NW, NO, SW, SO ), gäu!\n"
        "- Und oh gspieglet. Und gspieglet und diagonal. Sorry.\n"
        "- Umlutte gitts nid: Ä -> AE.  Dr Mäni wird zum Maeni (oder genau dä äbe nid?)\n"
        "- Dr H-U isch dr HU, aber dr Cédi blibt dr Cédi\n"
        "- We zwöi glich heisse, isch die Enderi die Gschwinderi  Deborah\n"
        "- We dr eint si Name us 50% vom andere macht, suechesi zäme eine\n"
        "+ Es chönnt si, dasses meh z finde gitt aus nur  Die Näme obe"
    )