import pandas as pd
import plotly.express as px

df = pd.read_csv(r"C:\Users\erwan\OneDrive\Documents\McGill\Data\1006b\Pre despeckle.csv")

fig = px.line(df)
fig.show()