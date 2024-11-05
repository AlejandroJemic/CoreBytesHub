import openai
import json
import src.utils as u




def get_message_from_prompt(prompt):
    config = u.read_config_file()
    if config is None:
        return None
    api_key = config['api_key']
    model = config['model']
    print("Getting message from prompt" + prompt[0:150] + "...")
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000
    )
    if response.choices and len(response.choices) > 0:
        return response.choices[0].message.content
    else:
        print("No choices received in the response.")
        return None

def generate_json_from_text(text, relatedTo):
    print("Generating JSON from text...")

    prompt = f"""k
     {"acerca de " + relatedTo if relatedTo != "" else ""}
    Procesa el siguiente texto y genera un JSON estructurado con los siguientes campos:
    - name: Nombre del tema
    - description: Descripción brebe del tema
    - id: ID secuencial en el formato [topic-NNN]
    - state: allways 'pending'
    - subTopics: Lista de subtemas, donde cada subtema tiene:
        - name: Nombre del sub tema
        - description: Descripción del subtema
        - id: ID secuencial en el formato [topic-NNN-subtopic-NNN]
        - isSub: true si es un subtema
        - state: allways 'pending'
    inicio del texto:
    {text}
    :fin de del texto
    considera que puede aver varios temas con subtemas, por tanto debes entregar un arreglo de temas
    debes omitir cualquier comentario adicional del tipo: Aquí tienes el JSON estructurado según lo solicitado:
    debes omitir cual marcado md como ```json 
    solo entrega contenido como texto plano en JSON
    """
    try:
        messageContent = get_message_from_prompt(prompt)
        if messageContent is None:
            return None
        else:
            json_data = json.loads(messageContent)
            return json_data
    except json.JSONDecodeError:
        print("Error al decodificar el JSON generado.")
        return None
    except openai.error.APIError as e:
        print("Error en la API:", e)
        return None
    
def sumarize_text(text, relatedTo):
    print("Summarizing text...")

    prompt= f"""
     {"acerca de " + relatedTo if relatedTo != "" else ""}
    Procesa el siguiente texto y extrae un temario estructurado en formato de texto plano. El temario debe cumplir con las siguientes características:
    1. Cada tema debe incluir:
    - Un título o palabra clave principal del tema.
    - Palabras clave relevantes, especialmente tecnologías, lenguajes de programación, herramientas, o conceptos de desarrollo, si están presentes.
    - Una descripción breve y precisa del tema, evitando detalles innecesarios o verbosidad.
    2. Si el tema tiene subtemas, lista cada subtema con:
    - Un título o palabra clave del subtema.
    - Una descripción breve del subtema, también precisa y concisa.
    Debes ser preciso y cuidar la extensión de las descripciones. No incluyas comentarios adicionales ni explicaciones fuera de lo solicitado. 
    A continuación, el texto a procesar:
    [INICIO DEL TEXTO]
    {text}
    [FIN DEL TEXTO]
    El resultado debe entregarse solo en texto plano.
    """
    try:
        messageContent = get_message_from_prompt(prompt)
        if messageContent is None:
            return None
        return messageContent
    
    except Exception as e:
        print("Error al procesar el texto:", e)
        return None
    except openai.error.APIError as e:
        print("Error en la API:", e)
        return None

