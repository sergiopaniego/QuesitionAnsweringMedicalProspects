import spacy
import Stemmer

nlp = spacy.load('es_core_news_sm')

files = ['prospecto-ibuprofeno.txt', 'prospecto-aspirina.txt', 'prospecto-lizipaina.txt', 'prospecto-paracetamol.txt',
         'prospecto-frenadol.txt']
medicines = []
medicines_names_glossary = ['lizipain', 'aspirin', 'frenadol', 'ibuprofen', 'paracetamol']
dimension_glossary = ['principi', 'activ', 'dosis', 'efect', 'prohibicion', 'composicion', 'aspect', 'conten', 'conserv',
                      'util', 'conduc', 'maquinari', 'advers']
synonymous_glossary = [('package_content', ['conten']),
                       ('medication_appearance', ['aspect']),
                       ('active_principle', ['principi', 'activ', 'composicion']),
                       ('purpose', ['efect', 'util']),
                       ('conservation_protocol', ['conserv']),
                       ('conduction_and_machinery_use', ['conduc', 'maquinari']),
                       ('adverse_effects', ['advers']),
                       ('dosis', ['dosis']),
                       ('prohibitions', ['prohibicion'])]


class Medicine:
    name = ''
    package_content = ''
    medication_appearance = ''
    active_principle = ''
    purpose = ''
    conservation_protocol = ''
    conduction_and_machinery_use = ''
    adverse_effects = ''
    dosis = ''
    prohibitions = ''


def extract_composition(medicine, file):
    composition_zone = True
    while composition_zone:
        line = file.readline()
        print(line)
        if medicine.active_principle == '':
            medicine.active_principle = line
        elif len(line.split('- ')) > 1 or len(line.split(' ')) > 1:
            medicine.active_principle += line
            if len(line.split('.')) > 1 and line.split('.')[1] == '\n':
                composition_zone = False
        elif len(line.split('Aspecto del producto')) > 1:
            composition_zone = False
    return line


def extract_medication_appearance_package_content(medicine, file):
    line = file.readline()
    divided_sentence = line.split('. ')
    medicine.medication_appearance = divided_sentence[0]
    medicine.package_content = divided_sentence[1].split('\n')[0] + ' '
    if len(divided_sentence[1].split('.')) == 1:
        line = file.readline()
        medicine.package_content += line


def extract_purpose(medicine, file):
    line = file.readline()
    while len(line.split('2. ')) <= 1:
        medicine.purpose += line
        line = file.readline()
    return line


def extract_conservation_protocol(medicine, file, line):
    while len(line.split('aducidad')) == 1:
        medicine.conservation_protocol += line
        line = file.readline()


def extract_conduction_and_machinery_use(medicine, file):
    line = file.readline()
    while len(line.split('3. ')) == 1:
        medicine.conduction_and_machinery_use += line
        line = file.readline()


def extract_adverse_effects(medicine, file):
    line = file.readline()
    while len(line.split('Comunicación de efectos adversos')) == 1 and len(line.split('Si le ocurre alguno de los siguientes efectos adversos')) == 1 and len(line.split('5.')) == 1:
        medicine.adverse_effects += line
        line = file.readline()
    return line


def extract_dosis(medicine, file, line):
    if line.split(':')[1] != '\n':
        medicine.dosis += line
    line = file.readline()
    medicine.dosis += line


def extract_prohibitions(medicine, file):
    line = file.readline()
    while (len(line.split('Uso de')) == 1 or len(line.split('otros medicamentos')) == 1) and len(line.split('Advertencias y precauciones')) == 1:
        medicine.prohibitions += line
        line = file.readline()
    return line


def extract_information():
    for file_name in files:
        medicine = Medicine()
        name = file_name.split(('prospecto-'))[1]
        medicine.name = name[:-4]
        file = open(file_name, 'r')
        line = file.readline()
        count_1 = 0
        count_2 = 0
        count_4 = 0
        count_5 = 0
        while line:
            if len(line.split('Composición')) > 1 or len(line.split('Composición')) > 1:
                line = extract_composition(medicine, file)
                print('Composition [\n' + medicine.active_principle + ']')
            elif len(line.split('Aspecto del producto y contenido del envase')) > 1:
                extract_medication_appearance_package_content(medicine, file)
                print('Medication appearance [\n' + medicine.medication_appearance + ']')
                print('Package content [\n' + medicine.package_content + ']')
                line = file.readline()
            elif len(line.split('1. ')) > 1:
                if count_1 != 1:
                    count_1 += 1
                    line = file.readline()
                else:
                    count_1 += 1
                    line = extract_purpose(medicine, file)
                    print('Purpose [\n' + medicine.purpose + ']')
            elif len(line.split('5. ')) > 1:
                if count_5 == 0:
                    count_5 += 1
                else:
                    line = file.readline()
                    extract_conservation_protocol(medicine, file, line)
                    print('Conservation [\n' + medicine.conservation_protocol + ']')
                line = file.readline()
            elif len(line.split('Conducción y uso de máquinas')) > 1 or len(line.split('Conducción y uso de máquinas')) > 1:
                extract_conduction_and_machinery_use(medicine, file)
                print('Conduction and Machinery use [' + medicine.conduction_and_machinery_use + ']')
                line = file.readline()
            elif len(line.split('4. Posibles efectos adversos')) > 1:
                if count_4 == 0:
                    count_4 += 1
                    line = file.readline()
                else:
                    line = extract_adverse_effects(medicine, file)
                    print('Adverse effects [' + medicine.adverse_effects + ']')
            elif len(line.split('Adultos y')) > 1:
                extract_dosis(medicine, file, line)
                print('Dosis [' + medicine.dosis + ']')
                line = file.readline()
            elif len(line.split('2.')) > 1 and count_2 < 2:
                if count_2 == 0:
                    count_2 += 1
                    line = file.readline()
                elif count_2 == 1:
                    count_2 += 1
                    line = extract_prohibitions(medicine, file)
                    print('Prohibitions [' + medicine.prohibitions + ']')
            else:
                line = file.readline()
        medicines.append(medicine)


def preprocess_document(tokens):
    stemmer = Stemmer.Stemmer('spanish')
    final = stemmer.stemWords(tokens)
    return final


def matching(question_tokens):
    question_tokens = preprocess_document(question_tokens)
    dimension_searched = ''
    medicine_searched = ''
    for token in question_tokens:
        if token in dimension_glossary:
            print('Dimension ' + token)
            dimension_searched = token
        if token in medicines_names_glossary:
            medicine_searched = token
            print('Medicine name ' + token)
    dimension_name = ''
    for synonymous in synonymous_glossary:
        if dimension_searched in synonymous[1]:
            dimension_name = synonymous[0]
    if medicine_searched != '':
        for medicine in medicines:
            if len(medicine.name.split(medicine_searched)) > 1:
                return medicine.__getattribute__(dimension_name)
    else:
        return 'Los medicamentos que sirven son: paracetamol, frenadol, aspirina'


extract_information()
# print(medicines)

while True:
    question = input()
    doc = nlp(question)
    important = []
    for token in doc:
        if token.head.text not in important:
            important.append(token.head.text)
    # print(important)
    answer = matching(important)
    print(answer)