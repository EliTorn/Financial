import streamlit as st
import pandas as pd


def load_data():
    # Load the CSV file
    try:
        df = pd.read_csv('data_2.csv')
        # Convert the 'Date' column to datetime
        print(df)
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
        print(df['Date'])
        # Convert 'Volume' to numeric, removing commas
        df['Volume'] = df['Volume'].replace(',', '', regex=True).astype(float)
        return df
    except Exception as e:
        print(f'An error occurred: {e}')
        return pd.DataFrame()


def app():
    st.title('Financial Dashboard')
    data = load_data()
    st.sidebar.header('Filters')
    # Date range filter
    min_date = data['Date'].min()
    max_date = data['Date'].max()
    selected_dates = st.sidebar.date_input('Select date range', [min_date, max_date])
    filtered_data = data[
        (data['Date'] >= pd.Timestamp(selected_dates[0])) & (data['Date'] <= pd.Timestamp(selected_dates[1]))]

    st.write(f'Displaying data from {selected_dates[0]} to {selected_dates[1]}')

    # Display data
    st.dataframe(filtered_data)

    # Line chart for closing prices
    st.subheader('Closing Prices Over Time')
    st.line_chart(filtered_data[['Date', 'Close']].set_index('Date'))

    # Volume histogram
    st.subheader('Volume Distribution')
    st.bar_chart(filtered_data[['Date', 'Volume']].set_index('Date'))

    # Display summary statistics
    st.subheader('Summary Statistics')
    st.write(filtered_data.describe())
