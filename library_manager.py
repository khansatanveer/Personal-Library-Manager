import streamlit as st 
import pandas as pd 
import json 
import os 
from datetime import datetime
import time
import random
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# set page config
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚✨", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# custom css
st.markdown("""
<style>
            .main-header {
                color: #f63366;
                font-size: 3rem !important;
                text-align: center;
                margin-top: 1rem;
                margin-bottom: 1rem;
                font-weight: 700;
                font-family: 'Roboto', sans-serif;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            }

        .sub-header  {
            color: #3B82F6;
    font-size: 1.8rem !important;
    text-align: center;
    margin-top: 1rem;
    margin-bottom: 1rem;
    font-weight: 600;
    font-family: 'Roboto', sans-serif;
}

            .success {
                padding: 1rem;
                background-color: #ECFDF5;
                border-left: 5px solid #10B981;
                border-radius: 0.375rem;
            }

            .warning {
                padding: 1rem;
                background-color: #FFFBEB;
                border-left: 5px solid #F59E0B;
                border-radius: 0.375rem;
            }

            .book-card {
                padding: 1rem;
                background-color: #F3F4F6;
                margin: 1rem;
                border-left: 5px solid #F59E0B;
                transition: transform 0.3s ease;
            }

            .book-card:hover {
                transform:translateY(-5px);
                box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
            }

            .read-badge {
                background-color: #10B981;
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 1rem;
                font-size: 0.875rem;
                font-weight: 600;
            }

            .not-read-badge {
                background-color: #F87171;
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 1rem;
                font-size: 0.875rem;
                font-weight: 600;
            }

            .action-button {
                margin-right: 0.5rem;
            }

            .st-btn>button {
                border-radius: 0.5rem;
            }
</style>
""", unsafe_allow_html=True)


def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None
# Initialize session states
if 'library' not in st.session_state:
    st.session_state.library = []
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'book_added' not in st.session_state:
    st.session_state.book_added = False
if 'book_removed' not in st.session_state:
    st.session_state.book_removed = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = "library"

# Load and save library functions
def load_library():
    try:
        if os.path.exists("library.json"):
            with open("library.json", "r") as file:
                st.session_state.library = json.load(file)
                return True
        return False
    except Exception as e:
        st.error(f"An error occurred while loading the library. {e}")
        return False

# save library
def save_library():
    try:
        with open("library.json", "w") as file:
            json.dump(st.session_state.library, file)
        return True
    except Exception as e:
        st.error(f"An error occurred while saving the library. {e}")
        return False
    
