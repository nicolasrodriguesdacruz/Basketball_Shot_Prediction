import pandas as pd

# Ruta a los archivos CSV
file_path_tiros = "C:\\Users\\mcapurro\\Desktop\\Analitica del deporte\\tirosC.csv"
file_path_scores = "C:\\Users\\mcapurro\\Desktop\\Analitica del deporte\\final_tableC.csv"

# Cargar los archivos CSV
tiros_df = pd.read_csv(file_path_tiros)
scores_df = pd.read_csv(file_path_scores)

# Convertir las columnas datetime a formato datetime
tiros_df['datetime'] = pd.to_datetime(tiros_df['datetime'])
scores_df['datetime'] = pd.to_datetime(scores_df['datetime'])

# Realizar el merge basándonos en el datetime más cercano anterior al momento del tiro
merged_df = pd.merge_asof(tiros_df.sort_values('datetime'), 
                          scores_df.sort_values('datetime'), 
                          on='datetime', 
                          direction='backward', 
                          suffixes=('', '_score'))

# Seleccionar y renombrar las columnas relevantes
merged_df = merged_df[['name', 'team_name', 'game_date', 'season', 'espn_player_id', 'team_id', 'espn_game_id', 'period', 
                       'minutes_remaining', 'seconds_remaining', 'shot_made_flag', 'action_type', 'shot_type', 'shot_distance', 
                       'opponent', 'x', 'y', 'dribbles', 'touch_time', 'defender_name', 'defender_distance', 'shot_clock', 
                       'pctimestring', 'total_time', 'datetime', 'score', 'matchup_home']]

# Guardar el DataFrame actualizado a un nuevo archivo CSV
output_file_path = "C:\\Users\\mcapurro\\Desktop\\Analitica del deporte\\mergeFinalC.csv"
merged_df.to_csv(output_file_path, index=False)

print(f'Archivo actualizado guardado en {output_file_path}')
