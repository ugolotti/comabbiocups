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


# Tab "Sorteggio"
def tab_sorteggio():
    # Carica i dati
    data = load_data("standings.csv")

    # Seleziona i partecipanti
    partecipanti = st.multiselect("Seleziona i partecipanti", data["name"].tolist())

    # Se sono stati selezionati partecipanti, mostra i pulsanti
    if partecipanti:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Genera coppie casuali"):
                # Genera coppie casuali
                random.shuffle(partecipanti)
                coppie = []
                for i in range(0, len(partecipanti), 2):
                    if i + 1 < len(partecipanti):
                        coppie.append((partecipanti[i], partecipanti[i + 1]))
                    else:
                        coppie.append((partecipanti[i], " Bye"))
                st.write("Coppie:")
                for coppia in coppie:
                    st.write(coppia)
        with col2:
            if st.button("Ranking-based"):
                # Ordina i partecipanti per punteggio
                partecipanti_ordinati = [nome for nome in partecipanti]
                punteggi = {}
                for index, row in data.iterrows():
                    punteggi[row["name"]] = row["result1"] + row["result2"] + row["result3"]
                partecipanti_ordinati.sort(key=lambda x: punteggi[x], reverse=True)
                # Accoppia i partecipanti
                coppie = []
                for i in range(len(partecipanti_ordinati) // 2):
                    coppie.append((partecipanti_ordinati[i], partecipanti_ordinati[-i - 1]))
                if len(partecipanti_ordinati) % 2 == 1:
                    coppie.append((partecipanti_ordinati[len(partecipanti_ordinati) // 2], " Bye"))
                st.write("Coppie:")
                for coppia in coppie:
                    st.write(coppia)

# Funzione principale
def main():
    # Crea le tab
    tabs = st.tabs(["Classifiche", "Regolamento", "Documenti", "Sorteggio"])

    # Aggiungi il contenuto alle tab
    with tabs[0]:
        st.header("<font color='red'>Classifiche</font>")
        tab_classifiche()
    with tabs[1]:
        st.header("<font color='blue'>Regolamento</font>")
        tab_regolamento()
    with tabs[2]:
        st.header("<font color='green'>Documenti</font>")
        tab_documenti()
    with tabs[3]:
        st.header("<font color='purple'>Sorteggio</font>")
        tab_sorteggio()

if __name__ == "__main__":
    main()
