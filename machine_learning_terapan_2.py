# -*- coding: utf-8 -*-
"""Machine Learning Terapan 2

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NVQefGg9ZNpPVZGLzBCk273g1nafbhzG

#Sistem Rekomendasi Film berdasarkan Content-Based Filtering

## Latar Belakang

Sistem rekomendasi telah menjadi komponen penting dalam berbagai platform digital seperti e-commerce, layanan streaming, dan sosial media. Dalam konteks film, pengguna seringkali kesulitan menemukan film yang sesuai dengan preferensi mereka karena banyaknya pilihan yang tersedia. Untuk mengatasi masalah ini, diperlukan sistem yang mampu merekomendasikan film yang relevan.

Proyek ini bertujuan mengembangkan sistem rekomendasi film berbasis konten (Content-Based Filtering) yang dapat memberikan saran film serupa berdasarkan karakteristik tertentu—dalam hal ini, bahasa asli film. Sistem ini penting sebagai pondasi awal pengembangan sistem rekomendasi yang lebih kompleks seperti yang digunakan Netflix, Hulu, dan layanan streaming lainnya.

# Business Understanding
## Problem Statement

Pengguna ingin mendapatkan rekomendasi film yang serupa dengan film yang telah ditonton atau disukai, namun tidak selalu tahu cara menemukannya. Tanpa sistem rekomendasi, pengguna dapat merasa kewalahan oleh banyaknya pilihan.

## Goals

Membangun sistem rekomendasi berbasis konten yang mampu:

- Memberikan rekomendasi film serupa berdasarkan karakteristik tertentu (dalam proyek ini: bahasa film).

- Menyediakan 10 film rekomendasi teratas (Top-N).

- Menyediakan dua pendekatan algoritmik yang berbeda untuk membandingkan hasil.

# Import Library
"""

!pip install -q kaggle

# Commented out IPython magic to ensure Python compatibility.
# Import Data Loading
from google.colab import files
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# %matplotlib inline
import seaborn as sns
import zipfile
import warnings
warnings.filterwarnings('ignore')

# Import TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer

# Import Model Development
from sklearn.metrics.pairwise import cosine_similarity

"""# 1. Data Understanding

## 1.1. Data Loading

Supaya isi dataset lebih mudah dipahami, kita perlu melakukan proses loading data terlebih dahulu. Tidak lupa, import library pandas untuk dapat membaca file datanya.
"""

files.upload() # Upload kaggle json

!mkdir ~/.kaggle # membuat folder .kaggle
!cp kaggle.json ~/.kaggle/ # menyalin file credential ke lokasi yang sesuai
!chmod 600 ~/.kaggle/kaggle.json # mengatur izin file agar bisa digunakan oleh kernel Colab
!kaggle datasets download -d rohan4050/movie-recommendation-data # mengunduh dataset dari Kaggle

# mengekstrak file ZIP dataset
zip_ref = zipfile.ZipFile('/content/movie-recommendation-data.zip', 'r')
zip_ref.extractall('/content')
zip_ref.close()

# load the dataset
movie = pd.read_csv('/content/movies_metadata.csv')
movie

