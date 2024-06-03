from flask import Flask, jsonify, render_template, request
import pandas as pd

# Load the dataset
df = pd.read_csv("final_dataset.csv")
app = Flask(__name__)

# Route for rendering the HTML page with the search button
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling the search request
@app.route('/search', methods=['GET'])
def search_laptop():
    amazon_title = request.args.get('title')
    print("Search Query:", amazon_title)  # Debugging print statement
    result = df[df['Amazon Title'].str.contains(amazon_title, case=False, regex=False)]
    print("Search Result:", result)  # Debugging print statement
    
    if len(result) == 0:
        return jsonify({"error": "Laptop not found"}), 404
    
    amazon_info = {
        "title": result.iloc[0]['Amazon Title'],
        "link": result.iloc[0]['Amazon Link'],
        "description": result.iloc[0]['Amazon Description'],
        "price": result.iloc[0]['Amazon Price']
    }
    
    best_buy_info = {
        "title": result.iloc[0]['Best Buy Title'],
        "link": result.iloc[0]['Best Buy Link'],
        "price": result.iloc[0]['Best Buy Price']
    }
    
    return render_template('search_results.html', amazon=amazon_info, best_buy=best_buy_info)

# Route for fetching available laptops
@app.route('/laptops', methods=['GET'])
def get_laptops():
    laptops = df['Amazon Title'].tolist()
    return jsonify(laptops)

if __name__ == '__main__':
    app.run(debug=True, port=9999)
