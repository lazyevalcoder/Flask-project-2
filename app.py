from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def form():
    return render_template('upload.html')

import pandas as pd
from io import StringIO

@app.route('/', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        
        # Read data from uploaded CSV file into a pandas DataFrame
        data = pd.read_csv(StringIO(file.stream.read().decode("UTF8"))) 
        
        # Strip whitespace from column names
        data.columns = data.columns.str.strip()

        # Check if 'Population' and 'City' columns are present
        if 'Population' not in data.columns or 'City' not in data.columns:
            return render_template('upload.html', error="CSV file must contain 'City' and 'Population' columns.")  # Error message for missing columns
        
        # Calculate top 3 cities with highest population
        top_cities = data.nlargest(3, 'Population')
        
        # Convert DataFrame to dictionary (for easy serialization)
        top_cities_dict = top_cities.to_dict('records')  

        # Calculate average population
        avg_population = data['Population'].mean()
        
        # Calculate median population
        median_population = data['Population'].median()

    return render_template('upload.html', top_cities=top_cities_dict, 
                           avg_population=avg_population, median_population=median_population)

if __name__ == '__main__':
    app.run(debug=True)