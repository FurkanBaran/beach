import streamlit as st
import profile_module as profile

st.set_page_config(
    page_title="Beach Nourishment Design Tool", 
    layout="wide", 
)

# Keep track of which page we're on (landing or project page)
if 'page' not in st.session_state:
    st.session_state.page = 'landing'  # Start on landing page

# Function to go to the project page
def switch_to_project():
    st.session_state.page = 'project'

# Function to go back to the landing page 
def reset_project():
    st.session_state.page = 'landing'

#  LANDING PAGE 
if st.session_state.page == 'landing':
    
    # Show the hero image at the top
    try:
        st.image("images/bg.jpg", width='stretch')
    except:
        st.warning("Background image not found.")
    
    # Main title and subtitle
    st.title("Beach Nourishment Design Tool")
    st.subheader("Professional solution for coastal engineering calculations, cross-section analysis and cost estimation")
    st.markdown("---")
    
    # Split into two columns: map on left, form on right
    col_map, col_form = st.columns([1, 1])
    
    with col_map:
        # Embed Google Maps showing the project location
        st.components.v1.iframe(
            "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3008.5!2d29.626743!3d41.175354!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDHCsDEwJzMxLjMiTiAyOcKwMzcnMzYuMyJF!5e1!3m2!1str!2str!4v1234567890",
            height=410
        )
    
    with col_form:
        st.markdown("### Start New Project")
        st.markdown("")
        
        # Create a form for the user to enter their project name
        with st.form("entry_form"):
            project_name = st.text_input(
                "Enter Project Name:", 
                placeholder="e.g., Şile Ağlayankaya Beach Nourishment", 
                value="Şile Ağlayankaya Beach Nourishment"
            )
            st.markdown("")
            submitted = st.form_submit_button("Start Project", type="primary", use_container_width=True)
            
            # When they click submit
            if submitted:
                if project_name:
                    # Save the project name and go to the project page
                    st.session_state.project_name = project_name
                    switch_to_project()
                    st.rerun()
                else:
                    st.error("Please enter a project name to continue.")
    
    # Footer at the bottom
    st.markdown("---")
    st.caption("© 2025 Coastal Engineering Solutions | Ağlayankaya Beach Nourishment Project")

#  PROJECT DATA ENTRY PAGE 
elif st.session_state.page == 'project':
    
    # Top bar with back button and project title
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("← Home", use_container_width=True):
            reset_project()
            st.rerun()
    with col_title:
        st.subheader(f"Project: {st.session_state.get('project_name', 'Untitled Project')}")
    
    st.divider()
    st.info("Please enter the required parameters for design calculations.")
    
    #  Getting all the data from the user 
    
    # Section 1: Wave and sediment stuff
    st.markdown("### 1. Wave and Sediment Properties")
    
    # Split into two columns so it looks cleaner
    c1, c2 = st.columns(2)
    with c1:
        Hs = st.number_input("Significant Wave Height (Hs) [m]", value=2.0, step=0.1, help="Design wave height for the project area")
        T = st.number_input("Wave Period (T) [s]", value=7.0, step=0.1, help="Peak wave period")
        L_coast = st.number_input("Total Coastline Length [m]", value=480.0, step=10.0, help="Total length of beach nourishment")
    with c2:
        d50 = st.number_input("Median Grain Size (d₅₀) [mm]", value=0.25, step=0.01, help="Median sediment grain diameter")
        A_param = st.number_input("Sediment Scale Parameter (A)", value=0.09, step=0.01, help="Dean's parameter based on grain size")
        h_toe = st.number_input("Sill Depth (h) [m]", value=2.5, step=0.1, help="Target depth for sill placement")
    
    st.markdown("---")
    
    # Section 2: The three cross-sections we need
    profile.render_profile_section()
    st.markdown("---")
    
    # Section 3: Optional structural stuff - groin and sill
    st.markdown("### 3. Structural Elements (Optional)")
    
    # Groin properties in an expandable section 
    with st.expander("Groin Properties"):
        use_groin = st.toggle("Include Groin in Project", value=False)
        if use_groin:  # Only show these inputs if they want a groin
            gc1, gc2 = st.columns(2)
            with gc1:
                groin_length = st.number_input("Groin Length (m)", value=28.3, key="gl")
                groin_width = st.number_input("Groin Width (m)", value=1.0, key="gw")
            with gc2:
                groin_depth = st.number_input("Groin Depth (m)", value=5.5, key="gd")
                groin_cost = st.number_input("Unit Cost ($/m³)", value=33.0, key="g_cost")
    
    # Sill properties (also in an expandable section)
    with st.expander("Sill (Submerged Breakwater) Properties"):
        use_sill = st.toggle("Include Sill in Project", value=False)
        if use_sill:  # Only show these inputs if they want a sill
            sl1, sl2 = st.columns(2)
            with sl1:
                sill_length = st.number_input("Sill Length (m)", value=258.0, key="sl", help="Length along A-A section")
                sill_width = st.number_input("Sill Width (m)", value=1.5, key="sw")
            with sl2:
                sill_depth = st.number_input("Sill Height (m)", value=2.5, key="sd")
                sill_cost = st.number_input("Unit Cost ($/m³)", value=19.0, key="s_cost")
    
    st.markdown("---")
    
    # Section 4: Cost stuff
    st.markdown("### 4. Cost Estimation")
    cost1, cost2 = st.columns(2)
    with cost1:
        sand_cost = st.number_input("Sand Unit Cost ($/m³)", value=20.0, step=1.0, help="Cost per cubic meter of fill material")
    with cost2:
        transport_cost = st.number_input("Transport & Placement Cost ($/m³)", value=5.0, step=1.0, help="Additional costs for material placement")
    
    st.markdown("---")
    
    # The big calculate button
    if st.button("START CALCULATIONS", type="primary", use_container_width=True):
        st.success("Data received successfully. Processing results...")
        
        # For now, just showing dummy results. we'll add real calculations later
        st.markdown("#### Results (Real calculations will be implemented)")
        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("Estimated Sand Volume", "~12,345 m³")
        col_res2.metric("Total Material Cost", "$123,000")
        col_res3.metric("Project Total", "$123,456")
