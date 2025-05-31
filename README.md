# Laporan Proyek Machine Learning - Dewi Puspita

## 1. Project Overview
### 1.1. Latar Belakang

Pertumbuhan besar-besaran dalam jumlah konten digital, terutama film telah menciptakan kebutuhan akan sistem yang dapat menyaring dan menyajikan konten yang relevan secara efisien. Layanan seperti Netflix dan Amazon Prime menggunakan sistem rekomendasi untuk membantu pengguna menemukan konten yang sesuai dengan preferensi mereka (Ricci, Rokach, & Shapira, 2015). Sistem ini menjadi penting karena mampu mempersonalisasi pengalaman pengguna berdasarkan data dan perilaku sebelumnya.

Content-Based Filtering (CBF) merupakan salah satu pendekatan dalam sistem rekomendasi yang merekomendasikan item berdasarkan kemiripan atribut konten. Proyek ini mengimplementasikan CBF dengan memanfaatkan fitur `original_language` dari dataset film sebagai dasar untuk mengukur kemiripan antar film. Meskipun sederhana, pendekatan ini memperkenalkan dasar penting dalam membangun sistem rekomendasi secara bertahap (Aggarwal, 2016).

Sistem rekomendasi memiliki banyak manfaat strategis, mulai dari meningkatkan engagement pengguna melalui rekomendasi yang dipersonalisasi, mengurangi informasi berlebih (information overload), dan meningkatkan efisiensi penemuan konten yang relevan dan sesuai preferensi.

Proyek ini dibuat untuk memberikan fondasi untuk sistem yang lebih kompleks, misalnya penggabungan data sinopsis (overview), genre, atau rating pengguna (collaborative filtering). Selain itu, sistem rekomendasi terbukti mampu meningkatkan nilai bisnis digital dan retensi pengguna.

## 2. Business Understanding 
### 2.1. Problem Statement:
1. Pengguna layanan streaming sering mengalami kebingungan dan kebanjiran informasi (information overload) saat memilih film karena jumlah pilihan yang sangat besar dan tidak terstruktur.
2. Pengguna membutuhkan sistem yang mampu merekomendasikan film-film yang memiliki kemiripan tertentu dengan film yang mereka sukai atau pernah tonton, tanpa harus mencari manual satu per satu.

### 2.2. Goals
1. Menyediakan sistem rekomendasi film berbasis konten untuk membantu pengguna menyaring film yang relevan dari ribuan pilihan secara otomatis dan efisien.
2. Membangun sistem yang mampu memberikan Top-N rekoemndasi film berdasarkan kemiripan atribut konten (`original_language`), sebagai dasar awal sistem rekomendasi yang lebih luas.

### 2.3. Solution Approach
Untuk mencapai goals yang ditetapkan, pendekatan yang diambil adalah:
1. Content-Based Filtering
   
Sistem rekomendasi dibangun menggunakan pendekatan Content-Based Filtering (CBF), yang bekerja dengan cara menghitung kemiripan antar film berdasarkan fitur konten yang dimiliki. Dalam proyek ini, fitur yang digunakan adalah `original_language` sebagai representasi awal konten.

2. TF-IDF Vectorization

Kolom `original_language` diubah menjadi representasi numerik menggunakan teknik TF-IDF (Term Frequency-Inverse Document Frequency), yang memungkinkan sistem memahami kemiripan antar teks bahasa.

3. Cosine Similarity
   
Setelah data ditransformasikan, dihitung kemiripan antar film menggunakan cosine similarity untuk mengetahui seberapa mirip satu film dengan film lainnya.

4. Top-N Recommendation

Sistem akan mengambil 10 film teratas yang paling mirip dengan film input (kecuali dirinya sendiri), dan menyajikannya sebagai hasil rekomendasi akhir.

5. Evaluasi Awal

Model dievaluasi menggunakan metrik Precision@10 dan Average Cosine Similarity untuk menilai sejauh mana sistem memberikan rekomendasi yang relevan.

## 3. Data Understanding
Pada proyek ini, dataset yang digunakan berasal dari **Kaggle** dengan judul **Movie Recommendation Data**, yang dapat diunduh melalui tautan berikut:
https://www.kaggle.com/datasets/rohan4050/movie-recommendation-data

Dataset ini berisi informasi mengenai berbagai parameters dengan mengambil input judul film dan memberikan output rekomendasi film berdasarkan nilai kemiripan (bahasa).

### Tahapan Data Understanding

1. Data Loading

Langkah awal dilakukan dengan memuat dataset ke dalam lingkungan analsis menggunakan library Python seperti `pandas`. Proses ini bertujuan untuk melihat struktur awal data, memastikan dataset terbaca dengan benar, dan mengidentifikasi tipe data setiap kolom.

2. Deskripsi Variabel

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

Dari output, terlihat adanya 4 kolom numerik dengan tipe float64, yakni `revenue`, `runtime`, `vote_average`, dan `vote_count`, serta 20 kolom kategorikal bertipe object, yakni `adult`, `belongs_to_collection`, `budget`, `genres`, `homepage`, `id`, `imdb_id`, `original_language`, `original_title`, `overview`, `popularity`, `poster_path`, `production_companies`, `production_countries`, `release_date`, `spoken_languages`, `status`, `tagline`, `title`, `video`.

3. Missing Value dan Duplicate

- **Missing Value**: Hasil dari pengecekan menunjukkan bahwa terdapat beberapa kolom yang memiliki missing value, seperti `original_language` yang memiliki 11 missing value dan `title` yang memiliki 6 missing value.
- **Duplicate**: Dari pengecekan, didapat bahwa dataset memiliki total 13 entri duplikat.

4. Distribusi Judul dan Bahasa Unik

Dari data yang didapat terlihat bahwa adanya 45.436 data yang berbeda, 93 bahasa yang berbeda, dan 42.278 judul berbeda.

## 4. Data Preparation
