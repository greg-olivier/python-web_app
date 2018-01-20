from flask import *
import sqlite3


app = Flask(__name__)
app.debug = True

########## ACCUEIL ############
@app.route('/')
def index():
    return render_template('TemplateIndex.html')

########## PAGE DE LISTING DES ETUDIANTS ############
@app.route('/etudiants/')
def liste():
    conn = sqlite3.connect("C:\\Users\\HB1\\Desktop\\app_etudiant_python\\listing_etudiant.db") ########### <------ adresse à changer en fonction du placement de la bdd
    cursor = conn.cursor()
    name_etudiant = cursor.execute("SELECT name_etudiant FROM app_etudiant_table") ########### JE RECUPERE LA COLONNE DU NOM DES ETUDIANTS
    return render_template('TemplateEtudiant.html', name_etudiant_html=name_etudiant)
    conn.close()

    

############### PAGE DU PROFIL DES ETUDIANTS -  ON RECUPERE LES DONNEES DE LA BDD POUR LES AFFICHER EN HTML ################
@app.route('/etudiants/<name_etudiant>')
def profil(name_etudiant):
    conn = sqlite3.connect("C:\\Users\\HB1\\Desktop\\app_etudiant_python\\listing_etudiant.db") # <------ adresse à changer en fonction du placement de la bdd
    cursor = conn.cursor()
    profil_etudiant = cursor.execute("""SELECT * FROM app_etudiant_table WHERE name_etudiant=? """, (name_etudiant,))  ########### JE RECUPERE LES LIGNES OU LE NOM DE L'ETUDIANT CORRESPOND A MA VARIABLE "name_etudiant"
    profil_etudiant = profil_etudiant.fetchone() # JE GARDE QUE LA PREMIERE LIGNE
    ##### JE VAIS CHERCHER LE NOM DES COLONNES DANS MA BASE  #####
    attr_etudiant = cursor.execute("PRAGMA table_info(app_etudiant_table);")
    attr_etudiant.fetchone()
    ##### J'ENRICHIS MON TABLEAU K AVEC LE NOM DES COLONNES #####
    k=[]
    for row in attr_etudiant:
        k.append(row[1])
    return render_template('TemplateListEtudiant.html', name_etudiant_html=name_etudiant, profil_etudiant_html=profil_etudiant, attr_etudiant_html=attr_etudiant,k=k)
    conn.close()


############### "PAGE" OU LE SCRIPT "AJOUTER" S'EXECUTE ################    
@app.route('/postform/', methods=['POST'])
def data_form():
    name_etudiant = request.form['name_etudiant']
    tel_etudiant = request.form['tel_etudiant']
    cp_etudiant = request.form['cp_etudiant']
    ville_etudiant = request.form['ville_etudiant']
    universite_etudiant = request.form['universite_etudiant']
    conn = sqlite3.connect("C:\\Users\\HB1\\Desktop\\app_etudiant_python\\listing_etudiant.db") # <------ adresse à changer en fonction du placement de la bdd
    cursor = conn.cursor()
    t = cursor.execute("""INSERT INTO app_etudiant_table(id_etudiant, name_etudiant, tel_etudiant, cp_etudiant, ville_etudiant, universite_etudiant)VALUES("{}","{}","{}","{}","{}","{}")""".format(1, name_etudiant, tel_etudiant, cp_etudiant, ville_etudiant, universite_etudiant))
    conn.commit()
    conn.close()
    return redirect(url_for("liste"))


############### "PAGE" OU LE SCRIPT "DELETE" S'EXECUTE ################
@app.route('/etudiants/<name_etudiant>/delete_profil/', methods=['POST']) 
def del_form(name_etudiant):
    conn = sqlite3.connect("C:\\Users\\HB1\\Desktop\\app_etudiant_python\\listing_etudiant.db") # <------ adresse à changer en fonction du placement de la bdd
    cursor = conn.cursor()
    data_name_etudiant = request.form['data_name_etudiant']
    t = cursor.execute("""DELETE FROM app_etudiant_table WHERE name_etudiant=? """, (data_name_etudiant,))
    conn.commit()
    conn.close()
    return redirect(url_for("liste"))

############### "PAGE" OU LE SCRIPT "UDPATE" ou "DELETE" S'EXECUTE ################
@app.route('/etudiants/<name_etudiant>/modify/<operation>/', methods=['POST'])
def upd_form(name_etudiant, operation):
    conn = sqlite3.connect("C:\\Users\\HB1\\Desktop\\app_etudiant_python\\listing_etudiant.db") # <------ adresse à changer en fonction du placement de la bdd
    cursor = conn.cursor()
    r = request.form[operation]
    t = cursor.execute("""UPDATE app_etudiant_table SET {name_column2} = ? WHERE name_etudiant= ? """.format(name_column2 = operation), (r, name_etudiant,))
    conn.commit()
    conn.close()
    return redirect(url_for("profil", name_etudiant=name_etudiant))