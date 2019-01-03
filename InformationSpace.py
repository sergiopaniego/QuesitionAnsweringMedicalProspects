'''import spacy

nlp = spacy.load('es_core_news_sm')
doc = nlp(u"Lea todo el prospecto detenidamente antes de empezar a tomar este medicamento")
for token in doc:
    print(token.text, token.dep_, token.head.text, token.head.pos_, [child for child in token.children])
'''

# La pregunta primero buscará por la sección que sew sabe que se refiere

# option = input()
# file = open(option, 'r')3

# file = open('prospecto-ibuprofeno.txt', 'r')
file = open('prospecto-aspirina.txt', 'r')
line = file.readline()
package_content = ''
medication_appearance = ''
active_principle = ''
administration_method = ''
purpose = ''
revision_date = ''
expiration_date = ''
conservation_protocol = ''
conduction_and_machinery_use = ''


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


count_1 = 0
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
    elif len(line.split('Cómo tomar')) > 1:
        # print(line)
        line = file.readline()
    elif len(line.split('1. Qué es')) > 1:
        if count_1 == 0:
            count_1 += 1
        else:
            extract_purpose(file)
            print('Purpose [\n' + purpose + ']')
        line = file.readline()
    elif len(line.split('2. ')) > 1:
        # print(line)
        line = file.readline()
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
    else:
        line = file.readline()
