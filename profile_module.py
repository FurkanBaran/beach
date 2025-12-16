import streamlit as st
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import xarray as xr
import numpy as np

# ===== HELPER FUNCTIONS =====
@st.cache_data
def load_bathymetry():
    try:
        import os
        file_name = "Mean depth in multi colour (no land).nc"
        if os.path.exists(file_name):
            file_path = os.path.abspath(file_name)
        else:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        
        try:
            return xr.open_dataset(file_path, engine='netcdf4')
        except:
            return xr.open_dataset(file_path, engine='scipy')
    except Exception as e:
        return None

def extract_depth_profile(ds, point1, point2, num_points=50):
    if ds is None:
        return None, None
    
    lats = np.linspace(point1['lat'], point2['lat'], num_points)
    lons = np.linspace(point1['lon'], point2['lon'], num_points)
    
    R = 6371000
    lat1_rad = np.radians(point1['lat'])
    lat2_rad = np.radians(lats)
    delta_lat = np.radians(lats - point1['lat'])
    delta_lon = np.radians(lons - point1['lon'])
    
    a = np.sin(delta_lat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(delta_lon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distances = R * c
    
    try:
        depth_var = None
        for var in ds.data_vars:
            if 'depth' in var.lower() or 'elevation' in var.lower():
                depth_var = var
                break
        if depth_var is None:
            depth_var = list(ds.data_vars)[0]
        
        coords = list(ds[depth_var].coords)
        lat_coord = [c for c in coords if 'lat' in c.lower()][0]
        lon_coord = [c for c in coords if 'lon' in c.lower()][0]
        
        depths = []
        for lat, lon in zip(lats, lons):
            try:
                depth = ds[depth_var].sel({lat_coord: lat, lon_coord: lon}, method='nearest').values
                depths.append(float(depth))
            except:
                depths.append(np.nan)
        
        depths = np.array(depths)
        
        if np.isnan(depths).any():
            valid_idx = ~np.isnan(depths)
            if valid_idx.sum() > 1:
                depths = np.interp(np.arange(len(depths)), np.arange(len(depths))[valid_idx], depths[valid_idx])
            else:
                depths = np.nan_to_num(depths, nan=-5.0)
        
        if np.nanmean(depths) > 0:
            depths = -depths
        
        return distances.tolist(), depths.tolist()
    except:
        return distances.tolist(), [0.0] * len(distances)

# ===== INITIALIZE SESSION STATE =====
if 'sections' not in st.session_state:
    st.session_state.sections = {
        'A': {'points': [], 'bathy_dist': [], 'bathy_depth': [], 'user_dist': [], 'user_depth': [], 'completed': False},
        'B': {'points': [], 'bathy_dist': [], 'bathy_depth': [], 'user_dist': [], 'user_depth': [], 'completed': False},
        'C': {'points': [], 'bathy_dist': [], 'bathy_depth': [], 'user_dist': [], 'user_depth': [], 'completed': False}
    }

if 'current_section' not in st.session_state:
    st.session_state.current_section = 'A'

if 'coord_version' not in st.session_state:
    st.session_state.coord_version = 0

def render_profile_section():
    bathymetry_ds = load_bathymetry()

    st.markdown("---")
    
    current = st.session_state.current_section
    
    st.markdown("### Section Navigation")
    col_a, col_b, col_c, col_all = st.columns(4)
    
    with col_a:
        label = "[Done] A-A'" if st.session_state.sections['A']['completed'] else "A-A'"
        if st.button(label, key="nav_a", use_container_width=True, type="primary" if current == 'A' else "secondary"):
            st.session_state.current_section = 'A'
            st.rerun()
    
    with col_b:
        label = "[Done] B-B'" if st.session_state.sections['B']['completed'] else "B-B'"
        if st.button(label, key="nav_b", use_container_width=True, type="primary" if current == 'B' else "secondary"):
            st.session_state.current_section = 'B'
            st.rerun()
    
    with col_c:
        label = "[Done] C-C'" if st.session_state.sections['C']['completed'] else "C-C'"
        if st.button(label, key="nav_c", use_container_width=True, type="primary" if current == 'C' else "secondary"):
            st.session_state.current_section = 'C'
            st.rerun()
    
    with col_all:
        completed_count = sum(1 for s in st.session_state.sections.values() if s['completed'])
        if st.button(f"All Results ({completed_count}/3)", key="nav_all", use_container_width=True, type="primary" if current == 'ALL' else "secondary"):
            st.session_state.current_section = 'ALL'
            st.rerun()
    
    # ===== ALL RESULTS VIEW =====
    if current == 'ALL':
        st.info("Viewing: **All Results Summary**")
        st.markdown("---")
        
        completed_sections = [name for name, data in st.session_state.sections.items() if data['completed']]
        
        if not completed_sections:
            st.warning("No sections completed yet. Please complete at least one section to view results.")
        else:
            st.markdown("## All Cross-Section Profiles")
            
            for sec_name in ['A', 'B', 'C']:
                sec_data = st.session_state.sections[sec_name]
                if sec_data['completed']:
                    st.markdown(f"### Section {sec_name}-{sec_name}'")
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=sec_data['bathy_dist'], 
                        y=sec_data['bathy_depth'], 
                        mode='lines+markers', 
                        name='Bathymetry',
                        line=dict(color='#0077B6', width=2)
                    ))
                    fig.add_trace(go.Scatter(
                        x=sec_data['user_dist'], 
                        y=sec_data['user_depth'], 
                        mode='lines+markers', 
                        name='Design Profile',
                        line=dict(color='#FF6B6B', width=2, dash='dash')
                    ))
                    fig.update_layout(
                        xaxis_title="Distance (m)", 
                        yaxis_title="Depth (m)", 
                        height=350,
                        legend=dict(x=0.01, y=0.99)
                    )
                    st.plotly_chart(fig)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Distance", f"{sec_data['bathy_dist'][-1]:.1f} m")
                    with col2:
                        st.metric("Max Depth (Bathy)", f"{abs(min(sec_data['bathy_depth'])):.2f} m")
                    with col3:
                        st.metric("Max Depth (Design)", f"{abs(min(sec_data['user_depth'])):.2f} m")
                    
                    st.markdown("---")
            
            st.markdown("## Combined View - All Sections")
            
            fig_combined = go.Figure()
            colors = {'A': '#2563EB', 'B': '#DC2626', 'C': '#FACC15'}
            
            for sec_name in ['A', 'B', 'C']:
                sec_data = st.session_state.sections[sec_name]
                if sec_data['completed']:
                    fig_combined.add_trace(go.Scatter(
                        x=sec_data['bathy_dist'], 
                        y=sec_data['bathy_depth'], 
                        mode='lines', 
                        name=f'{sec_name} Bathymetry',
                        line=dict(color=colors[sec_name], width=2)
                    ))
                    fig_combined.add_trace(go.Scatter(
                        x=sec_data['user_dist'], 
                        y=sec_data['user_depth'], 
                        mode='lines', 
                        name=f'{sec_name} Design',
                        line=dict(color=colors[sec_name], width=2, dash='dash')
                    ))
            
            fig_combined.update_layout(
                xaxis_title="Distance (m)", 
                yaxis_title="Depth (m)", 
                height=500,
                legend=dict(x=1.02, y=1, xanchor='left')
            )
            st.plotly_chart(fig_combined)
    
    # ===== SECTION EDITING VIEW =====
    else:
        section = st.session_state.sections[current]
        
        st.info(f"Working on: **Section {current}-{current}'**")
        st.markdown("---")

        st.markdown(f"### Step 1: Select Points for Section {current}-{current}'")

        m = folium.Map(location=[41.175354, 29.626743], zoom_start=15)
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satellite',
            overlay=False,
            control=True
        ).add_to(m)
        map_colors = {'A': 'blue', 'B': 'green', 'C': 'orange'}

        for sec_name, sec_data in st.session_state.sections.items():
            if sec_data['points']:
                color = map_colors.get(sec_name, 'gray')
                for idx, pt in enumerate(sec_data['points']):
                    folium.Marker(
                        [pt['lat'], pt['lon']],
                        popup=f"{sec_name if idx==0 else sec_name}'",
                        icon=folium.Icon(color=color if sec_name == current else 'gray')
                    ).add_to(m)
                if len(sec_data['points']) == 2:
                    folium.PolyLine(
                        [[p['lat'], p['lon']] for p in sec_data['points']],
                        color=color if sec_name == current else 'gray',
                        weight=3 if sec_name == current else 2,
                        opacity=1.0 if sec_name == current else 0.5
                    ).add_to(m)

        m.add_child(folium.LatLngPopup())
        map_data = st_folium(m, height=400, use_container_width=True, key=f"map_{current}")

        if map_data and map_data.get('last_clicked'):
            lat = map_data['last_clicked']['lat']
            lon = map_data['last_clicked']['lng']
            
            if len(section['points']) < 2:
                new_point = True
                if section['points']:
                    last = section['points'][-1]
                    if abs(last['lat'] - lat) < 0.0001 and abs(last['lon'] - lon) < 0.0001:
                        new_point = False
                
                if new_point:
                    section['points'].append({'lat': lat, 'lon': lon})
                    st.session_state.coord_version += 1
                    st.rerun()

        st.markdown("#### Manual Coordinates")

        v = st.session_state.coord_version
        default_lat1 = section['points'][0]['lat'] if section['points'] else 41.175354
        default_lon1 = section['points'][0]['lon'] if section['points'] else 29.626743
        default_lat2 = section['points'][1]['lat'] if len(section['points']) > 1 else 41.175000
        default_lon2 = section['points'][1]['lon'] if len(section['points']) > 1 else 29.627000

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Point {current}**")
            lat1 = st.number_input("Latitude", value=default_lat1, format="%.6f", key=f"lat1_{current}_{v}")
            lon1 = st.number_input("Longitude", value=default_lon1, format="%.6f", key=f"lon1_{current}_{v}")

        with col2:
            st.markdown(f"**Point {current}'**")
            lat2 = st.number_input("Latitude ", value=default_lat2, format="%.6f", key=f"lat2_{current}_{v}")
            lon2 = st.number_input("Longitude ", value=default_lon2, format="%.6f", key=f"lon2_{current}_{v}")

        col_apply, col_reset = st.columns(2)
        with col_apply:
            if st.button("Apply Coordinates", key=f"apply_{current}", use_container_width=True):
                section['points'] = [{'lat': lat1, 'lon': lon1}, {'lat': lat2, 'lon': lon2}]
                st.rerun()
        with col_reset:
            if st.button("Reset Points", key=f"reset_{current}", use_container_width=True):
                section['points'] = []
                section['completed'] = False
                section['bathy_dist'] = []
                section['bathy_depth'] = []
                section['user_dist'] = []
                section['user_depth'] = []
                st.session_state.coord_version += 1
                st.rerun()

        if len(section['points']) == 2:
            st.success("Both points selected!")
        else:
            st.warning("Select 2 points on the map or enter manually")

        st.markdown("---")

        if len(section['points']) == 2:
            st.markdown(f"### Step 2: Bathymetry Profile")
            
            if not section['bathy_dist']:
                dist, depth = extract_depth_profile(bathymetry_ds, section['points'][0], section['points'][1])
                if dist and depth:
                    section['bathy_dist'] = dist
                    section['bathy_depth'] = depth
            
            if section['bathy_dist']:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=section['bathy_dist'], y=section['bathy_depth'], mode='lines+markers', name='Bathymetry', line=dict(color='#0077B6', width=2)))
                fig.update_layout(xaxis_title="Distance (m)", yaxis_title="Depth (m)", height=350)
                st.plotly_chart(fig)
                
                st.metric("Total Distance", f"{section['bathy_dist'][-1]:.1f} m")
                
                st.markdown("---")
                
                st.markdown(f"### Step 3: Design Profile")
                
                num_pts = st.number_input("Number of points", min_value=2, max_value=20, value=5, key=f"npts_{current}")
                
                if not section['user_dist'] or len(section['user_dist']) != num_pts:
                    max_dist = section['bathy_dist'][-1]
                    section['user_dist'] = [float(i * max_dist / (num_pts - 1)) for i in range(num_pts)]
                    section['user_depth'] = [float(np.interp(d, section['bathy_dist'], section['bathy_depth'])) for d in section['user_dist']]
                
                st.markdown("**Distance (m) | Depth (m)**")
                
                for i in range(num_pts):
                    c1, c2 = st.columns(2)
                    with c1:
                        new_dist = st.number_input(f"D{i+1}", value=section['user_dist'][i], step=1.0, key=f"ud_{current}_{i}", label_visibility="collapsed")
                        section['user_dist'][i] = new_dist
                    with c2:
                        new_depth = st.number_input(f"H{i+1}", value=section['user_depth'][i], step=0.1, key=f"uh_{current}_{i}", label_visibility="collapsed")
                        section['user_depth'][i] = new_depth
                
                st.markdown("---")
                
                if st.button("Compare & Save", type="primary", key=f"compare_{current}"):
                    section['completed'] = True
                    st.rerun()
                
                if section['completed']:
                    st.markdown(f"### Step 4: Comparison")
                    
                    fig2 = go.Figure()
                    fig2.add_trace(go.Scatter(x=section['bathy_dist'], y=section['bathy_depth'], mode='lines+markers', name='Bathymetry', line=dict(color='#0077B6', width=2)))
                    fig2.add_trace(go.Scatter(x=section['user_dist'], y=section['user_depth'], mode='lines+markers', name='Design', line=dict(color='#FF6B6B', width=2, dash='dash')))
                    fig2.update_layout(xaxis_title="Distance (m)", yaxis_title="Depth (m)", height=400, legend=dict(x=0.01, y=0.99))
                    st.plotly_chart(fig2)
                    
                    st.success(f"Section {current}-{current}' saved!")
                    
                    _, col_prev, col_next, _ = st.columns([1, 2, 2, 1])
                    with col_prev:
                        if current in ['B', 'C']:
                            prev_sec = 'A' if current == 'B' else 'B'
                            if st.button(f"< Previous ({prev_sec})", key=f"prev_{current}", use_container_width=True):
                                st.session_state.current_section = prev_sec
                                st.rerun()
                    with col_next:
                        if current in ['A', 'B']:
                            next_sec = 'B' if current == 'A' else 'C'
                            if st.button(f"Next ({next_sec}) >", key=f"next_{current}", use_container_width=True):
                                st.session_state.current_section = next_sec
                                st.rerun()
    
