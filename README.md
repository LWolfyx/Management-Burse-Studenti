Minea Paul-Alexandru

# Sistem de Gestiune a Burselor Studențești

O aplicație web construită în Python cu Flask care permite gestionarea studenților și a burselor acestora. Aplicația oferă operații complete CRUD, filtrare, sortare și generare de rapoarte.

---

## Descriere

Aplicația permite unui secretariat sau unui utilizator să țină evidența studenților dintr-o facultate. Pe baza mediei generale, sistemul calculează automat tipul de bursă la care are dreptul fiecare student și oferă posibilitatea de a genera un fluturaș detaliat cu informațiile bursei.

---

## Funcționalități

- **Adăugare studenți** cu validare completă a datelor introduse
- **Editare** date student cu recalculare automată a statusului bursei
- **Ștergere** student cu confirmare
- **Căutare** după nume sau facultate
- **Filtrare** după tipul bursei (Bursă de Merit / Bursă de Studiu / Fără Bursă)
- **Sortare** după nume, medie sau facultate
- **Generare raport** (fluturaș de bursă) pentru fiecare student
- **Logging** complet al tuturor acțiunilor în consolă și în fișierul `app.log`

### Calcul automat status bursă

| Medie | Status |
|-------|--------|
| ≥ 9.50 |  Bursă de Merit — 1000 RON |
| ≥ 8.50 |  Bursă de Studiu — 700 RON |
| < 8.50 |  Fără Bursă |

---

Tehnologii utilizate

Python 3
Flask — framework web
SQLAlchemy — baza de date
SQLite — stocare date
Jinja2 + HTML/CSS — interfața grafică

---

## Structura proiectului

```
proiect/
├── app.py          # Logica aplicației și rutele Flask
├── models.py       # Modelul bazei de date (SQLAlchemy)
├── utils.py        # Generare rapoarte (fluturaș bursă)
├── studenti.db     # Baza de date SQLite (generată automat)
├── app.log         # Fișier de logging (generat automat)
└── templates/
    ├── index.html  # Pagina principală
    └── edit.html   # Formular editare student
```

---

proiect/
├── app.py
├── models.py
├── utils.py
└── templates/
    ├── index.html
    └── edit.html

Instalare și rulare
1. Instalează dependințele
bash
pip install flask flask-sqlalchemy
3. Pornește aplicația
bash
python app.py
Aplicația va fi disponibilă la http://localhost:5000.

## 📦 Dependințe

```
Flask
Flask-SQLAlchemy
```
---

## Utilizare

1. Deschide browserul la adresa `http://localhost:5000`
2. Adaugă studenți folosind formularul din partea de sus
3. Folosește bara de căutare, dropdown-ul de filtrare sau butoanele de sortare pentru a naviga prin lista de studenți
4. Apasă **✏️ Editează** pentru a modifica datele unui student
5. Apasă **📄 Raport** pentru a genera fluturașul de bursă
6. Apasă **🗑️ Șterge** pentru a elimina un student din bază

---
