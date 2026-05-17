import os
import logging
from typing import List, Union
from flask import Flask, render_template, request, redirect, url_for, Response
from models import db, Student
from utils import genereaza_fluturas_bursa

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("app.log", mode='a', encoding='utf-8')
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(console_handler)

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'studenti.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    logging.info("Baza de date a fost inițializată cu succes.")


def calculeaza_status_bursa(medie: float) -> str:
    """
    Determină tipul de bursă al unui student în funcție de media generală.

    Args:
        medie (float): Media generală a studentului (între 1.00 și 10.00).

    Returns:
        str: Tipul de bursă: 'Bursa de Merit', 'Bursa de Studiu' sau 'Fara Bursa'.
    """
    if medie >= 9.50:
        return "Bursa de Merit"
    elif medie >= 8.50:
        return "Bursa de Studiu"
    else:
        return "Fara Bursa"


@app.route('/')
def index() -> str:
    """
    Afișează lista studenților cu suport pentru căutare, filtrare și sortare.

    Parametri GET acceptați:
        - search (str): Termen de căutare aplicat pe nume și facultate.
        - bursa (str): Filtrare după statusul bursei ('Bursa de Merit', 'Bursa de Studiu', 'Fara Bursa').
        - sort_by (str): Câmpul după care se sortează ('nume', 'medie', 'facultate').

    Returns:
        str: Template-ul HTML randat cu lista de studenți.
    """
    sort_by: str = request.args.get('sort_by', 'nume')
    search_query: str = request.args.get('search', '').strip()
    filtru_bursa: str = request.args.get('bursa', '').strip()

    query = Student.query

    if search_query:
        query = query.filter(
            (Student.nume.ilike(f"%{search_query}%")) |
            (Student.facultate.ilike(f"%{search_query}%"))
        )
        logging.info(f"Căutare efectuată pentru: '{search_query}'")

    if filtru_bursa:
        query = query.filter(Student.status_bursa == filtru_bursa)
        logging.info(f"Filtrare după status bursă: '{filtru_bursa}'")

    if sort_by == 'medie':
        studenti: List[Student] = query.order_by(Student.medie.desc()).all()
    elif sort_by == 'facultate':
        studenti: List[Student] = query.order_by(Student.facultate.asc()).all()
    else:
        studenti: List[Student] = query.order_by(Student.nume.asc()).all()

    return render_template('index.html', studenti=studenti, search_query=search_query)


@app.route('/add', methods=['POST'])
def add_student() -> Response:
    """
    Adaugă un student nou în baza de date după validarea datelor din formular.

    Validări aplicate:
        - Numele nu poate conține cifre.
        - Facultatea nu poate conține cifre.
        - Media trebuie să fie un număr între 1.00 și 10.00.

    Returns:
        Response: Redirecționare către pagina principală sau mesaj de eroare HTTP.
    """
    try:
        nume: str = request.form.get('nume', '').strip()
        facultate: str = request.form.get('facultate', '').strip()
        medie_raw = request.form.get('medie', '0')

        if any(char.isdigit() for char in nume):
            logging.error(f"Tentativă eșuată: Numele '{nume}' nu este valid.")
            return "Eroare: Numele nu poate conține caractere invalide!", 400

        if any(char.isdigit() for char in facultate):
            logging.error(
                f"Tentativă eșuată: Facultatea '{facultate}' nu este validă.")
            return "Eroare: Numele facultății nu poate conține caractere invalide!", 400

        medie: float = float(medie_raw)
        if medie < 1 or medie > 10:
            logging.error(
                f"Tentativă eșuată: Media {medie} este în afara intervalului 1-10.")
            return "Eroare: Media trebuie să fie între 1.00 și 10.00!", 400

        nou_student = Student(
            nume=nume,
            facultate=facultate,
            medie=medie,
            status_bursa=calculeaza_status_bursa(medie)
        )
        db.session.add(nou_student)
        db.session.commit()
        logging.info(
            f"Student adăugat: {nume}, Facultate: {facultate}, Medie: {medie}")

    except ValueError:
        logging.error("Eroare: Formatul mediei este invalid.")
        return "Eroare: Media trebuie să fie un număr valid!", 400
    except Exception as e:
        logging.error(f"Eroare neprevăzută la adăugare: {e}")
        db.session.rollback()
        return "A apărut o eroare la salvarea datelor.", 500

    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id: int) -> Union[str, Response]:
    """
    Afișează formularul de editare și procesează actualizarea datelor unui student.

    Args:
        id (int): Identificatorul unic al studentului de editat.

    Validări aplicate (metodă POST):
        - Numele nu poate conține cifre.
        - Facultatea nu poate conține cifre.
        - Media trebuie să fie un număr între 1.00 și 10.00.

    Returns:
        Union[str, Response]: Template-ul de editare (GET) sau redirecționare
        către pagina principală după salvare (POST).
    """
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        try:
            nume: str = request.form.get('nume', '').strip()
            facultate: str = request.form.get('facultate', '').strip()
            medie_raw = request.form.get('medie', '0')

            if any(char.isdigit() for char in nume):
                logging.error(
                    f"Editare eșuată: Numele '{nume}' nu este valid.")
                return "Eroare: Numele nu poate conține cifre!", 400

            if any(char.isdigit() for char in facultate):
                logging.error(
                    f"Editare eșuată: Facultatea '{facultate}' nu este validă.")
                return "Eroare: Facultatea nu poate conține cifre!", 400

            medie: float = float(medie_raw)
            if medie < 1 or medie > 10:
                logging.error(
                    f"Editare eșuată: Media {medie} este în afara intervalului 1-10.")
                return "Eroare: Media trebuie să fie între 1.00 și 10.00!", 400

            student.nume = nume
            student.facultate = facultate
            student.medie = medie
            student.status_bursa = calculeaza_status_bursa(medie)
            db.session.commit()
            logging.info(f"Student editat: {nume} (ID: {id})")

        except ValueError:
            logging.error("Eroare: Formatul mediei este invalid la editare.")
            return "Eroare: Media trebuie să fie un număr valid!", 400
        except Exception as e:
            db.session.rollback()
            logging.error(f"Eroare neprevăzută la editare: {e}")
            return "Eroare la salvarea datelor.", 500

        return redirect(url_for('index'))

    return render_template('edit.html', student=student)


@app.route('/delete/<int:id>')
def delete_student(id: int) -> Response:
    """
    Șterge un student din baza de date pe baza ID-ului.

    Args:
        id (int): Identificatorul unic al studentului de șters.

    Returns:
        Response: Redirecționare către pagina principală.
    """
    student = Student.query.get(id)
    if student:
        nume_sters = student.nume
        db.session.delete(student)
        db.session.commit()
        logging.info(f"Student șters: {nume_sters} (ID: {id})")

    return redirect(url_for('index'))


@app.route('/report/<int:id>')
def report(id: int) -> Union[str, tuple]:
    """
    Generează și afișează fluturașul de bursă pentru un student specific.

    Args:
        id (int): Identificatorul unic al studentului.

    Returns:
        Union[str, tuple]: Conținutul HTML al raportului sau eroare 404
        dacă studentul nu există.
    """
    student = Student.query.get(id)
    if student:
        logging.info(f"Generare raport pentru: {student.nume}")
        content: str = genereaza_fluturas_bursa(student)
        return f"<pre>{content}</pre><a href='/'>Inapoi</a>"

    logging.error(f"Tentativă de generare raport pentru ID inexistent: {id}")
    return "Student negăsit", 404


if __name__ == '__main__':
    logging.info("Aplicația Flask pornește...")
    app.run(debug=True)
