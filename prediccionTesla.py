import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.preprocessing import MinMaxScaler
import requests
import csv
from datetime import datetime

def requestapi():
    # Get the current timestamp
    current_timestamp = int(datetime.now().timestamp())

    # Format the URL with the current timestamp
    url = f'https://api.profit.com/data-api/market_data/historical/TSLA?token=0048d74709ba4aab837dc102eeaa119c&start_date=1601934304&end_date={current_timestamp}&interval=1d'

    headers = {
        'Api-Key': '0048d74709ba4aab837dc102eeaa119c'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        for item in data:
            timestamp = item['time']
            date = datetime.utcfromtimestamp(timestamp)
            item['time'] = date  # Update the 'time' field with the formatted date and time

            # Format date and time
            formatted_date = date.strftime(
                '%Y-%m-%d %H:%M:%S %A')  # Year-Month-Day Hour:Minutes:Seconds Day of the week
            item['time'] = formatted_date  # Update the 'time' field with the formatted date and time

        # Name of the output CSV file
        csv_filename = 'datos.csv'

        # Extract column names (JSON fields)
        column_names = data[0].keys()

        # Write data to the CSV file
        with open(csv_filename, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=column_names)
            writer.writeheader()
            writer.writerows(data)

        print(f'Data has been saved to {csv_filename}')

    else:
        print('Error in the request. Status code:', response.status_code)


def funcionalidad(pred_days):
    requestapi()
    df = pd.read_csv("datos.csv")
    df = df.ffill()
    # Convert the 'time' field to a datetime index
    df['time'] = pd.to_datetime(df['time'])
    closedf = df[['time', 'close']]
    del closedf['time']
    scaler = MinMaxScaler(feature_range=(0, 1))
    closedf = scaler.fit_transform(np.array(closedf).reshape(-1, 1))
    training_size = int(len(closedf) * 0.70)
    test_size = len(closedf) - training_size
    train_data, test_data = closedf[0:training_size, :], closedf[training_size:len(closedf), :1]
    time_step = 15
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, y_test = create_dataset(test_data, time_step)

    my_model = XGBRegressor(n_estimators=250)
    my_model.fit(X_train, y_train, verbose=True)

    # Predicciones
    train_predict = my_model.predict(X_train)
    test_predict = my_model.predict(X_test)

    # Reshape a (n, 1)
    train_predict = train_predict.reshape(-1, 1)
    test_predict = test_predict.reshape(-1, 1)

    # Transformación inversa
    train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)
    y_train_inverse = scaler.inverse_transform(y_train.reshape(-1, 1))
    y_test_inverse = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Obtener los últimos datos de prueba para la entrada
    x_input = test_data[len(test_data) - time_step:].reshape(1, -1)
    #print("Entrada para predicción:", x_input)

    # Convertir la entrada a una lista
    temp_input = list(x_input)
    temp_input = temp_input[0].tolist()

    # Inicializar la lista de salida de predicciones
    lst_output = []

    # Configuración de parámetros
    n_steps = time_step
    i = 0
    #pred_days = 10

    # Realizar predicciones para los próximos pred_days días
    while i < pred_days:

        # Verificar si hay suficientes datos en temp_input para realizar la predicción
        if len(temp_input) > time_step:

            # Crear la entrada para el modelo eliminando el primer elemento de temp_input
            x_input = np.array(temp_input[1:])
            # print("{} day input {}".format(i,x_input))
            x_input = x_input.reshape(1, -1)

            # Realizar la predicción con el modelo
            yhat = my_model.predict(x_input)

            # Agregar la predicción a temp_input y eliminar el primer elemento
            temp_input.extend(yhat.tolist())
            temp_input = temp_input[1:]

            # Agregar la predicción a lst_output
            lst_output.extend(yhat.tolist())
            i = i + 1

        else:
            # Si no hay suficientes datos en temp_input, hacer la primera predicción
            yhat = my_model.predict(x_input)

            # Agregar la predicción a temp_input y lst_output
            temp_input.extend(yhat.tolist())
            lst_output.extend(yhat.tolist())

            i = i + 1

    # Imprimir la longitud de la lista de salida, que representa la predicción para los próximos pred_days días
    print("Previsión de los próximos días:", len(lst_output))
    lst_output = scaler.inverse_transform(np.array(lst_output).reshape(-1, 1))
    return lst_output


def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]  ###i=0, 0,1,2,3-----99   100
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

#for i in funcionalidad():
    #print(i)


def main_prediccion(dias):
    pred = funcionalidad(dias)

    return pred

if __name__ == "__main__":
    main_prediccion()
