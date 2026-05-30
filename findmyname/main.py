from word_search_generator import WordSearch
from config import RASTER_SIZE, EASTER_EGGS, DIFFICULTY
from loader import load_names_from_csv
from renderer import generate_pdf

def main():
    csv_filename = './findmyname/names.csv'
    
    # daten über den loader einlesen
    names_list, original_hyphen_names = load_names_from_csv(csv_filename)
    total_names_count = len(names_list)

    # =====================================================================
    # native trennung in zwei listen (verhindert den substring-fehler)
    # =====================================================================
    normal_words = []
    substring_words = []

    for name in names_list:
        is_substring = False
        for other_name in names_list:
            if name != other_name and name in other_name:
                is_substring = True
                break
        if is_substring:
            substring_words.append(name)
        else:
            normal_words.append(name)

    # die echten ostereierelemente werden in kleinbuchstaben konvertiert
    easter_eggs_clean = [egg.lower() for egg in EASTER_EGGS]
    
    # die unterwörter kommen zusammen mit den ostereiern in die geheime liste
    secret_words_pool = substring_words + easter_eggs_clean

    normal_words_string = ", ".join(normal_words)
    secret_words_string = ", ".join(secret_words_pool)
    # =====================================================================

    max_attempts = 50
    puzzle = None

    print(f"\nGeneriere Rätsel (Grösse {RASTER_SIZE}). Suche nach Layout...")

    for attempt in range(1, max_attempts + 1):
        puzzle = WordSearch(normal_words_string, size=RASTER_SIZE, secret_words=secret_words_string, level=DIFFICULTY)
        puzzle.generator.chars = "abcdefghijklmnopqrstuvwxyzäöüéèàçë"
        
        # extrahiere alle direkt vom generator platzierten wörter (kleingeschrieben)
        raw_placed = [word.text.lower() for word in puzzle.placed_words]
        
        # FIXED: ein name gilt als platziert, wenn er entweder eigenständig existiert
        # ODER wenn er nachweislich als unterwort in einem plazierten wort (wie dan in dani) steckt!
        placed_words_generator = []
        for name in names_list:
            if name in raw_placed or any(name in longer_word for longer_word in raw_placed):
                # wir filtern die echten ostereier aus, damit sie nicht auf die liste rutschen
                if name not in easter_eggs_clean:
                    placed_words_generator.append(name)
        
        # abgleich mit deiner originalen csv-liste für absolute mathematische präzision
        failed_names = [n for n in names_list if n not in placed_words_generator]
        
        placed_count = total_names_count - len(failed_names)
        failed_count = len(failed_names)
        
        log_message = f"  → Versuch {attempt}: Von {total_names_count} Namen wurden {placed_count} platziert und {failed_count} nicht."
        
        if failed_count == 0:
            print(f"  → [PERFEKT] Alle {total_names_count} Namen erfolgreich platziert im Versuch {attempt}!")
            break
        else:
            if attempt >= 45 or attempt == 1:
                print(log_message)
            else:
                print(log_message, end="\r")
    else:
        # =====================================================================
        # fehler-logausgabe nach fehlgeschlagenen versuchen
        # =====================================================================
        print(f"\n\n[WARNUNG] Nach {max_attempts} Versuchen fehlen immer noch {len(failed_names)} Namen!")
        print(f"Zusammenfassung: Von {total_names_count} Namen wurden {total_names_count - len(failed_names)} platziert und {len(failed_names)} nicht.")
        print("-" * 60)
        print("DIESE NAMEN KONNTEN NICHT PLATZIERT WERDEN:")
        for f_name in failed_names:
            orig_display = original_hyphen_names.get(f_name, f_name)
            print(f"  ❌ '{orig_display}'")
        print("-" * 60)

    # originalnamen für die spaltenanzeige wiederherstellen
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
