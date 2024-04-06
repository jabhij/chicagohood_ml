from flask import Flask, render_template, request, jsonify
import folium
import json

app = Flask(__name__)

# Load GeoJSON data
with open('chicago_neighborhoods.geojson') as f:
    geojson_data = json.load(f)

# Dictionary to store neighborhood data (tags, votes)
neighborhoods = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map():
    # Create a Folium map centered on Chicago
    m = folium.Map(location=[41.8781, -87.6298], zoom_start=10)

    # Add GeoJSON data for neighborhoods
    folium.GeoJson(geojson_data, name='geojson').add_to(m)

    # Add markers for neighborhoods with hover popup showing neighborhood name
    for feature in geojson_data['features']:
        properties = feature['properties']
        geometry = feature['geometry']
        neighborhood_name = properties['name']

        # Add marker with popup showing neighborhood name
        folium.Marker(location=[geometry['coordinates'][1], geometry['coordinates'][0]], 
                      popup=neighborhood_name).add_to(m)

    # Save the map
    m.save('templates/map.html')

    return render_template('map.html')

@app.route('/tag_neighborhood', methods=['POST'])
def tag_neighborhood():
    neighborhood = request.form['neighborhood']
    tag = request.form['tag']

    # Add the tag to the neighborhood
    if neighborhood in neighborhoods:
        neighborhoods[neighborhood]['tags'].append(tag)
    else:
        neighborhoods[neighborhood] = {'tags': [tag], 'votes': 0}
    
    return jsonify({'success': True})

@app.route('/vote_neighborhood', methods=['POST'])
def vote_neighborhood():
    neighborhood = request.form['neighborhood']
    vote_type = request.form['vote']

    # Upvote or downvote the neighborhood
    if neighborhood in neighborhoods:
        if vote_type == 'upvote':
            neighborhoods[neighborhood]['votes'] += 1
        elif vote_type == 'downvote':
            neighborhoods[neighborhood]['votes'] -= 1
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
