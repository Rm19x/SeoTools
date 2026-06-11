#  SeoTools 
SeoTools adalah sebuah *framework* berbasis CLI (Command Line Interface) yang dirancang secara profesional menggunakan Python untuk kebutuhan otomatisasi, ekstraksi, serta analisis mendalam terkait domain dan URL SEO. 

Alat ini menggabungkan performa tinggi dengan arsitektur modular, memungkinkan praktisi SEO dan developer melakukan audit teknis massal secara efisien.

---

##  Dikembangkan Oleh
<img src="https://raw.githubusercontent.com/Rm19x/SeoTools/refs/heads/main/seo.png">

* **Developer:** Mr.Rm19
* **GitHub:** [https://github.com/Rm19x](https://github.com/Rm19x)

---

##  Fitur Utama (26-in-1 Modules)

Sistem ini dibagi menjadi 3 kategori utama yang bekerja secara modular dan fungsional:

###  Kategori 1: Pondasi Utama & Crawler
1. **Bulk Status Code Checker (v3):** Memeriksa status keaktifan ribuan URL secara massal menggunakan optimasi *Multi-threading* kecepatan tinggi.
2. **Redirect Chain Tracker:** Melacak rantai pengalihan URL (301/302) hingga menemukan tujuan akhir halaman.
3. **Broken Link Finder (404 Crawler):** Melakukan crawling internal pada satu website untuk menemukan tautan yang rusak.
4. **Subdomain Finder / Enumerator:** Mencari subdomain aktif memanfaatkan integrasi log transparansi sertifikat SSL (`crt.sh`).
5. **Robots.txt & Sitemap Validator:** Memeriksa ketersediaan dan validitas struktur file sitemap serta robots suatu website.
6. **Domain Authority (DA) Fetcher:** Mengambil metrik skor otoritas halaman (PageRank) secara real-time via OpenPageRank API.

###  Kategori 2: Extractor & Deep Analysis
7. **TLD Filter & Extractor:** Memisahkan dan mengelompokkan daftar domain berdasarkan ekstensi TLD (`.com`, `.net`, `.id`, dll).
8. **Regex-Based URL Pattern Extractor:** Menyaring URL berdasarkan pola teks atau kata kunci spesifik.
9. **Mass Query String Stripper:** Membersihkan parameter pelacak iklan/sistem pada URL (seperti `?utm_source=...`).
10. **Protocol Stripper:** Menghapus skema `http://`, `https://`, dan `www.` untuk menghasilkan domain bersih.
11. **Port Stripper/Extractor:** Mendeteksi dan memisahkan domain yang berjalan di port kustom (misal `:8080`).
12. **File Extension Finder in URL:** Menemukan dan mengelompokkan URL yang mengarah langsung ke ekstensi file tertentu.
13. **UUID/Hash URL Detector:** Mendeteksi URL dinamis berstruktur ID panjang yang tidak ramah terhadap SEO.
14. **IP Address Domain Finder (Reverse DNS):** Melakukan reverse DNS jika ada target yang menggunakan alamat IP langsung.
15. **DNS Record Extractor:** Menarik data rekor DNS esensial (`A`, `MX`, `TXT`) secara massal.
16. **Nameserver (NS) Auditor & Grouper:** Mengambil dan mengaudit kepemilikan Nameserver dari domain target.
17. **Cloudflare / WAF Detector:** Memeriksa apakah website dilindungi oleh Cloudflare atau Web Application Firewall lainnya.
18. **Domain Availability Bulk Checker:** Mengecek ketersediaan registrasi domain via resolusi DNS lokal (Aman dari *rate-limit*).
19. **Malware/Phishing URL Scanner:** Memindai reputasi keamanan URL berdasarkan database ancaman siber publik.
20. **Banned Domain Checker (Deindex):** Mendeteksi indikasi apakah domain di-ban atau di-deindeks dari mesin pencari publik.
21. **Domain Expiry Countdown Timer:** Mengambil data tanggal kedaluwarsa masa aktif domain via integrasi protokol RDAP/WHOIS.
22. **Image URL Extractor & Auditor:** Mengoleksi dan mengaudit seluruh aset gambar (`<img>`) dari suatu halaman web.
23. **Video/Media URL Stream Extractor:** Mengekstrak sumber media streaming (`<video>`, `<audio>`) yang tertanam di halaman web.
24. **Downloadable File Link Extractor:** Mengumpulkan semua tautan file unduhan dokumen atau arsip kompresi (`.zip`, `.pdf`, `.exe`, dll).

###  Kategori 3: Fitur Tambahan Baru
25. **Base Domain Extractor:** Mengekstrak domain inti dari baris URL yang berantakan atau memiliki path panjang.
26. **URL List Cleaner (Add HTTP/HTTPS):** Membersihkan list domain mentah dan otomatis menambahkan protokol HTTP atau HTTPS secara seragam jika protokol belum tersedia.

---

## Panduan Lengkap Penggunaan (Usage Guide)
Seluruh fungsionalitas SeoTools dikendalikan melalui berkas utama main.py menggunakan argumen berbasis teks di terminal.

## Struktur Argumen Global:
-i, --input  : Mengarah ke file teks (.txt) yang berisi daftar URL atau Domain (untuk proses massal / bulk).

-u, --url    : Mengarah ke satu target URL atau Domain tunggal (untuk analisis spesifik).

-o, --output : (Opsional) Mengatur file teks baru sebagai tempat penyimpanan hasil akhir.

-m, --mode   : (Wajib) Nama modul atau fitur spesifik yang ingin dieksekusi.


---

###  BAGIAN 2: Contoh Perintah Kategori 1 & 2 




###  KATEGORI 1: PONDASI UTAMA & CRAWLER

#### 1. Bulk Status Code Checker (`status-checker`)
```
python main.py -i list_url.txt -m status-checker
2. Redirect Chain Tracker (redirect-tracker)



python main.py -u [https://example.com/promo-lama](https://example.com/promo-lama) -m redirect-tracker
3. Broken Link Finder (broken-finder)



python main.py -u [https://websitekamu.com](https://websitekamu.com) -m broken-finder -o hasil_404.txt
4. Subdomain Finder / Enumerator (subdomain-finder)



python main.py -u google.com -m subdomain-finder -o subdomains.txt
5. Robots.txt & Sitemap Validator (sitemap-validator)



python main.py -u [https://targetweb.com](https://targetweb.com) -m sitemap-validator
6. Domain Authority (DA) Fetcher (da-fetcher)



python main.py -i list_domain.txt -m da-fetcher
```
 ### KATEGORI 2: EXTRACTOR & DEEP ANALYSIS
 ```
7. TLD Filter & Extractor (tld-filter)



python main.py -i domain_acak.txt -m tld-filter -o hasil_tld.txt
8. Regex-Based URL Pattern Extractor (regex-extractor)



python main.py -i sitemap_dump.txt -m regex-extractor -o hasil_filter.txt
9. Mass Query String Stripper (query-stripper)



python main.py -i list_url_iklan.txt -m query-stripper -o url_bersih.txt
10. Protocol Stripper (protocol-stripper)



python main.py -i list_url.txt -m protocol-stripper -o domain_murni.txt
11. Port Stripper/Extractor (port-stripper)



python main.py -i target_server.txt -m port-stripper -o port_aktif.txt
12. File Extension Finder in URL (ext-finder)



python main.py -i log_url.txt -m ext-finder -o file_url.txt
13. UUID/Hash URL Detector (uuid-detector)



python main.py -i list_slug.txt -m uuid-detector

```
###  BAGIAN 3: Sisa Perintah Kategori 2, Kategori 3, & Penutup (Salin terakhir)
```
14. IP Address Domain Finder (`reverse-dns`)
python main.py -u 8.8.8.8 -m reverse-dns

15. DNS Record Extractor (dns-extractor)
python main.py -u github.com -m dns-extractor

16. Nameserver (NS) Auditor & Grouper (ns-auditor)
python main.py -i list_pbn.txt -m ns-auditor


17. Cloudflare / WAF Detector (cf-detector)
python main.py -i list_web.txt -m cf-detector

18. Domain Availability Bulk Checker (domain-avail)



python main.py -i ide_nama_domain.txt -m domain-avail -o domain_kosong.txt
19. Malware/Phishing URL Scanner (malware-scanner)



python main.py -i cek_keamanan.txt -m malware-scanner
20. Banned Domain Checker (banned-checker)



python main.py -u websitemati.com -m banned-checker
21. Domain Expiry Countdown Timer (expiry-timer)



python main.py -u internet.org -m expiry-timer
22. Image URL Extractor & Auditor (img-extractor)



python main.py -u [https://halamanweb.com/artikel-1](https://halamanweb.com/artikel-1) -m img-extractor -o list_gambar.txt
23. Video/Media URL Stream Extractor (media-extractor)



python main.py -u [https://situsnonton.com/video-page](https://situsnonton.com/video-page) -m media-extractor
24. Downloadable File Link Extractor (download-extractor)



python main.py -u [https://opensource-share.org](https://opensource-share.org) -m download-extractor -o link_download.txt
```
## KATEGORI 3: FITUR TAMBAHAN BARU
```
25. Base Domain Extractor (domain-extractor)
python main.py -i list_url_panjang.txt -m domain-extractor -o domain_inti.txt

26. URL List Cleaner - Add HTTP/HTTPS (url-cleaner-http / url-cleaner-https)



python main.py -i domain_mentah.txt -m url-cleaner-http -o hasil_http.txt



python main.py -i domain_mentah.txt -m url-cleaner-https -o hasil_https.txt

```

## Struktur Repositori

```
SeoTools/
├── main.py          # Handler utama argumen CLI dan tampilan banner identitas
├── modules.py       # Logika fungsional dan mesin inti dari 26 fitur utama
├── README.md        # Dokumentasi panduan instruksi penggunaan lengkap
└── requirements.txt # Catatan daftar dependensi library Python eksternal
📄 Kontribusi & Lisensi
Proyek ini dikembangkan secara open-source untuk membantu mempercepat proses audit teknis di bidang web development dan SEO. Jika Anda menemukan bug atau ingin menambahkan fitur baru di versi berikutnya, silakan ajukan Pull Request (PR) di repositori ini.

Developed with ❤️ by Mr.Rm19
```


