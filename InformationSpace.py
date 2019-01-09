import spacy

nlp = spacy.load('es_core_news_sm')

package_content = ''
medication_appearance = ''
active_principle = ''
purpose = ''
conservation_protocol = ''
conduction_and_machinery_use = ''
adverse_effects = ''
dosis = ''
prohibitions = ''


def extract_composition(file):
    global active_principle
    composition_zone = True
    while composition_zone:
        line = file.readline()
        if active_principle == '' and (len(line.split('- ')) > 1 or len(line.split(' ')) > 1):
            active_principle = line
        elif len(line.split('- ')) > 1 or len(line.split(' ')) > 1:
            active_principle += line
            if len(line.split('.')) > 1 and line.split('.')[1] == '\n':
                composition_zone = False
        elif active_principle != '':
            active_principle += line
            composition_zone = False
    return line


def extract_medication_appearance_package_content(file):
    global medication_appearance
    global package_content
    line = file.readline()
    divided_sentence = line.split('. ')
    medication_appearance = divided_sentence[0]
    package_content = divided_sentence[1].split('\n')[0] + ' '
    if len(divided_sentence[1].split('.')) == 1:
        line = file.readline()
        package_content += line


def extract_purpose(file):
    global purpose
    line = file.readline()
    while len(line.split('2. ')) <= 1:
        purpose += line
        line = file.readline()
    return line


def extract_conservation_protocol(file, line):
    global conservation_protocol
    while len(line.split('aducidad')) == 1:
        conservation_protocol += line
        line = file.readline()


def extract_conduction_and_machinery_use(file):
    global conduction_and_machinery_use
    line = file.readline()
    while len(line.split('3. ')) == 1:
        conduction_and_machinery_use += line
        line = file.readline()


def extract_adverse_effects(file):
    global adverse_effects
    line = file.readline()
    while len(line.split('Comunicación de efectos adversos')) == 1 and len(line.split('Si le ocurre alguno de los siguientes efectos adversos')) == 1:
        adverse_effects += line
        line = file.readline()
    return line


def extract_dosis(file, line):
    global dosis
    if line.split(':')[1] != '\n':
        dosis += line
    line = file.readline()
    dosis += line


def extract_prohibitions(file):
    global prohibitions
    line = file.readline()
    while (len(line.split('Uso de')) == 1 or len(line.split('otros medicamentos')) == 1) and len(line.split('Advertencias y precauciones')) == 1:
        prohibitions += line
        line = file.readline()
    return line


def extract_information(filename):
    # file = open('prospecto-ibuprofeno.txt', 'r')
    # file = open('prospecto-aspirina.txt', 'r')
    file = open('prospecto-lizipaina.txt', 'r')
    line = file.readline()
    count_1 = 0
    count_2 = 0
    count_4 = 0
    count_5 = 0
    while line:
        if len(line.split('Composición')) > 1 or len(line.split('Composición')) > 1:
            line = extract_composition(file)
            print('Composition [\n' + active_principle + ']')
        elif len(line.split('Aspecto del producto y contenido del envase')) > 1:
            extract_medication_appearance_package_content(file)
            print('Medication appearance [\n' + medication_appearance + ']')
            print('Package content [\n' + package_content + ']')
            line = file.readline()
        elif len(line.split('1. ')) > 1:
            print(line)
            if count_1 != 1:
                count_1 += 1
                line = file.readline()
            else:
                count_1 += 1
                line = extract_purpose(file)
                print('Purpose [\n' + purpose + ']')
        elif len(line.split('5. ')) > 1:
            if count_5 == 0:
                count_5 += 1
            else:
                line = file.readline()
                extract_conservation_protocol(file, line)
                print('Conservation [\n' + conservation_protocol + ']')
            line = file.readline()
        elif len(line.split('Conducción y uso de máquinas')) > 1 or len(line.split('Conducción y uso de máquinas')) > 1:
            extract_conduction_and_machinery_use(file)
            print('Conduction and Machinery use [' + conduction_and_machinery_use + ']')
            line = file.readline()
        elif len(line.split('4. Posibles efectos adversos')) > 1:
            if count_4 == 0:
                count_4 += 1
                line = file.readline()
            else:
                line = extract_adverse_effects(file)
                print('Adverse effects [' + adverse_effects + ']')
        elif len(line.split('Adultos y')) > 1:
            extract_dosis(file, line)
            print('Dosis [' + dosis + ']')
            line = file.readline()
        elif len(line.split('2.')) > 1 and count_2 < 2:
            if count_2 == 0:
                count_2 += 1
                line = file.readline()
            elif count_2 == 1:
                count_2 += 1
                line = extract_prohibitions(file)
                print('Prohibitions [' + prohibitions + ']')
        else:
            line = file.readline()


extract_information('')

'''
option = ''
print('Bienvenido al sistema de preguntas y respuestas sobre prospectos de medicamentos')
print('Introduce el nombre del archivo que contiene el prospecto médico:')
filename = input()
extract_information('')
while option != '1':
    print('¿Qué deseas hacer ahora?')
    print('[0] Introducir una pregunta')
    print('[1] Terminar')
    option = input()
    if option == '0':
        print('Introduce la pregunta:')
        question = input()
        doc = nlp(question)
        important = []
        for token in doc:
            if token.head.text not in important:
                important.append(token.head.text)
        print(important)
'''