# add book
def add_book(title, author,  publication_year, genre, read_status, pages):
    book = {
        "title": title,
        "author": author,
        "publication_year": publication_year,
        "genre": genre,
        "read_status": read_status,
        "pages": pages,
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(1)
    
# Remove book function
def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True
        return True
    return False

# search books
def search_books(search_term, search_by):
    search_term = search_term.lower()
    results = []

    for book in st.session_state.library:
        if search_by == "Title" and search_term in book["title"].lower():
            results.append(book)
        elif search_by == "Author" and search_term in book["author"].lower():
            results.append(book)
        elif search_by == "Genre" and search_term in book["genre"].lower():  # Fixed key name
            results.append(book)
    
    st.session_state.search_results = results

# Library status function (Move this outside of search_books)
def get_library_status():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read_status"])  # Fixed key name
    percentage = (read_books / total_books) * 100 if total_books > 0 else 0

    genres = {}
    authors = {}
    decades = {}

    for book in st.session_state.library:
        # For genres
        genre = book["genre"]  # Fixed key name
        if genre in genres:
            genres[genre] += 1
        else:
            genres[genre] = 1

        # For authors
        author = book["author"]  # Fixed key name
        if author in authors:
            authors[author] += 1
        else:
            authors[author] = 1

        # For decades
        decade = (book["publication_year"] // 10) * 10
        if decade in decades:
            decades[decade] += 1
        else:
            decades[decade] = 1

    # Sort by count
    genres = dict(sorted(genres.items(), key=lambda x: x[1], reverse=True))
    authors = dict(sorted(authors.items(), key=lambda x: x[1], reverse=True))
    decades = dict(sorted(decades.items(), key=lambda x: x[0], reverse=True))

    return {
        "total_books": total_books,
        "read_books": read_books,
        "percentage": percentage,
        "genres": genres,
        "authors": authors,
        "decades": decades
    }


def create_visulations(status):
    if status["total_books"] > 0:
        fig_read_status = go.Figure(data=[go.Pie(
            labels=["Read", "Not Read"], 
            values=[status["read_books"], 
            status["total_books"] - status["read_books"]],
            hole=0.3,
            marker_colors=["#10B981", "#F87171"]
        )])
        fig_read_status.update_layout(
            title="Read VS NotR=read books",
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig_read_status, use_container_width=True)

        # bar chart for genres
        if status['genres']:
            genres_df = pd.DataFrame({
                'Genre': list(status['genres'].keys()),
                'Count': list(status['genres'].values())
            })
            fig_genres = px.bar(
                genres_df, 
                x='Genre', 
                y='Count', 
                color='Count',
                color_continuous_scale=px.colors.sequential.Blues,
                )
            fig_genres.update_layout(
                title="Books by publication decade",
                xaxis_title="Decade",
                yaxis_title="Number of books",
                height=400
            )
            st.plotly_chart(fig_genres, use_container_width=True)
        if status['decades']:
            decades_df = pd.DataFrame({
            'Decade': [f"{decade}s" for decade in status['decades'].keys()], 
            'Count': list(status['decades'].values())
        })
    fig_decades = px.line(
        decades_df, 
        x='Decade', 
        y='Count', 
        markers=True,
        line_space="spline"
    )
    fig_decades.update_layout(
        title_text="Books by publication decade",
        xaxis_title="Decade",
        yaxis_title="Number of books",
        height=400
    )
    st.plotly_chart(fig_decades, use_container_width=True)

# load library
load_library()
st.sidebar.markdown("<h1 style='text-align: center;'>Navigation</h1>", unsafe_allow_html=True)
lottie_book = load_lottie_url("https://assets9.lottiefiles.com/temp/lf20_aKAfIn.json")
if lottie_book:
    with st.sidebar:
        st_lottie(lottie_book, 
                width=200,
                height=200,
                key="book_animation")
        nav_options = st.sidebar.radio(
            "Choose option", ["View Library", "Add Book", "Search Books", "Library Statistics"])
        if nav_options == "View Library":
            st.session_state.current_view = "library"
        elif nav_options == "Add Book":
            st.session_state.current_view = "add"
        elif nav_options == "Search Books":
            st.session_state.current_view = "search"
        elif nav_options == "Library Statistics":
            st.session_state.current_view = "status"


        st.markdown("<h1 class= 'main-header'> PERSONAL LIBRARY MANAGER </h1>" , unsafe_allow_html=True)
        if st.session_state.current_view == "add":
            st.markdown("<h2 class='sub-header'> Add a new book </h2>", unsafe_allow_html=True)

            with st.form ("add_book_form"):
                col1, col2 = st.columns(2)

                with col1:
                    title = st.text_input("Book Title", max_chars=100)
                    author = st.text_input("Author", max_chars=100)
                    publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, step=1, value=2023)

                    with col2:
                        genre = st.text_input("Genre", [
                            "Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery", "Thriller", "Romance", "Biography", "Autobiography", "Self-Help", "Historical Fiction", "Young Adult", "Children's", "Poetry", "Graphic Novel", "Others"
                            ])
                        read_status = st.radio("Read Status", ["Read", "Not Read"], horizontal=True)
                        read_bool = read_status == "Read"
                        pages = st.number_input("Pages", min_value=1, max_value=10000, step=1, value=100)
                        submit_button = st.form_submit_button(label="Add Book")

                        if submit_button and title and author :
                            add_book(title, author, publication_year, genre, read_bool, pages)


                        if st.session_state.book_added:
                            st.markdown("<div class='success-message'> Book added successfully! </div>", unsafe_allow_html=True)
                            st.balloons()
                            st.session_state.book_added = False
                        else:
                            st.session_state.current_view = "library"
                        st.markdown("<h2 class = 'sub-header'> YOUR LIBRARY </h2>", unsafe_allow_html=True)

                        if not st.session_state.library:
                            st.markdown("<div class='warning-message'> Your library is empty. Add a book to get started! </div>", unsafe_allow_html=True)
                        else:
                            cols = st.columns(2)
                            for i, book in enumerate(st.session_state.library):
                                with cols[i % 2]:
                                    st.markdown(f"""<div class='book-card'> 
                                                <h3> {book['title']} </h3> 
                                                <p><strong> Author:</strong> {book['author']} </p> 
                                                <p><strong> Genre:</strong> {book['genre']} </p> 
                                                <p><strong> Publication Year:</strong> {book['publication_year']} </p> 
                                                <p><strong> Pages:</strong> {book['pages']} </p>
                                                <p><span class='read-badge'> {"Read-badge" if book["read_status"] else "Not Read"} '>{
                                                "Read" if book["read_status"] else "Not Read"
                                                }</span></p> 
                                                <p> Added on: {book['date_added']} </p> 
                                                </div>
                                                """, unsafe_allow_html=True)
                                    
                                    cols1, cols2 = st.columns(2)
                                    with col1:
                                        if st.button("Remove Book", key=f"remove_{i}", use_container_width=True):
                                            if remove_book(i):
                                                st.rerun()
                                    with col2:
                                        new_status = not book["read_status"]
                                        status_lable = "Mark as  Read" if not book["read_status"] else "Mark as Not Read"
                                        if st.button(status_lable, key=f"status_{i}", use_container_width=True):
                                            st.session_state.library[i]["read_status"] = new_status
                                            save_library()
                                            st.rerun()
                                        

                                    if st.session_state.book_removed:
                                        st.markdown("<div class='success-message'> Book removed successfully! </div>", unsafe_allow_html=True)
                                        st.session_state.book_removed = False
                                    elif st.session_state.current_view == "search":
                                        st.markdown("<h2 class='sub-header'> Search Books </h2>", unsafe_allow_html=True)

                                        search_by = st.selectbox("Search by:", ["Title", "Author", "Genre"])
                                        search_term = st.text_input("Search term")

                                        if st.button("Search",use_container_width=True):
                                            if search_term:
                                                with st.spinner("Searching..."):
                                                    search_books(search_term, search_by)

                                                    if hasattr(st.session_state, 'search_results'):
                                                        if st.session_state.search_results:
                                                            st.markdown(f"<h3> Found {len(st.session_state.search_results)} results: </h3>", unsafe_allow_html=True)

                                                            for i, book in enumerate(st.session_state.search_results):
                                                                st.markdown(f"""<div class='book-card'>
                                                                            <h3> {book['title']} </h3>
                                                                            <p><strong> Author:</strong> {book['author']} </p>
                                                                            <p><strong> Genre:</strong> {book['genre']} </p>
                                                                            <p><strong> Publication Year:</strong> {book['publication_year']} </p>
                                                                            <p><strong> Pages:</strong> {book['pages']} </p>
                                                                            <p><span class='read-badge'> {"Read-badge" if book["read_status"] else "Not Read"} '>{
                                                                                "Read" if book["read_status"] else "Not Read"
                                                                                }</span></p>
                                                                                </div>
                                                                """, unsafe_allow_html=True)
                                                        elif search_term:
                                                            st.markdown("<div class='warning-message'> No book found matching your search. </div>", unsafe_allow_html=True)
                                                            
                                                        elif st.session_state.current_view == "status":
                                                            st.markdown("<h2 class='sub-header'> Library Statistics </h2>", unsafe_allow_html=True)

                                                            if not st.session_state.library:
                                                                st.markdown("<div class='warning-message'> Your library is empty. Add some book too see statics ! </div>", unsafe_allow_html=True)
                                                            else:
                                                                stats = get_library_status()
                                                                col1,col2,col3 = st.columns(3)
                                                                with col1:
                                                                    st.metric("Total Books", stats["total_books"])
                                                                with col2:
                                                                    st.metric("Read Books", stats["read_books"])
                                                                with col3:
                                                                    st.metric("Percentage Read", f"{stats['percentage']:.1f}%")
                                                                create_visulations()

                                                                if stats['authors']:
                                                                    st.markdown("<h3> Top Authors </h3>", unsafe_allow_html=True)
                                                                    top_authors = dict(list(stats['authors'].items())[:5])
                                                                    for author, count in top_authors.items():
                                                                        st.markdown(f"**{author}**: {count} book{'s' if count > 1 else ''}")

                                                                        st.markdown("---")
                                                                        st.markdown("Copyright @ 2025 Khansa TanveerAhmed Personal Library Manager", unsafe_allow_html=True)
                        


