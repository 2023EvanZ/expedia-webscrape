from flask import Flask, jsonify, request, render_template
from webscrap import fetch_data

app = Flask(__name__)

@app.route('/search', methods=['GET', 'POST'])
def get_data():
    print("RUNNING PROGRAM")
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    location = request.form.get('location')
    travelers = request.form.get('travelers')
    #url = "https://www.expedia.com/Hotel-Search?destination=Kitty+Hawk%2C+North+Carolina%2C+United+States+of+America&regionId=122251&latLong=36.06461%2C-75.705734&flexibility=0_DAY&d1=2024-05-18&startDate=2024-05-18&d2=2024-05-20&endDate=2024-05-20&adults=2&rooms=1&theme=&userIntent=&semdtl=&useRewards=false&sort=RECOMMENDED"
    url = f"https://www.expedia.com/Hotel-Search?destination={location}&startDate={start_date}&endDate={end_date}&adults={travelers}"

    data = fetch_data(url)
    #print(data)
    #print(jsonify(data))

    return render_template('results.html', data=data)

@app.route('/', methods=['GET'])
def home():
    print("TEST")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)