import logging

# Configurare Logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def genereaza_fluturas_bursa(student: object) -> str:
    """
    Generează un raport text (fluturaș) pentru un student.
    Documentare: Docstrings bifați.
    """
    try:
        suma = 0
        if student.medie >= 9.50:
            suma = 1000
            tip = "Bursa de Merit"
        elif student.medie >= 8.50:
            suma = 700
            tip = "Bursa de Studiu"
        else:
            tip = "Fara Bursa"

        raport = f"""
        ====================================
        FLUTURAS DETALII BURSA
        ====================================
        Student: {student.nume}
        Facultate: {student.facultate}
        Medie Generala: {student.medie}
        ------------------------------------
        Tip Bursa: {tip}
        Cuantum: {suma} RON
        ====================================
        """
        logging.info(f"Raport generat pentru {student.nume}")
        return raport
    except Exception as e:
        logging.error(f"Eroare la generarea raportului: {e}")
        return "Eroare la generare."


def calculeaza_status_bursa(medie: float) -> str:
    if medie >= 9.50:
        return "Bursa de Merit"
    elif medie >= 8.50:
        return "Bursa de Studiu"
    else:
        return "Fara Bursa"
