import streamlit as st
import pandas as pd

# Set the title of the app
st.title("Comabbio Cup")

# Load the CSV file into a pandas DataFrame
def load_data(file_name):
    try:
        data = pd.read_csv(file_name)
        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")

# Main function
def main():
    # Load the data
    data = load_data("standings.csv")

    # Display the data
    if data is not None:
        st.write(data)

if __name__ == "__main__":
    main()
