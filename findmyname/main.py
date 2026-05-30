import random
from word_search_generator import WordSearch
from config import RASTER_SIZE, EASTER_EGGS, DIFFICULTY
from loader import load_names_from_csv
from renderer import generate_pdf

def inject_word_manually(grid, word_text):
    """
    fuegt ein wort manuell an einer zufaelligen, freien stelle im grid ein.
    unterstuetzt horizontale, vertikale und diagonale platzierung (vorwaerts).
    """
    size = len(grid)
    word_len = len(word_text)
    
    # moegliche richtungen: (zeilen_schritt, spalten_schritt)
    directions = [
        (0, 1),   # horizontal links nach rechts
        (1, 0),   # vertikal oben nach unten
        (1, 1),   # diagonal oben-links nach unten-rechts
        (-1, 1)   # diagonal unten-links nach oben-rechts
    ]
    
    # wir versuchen bis zu 2000 mal, das wort kollisionsfrei reinzuquetschen
    for _ in range(2000):
        dr, dc = random.choice(directions)
        
        # startpositionen auswuerfeln basierend auf der richtung
        if dr == 0:
            start_r = random.randint(0, size - 1)
        elif dr == 1:
            start_r = random.randint(0, size - word_len)
        else:
            start_r = random.randint(word_len - 1, size - 1)
            
        start_c = random.randint(0, size - word_len)
        
        coords = []
        for i in range(word_len):
            curr_r = start_r + (i * dr)
            curr_c = start_c + (i * dc)
            coords.append((curr_r, curr_c))
            
        return coords, dr, dc, start_r, start_c
    return None

def main():
    csv_filename = './findmyname/names.csv'
    names_list, original_hyphen_names = load_names_from_csv(csv_filename)

    # =====================================================================
    # unterwort-konflikte isolieren
    # =====================================================================
    normal_words = []
    conflict_words = []

    for name in names_list:
        is_substring = False
        for other_name in names_list:
            if name != other_name and name in other_name:
                is_substring = True
                break
        if is_substring:
            conflict_words.append(name)
        else:
            normal_words.append(name)

    easter_eggs_clean = [egg.lower() for egg in EASTER_EGGS]
    
    normal_words_string = ", ".join(normal_words)
    secret_words_string = ", ".join(easter_eggs_clean)
    # =====================================================================

    max_attempts = 50
    puzzle = None
    placed_words_generator = []

    print(f"\nGeneriere Basis-Rätsel (Grösse {RASTER_SIZE})...")

    for attempt in range(1, max_attempts + 1):
        puzzle = WordSearch(normal_words_string, size=RASTER_SIZE, secret_words=secret_words_string, level=DIFFICULTY)
        puzzle.generator.chars = "abcdefghijklmnopqrstuvwxyzäöüéèàçë"
        
        placed_words_generator = [word.text.lower() for word in puzzle.placed_words if word.text.lower() not in easter_eggs_clean]
        failed_count = sum(1 for n in normal_words if n not in placed_words_generator)
        
        if failed_count == 0:
            print(f"  → [ERFOLG] Basis-Layout stabil generiert!")
            break
        else:
            print(f"  → Versuch {attempt}: Berechne Layout neu...", end="\r")
    else:
        print(f"\n[WARNUNG] Basis-Layout unvollstaendig. Erhöhe RASTER_SIZE.")

    # =====================================================================
    # MANUELLE INJEKTION DER KONFLIKT-NAMEN
    # =====================================================================
    grid = puzzle.puzzle
    
    # custom-klasse fuer manuell eingefuegte woerter
    class ManualWord:
        def __init__(self, text, coordinates):
            self.text = text
            self.coordinates = coordinates
            self.secret = False

    if conflict_words:
        print(f"\nInjiere {len(conflict_words)} Konflikt-Namen manuell ins Buchstabenfeld...")
        for c_word in conflict_words:
            result = inject_word_manually(grid, c_word)
            if result:
                coords, dr, dc, start_r, start_c = result
                for i, (r, c) in enumerate(coords):
                    grid[r][c] = c_word[i]
                
                # speichert die koordinaten sauber als koordinatenobjekt ab
                manual_obj = ManualWord(c_word, coords)
                puzzle.placed_words.add(manual_obj)
                placed_words_generator.append(c_word)
                print(f"  ✅ '{original_hyphen_names[c_word]}' erfolgreich eingebaut.")

    # originalnamen für die anzeige wiederherstellen
    restored_names = []
    for name in placed_words_generator:
        if name in original_hyphen_names:
            restored_names.append(original_hyphen_names[name])

    # pdfs erzeugen
    generate_pdf("./findmyname/landscape_names_puzzle.pdf", puzzle, restored_names, original_hyphen_names, is_solution=False)
    print("\n→ Spieldokument gespeichert unter: ./findmyname/landscape_names_puzzle.pdf")

    generate_pdf("./findmyname/landscape_names_solution.pdf", puzzle, restored_names, original_hyphen_names, is_solution=True)
    print("→ Lösungsdokument gespeichert unter: ./findmyname/landscape_names_solution.pdf")

if __name__ == "__main__":
    main()
