# Automaton 
### Este  es un programa para ayudar el proceso de rastreo de anuncios digirales en un caso muy específico, en su metodologia usamos web scrapping, deep learning y reutilizamos registros anteriores. Con este código podras reducir el trabajo de catalogación digital hasta en un 70%, si bien, ayuda a automatizar el proceso requiere de supervisión humana. 

## Instalación.

1. Descargar Anaconda [Aquí](https://www.anaconda.com/products/distribution)
2. Descargar los códigos que se encuentran en este repositorio y colocarlos en una carpeta aislada. (Puedes ponerle de nombre Automaton si quieres)
3. Abrir en programas Anaconda Prompt
4. Del lado izquierdo tendrás algo por estilo (base) C:\User\usuario, usando el comando CD navegar hasta donde se encuentra los códigos de este repositorio. Por ejemplo, yo lo  guarde en Documentos en una carperta llamada Automaton, digitar lo siguiente CD Documents enter, CD Automaton enter. En el lado izquierdo deberá decir ya te encuentras en la carpeta adecuada.
5. Copiar el siguiente codigo en la linea de comandos-> conda env create -f requirements.yml <- (sin las flechas) Posteriormente dar que si (y) a todo lo que pregunte.
6. Copiar el siguiente código en la linea de comandos -> conda activate automaton <- (sin las flechas)
7. Si del lado izquierdo en vez de (base) dice (automaton) el proceso se ha completado. Recordar siempre activar el ambiente (código de paso 6) antes de ejecutar el código.

## Uso
1. En Anaconda prompt dirigirte a la  carpeta donde se tiene guardado el código y activar el ambiente. 
2. Digitar el siguiente código, -> jupyter notebook <-
3. Abrir el documento Example_usage_automaton.ipynb, ahi vendra un ejemplo de como usarlo, ver la presentación para más detalle.


## ¿Quieres mejorar el código?
El código tiene dos principales componentes,  scrapping.py y AutomatonSamsung.py. El primer archivo se encarga de obtener la información de los productos de las páginas 
que más comunmente aparecen, este es importante tenerlo en cuenta ya que con el tiempo las paginas se actualizan y es importante monitorearlo para saber que tan atrasado está. Con esta información que racaba scrapping.py AutomatonSamsung.py lo usa. Este proceso consta de tres partes. 
1. COn la información histórica se actualiza el modelo y se entrena con los nuevos copys.
2. Se recaba nueva información usando el scrapping y se predice su catalogación mediante el modelo.
3. Se revisa si este copy ya exisitia en la base anterior, si es así se reutiliza.