"""Output di atas memberikan informasi sebagai berikut:
- Ada 45.466 baris data.
- Ada 24 kolom, yaitu `adult`, `belongs_to_collection`, `budget`, `genres`, `homepage`, `id`, `imdb_id`, `original_language`, `original_title`, `overview`, `popularity`, `poster_path`, `production_companies`, `production_countries`, `release_date`, `revenue`, `runtime`, `spoken_languages`, `status`, `tagline`, `title`, `video`, `vote_average`, `vote_count`.

## 1.2. Deskripsi Variabel
Berdasarkan informasi dari Kaggle, variabel-variabel pada dataset adalah berikut:

|Column |Description |
|---------------|--------------------------|
|adult |Apakah film tersebut untuk dewasa (konten eksplisit). Nilai: True atau False. |
|belongs_to_collection |Informasi tentang koleksi film jika film tersebut bagian dari suatu seri atau franchise. |
|budget |Anggaran biaya produksi film (dalam satuan mata uang dolar AS). |
|genres |Daftar genre film dalam format JSON string (misalnya: Action, Comedy, Drama, dll). |
|homepage |URL resmi halaman web film (jika ada). |
|id |ID unik dari film tersebut. |
|imdb_id |ID film di situs IMDb (Internet Movie Database). |
|original_language |Bahasa asli saat film tersebut diproduksi (kode bahasa ISO seperti 'en', 'fr', 'ja'). |
|original_title |Judul asli dari film sesuai dengan versi produksinya. |
|overview |Ringkasan atau sinopsis pendek mengenai cerita film. |
|popularity |Skor popularitas film berdasarkan sistem internal TMDb (semakin tinggi, semakin populer). |
|poster_path |Path (lokasi relatif) dari gambar poster film pada server TMDb. |
|production_companies |	Daftar perusahaan produksi yang memproduksi film (format JSON). |
|production_countries |Daftar negara tempat film tersebut diproduksi (format JSON). |
|release_date |Tanggal rilis resmi film (format: YYYY-MM-DD). |
|revenue |Pendapatan kotor dari film di seluruh dunia (dalam dolar AS). |
|runtime |Durasi tayang film dalam satuan menit. |
|spoken_languages |Daftar bahasa yang digunakan dalam dialog film (format JSON). |
|status |Status rilis film (contoh: Released, Post Production, Rumored). |
|tagline |Slogan atau kutipan promosi film yang biasanya muncul di poster. |
|title |Judul film versi internasional yang umum digunakan. |
|video |Menunjukkan apakah data video tersedia (True atau False). |
|vote_average |Rata-rata skor rating film berdasarkan penilaian pengguna TMDb (skala 0–10). |
|vote_count |Jumlah total pengguna yang memberikan rating untuk film tersebut. |

Setelah memahami deskripsi variabel pada data, langkah selanjutnya adalah mengecek informasi pada dataset dengan fungsi `info()` berikut.
"""

movie.info() # cari tau keterangan dan tipe dari tiap kolom data

"""Dari output terlihat bahwa, data yang diambil memiliki:
- 4 kolom numerik dengan tipe float64, yakni `revenue`, `runtime`, `vote_average`, dan `vote_count`.
- 20 kolom kategorikal bertipe object, yakni `adult`, `belongs_to_collection`, `budget`, `genres`, `homepage`, `id`, `imdb_id`, `original_language`, `original_title`, `overview`, `popularity`, `poster_path`, `production_companies`, `production_countries`, `release_date`, `spoken_languages`, `status`, `tagline`, `title`, `video`.

## 1.3. EDA - Missing Value dan Duplicate
"""

movie.isnull().sum() # cek jumlah missing value

"""Dari hasil, terlihat bahwa terdapat beberapa kolom yang memiliki missing value, seperti `original_language` yang memiliki 11 missing value dan `title` yang memiliki 6 missing value."""

movie.duplicated().sum() # cek jumlah data duplikat

"""Dari hasil, terlihat bahwa terdapat 13 baris data yang duplikat."""

# melihat ada berapa banyak entri yang unik berdasarkan id
print('Banyak data: ', len(movie.id.unique()))

# melihat ada berapa banyak koleksi unik berdasarkan bahasa
print('Banyak bahasa: ', len(movie.original_language.unique()))
print('Jenis bahasa: ', movie.original_language.unique())

# melihat ada berapa banyak judul unik berdasarkan genres
print('Banyak judul: ', len(movie.title.unique()))

"""Dari data, terlihat bahwa data yang kita ambil memiliki jumlah 45.436 data yang berbeda dengan total 93 bahasa dan 42.278 judul yang berbeda.

# 2. Data Preparation
Pada tahap ini, kita akan mengambil kolom-kolom yang akan digunakan saja dan mempersiapkan data agar siap untuk dipakai permodelan.

## 2.1. Pengambilan Sampling 10.000 Data Acak

Karena dataset asli berisi sekitar 45.000 entri yang tergolong cukup besar untuk proses eksplorasi awal dan eksperimen. Maka dilakukan sampling acak sebanyak 10.000 baris data menggunakan sample (n=10.000, random_sate=42) agar proses komputasi berjalan lebih cepat dan efisien serta hasilnya tetap representatif karena diambil secara acak.

Hal ini dilakukan untuk mengurangi beban memori dan waktu komputasi di Google Colab, tetap mempertahankan keberagaman data dengan pengambilan acak, dan pengujian model awal sebelum mengembangkan ke full dataset.
"""

