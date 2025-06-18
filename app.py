import streamlit as st
import scipy.stats
import time
import pandas as pd



## con pandas esto va al proncipio
# estas son variables de estado que se conservan cuando Streamlin vuelve a ejecutar este script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])
    
    
st.header('Lanzar una moneda')

#st.write('Esta aplicación aún no es funcional. En construcción.')


#añadir los resultados del experimento a la interfaz de usuario, 
# calculando la media y mostrando cómo cambia a medida que avanzan los intentos.
#Primero, vamos a agregar la variable chart para el gráfico de líneas y la función toss_coin 
# que emula el lanzamiento de una moneda n veces y calcula la media en cada nueva iteración,
# que se añade a chart (como una nueva observación).

chart = st.line_chart([0.5])

def toss_coin(n): # función que emula el lanzamiento de una moneda

    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no +=1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean

#Agregar el control deslizante y el botón al programa de la libreria:

number_of_trials = st.slider('¿Número de intentos?', 1, 100, 10)
start_button = st.button('Ejecutar')


##before pandas
#if start_button:
#    st.write(f'Experimento con {number_of_trials} intentos en curso.')
#    mean = toss_coin(number_of_trials)
    


##vamos a añadir las salidas a una tabla con los resultados de todos los intentos.
#En primer lugar, tenemos que añadir dos variables de estado como claves de st.session_state
#El estado de la sesión se conserva tras cada nueva ejecución de la aplicación Streamlit. 
#A continuación, añadimos la recopilación de los resultados de todos los intentos en el DataFrame 
# guardado como st.session_state['df_experiment_results'].

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                            columns=['no', 'iteraciones', 'media'])
        ],
        axis=0)
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])