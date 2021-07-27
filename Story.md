Cara saya cari inspirasi desain [kasus pertama]

Saya ingin membuat desain kartu nama. Jika kita hanya membuat satu buah mungkin kita bisa membuatnya dengan ide yang kita miliki dan sedikit eksperiment yang memakan waktu. Tapi jika kita ingin membuat seribu buah dengan kondisi tertentu seperti mengikuti trend maka kita wajib melihat trend yang ada untuk bisa meng-generate seribu buah dalam deadline waktu tertentu.

Jumlah yang banyak waktu yang sedikit membuat saya berfikir kenapa saya tidak membuat robot untuk menemukan ide tersebut.

Dari situ saya mulai mempelajari alur kerja situs yang nantinya akan menjadi tujuan. Situs itu adalah freepik dan saya coba mempelajari layouting webnya dan jenis data fetching yang digunakannya. Saya sudah mengenal freepik sejak smk kelas 2 atau di tahun 2012 lalu dan mereka masih menggunakan codeigniter.

Okeh, saya mulai dengan mencari ide tersebut di kotak pencarian dan sedikit bumbu di filternya untuk mendapatkan yang saya inginkan.

dari situlah awalnya saya mulai menyimpan satu persatu gambar yang menurut saya bisa saya perbaiki dan melakukan mixxing dengan ide yang saya miliki. setelah setengah perjalanan saya mulai menyadari kenapa saya tidak buatkan robot untuk mempermudah kerjaan yang memakan waktu ini. 

kemudian saya mulailah mencari inspirasi teknologi yang bisa saya gunakan, akhirnya saya memilih typescript dengan cheerio dan ternyata saya tidak menemukan solusi permasalahan dapat penggunaannya dan menemukan kembali puppeteer. setelah saya mencoba puppeteer dan cheerio saya merasa kurang greget dan memakan waktu kembali untuk mendalaminya walaupun kodenya sudah jalan di contoh yang bukan situs yang menjadi tujuan.

klik demi klik akhirnya menemukan https://www.webscraper.io/ dan saya coba gunakan ternyata saya pernah menggunakan sebelumnya di kasus yang lain namun akhirnya saya belajar ulang kembali untuk menaklukkannya setelah beberapa ulang kaji yang memakan waktu sejam lebih akhirnya saya mendapatkan file csv dengan berisikan file inspirasi yang saya inginkan.

untuk kasus pertama ini saya mendapatkan 1774 gambar dan itu semua belum dalam pilahan gambar-gambar inspirasi yang saya inginkan. Kasus selanjutnya adalah saya harus mendownload semua gambar tersebut dan ternyata di situs webscraper itu udah ada sebuah Image downloader script yang dibuat dengan python tapi sayangnya tidak ada format yang jelas untuk file csvnya dan tidak berhasil digunakan. Akhirnya dari permasalahan itu saya mulai ngoding ulang untuk membuat Image downloader script dengan versi saya sendiri dan akhirnya berhasil.

Sialnya setelah sejam lebih saya ngulik dari gunain wget, requests dan kawan-kawannya saya mulai kepikiran kenapa saya tidak gunakan IDM aja untuk download semua gambarnya padahal linknya sudah saya data cleankan dan tinggal URL yang sudah sangat clean untuk didownload.

buka "IDM > Task > Add batch download from clipboard" adalah cara sial yang lebih cepat dari pada koding yang sudah saya buat. 

tapi dari kejadian mencari inspirasi ini setidaknya saya bisa belajar 
1. Menemukan selektor yang tepat untuk scrape
2. Lebih ngulang lagi perkara regular expression
3. Typescript itu keren tapi sayang materi di komunitasnya kadang bercampur dengan javascript yang kadang bikin bingung
4. Jadi lebih belajar python lagi
5. Ternyata yang saya pikir bisa lebih cepat malah itu cara yang lambat

berikut selektor di freepik 
```
untuk kontainer gambar  -> div.bg
untuk gambar (global)	-> .showcase__link img.loaded
untuk gambar bisa juga  -> .showcase__link > img
untuk judul 		    -> p.title
untuk nama kontributor  -> span.name
untuk avatar kontributor-> .avatar img.loaded
untuk statistik download-> i.badge--download
untuk statistik suka    -> i.badge--favorite
```

ini hasil export sitemapnya dengan webscraper.io

```
{"_id":"freepik","startUrl":["https://www.freepik.com/search?dates=any&format=search&page=[1-200]&query=business+card&sort=popular"],"selectors":[{"id":"gambar","type":"SelectorImage","parentSelectors":["_root"],"selector":".showcase__link > img","multiple":true,"delay":0},{"id":"judul","type":"SelectorText","parentSelectors":["_root"],"selector":"p.title","multiple":true,"regex":"","delay":0},{"id":"download","type":"SelectorText","parentSelectors":["_root"],"selector":"i.badge--download","multiple":true,"regex":"","delay":0},{"id":"favorite","type":"SelectorText","parentSelectors":["_root"],"selector":"i.badge--favorite","multiple":true,"regex":"","delay":0},{"id":"author","type":"SelectorText","parentSelectors":["_root"],"selector":"span.name","multiple":true,"regex":"","delay":0}]}
```

mainkan di urlnya untuk dapatkan inspirasi yang kamu mau pada "&query=kata+kunci" dan sesuaikan halamannya dengan yang ada

jika sudah langsung di scrape aja dan export ke csv. Tidak sepenuhnya oke sih perlu data cleaning lagi setidaknya untuk menghapus gambar yang sebenarnya tidak penting.
saya gunakan notepad++ dengan cara di menu search > mark > masukkan link yang benar "https://img.freepik.com" lalu klik bookmark line dan mark all
setelah itu balik ke menu search > bookmark > Remove Unmarked Lines

Tidak sampai disitu aja sih saya ingin url lebih clean jadi saya gunakan regex untuk menghapus semua yang gak penting setelah ".jpg" dengan regex "\?.*$"

setelah itu barulah download gambar dengan python

```
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

```

jadi topik ini sebenarnya bisa dikatakan "how to scrape inspiration from freepik" tapi begitulah cara saya mendapatkan inspirasi sebagai bahan moodboard untuk mendesain sesuatu yang menjadi tujuan saya.

Semoga membuat anda bingung, jika ada unek2 mengenai ini silahkan japri aja.

 