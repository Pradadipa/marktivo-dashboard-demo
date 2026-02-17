import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(layout="wide")

st.title("🧪 AG Grid Minimal Test")

# Simple data
df = pd.DataFrame({
    'ID': [1, 2, 3, 4, 5],
    'Name': ['Post A', 'Post B', 'Post C', 'Post D', 'Post E'],
    'Views': [1000, 2000, 1500, 3000, 2500],
    'Likes': [100, 200, 150, 300, 250]
})

st.write("Data:")
st.write(df)

st.markdown("---")
st.subheader("AG Grid Test:")

# Configure grid
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_selection('single')
grid_options = gb.build()

# Display grid
try:
    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_on=['selectionChanged'],
        theme='streamlit',
        height=300
    )
    
    st.success("✅ AG Grid is working!")
    
    if grid_response['selected_rows'] is not None and len(grid_response['selected_rows']) > 0:
        st.write("Selected row:", grid_response['selected_rows'])
        
except Exception as e:
    st.error(f"❌ AG Grid Error: {str(e)}")
    st.write("Full error:", e)