# 🧪 Laboratorio 1: Introducción a ANTLR

## 📋 Descripción General

En este laboratorio trabajarás con **ANTLR**, un generador de analizadores sintácticos. Hemos proporcionado un `Dockerfile` para ayudarte a configurar el entorno rápidamente. Utilizaremos Python para hacer pruebas, ya que es más sencillo que Java para pruebas pequeñas.

* **Modalidad: Individual**

## 🧰 Instrucciones de Configuración

1. **Construir y Ejecutar el Contenedor Docker**Desde el directorio raíz de este laboratorio, ejecuta el siguiente comando para construir la imagen y lanzar un contenedor interactivo:

   ```bash
   docker build --rm . -t lab1-image && docker run --rm -ti -v "$(pwd)/program":/program lab1-image
   ```
2. **Entender el Entorno**

   - El directorio `program` se monta dentro del contenedor.
   - Este contiene la **gramática de ANTLR**, un archivo `Driver.py` (punto de entrada principal) y un archivo `program_test.txt` (entrada de prueba).
3. **Generar Archivos de Lexer y Parser**Dentro del contenedor, compila la gramática ANTLR a Python con:

   ```bash
   antlr -Dlanguage=Python3 MiniLang.g4
   ```
4. **Ejecutar el Analizador**
   Usa el driver para analizar el archivo de prueba:

   ```bash
   python3 Driver.py program_test.txt
   ```

   - ✅ Si el archivo es sintácticamente correcto, **no se mostrará ningún resultado**.
   - ❌ Si existen errores, ANTLR los mostrará en la consola.
   - **Next Step:** Jueguen editando el archivo y vean los cambios en los resultados de compilación.

## 📋 Entregables

- Realice un análisis sobre la gramática de ANTLR y el archivo de Driver y comente acerca del funcionamiento de estos, es decir, explique sus partes lo más brevemente posible e indique cómo funcionan los distintos elementos de la gramática escrita en ANTLR, e.g. "Utilizar # en ANTLR sirve para...", "Un archivo .g4 tiene las siguientes secciones...", etc.
- **Video de YouTube no listado** (pero público) con sus pruebas, donde compila bien y donde no compila bien y con sus comentarios al punto anterior.
- Repo de Github con todo su código.

## 🚀 ¿Qué Sigue?

- Esta configuración es un **entorno básico** para experimentar con ANTLR.
- A medida que avances en el curso:
  - Implementarás **Visitors** o **Listeners**
  - Realizarás **análisis semántico**
- Para tus proyectos, se recomienda **extender este entorno** para soportar una arquitectura más robusta y modular.

---

## ⚙️ Ejecución local (sin Docker)

Este laboratorio también se puede ejecutar sin Docker, siguiendo la alternativa recomendada en `README_NOTES.md`. Pasos usados en este repositorio (dato que mi entorno es uno Linux me puedo permitir esto):

1. Instalar Java (JDK), requerido por ANTLR ya que corre sobre la JVM.
2. Crear un alias apuntando al jar incluido en el repo:
   ```bash
   alias antlr='java -jar $(pwd)/antlr-4.13.2-complete.jar'
   ```
3. Generar el Lexer y Parser desde la carpeta `program`:
   ```bash
   cd program
   antlr -Dlanguage=Python3 MiniLang.g4
   ```
4. Crear un entorno virtual e instalar el runtime de Python:
   ```bash
   cd ..
   python3 -m venv venv
   source venv/bin/activate
   pip install antlr4-python3-runtime==4.13.0
   ```
5. Ejecutar el driver:
   ```bash
   cd program
   python3 Driver.py program_test.txt
   ```

---

## 📖 Análisis: Gramática MiniLang y Driver.py

### 1. ¿Qué es un archivo `.g4`?

Un archivo `.g4` es el archivo de gramática que utiliza ANTLR para generar automáticamente un analizador léxico (Lexer) y un analizador sintáctico (Parser) para un lenguaje definido por el programador. En este laboratorio, el archivo `MiniLang.g4` define un pequeño lenguaje de tipo calculadora con variables, y contiene las siguientes secciones principales:

