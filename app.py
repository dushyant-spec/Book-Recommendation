# import libraries
import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(layout='wide')

st.header('❤️ Book Recommender System ❤️')

st.markdown('''
          ##### The site using colaborative filtering suggests books from our catalog.
          ##### We recommend top 50 books for every one as well
          ''')

# import out models : 

popular = pickle.load(open('popular.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Top 50 Books :

st.sidebar.title("Top 50 Books")

if st.sidebar.button("SHOW"):
  cols_per_row = 5
  num_rows = 10
  for row in range(num_rows):
    cols = st.columns(cols_per_row)
    for col in range(cols_per_row):
      book_indx = row * cols_per_row + col
      if book_indx < len(popular):
        with cols[col]:
          st.image(popular.iloc[book_indx]['Image-URL-M']) # Displays the image
          st.text(popular.iloc[book_indx]['Book-Title']) # Displays the Book Title
          st.text(popular.iloc[book_indx]['Book-Author']) # Displays the Author name


# Function to recommend Books

def recommend(book_name):
  index = np.where(pt.index == book_name)[0][0]
  similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x : x[1], reverse=True)[1:6]
  # Lets create empty list and in that list i want at populate with the book information
  # Book author boo-title image-url 
  # Empty list
  data = []
  for i in similar_items: 
      item = []
      temp_df = books[books['Book-Title'] == pt.index[i[0]]]
      item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
      item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
      item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
      data.append(item)
  return data

# this is giving the names list of books.
book_list = pt.index.values

st.sidebar.title("Similar Book Suggestions")
# Drop down to select the books
selected_book = st.sidebar.selectbox("Select a bookfrom the dropdown", book_list)

# 
if st.sidebar.button("Recommend Me"):
  book_recommend = recommend(selected_book)
  cols = st.columns(5)
  for col_idx in range(5):
    with cols[col_idx]:
      if col_idx < len(book_recommend):
        st.image(book_recommend[col_idx][2])
        st.text(book_recommend[col_idx][0])
        st.text(book_recommend[col_idx][1])



# import data

books = pd.read_csv('Books.csv')
users = pd.read_csv('Users.csv')
ratings = pd.read_csv('Ratings.csv')


st.sidebar.title("Data Used")


if st.sidebar.button("Show Data"):
  st.subheader("This is the books data we used in our model")
  st.dataframe(books)
  st.subheader("This is the User ratings data we used in our model")
  st.dataframe(ratings)
  st.subheader("This is the user data we used in our model")
  st.dataframe(users)

