movie_new = movie.sample(n=10000, random_state=42)  # random_state agar hasilnya konsisten

"""## 2.2. Hanya Ambil Kolom yang Dipakai

Kolom-kolom seperti `budget`, `homepage`, `status`, dan sebagainya tidak digunakan karena fokus kita adalah untuk melakukan rekomendasi berdasarkan bahasa.

Sehingga, kolom yang dipertahankan hanyalah:
- `id` sebagai identifikasi film
- `title` sebagai index dan tampilan
- `original_language` sebagai fitur utama dalam model

Dengan menerapkan ini, kita bisa fokus hanya pada fitur relevan, menyederhanakan preprocessing dan vektorisasi, dan menghindari noise dari data yang tidak terstruktur atau tidak digunakan.
"""

movie_clean = pd.DataFrame({
    'id': movie_new['id'],
    'title': movie_new['title'],
    'language': movie_new['original_language']
})
movie_clean

"""## 2.3. Handling Missing Value dan Duplikasi

Setelah kolom data difilter, dilakukan penggecekan dan pembersihan terhadap missing values karena baris dengan `Nan` pada kolom tidak bisa digunakan untuk TF-IDF.
"""

movie_clean = movie_clean.dropna()
movie_clean.isna().sum()

"""Setelah kolom Nan dibersihkan, sekarang dilakukan penanganan duplikat agar satu film tidak muncul lebih dari sekali dan mennggangu hasil kemiripan."""

movie_clean = movie_clean.drop_duplicates()
movie_clean.shape

"""Setelah kolom duplikat juga dihapus, data tersisa adalah 9.997 entri dan 3 kolom.

# 2.4. TF_IDF Vectorizer

`original_language` berisi kode bahasa film. Meskipun sederhana, kita perlakukan kolom ini sebagai representasi konten dan vektorisasi dilakukan menggunakan TF-IDF di mana TF (Term Frequency) berarti seberapa sering kata muncul, dan IDF (inverse Document Frequency) berarti seberapa unik kata tersebut dibandingkan dokumen lain.

Pertama, objek TF-IDF Vectorizer diinisiasi terlebih dahulu. Lalu model dilatih pada data `language` dan ditampilkan daftar kata unik yang digunakan sebagai fitur.
"""

# Inisialisasi TfidfVectorizer
tf = TfidfVectorizer()

# Melakukan perhitungan idf pada data language
tf.fit(movie_clean['language'])

# Mapping array dari fitur index integer ke fitur nama
tf.get_feature_names_out()

"""Selanjutnya, kita mengubah teks menjadi matriks vektor supaya dapat melatih dan langsung mentransformasikan data ke bentuk matriks TF-IDP. `shape` digunakan untuk melihat dimensi matriks TF-IDF, di mana terlihat adanya 9.997 film dengan 64 jenis bahasa unik."""

# Melakukan fit lalu ditransformasikan ke bentuk matrix
tfidf_matrix = tf.fit_transform(movie_clean['language'])

# Melihat ukuran matrix tfidf
tfidf_matrix.shape

"""Lalu, matriks TF-IDF diubah ke bentuk dense (penuh)."""

tfidf_matrix.todense()

"""Terakhir, DataFrame dari TF-IDF dibuat dan ditampilkan 10 baris film dan 22 kolom bahasa secara acak untuk melihat bagaimana bobot TF-IDF dibentuk per bahasa dan per film."""

pd.DataFrame(
    tfidf_matrix.todense(),
    columns=tf.get_feature_names_out(),
    index=movie_clean.title
).sample(22, axis=1).sample(10, axis=0)

"""# 3. Model Development dengan Content Based Filtering

Model Development adalah tahapan di mana kita menggunakan algoritma machine learning untuk menjawab problem statement dari tahap business understanding.

Pada tahap ini, kita akan membangun sistem rekomendasi berbasis konten untuk menyarankan film yang mirip berdasarkan karakteristik tertentu (dalam hal ini: `original_language`) dan menyajikan rekomendasi Top 10 (Top-N Recommendation).

## 3.1. Membuat Matriks Kemiripan

Pertama, data akan membuat matriks kemiripan dimana fungsi akan menghitung cosine similarity antar vektor TF-IDF dari fitur `original_language`, menghasilkan skor kemiripan antara 0 (tidak mirip) sampai 1 (identik).
"""

