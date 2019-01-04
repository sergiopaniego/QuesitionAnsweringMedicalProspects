import spacy

nlp = spacy.load('es_core_news_sm')

package_content = ''
medication_appearance = ''
active_principle = ''
administration_method = ''
purpose = ''
revision_date = ''
expiration_date = ''
conservation_protocol = ''
conduction_and_machinery_use = ''
kids_administration_method = ''
elderly_administration_method = ''
overdose_protocol = ''
forgot_medication = ''
adverse_effects = ''
adverse_effects_communication = ''
dosis = ''
prohibitions = ''


def extract_composition(file):
    global active_principle
    composition_zone = True
    while composition_zone:
        line = file.readline()
        if active_principle == '' and len(line.split('- ')) > 1:
            active_principle = line
        elif len(line.split('- ')) > 1:
            active_principle += line
            if len(line.split('.')) > 1 and line.split('.')[1] == '\n':
                composition_zone = False
        elif active_principle != '':
            active_principle += line
            composition_zone = False


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


def extract_administration_method(file):
    global administration_method
    line = file.readline()
    administration_method = line


def extract_purpose(file):
    global purpose
    line = file.readline()
    while len(line.split('2. ')) <= 1:
        purpose += line
        line = file.readline()
    return line


def extract_expiration_date(file, line):
    global expiration_date
    while len(line.split('caducidad')) > 1:
        expiration_date += line.split('\n')[0] + ' '
        line = file.readline()


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


def extract_kids_administration_method(file):
    global kids_administration_method
    line = file.readline()
    while len(line.split('.')) == 1:
        kids_administration_method += line
        line = file.readline()
    kids_administration_method += line


def extract_elderly_administration_method(file):
    global elderly_administration_method
    line = file.readline()
    while len(line.split('.')) == 1:
        elderly_administration_method += line
        line = file.readline()
    if line.split('.')[1] != '\n':
        elderly_administration_method += line
        line = file.readline()
    elderly_administration_method += line


def extract_overdose_protocol(file):
    global overdose_protocol
    line = file.readline()
    while len(line.split('Si olvidó tomar')) == 1:
        overdose_protocol += line
        line = file.readline()
    return line


def extract_forgot_medication(file):
    global forgot_medication
    line = file.readline()
    while len(line.split('4.')) == 1:
        forgot_medication += line
        line = file.readline()
    return line


def extract_adverse_effects(file):
    global adverse_effects
    line = file.readline()
    while len(line.split('Comunicación de efectos adversos')) == 1:
        adverse_effects += line
        line = file.readline()
    return line


def extract_adverse_effects_communication(file):
    global adverse_effects_communication
    line = file.readline()
    while len(line.split('5. Conservación de')) == 1:
        adverse_effects_communication += line
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
    while len(line.split('Uso de')) == 1 or len(line.split('otros medicamentos')) == 1:
        prohibitions += line
        line = file.readline()
    return line


def extract_information(filename):
    # file = open('prospecto-ibuprofeno.txt', 'r')
    file = open('prospecto-aspirina.txt', 'r')
    line = file.readline()
    count_1 = 0
    count_2 = 0
    count_4 = 0
    count_5 = 0
    while line:
        if len(line.split('Composición')) > 1:
            extract_composition(file)
            print('Composition [\n' + active_principle + ']')
            line = file.readline()
        elif len(line.split('Aspecto del producto y contenido del envase')) > 1:
            extract_medication_appearance_package_content(file)
            print('Medication appearance [\n' + medication_appearance + ']')
            print('Package content [\n' + package_content + ']')
            line = file.readline()
        elif len(line.split('Forma de administración')) > 1:
            extract_administration_method(file)
            print('Administration method [' + administration_method + ']')
            line = file.readline()
        elif len(line.split('1. Qué es')) > 1:
            if count_1 == 0:
                count_1 += 1
            else:
                line = extract_purpose(file)
                print('Purpose [\n' + purpose + ']')
        elif len(line.split('Este prospecto ha sido')) > 1:
            revision_date = line
            print('Revision date [\n' + revision_date + ']')
            line = file.readline()
        elif len(line.split('caducidad')) > 1:
            extract_expiration_date(file, line)
            print('Expiration date [\n' + expiration_date + ']')
            line = file.readline()
        elif len(line.split('5. Conservación')) > 1:
            if count_5 == 0:
                count_5 += 1
            else:
                line = file.readline()
                extract_conservation_protocol(file, line)
                print('Conservation [\n' + conservation_protocol + ']')
            line = file.readline()
        elif len(line.split('Conducción y uso de máquinas')) > 1:
            extract_conduction_and_machinery_use(file)
            print('Conduction and Machinery use [' + conduction_and_machinery_use + ']')
            line = file.readline()
        elif len(line.split('Uso en niños:')) > 1:
            extract_kids_administration_method(file)
            print('Kids administration [' + kids_administration_method + ']')
            line = file.readline()
        elif len(line.split('Pacientes de edad avanzada')) > 1 or len(line.split('Uso en mayores de 65 años')) > 1:
            extract_elderly_administration_method(file)
            print('Elderly people administration [' + elderly_administration_method + ']')
            line = file.readline()
        elif len(line.split('toma más')) > 1:
            line = extract_overdose_protocol(file)
            print('Overdose protocol [' + overdose_protocol + ']')
        elif len(line.split('Si olvidó tomar')) > 1:
            line = extract_forgot_medication(file)
            print('Forgot medication [' + forgot_medication + ']')
        elif len(line.split('4. Posibles efectos adversos')) > 1:
            if count_4 == 0:
                count_4 += 1
                line = file.readline()
            else:
                line = extract_adverse_effects(file)
                print('Adverse effects [' + adverse_effects + ']')
        elif len(line.split('Comunicación de efectos adversos')) > 1:
            line = extract_adverse_effects_communication(file)
            print('Adverse effects communication [' + adverse_effects_communication + ']')
        elif len(line.split('Adultos y')) > 1:
            extract_dosis(file, line)
            print('Dosis [' + dosis + ']')
            line = file.readline()
        elif len(line.split('2.')) > 1:
            if count_2 == 0:
                count_2 += 1
                line = file.readline()
            else:
                line = extract_prohibitions(file)
                print('Prohibitions [' + prohibitions + ']')
        else:
            line = file.readline()


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

# ¿Cúal es la forma de administrar el medicamento?
