from lib2to3.fixes.fix_metaclass import remove_trailing_newline
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from werkzeug.utils import secure_filename
from flask import flash  # Flash mesajları ekleyin


app = Flask(__name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Yüklenen fotoğrafların kaydedileceği klasör

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def kullanici_var_mi(isim, soyisim):
    with open('veriler.json', 'r') as file:
        veriler = json.load(file)
        for kullanici in veriler:
            if kullanici["isim"] == isim and kullanici["soyisim"] == soyisim:
                return True
    return False

#SAYFA ROTE DENEME
@app.route('/deneme')
def deneme():
    return render_template("deneme.html")

#SAYFA ROTE 404
@app.route('/hata')
def hata():
    return render_template("hata.html")

# MAIN PAGE AND ADD USERS
@app.route('/', methods=['GET', 'POST'])
def ana_sayfa():
    mesaj = ""

    if request.method == 'POST':
        isim = request.form['isim']
        soyisim = request.form['soyisim']

        if kullanici_var_mi(isim, soyisim):
            mesaj = "Bu kullanıcı zaten kayıtlı. Tekrar kayıt yapılamaz."
        else:
            with open('veriler.json', 'r') as file:
                veriler = json.load(file)
                if veriler:
                    son_id = max([kullanici["id"] for kullanici in veriler])
                    otomatik_id = son_id + 1
                else:
                    otomatik_id = 1

            yas = request.form['yas']
            boy = request.form['boy']

            # Yeni veri oluşturulurken fotoğraf işlemi
            # Yeni veri oluşturulurken fotoğraf işlemi
            photo_path = ''  # Varsayılan olarak boş bırakın

        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '' and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                # Dosya adını JSON verilerine eklemek için kullanabilirsiniz
                yeni_veri = {
                    "id": otomatik_id,
                    "isim": isim.capitalize(),
                    "soyisim": soyisim.capitalize(),
                    "yas": yas,
                    "boy": boy,
                    "user_photo": filename,  # Sadece dosya adını kaydedin
                    "years": {
                        "2025": {
                            "trainings": {}
                        }
                    }
                }
                # Fotoğrafı yükleyin
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                photo.save(photo_path)
            else:
                mesaj = "Lütfen geçerli bir fotoğraf dosyası seçin."

            veriler.append(yeni_veri)

            with open('veriler.json', 'w') as file:
                json.dump(veriler, file, indent=4)

            mesaj = "Yeni veri başarıyla eklendi."

    try:
        with open('veriler.json', 'r') as file:
            veriler = json.load(file)
    except Exception as e:
        veriler = []

    return render_template('index.html', mesaj=mesaj, veriler=veriler)

############################################

#ADD SPORCU

@app.route('/add_sporcu', methods=['GET', 'POST'])
def add_sporcu():
    mesaj = ""

    if request.method == 'POST':
        isim = request.form['isim']
        soyisim = request.form['soyisim']

        if kullanici_var_mi(isim, soyisim):
            mesaj = "Bu kullanıcı zaten kayıtlı. Tekrar kayıt yapılamaz."
        else:
            with open('veriler.json', 'r') as file:
                veriler = json.load(file)
                if veriler:
                    son_id = max([kullanici["id"] for kullanici in veriler])
                    otomatik_id = son_id + 1
                else:
                    otomatik_id = 1

            yas = request.form['yas']
            boy = request.form['boy']

            # Yeni veri oluşturulurken fotoğraf işlemi
            # Yeni veri oluşturulurken fotoğraf işlemi
            photo_path = ''  # Varsayılan olarak boş bırakın

        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '' and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                # Dosya adını JSON verilerine eklemek için kullanabilirsiniz
                yeni_veri = {
                    "id": otomatik_id,
                    "isim": isim.capitalize(),
                    "soyisim": soyisim.capitalize(),
                    "yas": yas,
                    "boy": boy,
                    "user_photo": filename,  # Sadece dosya adını kaydedin
                    "years": {
                        "2025": {
                            "trainings": {}
                        }
                    }
                }
                # Fotoğrafı yükleyin
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                photo.save(photo_path)
            else:
                mesaj = "Lütfen geçerli bir fotoğraf dosyası seçin."

            veriler.append(yeni_veri)

            with open('veriler.json', 'w') as file:
                json.dump(veriler, file, indent=4)

            mesaj = "Yeni sporcu başarıyla eklendi."

    try:
        with open('veriler.json', 'r') as file:
            veriler = json.load(file)
    except Exception as e:
        veriler = []

    return render_template('add_sporcu.html', mesaj=mesaj, veriler=veriler)



# SINGLE USER
@app.route('/user/<int:user_id>')
def single_user(user_id):
    with open('veriler.json', 'r') as file:
        veriler = json.load(file)
        for kullanici in veriler:
            if kullanici["id"] == user_id:
                user = kullanici
                break
        else:
            print("bulunamadi")

    return render_template('single_user.html', user=user)

def get_user_data_from_file():
    try:
        with open('veriler.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_user_data_to_file(data):
    with open('veriler.json', 'w') as file:
        json.dump(data, file, indent=4)



###############################################



#### EDIT USER
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # Kullanıcıyı veritabanından veya başka bir kaynaktan bulun
    # user_id parametresini kullanarak gerekli kullanıcıyı alın
    # Örneğin, kullanıcıyı veriler.json dosyasından alabilirsiniz
    with open('veriler.json', 'r') as file:
        veriler = json.load(file)
        for kullanici in veriler:
            if kullanici["id"] == user_id:
                user = kullanici
                break
        else:
            # Kullanıcı bulunamadıysa, isteği reddedin veya bir hata sayfasına yönlendirin
            print("Kullanıcı bulunamadı.")

    if request.method == 'POST':
        # Kullanıcının yaptığı değişiklikleri alın
        yeni_isim = request.form['isim']
        yeni_soyisim = request.form['soyisim']
        yeni_yas = request.form['yas']

        # Kullanıcının verilerini güncelleyin
        user['isim'] = yeni_isim
        user['soyisim'] = yeni_soyisim
        user['yas'] = yeni_yas

        # Fotoğrafı yükleyin
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                # Fotoğraf dosyasının adını güncelleyin
                filename = secure_filename(photo.filename)
                user['user_photo'] = filename

                # Fotoğrafı yükleyin ve kaydedin
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                photo.save(photo_path)

        # Güncellenmiş verileri JSON dosyasına yazın
        with open('veriler.json', 'w') as file:
            json.dump(veriler, file, indent=4)

        # Kullanıcıyı ayrıntı sayfasına yönlendirin
        return redirect(url_for('single_user', user_id=user_id))

    return render_template('edit_user.html', user=user)

###############################################


# FITNESS ANTRENMAN EKLE
@app.route('/fitness_antrenman_ekle', methods=['POST', 'GET'])
def fitness_antrenman_ekle():
    kullaniciVerileri = get_user_data_from_file()  # Kullanıcı verilerini al

    if request.method == 'POST':
        # Seçilen kullanıcıların ID'lerini bir liste olarak alın
        selected_user_ids = request.form.getlist('user_id[]')
        tarih = request.form['tarih']
        sure = request.form['sure']

        # Kullanıcıları veri dosyasından alın
        with open('veriler.json', 'r') as file:
            veriler = json.load(file)

        for user_id in selected_user_ids:
            user_id = int(user_id)
            
            # Kullanıcıyı bulun
            user = None
            for kullanici in veriler:
                if kullanici["id"] == user_id:
                    user = kullanici
                    # "fitness" antrenmanını ekleyin
                    if "trainings" not in user["years"]["2025"]:
                        user["years"]["2025"]["trainings"] = {}
                    if "fitness" not in user["years"]["2025"]["trainings"]:
                        user["years"]["2025"]["trainings"]["fitness"] = []

                    user["years"]["2025"]["trainings"]["fitness"].append({"tarih": tarih, "sure": sure})

            # Verileri JSON dosyasına kaydedin
        
        # Tüm işlem bittiğinde mesajı oluşturun
        mesaj = "Yeni veri başarıyla eklendi."
        
        # Verileri JSON dosyasına kaydedin (döngünün dışında)
        with open('veriler.json', 'w') as file:
            json.dump(veriler, file, indent=4)

        return render_template('fitness_antrenman_ekle.html', mesaj=mesaj, kullaniciVerileri=kullaniciVerileri)

    # Verileri veriler.json dosyasından alın
    with open('veriler.json', 'r') as file:
        veriler = json.load(file)

    return render_template('fitness_antrenman_ekle.html', kullaniciVerileri=kullaniciVerileri)

# FITNESS ANTRENMAN SIL FONKSIYONU
def remove_fitness_training(user_id, tarih, sure):
    try:
        with open('veriler.json', 'r') as file:
            veriler = json.load(file)
        
        for kullanici in veriler:
            if kullanici["id"] == user_id:
                if "trainings" in kullanici["years"]["2025"] and "fitness" in kullanici["years"]["2025"]["trainings"]:
                    for training in kullanici["years"]["2025"]["trainings"]["fitness"]:
                        if training["tarih"] == tarih and training["sure"] == sure:
                            kullanici["years"]["2025"]["trainings"]["fitness"].remove(training)
                            break

        with open('veriler.json', 'w') as file:
            json.dump(veriler, file, indent=4)
            return True
    except Exception as e:
        print("Hata:", e)
        return False

# FITNESS ANTRENMAN SIL FONKSIYONU DEVAMI
@app.route('/sil_training', methods=['POST'])
def sil_fitness_training():
    if request.method == 'POST':
        # Silinecek verinin bilgilerini alın
        user_id = int(request.form['user_id'])
        tarih = request.form['tarih']
        sure = request.form['sure']

        # Verileri JSON dosyasından kaldırın
        if remove_fitness_training(user_id, tarih, sure):
            return jsonify({'message': 'Veri başarıyla silindi.'}), 200
        else:
            return jsonify({'message': 'Veri silinirken bir hata oluştu.'}), 500



###############################################


# SAILING ANTRENMAN EKLE
@app.route('/sailing_antrenman_ekle', methods=['POST', 'GET'])
def sailing_antrenman_ekle():
    kullaniciVerileri = get_user_data_from_file()  # Kullanıcı verilerini al

    if request.method == 'POST':
        # Seçilen kullanıcıların ID'lerini bir liste olarak alın
        selected_user_ids = request.form.getlist('user_id[]')
        tarih = request.form['tarih']
        sure = request.form['sure']

        # Kullanıcıları veri dosyasından alın
        with open('veriler.json', 'r') as file:
            veriler = json.load(file)

        for user_id in selected_user_ids:
            user_id = int(user_id)
            
            # Kullanıcıyı bulun
            user = None
            for kullanici in veriler:
                if kullanici["id"] == user_id:
                    user = kullanici
                    # "fitness" antrenmanını ekleyin
                    if "trainings" not in user["years"]["2025"]:
                        user["years"]["2025"]["trainings"] = {}
                    if "sailing" not in user["years"]["2025"]["trainings"]:
                        user["years"]["2025"]["trainings"]["sailing"] = []

                    user["years"]["2025"]["trainings"]["sailing"].append({"tarih": tarih, "sure": sure})

            # Verileri JSON dosyasına kaydedin
        
        # Tüm işlem bittiğinde mesajı oluşturun
        mesaj = "Yeni veri başarıyla eklendi."
        
        # Verileri JSON dosyasına kaydedin (döngünün dışında)
        with open('veriler.json', 'w') as file:
            json.dump(veriler, file, indent=4)

        return render_template('sailing_antrenman_ekle.html', mesaj=mesaj, kullaniciVerileri=kullaniciVerileri)

    # Verileri veriler.json dosyasından alın
    with open('veriler.json', 'r') as file:
        veriler = json.load(file)

    return render_template('sailing_antrenman_ekle.html', kullaniciVerileri=kullaniciVerileri)

#SAILING ANTRENMAN SIL
def remove_sailing_training(user_id, tarih, sure):
    try:
        with open('veriler.json', 'r') as file:
            veriler = json.load(file)
        
        for kullanici in veriler:
            if kullanici["id"] == user_id:
                if "trainings" in kullanici["years"]["2025"] and "sailing" in kullanici["years"]["2025"]["trainings"]:
                    for training in kullanici["years"]["2025"]["trainings"]["sailing"]:
                        if training["tarih"] == tarih and training["sure"] == sure:
                            kullanici["years"]["2025"]["trainings"]["sailing"].remove(training)
                            break

        with open('veriler.json', 'w') as file:
            json.dump(veriler, file, indent=4)
            return True
    except Exception as e:
        print("Hata:", e)
        return False

# SAILING ANTRENMAN SIL FONKSIYONU DEVAMI
@app.route('/sil_sailing', methods=['POST'])
def sil_sailing_training():
    if request.method == 'POST':
        # Silinecek verinin bilgilerini alın
        user_id = int(request.form['user_id'])
        tarih = request.form['tarih']
        sure = request.form['sure']

        # Verileri JSON dosyasından kaldırın
        if remove_sailing_training(user_id, tarih, sure):
            return jsonify({'message': 'Veri başarıyla silindi.'}), 200
        else:
            return jsonify({'message': 'Veri silinirken bir hata oluştu.'}), 500


###############################################



# KULLANICIYI SİL
@app.route('/delete_user/<int:user_id>', methods=['GET'])
def sil_user(user_id):
    if request.method == 'GET':
        # Verileri JSON dosyasından kaldırın
        if remove_user(user_id):
            return jsonify({'message': 'Kullanıcı başarıyla silindi.'}), 200
        else:
            return jsonify({'message': 'Kullanıcı silinirken bir hata oluştu.'}), 500

# KULLANICIYI SİL
def remove_user(user_id):
    try:
        with open('veriler.json', 'r') as file:
            veriler = json.load(file)

        kullanici_index = None
        for i, kullanici in enumerate(veriler):
            if kullanici["id"] == user_id:
                kullanici_index = i
                break

        if kullanici_index is not None:
            veriler.pop(kullanici_index)

        with open('veriler.json', 'w') as file:
            json.dump(veriler, file, indent=4)
            return True
    except Exception as e:
        print("Hata:", e)
        return False

if __name__ == '__main__':
    app.run(debug=True)
