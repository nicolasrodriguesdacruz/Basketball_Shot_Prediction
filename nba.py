import pandas as pd

# Cargar los archivos CSV, asegurándose de que las columnas relevantes sean de tipo int
tiros_df = pd.read_csv("C:\\Users\\mcapurro\\Desktop\\Analitica del deporte\\tiros.csv", dtype={'minutes_remaining': int, 'seconds_remaining': int})
scores_df = pd.read_csv("C:\\Users\\mcapurro\\Desktop\\Analitica del deporte\\final_table.csv")

# Función para convertir tiempo restante a tiempo transcurrido
def convert_time_remaining(row):
    max_minutes = 11  # Máximo de minutos en un cuarto
    max_seconds = 60 # Máximo de segundos en un cuarto
    
    # Tiempo restante en minutos y segundos
    minutes_remaining = int(row['minutes_remaining'])
    seconds_remaining = int(row['seconds_remaining'])
    
    # Convertir el tiempo restante a segundos
    total_seconds_remaining = minutes_remaining * 60 + seconds_remaining
    
    # Calcular el tiempo transcurrido en segundos
    total_seconds_elapsed = (max_minutes * 60 + max_seconds) - total_seconds_remaining
    
    # Convertir el tiempo transcurrido a minutos y segundos
    minutes_elapsed = total_seconds_elapsed // 60
    seconds_elapsed = total_seconds_elapsed % 60
    
    # Formatear los segundos para que siempre tengan dos dígitos
    return f"{minutes_elapsed:02}:{seconds_elapsed:02}"

# Aplicar la función a cada fila del scores_dfFrame
tiros_df['pctimestring'] = tiros_df.apply(convert_time_remaining, axis=1)

# Mostrar las primeras filas del scores_dfFrame resultante con la nueva columna 'time_elapsed'
print(tiros_df[['game_date', 'period', 'minutes_remaining', 'seconds_remaining', 'pctimestring']].head())

# Calcular el tiempo total de juego en segundos
total_time_seconds = (tiros_df['period']) * 12 * 60 - (tiros_df['minutes_remaining'] * 60 + tiros_df['seconds_remaining'])
total_minutes = total_time_seconds // 60
total_seconds = total_time_seconds % 60

# Crear una columna para el tiempo total de juego en formato "minuto:segundos"
tiros_df['total_time'] = total_minutes.apply(lambda x: f"{x:02}") + ':' + total_seconds.apply(lambda x: f"{x:02}")

## SCORES

# Función para convertir tiempo en formato 'mm:ss' a segundos
def convert_to_seconds(time_string):
    minutes, seconds = map(int, time_string.split(':'))
    return minutes * 60 + seconds

# Aplicar la conversión a segundos en la columna pctimestring
scores_df['pctimestring_seconds'] = scores_df['pctimestring'].apply(convert_to_seconds)

# Calcular el tiempo total jugado en segundos
scores_df['total_time_played'] = (scores_df['period'])*12*60 - (scores_df['pctimestring_seconds'])

# Función para convertir segundos a formato 'mm:ss'
def convert_to_mmss(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f'{minutes:02}:{seconds:02}'

# Aplicar la conversión a formato 'mm:ss'
scores_df['total_time'] = scores_df['total_time_played'].apply(convert_to_mmss)

# Eliminar columnas intermedias que ya no son necesarias
scores_df.drop(columns=['pctimestring_seconds', 'total_time_played'], inplace=True)

# Crear una nueva fila para el comienzo de cada partido
new_rows = []

# Iterar sobre cada fecha/game_id único
for game_id, game_date in scores_df[['game_id', 'game_date']].drop_duplicates().values:
    new_row = {
        'game_id': game_id,
        'score': '0 - 0',
        'period': 1,
        'pctimestring': '12:00',
        'game_date': game_date,
        'matchup_home': scores_df[scores_df['game_id'] == game_id]['matchup_home'].iloc[0],
        'total_time': '00:00'
    }
    new_rows.append(new_row)

# Convertir las nuevas filas a un DataFrame
new_rows_df = pd.DataFrame(new_rows)

# Concatenar el DataFrame original con las nuevas filas
scores_df = pd.concat([new_rows_df, scores_df], ignore_index=True)

# Ordenar el DataFrame resultante por game_id y period
scores_df = scores_df.sort_values(by=['game_id', 'period', 'pctimestring'])





# Convertir game_date a datetime
scores_df['game_date'] = pd.to_datetime(scores_df['game_date'])

# Convertir pctimestring a timedelta
scores_df['total_time'] = pd.to_timedelta('00:' + scores_df['total_time'])

# Crear la columna datetime combinando game_date y pctimestring
scores_df['datetime'] = scores_df['game_date'] + scores_df['total_time']

# Convertir pctimestring de vuelta a string para mantener el formato original
scores_df['total_time'] = scores_df['total_time'].dt.components.apply(lambda row: f'{row["minutes"]:02}:{row["seconds"]:02}', axis=1)



# Convertir game_date a datetime
tiros_df['game_date'] = pd.to_datetime(tiros_df['game_date'], dayfirst=True)

# Convertir total_time a timedelta
tiros_df['total_time'] = pd.to_timedelta('00:' + tiros_df['total_time'])

# Crear la columna datetime combinando game_date y total_time
tiros_df['datetime'] = tiros_df['game_date'] + tiros_df['total_time']

# Convertir total_time de vuelta a string para mantener el formato original
tiros_df['total_time'] = tiros_df['total_time'].dt.components.apply(lambda row: f'{row["minutes"]:02}:{row["seconds"]:02}', axis=1)




# Guardar el scores_dfframe actualizado en un nuevo archivo CSV
output_file_path = "C:\\Users\\mcapurro\\Desktop\\Analitica del deporte\\final_tableC.csv"
scores_df.to_csv(output_file_path, index=False)



tiros_df.to_csv("C:\\Users\\mcapurro\\Desktop\\Analitica del deporte\\tirosC.csv", index=False)