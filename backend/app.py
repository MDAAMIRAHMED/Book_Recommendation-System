from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

def load_data_and_model():
    books = pd.read_csv('dataset/Books.csv', dtype=str, low_memory=False)
    ratings = pd.read_csv('dataset/Ratings.csv', low_memory=False)

    ratings = ratings.dropna(subset=['User-ID', 'ISBN', 'Book-Rating'])
    books = books.dropna(subset=['ISBN', 'Book-Title'])

    user_rating_counts = ratings['User-ID'].value_counts()
    book_rating_counts = ratings['ISBN'].value_counts()
    user_threshold = 10
    book_threshold = 5
    ratings = ratings[ratings['User-ID'].isin(user_rating_counts[user_rating_counts >= user_threshold].index)]
    ratings = ratings[ratings['ISBN'].isin(book_rating_counts[book_rating_counts >= book_threshold].index)]

    ratings_agg = ratings.groupby(['User-ID', 'ISBN']).agg({'Book-Rating': 'mean'}).reset_index()
    combine_book_rating = pd.merge(ratings_agg, books, on='ISBN')
    combine_book_rating = combine_book_rating.dropna(axis=0, subset=['Book-Title'])
    book_rating_count = (combine_book_rating.groupby(by=['Book-Title'])['Book-Rating']
                         .count().reset_index().rename(columns={'Book-Rating': 'totalRatingCount'}))
    rating_with_total_rating_count = combine_book_rating.merge(book_rating_count, left_on='Book-Title', right_on='Book-Title', how='left')
    POP_THRESHOLD = 50
    rating_popular_book = rating_with_total_rating_count[rating_with_total_rating_count['totalRatingCount'] >= POP_THRESHOLD]
    rating_popular_book = rating_popular_book.drop_duplicates(subset=['Book-Title', 'User-ID'])
    combined_pivot = rating_popular_book.pivot(index='Book-Title', columns='User-ID', values='Book-Rating').fillna(0)
    combined_matrix = csr_matrix(combined_pivot.values)

    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(combined_matrix)
    joblib.dump(model_knn, 'knn_model.pkl')
    model_knn = joblib.load('knn_model.pkl')

    return books, ratings, model_knn, combined_pivot, book_rating_count

books, ratings, model_knn, combined_pivot, book_rating_count = load_data_and_model()

def convert_to_serializable(data):
    """ Convert data to a JSON serializable format """
    if isinstance(data, pd.Series):
        return data.to_list()
    elif isinstance(data, pd.DataFrame):
        return data.to_dict(orient='records')
    elif isinstance(data, pd.Index):
        return data.tolist()
    elif isinstance(data, (int, float, str, bool)):
        return data
    elif isinstance(data, (dict, list)):
        return data
    else:
        raise TypeError(f"Type {type(data).__name__} not serializable")

def recommend_books_by_title(model_knn, combined_pivot, book_title, n_neighbors=7):
    if book_title not in combined_pivot.index:
        return [{'title': f'Book title "{book_title}" not found in the dataset.'}]

    query_index = combined_pivot.index.get_loc(book_title)
    distances, indices = model_knn.kneighbors(combined_pivot.iloc[query_index, :].values.reshape(1, -1), n_neighbors=n_neighbors)

    recommendations = []
    for i in range(1, len(distances.flatten())):
        book = combined_pivot.index[indices.flatten()[i]]
        book_details = books[books['Book-Title'] == book].iloc[0]
        recommendations.append({
            'title': book,
            'author': book_details.get('Book-Author', 'N/A'),
            'rating': book_details.get('Book-Rating', 'N/A'),
            'year': book_details.get('Year-Of-Publication', 'N/A'),
            'publisher': book_details.get('Publisher', 'N/A'),
            'image_url': book_details.get('Image-URL-M', ''),
            'totalRatingCount': int(book_rating_count[book_rating_count['Book-Title'] == book]['totalRatingCount'].values[0])
        })

    return recommendations

@app.route('/recommend', methods=['GET'])
def recommend():
    book_title = request.args.get('title')
    if not book_title:
        return jsonify({"error": "Please provide a book title."}), 400
    recommendations = recommend_books_by_title(model_knn, combined_pivot, book_title)
    recommendations = convert_to_serializable(recommendations)
    return jsonify(recommendations)

@app.route('/top_recommendations', methods=['GET'])
def top_recommendations():
    try:
        n_top = int(request.args.get('n', 10))
    except ValueError:
        return jsonify({"error": "Invalid value for parameter 'n'."}), 400

    top_books = book_rating_count.sort_values(by='totalRatingCount', ascending=False).head(n_top)
    recommendations = []
    for index, row in top_books.iterrows():
        book_details = books[books['Book-Title'] == row['Book-Title']].iloc[0]
        recommendations.append({
            'title': row['Book-Title'],
            'author': book_details.get('Book-Author', 'N/A'),
            'rating': book_details.get('Book-Rating', 'N/A'),
            'year': book_details.get('Year-Of-Publication', 'N/A'),
            'publisher': book_details.get('Publisher', 'N/A'),
            'image_url': book_details.get('Image-URL-M', ''),
            'totalRatingCount': int(row['totalRatingCount'])
        })

    recommendations = convert_to_serializable(recommendations)
    return jsonify(recommendations)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