- **Declaración de la gramática:** la línea `grammar MiniLang;` le da nombre a la gramática. Este nombre debe coincidir exactamente con el nombre del archivo.
- **Reglas del Parser (minúsculas):** reglas como `prog`, `stat` y `expr`, que definen cómo se combinan los tokens para formar sentencias y expresiones válidas del lenguaje.
- **Reglas del Lexer (mayúsculas):** reglas como `MUL`, `DIV`, `ID`, `INT` y `NEWLINE`, que definen cómo se forman los tokens individuales a partir de los caracteres del texto de entrada.

### 2. La regla `prog` (punto de entrada)

La regla `prog: stat+ ;` es el punto de partida de la gramática. Indica que un programa válido en MiniLang está compuesto por una o más sentencias (`stat`) escritas de forma consecutiva. Esta es la regla que se invoca desde el `Driver.py` mediante `parser.prog()` para iniciar el análisis.

### 3. La regla `stat` y el uso de `#`

La regla `stat` define tres tipos posibles de sentencia: una expresión suelta seguida de salto de línea, una asignación de variable, o una línea en blanco. El símbolo `#` que aparece después de cada alternativa (por ejemplo `# printExpr`, `# assign`, `# blank`) sirve para etiquetar cada alternativa con un nombre. ANTLR utiliza estas etiquetas para generar un método o clase independiente por cada alternativa dentro del código del Parser (y del Listener/Visitor), lo que permite distinguir programáticamente qué tipo de sentencia se encontró al recorrer el árbol sintáctico, en lugar de tener que revisar manualmente el contenido de cada nodo.

### 4. La regla `expr` y la precedencia de operadores

La regla `expr` define las expresiones matemáticas de forma recursiva: una expresión puede contener otras expresiones dentro de sí misma. Las alternativas incluyen multiplicación y división, suma y resta, un número entero, un identificador, o una expresión entre paréntesis. Un detalle importante de ANTLR es que el orden en que se escriben las alternativas determina su precedencia: como `MulDiv` aparece antes que `AddSub`, ANTLR le da mayor prioridad, resolviendo así la ambigüedad de expresiones como `2 + 3 * 4` (se multiplica primero, como es matemáticamente correcto).

### 5. Reglas léxicas (tokens)

Las reglas en mayúsculas definen cómo se reconocen los tokens a partir del texto crudo de entrada. `ID` reconoce una o más letras consecutivas (nombres de variable), `INT` reconoce uno o más dígitos, y `NEWLINE` reconoce el salto de línea que marca el fin de una sentencia. La regla `WS` (espacios y tabulaciones) utiliza la instrucción `-> skip`, que le indica a ANTLR que descarte esos caracteres sin generar ningún token, ya que no aportan significado a la gramática.

### 6. Funcionamiento del `Driver.py`

El archivo `Driver.py` es el punto de entrada del programa en Python y conecta el Lexer y el Parser generados por ANTLR. Su funcionamiento sigue cuatro pasos:

- **FileStream:** lee el archivo de entrada (por ejemplo `program_test.txt`) como un flujo de caracteres.
- **MiniLangLexer:** toma ese flujo de caracteres y lo convierte en una secuencia de tokens, según las reglas léxicas definidas en la gramática.
- **CommonTokenStream:** envuelve los tokens generados por el Lexer en un flujo que el Parser puede consumir.
- **MiniLangParser y parser.prog():** el Parser toma el flujo de tokens y aplica las reglas sintácticas comenzando por la regla inicial `prog`, construyendo (o validando) el árbol sintáctico del programa. Si la entrada no respeta la gramática, ANTLR reporta los errores léxicos o sintácticos correspondientes en la consola; si es válida, el programa termina sin mostrar ningún mensaje.

### 7. Conclusión

En conjunto, la gramática `MiniLang.g4` y el `Driver.py` muestran el flujo básico de un compilador o intérprete: primero un análisis léxico que agrupa caracteres en tokens con significado, y luego un análisis sintáctico que valida que esos tokens sigan una estructura gramatical correcta. ANTLR automatiza la generación de ambos componentes a partir de una única definición declarativa, lo que permite enfocarse en diseñar las reglas del lenguaje en lugar de implementar manualmente el analizador.

---

## 🔗 Enlaces

- **Video (YouTube, no listado):** https://youtu.be/YBo3vtLCF3s
- **Repositorio de GitHub:** https://github.com/ecarcamo/CC3032-COMPIS