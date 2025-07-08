import streamlit as st
import pandas as pd
import random

# Set il titolo dell'app
st.title("Gloria e Disagio - Comabbio Cup")

# Funzione per calcolare i punti in base al piazzamento
def calcola_punti(piazzamento):
    if pd.isnull(piazzamento):
        return 0
    elif piazzamento == 1:
        return 100
    elif piazzamento == 2:
        return 80
    elif piazzamento == 3:
        return 60
    elif piazzamento == 4:
        return 40
    else:
        return 10

# Carica il file CSV in un DataFrame di pandas
def load_data(file_name):
    try:
        data = pd.read_csv(file_name)
        # Calcola il punteggio per ogni tappa
        data["points"] = 0
        for col in data.columns:
            if col.startswith("Tappa"):
                data["points"] += data[col].apply(calcola_punti)
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
    """)

    # List of documents
    documents = {
        "Template programma 4 squadre": "documenti/schedule_4.pdf",
        "Template programma 5 squadre": "documenti/schedule_5.pdf",
        "Template programma 6 squadre": "documenti/schedule_6.pdf"
    }

    # Loop through documents and create a download button for each
    for doc_name, doc_path in documents.items():
        with open(doc_path, "rb") as file:
            btn = st.download_button(
                label=f"Scarica {doc_name}",
                data=file,
                file_name=os.path.basename(doc_path),
                mime="application/pdf"
            )


# Tab "Sorteggio"
def tab_sorteggio():
    # Carica i dati
    data = load_data("standings.csv")

    # Seleziona i partecipanti
    partecipanti = st.multiselect("Seleziona i partecipanti", data["Nome"].tolist())

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
                df_coppie = pd.DataFrame(coppie, columns=["Player 1", "Player 2"])
                st.table(df_coppie)
        with col2:
            if st.button("Ranking-based"):
                # Ordina i partecipanti per punteggio
                partecipanti_ordinati = [nome for nome in partecipanti]
                punteggi = {}
                for index, row in data.iterrows():
                    punteggi[row["Nome"]] = row["points"]
                partecipanti_ordinati.sort(key=lambda x: punteggi[x], reverse=True)
                # Accoppia i partecipanti
                coppie = []
                for i in range(len(partecipanti_ordinati) // 2):
                    coppie.append((partecipanti_ordinati[i], partecipanti_ordinati[-i - 1]))
                if len(partecipanti_ordinati) % 2 == 1:
                    coppie.append((partecipanti_ordinati[len(partecipanti_ordinati) // 2], " Bye"))
                st.write("Coppie:")
                df_coppie = pd.DataFrame(coppie, columns=["Player 1", "Player 2"])
                st.table(df_coppie)

# Funzione principale
def main():
    # Crea le tab
    tabs = st.tabs(["Classifiche", "Regolamento", "Documenti", "Sorteggio"])

    # Aggiungi il contenuto alle tab
    with tabs[0]:
        st.header("Classifiche")
        tab_classifiche()
    with tabs[1]:
        st.header("Regolamento")
        tab_regolamento()
    with tabs[2]:
        st.header("Documenti")
        tab_documenti()
    with tabs[3]:
        st.header("Sorteggio")
        tab_sorteggio()

if __name__ == "__main__":
    main()
