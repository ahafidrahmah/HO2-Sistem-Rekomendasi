# Proyek Sistem Rekomendasi Course Berdasarkan Pekerjaan

Sistem ini bertujuan untuk merekomendasikan kursus online yang relevan untuk suatu lowongan pekerjaan. Pendekatan yang digunakan adalah dengan memproses teks deskripsi pekerjaan dan teks dari kursus, lalu mengukur kemiripan antara keduanya menggunakan vektorisasi berbasis model *Sentence Transformers*.

---

### 🔧 Bagaimana Set-Up

1. Clone repositori atau salin file proyek.
2. Aktifkan virtual environment (opsional tapi disarankan).
3. Install dependensi:
   ```bash
   pip install -r requirements.txt
    ```
4. Jalankan program utama:
   ```bash
   python main.py
    ```
## 1. Tentang Data 📊
- 💼 **Jobstreet**
  Dataset berasal dari scraping situs Jobstreet.
  
  Kolom yang digunakan adalah:
  
  `job_title` : nama posisi pekerjaan
  
  `category` : kategori pekerjaan
  
  `job_details` : deskripsi pekerjaan yang akan dibersihkan
  
  Terdapat 32 data unik lowongan pekerjaan.

- 📚 **Coursera Course Dataset**
Menggunakan dataset Coursera Courses 2021 dari Kaggle karena pada HO1 fokus pada scraping lowongan pekerjaan. Dipilih dataset yang masih memerlukan pembersihan format untuk digunakan.
  - Link Dataset: [https://www.kaggle.com/datasets/khusheekapoor/coursera-courses-dataset-2021](https://www.kaggle.com/datasets/khusheekapoor/coursera-courses-dataset-2021)

  Dataset berisi informasi nama kursus, deskripsi, level, dan keterampilan yang berhubungan dengan course. Dalam kode, kolom-kolom tersebut digabung menjadi 1 kolom teks deskriptor 1 nama kursus.
  
  Diambil 3416 kursus unik setelah pembersihan data.

## 2. Proses Vektorisasi dan Alasan Pemilihan ✨
Untuk mengubah teks menjadi representasi numerik (vektor), digunakan model:

- `all-MiniLM-L6-v2` dari sentence-transformers

Alasan memilih metode ini:

- Mampu menangkap makna semantik dari kalimat, bukan hanya kata kunci seperti di TF-IDF.

- Lebih ringan dan cepat dibanding model BERT biasa.

- Akurat dan efisien untuk sistem berbasis teks panjang seperti ini.

## 3. Proses Rekomendasi 🔍
  Langkah-langkah yang dilakukan:
  
 -  **Preprocessing** :
    Membersihkan teks dari simbol, angka, dan kata-kata tidak penting.
  
 -  **Vektorisasi** :
    Menggunakan Sentence Transformers untuk mengubah teks menjadi vektor.
  
 -  **Perhitungan Similarity** :
    Menggunakan cosine similarity antara vektor job dan vektor course. dipilih karena mampu mengukur kemiripan makna antar teks secara efisien tanpa terpengaruh panjang kalimat seperti metoda lain yang distance based.
  
 -  **Output** :
    Untuk setiap job, diambil 3 course dengan similarity tertinggi.
  
  Contoh output JSON:
  ```json
  {
    "job_title": "Sales Manager",
    "job_category": "Sales/Marketing",
    "recommended_courses": [
      {"course_name": "Sales Operations: Final Project", "score": 0.6953},
      {"course_name": "Account Management & Sales Force Design", "score": 0.6719},
      {"course_name": "Sales Force Management", "score": 0.6585}
    ]
  }
  
  ```
## Refleksi & Kendala 🚧
Kendala:
- Modul `deep_translator` tidak tersedia saat awal dijalankan.

- Error saat membaca kolom job_title dan category karena perbedaan format.

- Proses encoding agak lambat untuk data besar.

Solusi:
- Memastikan semua dependensi dimasukkan ke dalam requirements.txt.

- Mengecek ulang nama kolom yang relevan dan menyesuaikan kode untuk penggunaan.

- Melakukan optimasi dengan batch encode dari sentence-transformers.

## Pengembangan Selanjutnya 💡
- Format seperti ini kurang lebih sudah siap untuk dikembangkan menjadi API untuk project software.
