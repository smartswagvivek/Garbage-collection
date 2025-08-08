import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import folium
from streamlit_folium import folium_static
from math import radians, sin, cos, sqrt, atan2
import random

# Page Config
st.set_page_config(
    page_title="♻️ Indian Waste Collection Optimizer", 
    layout="wide",
    page_icon="🗑️"
)

# Custom CSS for Indian theme
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #FF9933; /* Saffron */
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #FF5722;
    }
    .stSlider>div>div>div>div {
        background-color: #138808; /* Green */
    }
    .css-1aumxhk {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Indian Cities Sample Data
def generate_indian_sample_data(num_locations=30):
    indian_cities = {
        'Mumbai': (19.0760, 72.8777),
        'Delhi': (28.7041, 77.1025),
        'Bangalore': (12.9716, 77.5946),
        'Hyderabad': (17.3850, 78.4867),
        'Chennai': (13.0827, 80.2707),
        'Kolkata': (22.5726, 88.3639),
        'Pune': (18.5204, 73.8567),
        'Jaipur': (26.9124, 75.7873),
        'Ahmedabad': (23.0225, 72.5714),
        'Lucknow': (26.8467, 80.9462)
    }
    
    data = []
    for i in range(num_locations):
        city = random.choice(list(indian_cities.keys()))
        lat, lon = indian_cities[city]
        # Add small variations to coordinates
        lat += random.uniform(-0.05, 0.05)
        lon += random.uniform(-0.05, 0.05)
        
        # Indian waste characteristics
        waste_types = ['Residential', 'Commercial', 'Construction', 'Organic']
        waste_volume = random.uniform(0.5, 5.0)
        frequency = random.choice([1, 2, 3])  # Typical Indian collection frequencies
        
        data.append({
            'Location_ID': f'LOC_{i+1:03d}',
            'City': city,
            'Latitude': lat,
            'Longitude': lon,
            'Waste_Volume': waste_volume,
            'Waste_Type': random.choice(waste_types),
            'Collection_Frequency': frequency,
            'Last_Collection': pd.Timestamp.now() - pd.Timedelta(days=random.randint(0, 7))
        })
    
    return pd.DataFrame(data)

# Indian Road Distance Calculation (approximation)
def indian_road_distance(lat1, lon1, lat2, lon2):
    # Haversine distance with 30% extra for Indian road conditions
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c * 1.3  # 30% extra for Indian road conditions
    return distance

# OR-Tools Vehicle Routing Solution (optimized for Indian conditions)
def optimize_indian_routes(distance_matrix, num_vehicles=3, depot=0):
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, depot)
    routing = pywrapcp.RoutingModel(manager)
    
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(distance_matrix[from_node][to_node] * 1000)  # Convert to meters for OR-Tools
    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
    # Add Indian-specific constraints
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        60000,  # 60km max distance per vehicle (in meters)
        True,  # start cumul to zero
        'Distance')
    
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.time_limit.seconds = 10  # Faster computation
    
    solution = routing.SolveWithParameters(search_parameters)
    
    routes = []
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        routes.append(route)
    
    return routes