def generate_note_from_json(json, relatedTo):
    config = u.read_config_file()

    if relatedTo != "":
        encabesado = f"""
        ESTE ES EL CONCEPTO PRINCIPAL QUE DEBE GUIAR TODO LO QUE ESCRIBAS A CONTINUACION
        TU PRICIPAL OBJETIVO ES CUBIRIR APROPIADAMENTE ESTE CONCEPTO:
        {relatedTo}
        """
    prompt = f"""
    {"OBJETIVO: " + encabesado if relatedTo != "" else ""}
    actuaras como un desarrollador fullstack senior
    que se esta preparando para entrevistas de trabajo
    tu objetivo es dar confianza y mostrar solidez desde el conosimiento tecnico(preferible) o la experiencia profecional(en segundo plano)
    recibiras un texto json con el siguiente formato:
    <inicio formato>
    - name: Nombre del tema
    - description: Descripción brebe del tema
    - id: ID secuencial en el formato [topic-NNN]
    <fin formato>
    tu mision sera proveer informacion clara y consisa sobre el tema para prepararme a una enrtevista tecnica.
    para el tema, tecnologia o consepto deveras dar una ficha de estudio (en formato marckdown) con el siguiente formato:
    <inicio ficha>
    # name: nombre del tema
    ## god-to-know: lo mas importante que debo saber del tema
    ## descrption: un descripcin clara pero consisa del tema en cuestion
    ## importance: definir las ventajas de porque se emplea o cuando es mas recomendable aplicarlo, puede ser un punteo o lista brebe, nunca mas de 5
    ## keywords: una lista separada por comas de palabras clave fundamentales en una conversacion sobre este tema, cosas que deveria manejar bien
    ## first steps: primeros pasos, configuracion basica o como iniciar o instalar con ejemplos, debe ser ago completo que funcione
    ## ejemplo completo de configuracion o codificacion:
        aqui debes generar un ejemplo funcional y completo del tema principal que se esta estudiando, algo que al copiarlo funcione.
        si requiere barios pasos debes explicarlos apropiadamente

    ## code examples: 
        una lista de ejemplos tecnicos adicionale,  de codigos o configuraciones, que complemente el ejemplo anterior, no debes repetir lo mismo de antes,  
        debes hacer enfacies en incluir tantos ejemplos practicos como sea pertinente. idealmente que sigan el orden trabajo, incluye ejemplos abanzados, 
        simempre deben ser mas de 3
        
    ## questions-anwers: una lista de 3 a 7 perguntas claves que un reclutador podria buscar o querer validar o determinar mi nivel, recuerda que soy un senior. 
        las preguntas no den ser naive, deben ser tecnicas enfocadas a ver conosiminetos practios de uso, programacion, o configuraciones
        cada prengta tendra su corespondiente respuesta, explicativa pero consisa,  incluye un ejemplo de codigo o configuracion pertinente en cada pregunta
    -si es un tema:
        deberas incluir cuando sea pertinente
        un punteo detallado detallado de los conseptos claves, nunca mas de 10, sobre todo desde el punto de vista de una conversacion
        si aplica algo referente a las keywords que incluiste anteriormente
    -si es una tecnologia framework o lenguaje:
        deberas incluir cuando sea pertinente
        - setup basico
        - package o librerias claves
        - code sinepets muy brebes pero muy significativos, espesialmente para un nivel senior
        si aplica algo referente a las keywords que incluiste anteriormente
    -si es un consepto:
        deberas incluir cuando sea pertinente
        un punteo detallado detallado de los conseptos claves, nunca mas de 10, sobre todo desde el punto de vista de una conversacion
        si aplica algo referente a las keywords que incluiste anteriormente

    ## more concept: 
    una lista de conseptos mas avanzados o subsiguientes que se pueden aplicar,aqui tambien debes dar una lista ejemplos tecnicos para cada item en la lista de modo que pued aplicarlo de la mejor manera en la vida real o el trabajo del dia a dia
    <fin ficha>

    aqui esta el json del que tienes que hacer la <ficha>:
    <incio tema>
    {json}
    <fin tema>
    
    consideraciones finales:
    si es pertinente agrega una seccion 
    # donde o como hacerlo
    siempre incluye algun ejemplo practico pertinente de configuracion o codigo
    siempre incluye algun link para mas informacion odoc oficial
    recuerda ser explicativo pero consiso
    enfocate mas en el trabajo del dia a dia que en la dialectica 
    considera no ser redundante, homite las repeticiones
    todo debe ser en idioma {config['language']}
    puedes aprovechar marckdonw para resaltar elementos y secciones
    recuerta tu objetivo es dar confianza y mostrar solidez desde el conosimiento tecnico(preferible) o la experiencia profecional(en segundo plano)
    no denes incluir etiquetas del tipo ```markdown
    """
    try:
        note = get_message_from_prompt(prompt)
        if note is None:
            return None
        return note
    except Exception as e:
        print("Error al procesar el json:", e)
        return None
    except openai.error.APIError as e:
        print("Error en la API:", e)
        return None

def generate_note_from_text(text):
    prompt = f"""explica el/los siguiente/s temas 
    el/los tema/s esta/n dividido/s en categorias y temas espesificoscon el siguinete formato:
    categoria|tema
    los temas son:
    {text}
    :fin de los temas
    para cada uno proporciona:
    - una explicacion clara, completa y consisa,
    - aspectos principales
    - un ejemplo completo y funconal detallado y comentado que funcione, debe ser un buen ejemplo, en calidad y extension
    - si hace o es deseableagregar falta algunos ejemplos complementarios o adicionales para ampliar el tema, tambien de buena calidad y extension
    - si cabe indica los posibles uso s y aplicaciones
    - si cabe genera algunas preguntas y repuestas enfocadas a una entevista tecnica
    es fundamental que expliques el tema, los ejemplos y las preguntas conn relacion a la categoria que le corespond
    """
    try:
        note = get_message_from_prompt(prompt)
        if note is None:
            return None
        return note
    except Exception as e:
        print("Error al procesar el json:", e)
        return None
    except openai.error.APIError as e:
        print("Error en la API:", e)
        return None
    



# genera un roadmap para el o los siguientes temas
# para un programador de junior a senior
# considera dividirlo en los siguientes niveles
# indispensable
# basico 
# intermedio
# abanzado
# posibles espocializaciones
# la salida debeser consisa siguendo el siguiente formato
# nivel
# temas	
# lista de subtemas: por cada tema genera una lista con los sub temas corespondientes
# descripcion: cada item en la lista de los sudtemas debe tener su corespondiente descripioc o comentario de lo que engloba/incluye  (maximo 300ch)
# considera usar el enfoque del 80-20 enfocandote en el 20% de temas que aportan el 80% de valor o importancia en aprnder o saver los emas que inclurias
# pero no lo hagas demaciado acortado tampoco, manten el balance en la cantidad de temas
# el/los temas son:
# ademas considera generar un anexo incluyendo temas que se emplean en el dia a dia programando o configurando y que son de usao comun
# sigue el mismo formato en la salida
# --------------------------------------------------------------
# evalua tu respuesta anterior, creees que fue demaciado corta, escueta o consisa?
# crees que hay otros temas de alto valor qu edeviste haber mencionado?
# si es as igener aun anexo incluyendolos empleando el mismo formato