cosine_sim = cosine_similarity(tfidf_matrix) # hitung cosine similarity antar vektor TF-IDF
cosine_sim

"""## 3.2. Membuat DataFrame dari Matriks Kemiripan

Matriks `cosine_sim` diubah menjadi DataFrame agar mudah diakses berdasarkan `title`.
"""

# Membuat dataframe dari variabel cosine_sim dengan baris dan kolom berupa nama judul
cosine_sim_df = pd.DataFrame(cosine_sim, index=movie_clean['title'], columns=movie_clean['title'])
print('Shape:', cosine_sim_df.shape)

# Melihat similarity matrix pada setiap judul
cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

"""## 3.3. Membuat Fungsi Rekomendasi

Pada tahap ini, dibuat fungsi `recommend_movies` yang berfungsi untuk mengambil skor kemiripan dari film input ke semua film lain, mengurutkan skor, menghapus dirinya sendiri dari daftar, dan mengembalikan **Top-10 film paling mirip** berdasarkan fitur `original_language`.
"""

def recommend_movies(title, cosine_sim=cosine_sim_df):
    # Ambil skor similarity dari judul yang diminta
    sim_scores = list(cosine_sim_df[title].items())

    # Urutkan berdasarkan skor tertinggi, kecuali dirinya sendiri
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Ambil 10 film teratas selain dirinya sendiri
    sim_scores = [item for item in sim_scores if item[0] != title]
    top_titles = [item[0] for item in sim_scores[:10]]

    # Ambil info dari movie_clean berdasarkan judul
    return movie_clean[movie_clean['title'].isin(top_titles)][['id', 'title', 'language']]

"""## 3.4. Contoh Output Rekomendasi

Di tahap ini, hasil rekomendasi berdasarkan input judul film akan ditampilkan.
"""

recommend_movies("Elephant")

"""Dari hasil rekomendasi, terlihat bahwa **Top-N Recommendation** berhasil disajikan.

# 4. Evaluasi

Tahapan evaluasi dilakukan untuk menilai performa sistem rekomendasi menggunakan metrik evaluasi **Precision@10** dan hasilnya.

## 4.1. Precision@10
"""

def precision_at_k(recommended_titles, true_language, k=10):
    # Ambil hanya k item
    top_k = recommended_titles[:k]

    # Ambil subset dari movie_clean berdasarkan judul
    relevant = movie_clean[movie_clean['title'].isin(top_k)]

    # Hitung jumlah film yang bahasanya sama dengan input
    relevant_count = (relevant['language'] == true_language).sum()

    # Bagi dengan k, bukan panjang asli dari daftar
    return (relevant_count -1)/ k # dikurangi 1 karena biasanya input film ikut direkomendasikan

"""Pada metrik ini, relevansi didefinisikan sebagai film yang memiliki bahasa sama dengan film input dengan nilai ideal Precision@10 = 1.0 (semua rekomendasi relevan).

## 4.2. Average Cosine Similarity
"""

def average_cosine_similarity(input_title, k=10):
    sim_scores = cosine_sim_df[input_title].sort_values(ascending=False)
    sim_scores = sim_scores.drop(index=input_title)
    return sim_scores.head(k).mean()

"""Metrik ini menghitung skor rata-rata cosine similarity dari Top-k rekomendasi terhadap film input. Skor mendekati 1 menunjukkan bahwa kemiripan yang tinggi.

## 4.3. Menjalankan Evaluasi
"""

# Uji presisi
input_title = "Elephant"
recommended_df = recommend_movies(input_title)
recommended_titles = recommended_df['title'].tolist()
true_language = movie_clean[movie_clean['title'] == input_title]['language'].values[0]

print("Precision@10:", precision_at_k(recommended_titles, true_language))
print("Rata-rata Cosine Similarity terhadap rekomendasi:", average_cosine_similarity("Elephant"))

"""Dari hasil yang didapat terlihat bahwa semua film rekomendasi memiliki bahasa yang sama, yang berarti sistem memberikan rekomendasi yang sangat mirip dari sisi `original_language`.

Karena hanya menggunakan satu fitur sederhana (bahasa), kemiripan menjadi maksimal tapi kurang kaya dalam makna konten.
"""