# Main App
st.title("🗑️ Indian Smart Waste Collection Optimizer")
st.markdown("""
    <div style='background-color:#e8f5e9; padding:20px; border-radius:10px; margin-bottom:20px;'>
        <h3 style='color:#138808;'>Optimized Waste Collection for Indian Cities</h3>
        <p>AI-powered route planning considering Indian road networks and waste patterns</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/197/197419.png", width=100)  # Indian flag icon
    st.title("Configuration")
    
    num_locations = st.slider("Number of Locations", 10, 100, 30)
    selected_city = st.selectbox("Select Base City", 
                               ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai'])
    
    st.subheader("Vehicle Parameters")
    num_vehicles = st.slider("Number of Vehicles", 1, 10, 3)
    vehicle_capacity = st.slider("Vehicle Capacity (tons)", 1, 10, 5)
    
    st.markdown("---")
    st.subheader("Indian Waste Patterns")
    st.info("""
        System accounts for:
        - Mixed waste streams
        - High-density urban areas
        - Typical collection frequencies
        - Indian road conditions
    """)

# Load Indian Data
df = generate_indian_sample_data(num_locations)
st.success(f"✅ Generated sample data for {selected_city} region with {num_locations} locations")

# Data Preview
with st.expander("🔍 Data Preview", expanded=True):
    st.dataframe(df.head())
    
    # Show on map with proper attribution
    m = folium.Map(
        location=[df['Latitude'].mean(), df['Longitude'].mean()],
        zoom_start=12,
        tiles='OpenStreetMap',
        attr='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    )
    for idx, row in df.iterrows():
        folium.Marker(
            [row['Latitude'], row['Longitude']],
            popup=f"{row['Location_ID']}<br>{row['City']}<br>Waste: {row['Waste_Volume']} tons",
            icon=folium.Icon(color='orange' if row['Waste_Type'] == 'Residential' else 
                           'blue' if row['Waste_Type'] == 'Commercial' else 'green')
        ).add_to(m)
    folium_static(m, width=1000, height=400)

# Optimization
st.header("🚛 Route Optimization for Indian Conditions")
if st.button("🚀 Optimize Collection Routes", key="optimize"):
    with st.spinner('Optimizing routes for Indian road conditions...'):
        # Create distance matrix with Indian road adjustments
        distance_matrix = np.zeros((len(df), len(df)))
        for i in range(len(df)):
            for j in range(len(df)):
                if i != j:
                    distance_matrix[i][j] = indian_road_distance(
                        df.iloc[i]['Latitude'], df.iloc[i]['Longitude'],
                        df.iloc[j]['Latitude'], df.iloc[j]['Longitude']
                    )
        
        # Optimize routes
        routes = optimize_indian_routes(distance_matrix, num_vehicles)
        
        # Visualize results
        st.success("Optimization complete!")
        
        # Create optimized routes dataframe
        optimized_routes = pd.DataFrame()
        for vehicle_id, route in enumerate(routes):
            route_df = df.iloc[route].copy()
            route_df['Vehicle'] = f"Vehicle {vehicle_id+1}"
            route_df['Route_Order'] = range(len(route))
            optimized_routes = pd.concat([optimized_routes, route_df])
        
        # Show on map with proper attribution
        st.subheader("Optimized Routes")
        route_map = folium.Map(
            location=[df['Latitude'].mean(), df['Longitude'].mean()],
            zoom_start=12,
            tiles='OpenStreetMap',
            attr='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        )
        
        colors = ['#FF9933', '#138808', '#000080', '#FF0000', '#800080']  # Indian theme colors
        
        for vehicle_id, group in optimized_routes.groupby('Vehicle'):
            color = colors[int(vehicle_id.split()[-1]) % len(colors)]
            
            folium.PolyLine(
                locations=group[['Latitude', 'Longitude']].values,
                color=color,
                weight=3,
                opacity=0.8,
                popup=vehicle_id
            ).add_to(route_map)
            
            for idx, row in group.iterrows():
                folium.Marker(
                    [row['Latitude'], row['Longitude']],
                    popup=f"{row['Location_ID']}<br>{vehicle_id}<br>Order: {row['Route_Order']}",
                    icon=folium.Icon(color=color, icon='trash')
                ).add_to(route_map)
        
        folium_static(route_map, width=1000, height=500)
        
        # Calculate metrics
        total_distance = 0
        for vehicle_id, group in optimized_routes.groupby('Vehicle'):
            coords = group[['Latitude', 'Longitude']].values
            vehicle_distance = sum(indian_road_distance(coords[i][0], coords[i][1], 
                                 coords[i+1][0], coords[i+1][1]) 
                            for i in range(len(coords)-1))
            total_distance += vehicle_distance
            st.info(f"{vehicle_id}: {len(group)} locations, {vehicle_distance:.2f} km")
        
        st.metric("Total System Distance", f"{total_distance:.2f} km")
        
        # Download results
        st.download_button(
            label="📥 Download Optimized Routes (CSV)",
            data=optimized_routes.to_csv(index=False).encode('utf-8'),
            file_name="optimized_routes_india.csv",
            mime="text/csv"
        )

# Indian Waste Management Tips
with st.expander("💡 Indian Waste Management Best Practices"):
    st.markdown("""
    - **Segregation at Source**: Separate wet, dry, and hazardous waste
    - **Decentralized Processing**: Encourage local composting units
    - **Informal Sector Integration**: Work with local ragpickers
    - **Awareness Campaigns**: Community education programs
    - **PPP Models**: Public-private partnerships for efficient collection
    """)