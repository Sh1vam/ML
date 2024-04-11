from pandas_profiling import ProfileReport
import pandas as pd

df = pd.read_csv('Rainfall.csv')
df.replace(to_replace=['yes','no','Yes',"No"],value=[1,0,1,0],inplace=True)
df.rename(str.strip,axis='columns',inplace=True)
Report = ProfileReport(df,title="Profiling Report on Historical Rainfall Data")
Report.to_file(output_file = 'Rainfall.html')
