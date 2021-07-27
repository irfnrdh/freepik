# dibuat dari Ruèma bersama orang dalam 

import csv # bermain dengan csv hasil scrape
import requests # untuk mengakses gambar ke web
import shutil # untuk simpan di lokal

datax = [] 

# kita mulai baca filenya dulu
with open('freepik.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",") # rubah dilimiter sesuai dengan csv
    for row in csv_reader:
        datax.append(row)
labels = datax.pop(0)

for data in datax:
    # print(data[0]) # kolom pertama untuk nomor

    ## inisialisasi nama file dan url
    image_url = data[1] # kolom kedua untuk url
    filename = image_url.split("/")[-1]

    # saatnya memulai membuka dan stream untuk menjadi konten stream
    r = requests.get(image_url, stream = True)

    # cek jika file berhasil didapatkan
    if r.status_code == 200:

        ## buat decode_content value jadi True, jadi hasil besar download akan jadi kosong. otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        ## langsung menyimpan file dengan wb ( write binary ) permission.
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')