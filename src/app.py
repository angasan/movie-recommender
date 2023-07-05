"""
Main module to implement the foundational functionalities and layout of the app
"""
import streamlit as st
import traceback

from pages import (
    home,
    random_recommender,
    rating_recommender,
    similarity_recommender
    )

def main():
    """
    Main function to implement a movie recommender app
    """

    with st.sidebar:
        # title
        st.title("It's movie time!")

        # blank space
        st.write("")

        # selectbox
        page = st.selectbox(
            "What type of recommendation do you want?",
            [
                "Scroll down:",
                "Based on similarity",
                "Based on ratings",
                "Based on popularity"
                ]
            ) 
        
    if page == "Scroll down:":
        page = home()

    if page == "Based on similarity":
        similarity_recommender()

    if page == "Based on ratings":
        rating_recommender()

    if page == "Based on popularity":
        random_recommender()

if __name__ == "__main__":
    main()
