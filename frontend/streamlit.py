import streamlit as st
import requests
import json
import pandas as pd
import base64


def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="file.csv">Download CSV File</a>'
    return href


def run():
    st.title("Movie Maniac")

    menu = ["Netflix weekly top10", "Predict movies to watch", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Netflix weekly top10":
        st.subheader("Netflix weekly top10")
        resp = requests.get("http://127.0.0.1:8000/get_movies")
        json_data = json.loads(resp.text)
        json_data = eval(json_data)
        df = pd.DataFrame(json_data)
        st.dataframe(df)
        st.markdown(filedownload(df), unsafe_allow_html=True)

    if choice == "Predict movies to watch":
        st.subheader("Predict movies to watch")

        movie = st.text_input("Enter the movie you have watched")
        data = {
            "movie": movie
        }
        if st.button("Predict"):
            resp = requests.post("http://127.0.0.1:8000/predict_movies", json=data)
            json_data = json.loads(resp.text)
            # print(json_data)
            df = pd.DataFrame(json_data.values(), columns=['movies'])
            st.dataframe(df)
            st.markdown(filedownload(df), unsafe_allow_html=True)
    if choice == "About":
        st.subheader("About")
        frameworks_expand = st.expander("Frameworks used")
        frameworks_expand.markdown("""
           * **Python libraries:** base64, requests, json, time
           * **Front-end:** streamlit
           * **Back-end:** FastAPI
           * **ML:** collaborative based filtering to predict movies using sklearn, scipy, numpy, pandas 
           """)

        data_source = st.expander("Data Source")
        data_source.markdown("""
           * **Netflix weekly top 10:** [Rapid API netflix weekly top 10](https://rapidapi.com/mhtdy/api/netflix-weekly-top-10/)
           * **Find nearby theatres:** [Google maps API](https://developers.google.com/maps/documentation/places/web-service/search-nearby)
           """)

        about_me = st.expander("Source code and connectivity")
        about_me.markdown("""
           * **Github:** [Github repo](https://github.com/sanial2001/movies_fastapi)
           * **LinkedIn:** [LinkedIn](https://www.linkedin.com/in/muskan-verma-b45648206/)
           """)


if __name__ == "__main__":
    run()
