import pandas as pd
import numpy as np
import math as m
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from IPython.display import clear_output
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report
from tensorflow.keras.utils import to_categorical
from sklearn.utils import shuffle
import plotly.express as px
from sklearn.utils import class_weight
import sklearn
from sklearn.naive_bayes import MultinomialNB
import warnings
import nltk
nltk.download("stopwords")
warnings.filterwarnings('ignore')
import scrapping

Mobile_upper = ["Smartphone",
"Tablet",
"Wearable: Fitness Band",
"Wearable: Smart Watch",
"Wearable: Earbuds",
"Wearables: Others",
"Feature Phone",
"Wireless Carrier",
"Desktop Computer",
"Laptop",
"Music Service - Radio",
"Music Service - Streaming App",
"Mobile Branding"]
Mobile = [x.lower() for x in Mobile_upper]

VD_upper = ["Home Theater",
"Monitor",
"TV",
"Connected TV",
"VD Branding"]
VD = [x.lower() for x in VD_upper]

DA_upper = ["Air Conditioner",
"Refrigerator",
"Stove Top",
"Oven",
"Air Purifier",
"Dishwasher",
"Microwave",
"Vacuum Cleaner",
"Connected Home",
"DA Branding",
"Washing Machine"
]
DA = [x.lower() for x in DA_upper]

Memory = ["memory"]
Corporate = ["corporate"] 
    
clases_modelo_ = ["Smartphone", "Tablet", "Wearable: Fitness Band", "Wearable: Smart Watch", "Wearable: Earbuds",
"Wearables: Others", "Feature Phone", "Wireless Carrier", "Desktop Computer", "Laptop", "Music Service - Radio",
"Music Service - Streaming App", "Mobile Branding", "Home Theater", "Monitor", "TV", "Connected TV", "VD Branding",
"Air Conditioner", "Refrigerator", "Stove Top", "Oven", "Air Purifier", "Dishwasher", "Microwave", "Vacuum Cleaner",
"Connected Home", "DA Branding", "Washing Machine", "Memory","Corporate", "x"]

clases_modelo = []
for i in clases_modelo_:
    clases_modelo.append(i.lower())

