import openai
import json
import src.utils as u




def get_message_from_prompt(prompt):
    print("Getting message from prompt" + prompt[0:150] + "...")
    config = u.read_config_file()
    if config is None:
        return None
    api_key = config['api_key']
    model = config['model']
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

def generate_json_from_text(text):
    print("Generating JSON from text...")

    prompt = f"""
    Procesa el siguiente texto y genera un JSON estructurado con los siguientes campos:
    - name: Nombre del tema
    - description: Descripción brebe del tema
    - id: ID secuencial en el formato [topic-NNN]
    - subTopics: Lista de subtemas, donde cada subtema tiene:
        - name: Nombre del sub tema
        - description: Descripción del subtema
        - id: ID secuencial en el formato [topic-NNN-subtopic-NNN]
        - isSub: true si es un subtema
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
    
def sumarize_text(text):
    print("Summarizing text...")

    prompt= f"""
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

def generate_note_from_json(json):
    config = u.read_config_file()
    prompt = f"""
    actuaras como un desarrollador fullstack senior
    que se esta preparando para entrevistas de trabajo
    tu objetivo es dar confianza y mostrar solidez desde el conosimiento tecnico(preferible) o la experiencia profecional(en segundo plano)
    reciviras un text json con el siguiente formato:
    <inicio formato>
    - name: Nombre del tema
    - description: Descripción brebe del tema
    - id: ID secuencial en el formato [topic-NNN]
    <fin formato>
    tu mision sera proveer informacion clara y consisa sobre el tema para prepararme ante una eventual enrtevista tecnica
    para el tema, tecnologia o consepto deveras dar una ficha de estudio (en formato marckdown) con el siguiente formato:
    <inicio ficha>
     # name: nombre del tema
    ## descrption: un descripcin clara pero consisa del tema en cuestion
    ## importance: definir las ventajas de porque se emplea o cuando es mas recomendable aplicarlo, puede ser un punteo o lista brebe, nunca mas de 5
    ## keywords: una lista separada por comas de palabras clave fundamentales en una conversacion sobre este tema, cosas que deveria manejar bien
    ## god-to-know: lo mas importante que debo saber del tema
    ## questions-anwers: una lista de 3 a 7 perguntas claves que un reclutador podria buscar o querer validar o determinar mi nivel, recuerda que soy un senior. 
        cada prengta tendra su corespondiente respuesta, explicativa pero consisa, si puedes incluye algn ejemplo de codigo o configuracion pertinente en cada pregunta

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