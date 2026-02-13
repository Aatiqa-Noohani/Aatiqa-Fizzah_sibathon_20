import strreamlit as st
import pandas as pd 
import plotly.express as px 
from model import EnergyAI

###Configuration & UI Theme
st.set_page_config(page_title="Smart Energy AI", layout="wide")

## Styling With CSS
st.markdown("""<style>
.main{background-color:#1f2937;color:white;}



</style>""")