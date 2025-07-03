import streamlit as st
import pandas as pd

# Set il titolo dell'app
st.title("Comabbio Cup - Gloria e Disagio")

# Carica il file CSV in un DataFrame di pandas
def load_data(file_name):
    try:
        data = pd.read_csv(file_name)
        return data
    except Exception as e:
        st.error(f"Errore di caricamento dei dati: {e}")

# Tab "Classifiche"
def tab_classifiche():
    # Carica i dati
    data = load_data("standings.csv")

    # Visualizza i dati
    if data is not None:
        st.write(data)

# Tab "Regolamento"
def tab_regolamento():
    st.markdown("""
    # Regolamento della Comabbio Cup

    Il torneo si compone di un numero variabile di tappe.

    In ogni tappa partecipano N squadre, composte da 2 giocatori ciascuna.

    Le squadre sono formate casualmente all’inizio di ogni tappa tramite sorteggio.

    Ogni giocatore accumula punti individuali in base alla posizione finale ottenuta dalla sua squadra.
    """)

# Tab "Documenti"
def tab_documenti():
    st.markdown("""
    # Documenti della Comabbio Cup

    Di seguito è riportata la lista dei documenti disponibili per il download:
    * [Regolamento del torneo](documenti/regolamento.pdf)
    * [Template programma](documenti/programma.pdf)
    """)

# Funzione principale
def main():
    # Crea le tab
    tabs = st.tabs(["Classifiche", "Regolamento", "Documenti"])

    # Aggiungi il contenuto alle tab
    with tabs[0]:
        tab_classifiche()
    with tabs[1]:
        tab_regolamento()
    with tabs[2]:
        tab_documenti()

if __name__ == "__main__":
    main()
