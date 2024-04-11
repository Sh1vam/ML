from pandas_profiling import ProfileReport
import pandas as pd

df = pd.read_csv('weatherHistory.csv')
Report = ProfileReport(df,title="Profiling Report on Historical Weather")
Report.to_file(output_file = 'Weather.html')
