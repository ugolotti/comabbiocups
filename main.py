import streamlit as st
import pandas as pd

# Set il titolo dell'app
st.title("Comabbio Cup")

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

    La Comabbio Cup è un torneo di calcio che si svolge ogni anno a Comabbio.
    Il regolamento prevede che le squadre partecipanti siano divise in due gruppi,
    con partite di andata e ritorno. La squadra vincitrice del torneo sarà quella
    che avrà totalizzato più punti alla fine del torneo.

    Per ulteriori informazioni, si prega di contattare l'organizzazione del torneo.
    """)

# Tab "Documenti"
def tab_documenti():
    st.markdown("""
    # Documenti della Comabbio Cup

    Di seguito è riportata la lista dei documenti disponibili per il download:
    * [Regolamento del torneo](documenti/regolamento.pdf)
    * [Modulo di iscrizione](documenti/iscrizione.pdf)
    * [Lista dei partecipanti](documenti/partecipanti.pdf)
    """)

# Funzione principale
def main():
    # Crea le tab
    tab_classifiche, tab_regolamento, tab_documenti = st.tabs(["Classifiche", "Regolamento", "Documenti"])

    # Aggiungi il contenuto alle tab
    with tab_classifiche:
        tab_classifiche()
    with tab_regolamento:
        tab_regolamento()
    with tab_documenti:
        tab_documenti()

if __name__ == "__main__":
    main()