class Automaton:
    """Esta es la clase en la cual se hace todo el modelo y revisión de base de datos para reutilizar los copys ya existentes"""
    def __init__(self, mes, ano, historico, predecir = None):
        """El constructor toma inicialmente cuatro variables
        mes: cadena de caracteres del nombre del mes del análisis
        Ano: Año del analisis que se esta analizando
        predecir: Opcional, si se da, es el pandas dataframe que tiene las paginas a predecir junto con la marca a la que corresponden"""
        self.mes = mes
        self.ano = ano
        self.historico = historico
        self.predecir = predecir
        self.productos = None
        self.productos_name = None
        self.modelo = None
        self.X_test = None
        self.y_test = None
        self.conocido = None
        self.clase_conocido = None
        self.clases_inv = None
        self.tokenizer = None

        # Verificamos que la información proporcionada tenga todo lo que se requiere en el análisis, si no lo tiene hay que cambiar el nombre de las columnas        
        columnas_necesarias = ["page", "marca", "subcategoria", "producto", "mes"]
        for i in range(len(columnas_necesarias)):
            if columnas_necesarias[i] not in historico.columns:
                raise RuntimeError(columnas_necesarias[i] + " not in columns of historical data")
       # Verificamos que las categorias que vienen en la base de datos coincidan con las que tenemos nosotros originalmente 
        clases_presentes = np.unique(historico["subcategoria"])
        for clase in clases_presentes:
            if clase not in clases_modelo:
                raise RuntimeError("La etiqueta-" + clase + "-No existe en los elementos a catalogar")
        self.clases_presentes = np.unique(historico[historico["subcategoria"] != "x"]["subcategoria"]) # Las que no se catalogan no se usan para el modelo      
    
    def fit(self, num_words = 600, epochs=30, verbose=1):
        """Esta es la función que va a tomar la información historica para crear un modelo de Deep Learning, particularmente una LSTM para predecir aquellos productos
        de los cuales no se tenga registro anteriormente. Toma tres parámetros.
        num_words: Esta se refiere al numero de palabras máximo que vamos a tomar como referencia para que el modelo aprenda, si la base crece mucho, podría ser necesario incrementear este numero
        epochs: Los pasos del algoritmo de optimización que se daran para ajustar el modelo
        verbose: 0 si no queremos ver el proces 1 si lo queremos ver"""
        rango = list(range(len(self.clases_presentes)))
        clases = dict(zip(self.clases_presentes, rango))
        clases_inv = dict(zip(rango, self.clases_presentes))
        self.clases_inv = clases_inv
        num_clases = len(self.clases_presentes)
        self.clases = clases
        
        clases_datos = np.zeros(len(self.historico))
        idx = 0
        ## No incluimos los catalogados al modelo
        for i in self.historico[self.historico["subcategoria"] != "x"].index:
            clases_datos[idx] = clases[self.historico[self.historico["subcategoria"] != "x"].loc[i, "subcategoria"]]
            idx +=1
        self.historico["clase"] = clases_datos
        
        stop = nltk.corpus.stopwords.words("spanish")
        
        marca = self.historico[self.historico["subcategoria"] != "x"]["marca"].values
        X = self.historico[self.historico["subcategoria"] != "x"]["producto"].values
        y = self.historico[self.historico["subcategoria"] != "x"]["clase"].values
        #Nos aseguramos que todos esten en forma de string, pueden llegar numeros
        for i in range(len(X)):
            if(type(X[i]) != str):
                X[i] = str(X[i])
        # limpiamos un poco la data, podria mejorar
        X = [marca[i] + " " + X[i] for i in range(len(X))]
        X = [" ".join(filter(lambda x:(not (x in stop)), X[i].split())) for i in range(len(X))]
        
        num_words=600

        # tokenizamos la información para poder meterla a la red neuronal
        tokenizer = Tokenizer(num_words=num_words)
        tokenizer.fit_on_texts(X)
        
        self.tokenizer = tokenizer
        
        sequences = tokenizer.texts_to_sequences(X)
        Xs = keras.utils.pad_sequences(sequences)
        ################# Arquitectura del modelo ###########################        
        model_lstm = keras.models.Sequential([
              keras.layers.Embedding(num_words, 100, input_length=Xs.shape[1]),
              keras.layers.SpatialDropout1D(0.2),
              keras.layers.LSTM(100, dropout=0.2, recurrent_dropout=0.2),
              keras.layers.Dense(num_clases, activation="softmax")
        ])

        model_lstm.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
        
        X_train, X_test, y_train, y_test = train_test_split(Xs, y, test_size=0.3, random_state=0)
        
        history = model_lstm.fit(X_train, keras.utils.to_categorical(y_train), epochs=epochs, verbose = verbose, validation_split=0.2)
        
        self.modelo = model_lstm
        self.X_test = X_test
        self.y_test = y_test
        loss, auc = model_lstm.evaluate(X_test, keras.utils.to_categorical(y_test))
        print("Precisión Obtenida:  " +str(auc))
        
    def model_report(self):
        """Esta método nos sirve para que, una vez ajustado el modelo podamos tener una idea si esta funcionando bien, 
        va a imprimir la matriz de confusión y un reporte ed clasificación con diferentes métricas, asi como la etiqueta de cada una de las clases"""
        y_pred = self.modelo.predict(self.X_test)
        if self.modelo == None:
            raise RuntimeError("Este modelo no ha sido ajustado aún")
        CM = tf.math.confusion_matrix(self.y_test, y_pred.argmax(axis=1))

        fig = px.imshow(CM, color_continuous_scale="inferno")
        fig.show()
        
        print(classification_report(y_true=self.y_test, y_pred=y_pred.argmax(axis=1)))
        print(self.clases)
       
        
    def set_data(self, predecir):
        """Esta método se utiliza para indicar cual es la base de datos que usaremos para predecir, es decir para automatizar dentro del proceso. Ocuparemos un dataframe
        el cual tendrá que tener dos columnas, page y marca, marca refiere a la marca que admetricks encontro era esa pagina y page a la pagina que contiene la publicidad a encontrar
        """
        self.predecir = predecir
        columnas_necesarias = ["marca", "page"]
        for x in columnas_necesarias:
            if x not in predecir:
                raise RuntimeError(x + " not in prediction columns")
        paginas = predecir["page"]
        marcas = predecir["marca"]
        productos, productos_name = scrapping.get_products(paginas, marcas)
        print("Termine!")
        print("Porcentaje de éxito:" + str(sum([productos[i] != None for i in range(len(productos))]) / len(productos)))
        self.productos = productos
        self.productos_name = productos_name
        
    def check_history(self):
        """Este metodo nos sirve para revisar los elementos que se van a predecir y ver si ya existen en el historico para no tener que hacer una predicción sobre ellos.
        """
        self.conocidos = [0 for i in range(len(self.productos))]
        self.clase_conocido = [None for i in range(len(self.productos))]
        for i in range(len(self.predecir)):
            if len(self.historico[self.historico["page"] == self.predecir.at[i, "page"]]) != 0:
                self.productos_name[i] = self.historico[self.historico["page"] == self.predecir.at[i, "page"]]["producto"].values[-1]
                self.conocidos[i] = 1
                self.clase_conocido[i] = self.historico[self.historico["page"] == self.predecir.at[i, "page"]]["subcategoria"].values[-1]
    
    def generate_automation(self, file_name = None):
        """Este método centra todo el esfuerzo, toma un unico parametro, el nombre del excel al que queremos la predicción vaya,
        Esta tomara la base a predecir verificara si tenemos esa información en el historico, si no la tiene trateremos de hace scrapping a la página y de la información que obtrengamos 
        predeciremos la clasificación usando el modeolo"""
        if self.modelo == None:
            raise RuntimeError("Este modelo no ha sido ajustado aún")
        if file_name == None:
            file_name = "Automatización_"+ self.mes + "_" + self.ano
        self.check_history() # Checamos la base de datos para no repetir a los que se encuentren en historico
        # En esdta parte debemos llevar una trackeo de cuales si tenemos informacion y cuales para poder obtenerlos en el mismo orden que llegaron
        track = np.zeros((len([x for x in self.productos if x != None])))
        productos_clean = []
        idx = 0
        for i in range(len(self.productos)):
          if self.productos[i] != None:
            productos_clean.append(self.productos[i])
            track[idx] = i
            idx += 1

        todos = self.tokenizer.texts_to_sequences(productos_clean)

        track_track = np.zeros(len([todos[i] for i in range(len(todos)) if todos[i] != list([])]))
        conocidos_palabras = []
        idx2=0
        for i in range(len(todos)):
          if len(todos[i]) != 0:
            conocidos_palabras.append(todos[i])
            track_track[idx2] = i
            idx2 += 1

        conocidos_padded = keras.utils.pad_sequences(conocidos_palabras,  maxlen=17)
        
        y_pred = self.modelo.predict(conocidos_padded)
        y_pred_class = y_pred.argmax(axis=1)
        
        clases_predichas = []
        # asignamos las clases 
        for i in range(len(y_pred_class)):
            clases_predichas.append(self.clases_inv[int(y_pred_class[i])])

        glob = [None for i in range(len(self.productos))]
        for i in range(len(track_track)):
            index = int(track[int(track_track[i])])
            glob[index] = clases_predichas[i]
        
        
            
        cat = [None for i in range(len(self.productos))]
        for i in range(len(self.productos)):
            if self.conocidos[i] == 1:
                glob[i] = self.clase_conocido[i]
            if glob[i] in Mobile:
                cat[i] = "Mobile"
            if glob[i] in VD:
                cat[i] = "VD"
            if glob[i] in DA:
                cat[i] = "DA"
            if glob[i] in Memory:
                cat[i] = "Memory"
            if glob[i] in Corporate:
                cat[i] = "Corporate"
            if glob[i] == "x":
                cat[i] = "x"
        self.predecir["categoria"] = cat
        self.predecir["subcategoria"] = glob
        self.predecir["subcategoria"] = glob
        self.predecir["producto"] = self.productos_name
        self.predecir.to_excel(file_name+".xlsx")
        return self.predecir
        
    