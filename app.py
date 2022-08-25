import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px


st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")

image_full = Image.open('MH_12_PQ_5841.png')

# Data
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

df = pd.read_csv('vehicle_list.csv', index_col=[0])
vehicle = pd.read_csv('BC 12 CD 3456.csv', index_col=[0])
vehicle=(vehicle[vehicle["iq"]!=0]).groupby('master_row_id').agg('mean').reset_index()


st.sidebar.header("Please Filter Here:")

#dummy function for on_change
def new():
    pass

manufacturer = st.sidebar.selectbox('Choose Manufacturer',(df["Manufacturer"].unique()), on_change=new)
model = st.sidebar.selectbox('Choose Model',df["Model"][df["Manufacturer"]==manufacturer].unique(),on_change=new)
subsystem = st.sidebar.selectbox('Choose Subsystem',["","Fuel","Air","Oil","Powertrain","ECU","Brakes"],on_change=new)
component = st.sidebar.selectbox('Choose Component',["Injector","Common Rail","Metering Unit"],on_change=new)
dicts={"Injector":"iq_pred","Common Rail":"rp_pred","Metering Unit":"mu_pred"}

st.image(image_full)

error=(vehicle[dicts[component]]-vehicle[dicts[component][:2]])/vehicle[dicts[component][:2]]
vehicle["Error %"]=(vehicle[dicts[component]]-vehicle[dicts[component][:2]])/vehicle[dicts[component][:2]]


col1, col2 = st.columns((4,1))
with col1 :

    fig = px.line(        
        vehicle,
        x = 'master_row_id',
        y = "Error %", 
        title = "Error Percentage Per Trip for "+dicts[component],
        
    )
    fig.update_traces(line_color = "black")
    st.plotly_chart(fig)
    
col2, col4,col5 = st.columns((1,1,4))
with col2:
    st.metric("Effectiveness", "{:.2%}".format(1+error.mean()))
with col4:
    st.metric("No. Of Vehicles", len(df["vehiclenum"].unique()))
















