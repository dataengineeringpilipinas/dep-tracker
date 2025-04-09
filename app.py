from flask import Flask, render_template, request, redirect, url_for
from models import init_db, save_location, get_all_locations
import logging
import folium
from folium.plugins import MarkerCluster
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inject current datetime into all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        if None in (username, latitude, longitude):
            return render_template('index.html', error="All fields are required")
            
        try:
            action = save_location(username, float(latitude), float(longitude))
            logger.info(f"Location {action} for {username}: {latitude}, {longitude}")
            return redirect(url_for('view_locations'))
        except ValueError:
            return render_template('index.html', error="Invalid coordinates")
        except Exception as e:
            logger.error(f"Error saving location: {str(e)}")
            return render_template('index.html', error="Internal server error")
    
    return render_template('index.html')

@app.route('/locations')
def view_locations():
    try:
        locations = get_all_locations()
        return render_template('locations.html', locations=locations)
    except Exception as e:
        logger.error(f"Error retrieving locations: {str(e)}")
        return render_template('locations.html', error="Could not load locations")

@app.route('/map')
def view_map():
    try:
        locations = get_all_locations()
        
        if not locations:
            return render_template('map.html', error="No locations to display")
        
        # Create map centered on first location
        first_location = locations[0]
        m = folium.Map(
            location=[first_location['latitude'], first_location['longitude']],
            zoom_start=10,
            tiles='cartodbpositron'  # Light theme
        )
        
        # Add marker cluster
        marker_cluster = MarkerCluster().add_to(m)
        
        # Add markers
        for loc in locations:
            folium.Marker(
                location=[loc['latitude'], loc['longitude']],
                popup=f"<strong>{loc['username']}</strong><br>"
                      f"Lat: {loc['latitude']:.4f}<br>"
                      f"Lon: {loc['longitude']:.4f}<br>"
                      f"Updated: {loc['last_update_timestamp']}",
                tooltip=loc['username'],
                icon=folium.Icon(color='blue', icon='user', prefix='fa')
            ).add_to(marker_cluster)
        
        map_html = m._repr_html_()
        return render_template('map.html', map_html=map_html)
        
    except Exception as e:
        logger.error(f"Error generating map: {str(e)}")
        return render_template('map.html', error="Could not generate map")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)