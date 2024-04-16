import processing.serial.*;

Serial myPort;
PrintWriter output;  // Archivo de salida CSV
int xPos = 0; // Variable para almacenar la posición horizontal de la gráfica
float minY = 0; // Límite mínimo de los datos
float maxY = 400; // Límite máximo de los datos
String csvFileName; // Nombre del archivo CSV
int dataID = 0; // ID del dato

void setup() {
  size(800, 400);
  csvFileName = "datos_sensor_" + year() + "-" + month() + "-" + day() + "_" + hour() + "-" + minute() + "-" + second() + ".csv";
  // Abre el puerto serie, asegúrate de cambiar el nombre del puerto según tu configuración
  String portName = "COM7";
  myPort = new Serial(this, portName, 115200);
  
  // Abre el archivo CSV para escribir
  output = createWriter(csvFileName);
  
  // Escribe los títulos de las columnas en el archivo CSV
  output.println("ID,Datos ECG,Segundos,Milisegundos");
  output.flush(); // Para asegurar que los títulos se escriban antes de empezar a escribir los datos
}

void draw() {
  background(255); // Borra la pantalla en cada cuadro
  
  // Lee el valor del puerto serie
  if (myPort.available() > 0) {
    String valor = myPort.readStringUntil('\n');
    if (valor != null) {
      valor = trim(valor);  // Elimina espacios en blanco al principio y al final
      println(valor);  // Imprime el valor leído en la consola
      
      // Obtiene los segundos y milisegundos actuales
      int seconds = second();
      int milliseconds = millis() % 1000;
      
      // Escribe los datos en el archivo CSV en columnas separadas
      output.println(dataID + "," + valor + "," + seconds + "," + milliseconds);
      output.flush();
      
      // Incrementa el ID del dato
      dataID++;
      
      // Convierte el valor a un número
      float val = float(valor);
      
      // Ajusta los límites mínimo y máximo
      if (val < minY) minY = val;
      if (val > maxY) maxY = val;
      
      // Dibuja el valor recibido en la gráfica
      float y = map(val, minY, maxY, height, 0); // Convierte el valor a un rango vertical
      stroke(0); // Color de los puntos
      strokeWeight(5); // Tamaño de los puntos
      point(xPos, y); // Dibuja un punto en la posición actual
      xPos++; // Incrementa la posición horizontal
      if (xPos >= width) { // Si llegamos al final de la ventana
        xPos = 0; // Reinicia la posición horizontal
        background(255); // Borra la pantalla
        minY = 0; // Reinicia el límite mínimo
        maxY = 400; // Reinicia el límite máximo
      }
    }
  }
}

void keyPressed() {
  // Cierra el archivo CSV y el puerto serie al presionar una tecla
  output.flush();
  output.close();
  myPort.stop();
  exit();
}
