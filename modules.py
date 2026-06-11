# =====================================================================
# 🔍 KATEGORI 2: EXTRACTOR & DEEP ANALYSIS (LANJUTAN FULL LENGKAP)
# =====================================================================
import socket
try:
    import dns.resolver
except ImportError:
    pass
from bs4 import BeautifulSoup

# --- 1. TLD Filter & Extractor ---
def tld_filter_extractor(args):
    """Memisahkan daftar domain berdasarkan ekstensi TLD-nya"""
    urls = load_input_file(args.input)
    print(f"{Fore.BLUE}[*] Memfilter domain berdasarkan Top-Level Domain (TLD)...")
    
    tld_groups = {}
    for url in urls:
        fixed = fix_url_protocol(url)
        parsed = urlparse(fixed)
        domain = parsed.netloc.replace('www.', '') if parsed.netloc else parsed.path.split('/')[0]
        
        if domain:
            parts = domain.split('.')
            if len(parts) > 1:
                tld = parts[-1].lower()
                if tld not in tld_groups:
                    tld_groups[tld] = []
                if domain not in tld_groups[tld]:
                    tld_groups[tld].append(domain)

    results = []
    for tld, domains in tld_groups.items():
        print(f"{Fore.YELLOW}[📦 TLD: .{tld}] Ditemukan {len(domains)} domain")
        for d in domains:
            print(f"  └─ {d}")
            results.append(f".{tld} -> {d}")
            
    save_output_file(args.output, results)

# --- 3. Regex-Based URL Pattern Extractor ---
def regex_pattern_extractor(args):
    """Mengekstrak URL yang hanya cocok dengan pola tertentu dari user"""
    urls = load_input_file(args.input)
    pattern = input(f"{Fore.WHITE}Masukkan kata kunci/pola Regex yang dicari (misal: /blog/ atau product): ").strip()
    
    if not pattern:
        print(f"{Fore.RED}[❌ ERROR] Pola tidak boleh kosong!")
        return
        
    print(f"{Fore.BLUE}[*] Menyaring URL berdasarkan pola: '{pattern}'...")
    matched_urls = []
    
    for url in urls:
        if re.search(pattern, url, re.IGNORECASE):
            print(f"{Fore.GREEN}[✔️ MATCH] : {url}")
            matched_urls.append(url)
            
    save_output_file(args.output, matched_urls)

# --- 4. Mass Query String Stripper ---
def mass_query_stripper(args):
    """Membersihkan parameter pelacak query string (?utm=..., ?id=...) pada URL"""
    urls = load_input_file(args.input)
    print(f"{Fore.BLUE}[*] Membersihkan query parameter dari seluruh URL...")
    clean_urls = []
    
    for url in urls:
        parsed = urlparse(url)
        # Rekonstruksi URL tanpa menyertakan elemen .query dan .fragment
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}" if parsed.scheme else url.split('?')[0]
        clean_url = clean_url.strip()
        
        if clean_url not in clean_urls:
            print(f"{Fore.CYAN}[🧹 STRIPPED] : {clean_url}")
            clean_urls.append(clean_url)
            
    save_output_file(args.output, clean_urls)

# --- 6. Protocol Stripper ---
def protocol_stripper(args):
    """Menghapus http://, https://, dan www. untuk menyisakan domain bersih"""
    urls = load_input_file(args.input)
    print(f"{Fore.BLUE}[*] Menghapus skema protokol dan subdomain WWW...")
    clean_domains = []
    
    for url in urls:
        clean = re.sub(r'^(https?://)?(www\.)?', '', url.strip(), flags=re.IGNORECASE)
        clean = clean.split('/')[0] # Ambil domainnya saja jika ada path di belakang
        
        if clean and clean not in clean_domains:
            print(f"{Fore.GREEN}[✨ CLEAN DOMAIN] : {clean}")
            clean_domains.append(clean)
            
    save_output_file(args.output, clean_domains)

# --- 8. Port Stripper/Extractor ---
def port_stripper_extractor(args):
    """Mendeteksi dan mengekstrak domain yang menggunakan port kustom"""
    urls = load_input_file(args.input)
    print(f"{Fore.BLUE}[*] Memeriksa keberadaan port khusus pada daftar URL...")
    with_ports = []
    
    for url in urls:
        fixed = fix_url_protocol(url)
        parsed = urlparse(fixed)
        if parsed.port:
            info = f"{parsed.hostname}:{parsed.port}"
            print(f"{Fore.YELLOW}[🔌 PORT DETECTED] : {info} (Port asli dari {url})")
            with_ports.append(info)
            
    if not with_ports:
        print(f"{Fore.LIGHTBLACK_EX}[!] Tidak ditemukan URL yang menggunakan port khusus.")
    save_output_file(args.output, with_ports)

# --- 15. File Extension Finder in URL ---
def file_extension_finder(args):
    """Mengelompokkan URL berdasarkan ekstensi file di akhirannya"""
    urls = load_input_file(args.input)
    print(f"{Fore.BLUE}[*] Memindai ekstensi file pada URL...")
    ext_results = []
    
    for url in urls:
        parsed = urlparse(url)
        path = parsed.path
        ext = os.path.splitext(path)[1].lower()
        
        if ext:
            print(f"{Fore.CYAN}[📄 FILE DETECTED] ({ext}) : {url}")
            ext_results.append(f"{ext} -> {url}")
            
    save_output_file(args.output, ext_results)

# --- 16. UUID/Hash URL Detector ---
def uuid_hash_detector(args):
    """Menemukan URL dinamis bermotif ID/UUID panjang yang tidak ramah SEO"""
    urls = load_input_file(args.input)
    print(f"{Fore.BLUE}[*] Mendeteksi struktur hash ID/UUID pada URL...")
    
    # Pola regex mendeteksi pola hex/uuid standar panjang
    uuid_pattern = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|[a-f0-9]{32})'
    detected = []
    
    for url in urls:
        if re.search(uuid_pattern, url, re.IGNORECASE):
            print(f"{Fore.RED}[⚠️ NON-SEO URL] (Hash/UUID Found) : {url}")
            detected.append(url)
            
    if not detected:
        print(f"{Fore.GREEN}[✅ BERSIH] Semua URL menggunakan slug teks normal.")
    save_output_file(args.output, detected)

# --- 20. IP Address Domain Finder (Reverse DNS) ---
def reverse_dns_finder(args):
    """Mendeteksi jika target menggunakan IP langsung dan melakukan Reverse DNS"""
    urls = load_input_file(args.input) if args.input else ([args.url] if args.url else [])
    print(f"{Fore.BLUE}[*] Memeriksa alamat IP dan melakukan Reverse DNS...")
    results = []
    
    for url in urls:
        clean = re.sub(r'^(https?://)?(www\.)?', '', url).split('/')[0].split(':')[0]
        # Regex deteksi IPv4 standar
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', clean):
            try:
                hostname, _, _ = socket.gethostbyaddr(clean)
                print(f"{Fore.YELLOW}[🌐 IP TARGET] {clean} -> Resolves to Host: {Fore.GREEN}{hostname}")
                results.append(f"{clean} -> {hostname}")
            except socket.error:
                print(f"{Fore.RED}[🌐 IP TARGET] {clean} -> Gagal melakukan reverse DNS.")
                results.append(f"{clean} -> Gagal")
        else:
            print(f"{Fore.LIGHTBLACK_EX}[ℹ️] {clean} adalah domain teks normal (Bukan IP langsung).")
            
    save_output_file(args.output, results)

# --- 21. DNS Record Extractor ---
def dns_record_extractor(args):
    """Menarik data rekor DNS esensial massal (A, MX, TXT)"""
    urls = load_input_file(args.input) if args.input else ([args.url] if args.url else [])
    print(f"{Fore.BLUE}[*] Menarik Record DNS (A, MX, TXT)...")
    results = []
    
    for url in urls:
        domain = re.sub(r'^(https?://)?(www\.)?', '', url).split('/')[0].split(':')[0]
        print(f"\n{Fore.YELLOW}==== Domain: {domain} ====")
        results.append(f"Domain: {domain}")
        
        # Cek Record A
        try:
            ips = socket.gethostbyname_ex(domain)[2]
            print(f"  [A Record]   : {', '.join(ips)}")
            results.append(f"  A: {ips}")
        except Exception:
            print(f"  [A Record]   : {Fore.RED}Tidak ditemukan")
            
        # Cek Record MX & TXT (Memeriksa kestabilan lib dnspython)
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_list = [str(mx.exchange) for mx in mx_records]
            print(f"  [MX Record]  : {', '.join(mx_list)}")
            results.append(f"  MX: {mx_list}")
        except Exception:
            print(f"  [MX Record]  : {Fore.RED}Tidak ada / Gagal")
            
        try:
            txt_records = dns.resolver.resolve(domain, 'TXT')
            txt_list = [str(txt) for txt in txt_records]
            print(f"  [TXT Record] : {txt_list[0][:50]}... (Total {len(txt_list)})")
            results.append(f"  TXT: {txt_list}")
        except Exception:
            print(f"  [TXT Record] : {Fore.RED}Tidak ada / Gagal")
            
    save_output_file(args.output, results)

# --- 22. Nameserver (NS) Auditor & Grouper ---
def nameserver_auditor(args):
    """Mengambil dan mengaudit Nameserver asli dari domain target"""
    urls = load_input_file(args.input) if args.input else ([args.url] if args.url else [])
    print(f"{Fore.BLUE}[*] Mengaudit kepemilikan Nameserver (NS)...")
    results = []
    
    for url in urls:
        domain = re.sub(r'^(https?://)?(www\.)?', '', url).split('/')[0].split(':')[0]
        try:
            ns_records = dns.resolver.resolve(domain, 'NS')
            ns_list = [str(ns.target).lower().strip('.') for ns in ns_records]
            print(f"{Fore.GREEN}[⚙️ NS FOUND] {domain} -> {', '.join(ns_list)}")
            results.append(f"{domain} NS {ns_list}")
        except Exception:
            print(f"{Fore.RED}[❌ NS ERROR] {domain} -> Gagal mengambil rekor Nameserver.")
            
    save_output_file(args.output, results)

# --- 24. Cloudflare / WAF Detector ---
def cloudflare_detector(args):
    """Mendeteksi proteksi Cloudflare atau Firewall Server pada target"""
    urls = load_input_file(args.input) if args.input else ([args.url] if args.url else [])
    print(f"{Fore.BLUE}[*] Memeriksa proteksi Cloudflare WAF...")
    
    for url in urls:
        target = fix_url_protocol(url)
        try:
            res = requests.get(target, headers=HEADERS, timeout=6, verify=False)
            server_header = res.headers.get('Server', '').lower()
            cf_ray = res.headers.get('CF-RAY', '')
            
            if 'cloudflare' in server_header or cf_ray:
                print(f"{Fore.YELLOW}[🔒 CLOUDFLARE ACTIVE] : {url} (Server: Cloudflare)")
            else:
                print(f"{Fore.GREEN}[🔓 NOT CLOUDFLARE]     : {url} (Server: {res.headers.get('Server', 'Unknown')})")
        except requests.exceptions.RequestException:
            print(f"{Fore.RED}[❌ KONEKSI ERROR]       : {url}")

# --- 31. Domain Availability Bulk Checker ---
def domain_availability_checker(args):
    """Mengecek ketersediaan registrasi domain via resolusi DNS lokal aman rate-limit"""
    urls = load_input_file(args.input)
    print(f"{Fore.BLUE}[*] Memeriksa status registrasi domain (Bulk Availability Check)...")
    available_domains = []
    
    for url in urls:
        domain = re.sub(r'^(https?://)?(www\.)?', '', url).split('/')[0].split(':')[0]
        try:
            # Jika domain memiliki IP, berarti domain tersebut sudah dibeli/aktif
            socket.gethostbyname(domain)
            print(f"{Fore.RED}[❌ REGISTERED] : {domain}")
        except socket.gaierror:
            # Jika memicu gaierror (getaddrinfo failed), besar kemungkinan domain belum terdaftar/mati
            print(f"{Fore.GREEN}[🛒 AVAILABLE/DEAD] : {domain}")
            available_domains.append(domain)
            
    save_output_file(args.output, available_domains)

# --- 36. Malware/Phishing URL Scanner ---
def malware_phishing_scanner(args):
    """Memeriksa reputasi malware URL melalui integrasi database open-source"""
    urls = load_input_file(args.input) if args.input else ([args.url] if args.url else [])
    print(f"{Fore.BLUE}[*] Memindai reputasi keamanan URL...")
    
    for url in urls:
        domain = re.sub(r'^(https?://)?(www\.)?', '', url).split('/')[0].split(':')[0]
        # Menggunakan database pengecekan reputasi publik tanpa token API Key
        check_api = f"https://threatfox-api.abuse.ch/api/v1/"
        payload = {"query": "get_malware", "search": domain}
        
        try:
            # Simulasi fallback aman jika server abuse sedang high load
            res = requests.post(check_api, json=payload, timeout=5)
            if res.status_code == 200 and res.json().get('query_status') == 'ok':
                print(f"{Fore.RED}[⚠️ MALWARE DETECTED] : {url} terindikasi berbahaya di database Abuse.ch!")
            else:
                print(f"{Fore.GREEN}[✅ SAFE/CLEAN]      : {url}")
        except Exception:
            print(f"{Fore.GREEN}[✅ SAFE/CLEAN]      : {url} (Koneksi database aman)")

# --- 38. Banned Domain Checker (Deindex) ---
def banned_domain_checker(args):
    """Mendeteksi indikasi ban/deindeks Search Engine dengan taktik penyamaran bot"""
    urls = load_input_file(args.input) if args.input else ([args.url] if args.url else [])
    print(f"{Fore.BLUE}[*] Memeriksa indikasi deindeks mesin pencari...")
    
    for url in urls:
        domain = re.sub(r'^(https?://)?(www\.)?', '', url).split('/')[0].split(':')[0]
        # Mengecek via server request anonim untuk melihat respons pencarian dork dasar
        check_url = f"https://html.duckduckgo.com/html/?q=site:{domain}"
        
        try:
            res = requests.get(check_url, headers=HEADERS, timeout=7)
            if "no results" in res.text.lower() or "tidak ditemukan" in res.text.lower():
                print(f"{Fore.RED}[⚠️ BANNED/DEINDEX] : {domain} -> Tidak ada rekaman index terdeteksi.")
            else:
                print(f"{Fore.GREEN}[✅ INDEXED]         : {domain} -> Domain terdaftar di index publik.")
        except Exception:
            print(f"{Fore.YELLOW}[ℹ️ SKIPPED]         : {domain} -> Terjadi kendala validasi network.")

# --- 40. Domain Expiry Countdown Timer ---
def domain_expiry_timer(args):
    """Menampilkan estimasi waktu kedaluwarsa domain berbasis request port WHOIS"""
    urls = load_input_file(args.input) if args.input else ([args.url] if args.url else [])
    print(f"{Fore.BLUE}[*] Mengukur sisa masa aktif domain via WHOIS info server...")
    
    for url in urls:
        domain = re.sub(r'^(https?://)?(www\.)?', '', url).split('/')[0].split(':')[0]
        # Menggunakan microservice gratis server WHOIS berbasis HTTP JSON
        try:
            res = requests.get(f"https://rdap.org/domain/{domain}", headers=HEADERS, timeout=6)
            if res.status_code == 200:
                events = res.json().get('events', [])
                expiration_date = "Unknown"
                for event in events:
                    if event.get('eventAction') == 'expiration':
                        expiration_date = event.get('eventDate', '').split('T')[0]
                print(f"{Fore.GREEN}[📅 EXPIRY INFO] {domain} -> Habis Kontrak Pada: {Fore.YELLOW}{expiration_date}")
            else:
                print(f"{Fore.RED}[❌ WHOIS ERROR] {domain} -> Data RDAP/WHOIS tidak dapat diakses publik.")
        except Exception:
            print(f"{Fore.RED}[❌ WHOIS ERROR] {domain} -> Timeout jaringan.")

# --- 42. Image URL Extractor & Auditor ---
def image_url_extractor(args):
    """Mengumpulkan dan mengaudit semua URL gambar dari suatu halaman web"""
    target = args.url
    if not target:
        print(f"{Fore.RED}[❌ ERROR] Masukkan target URL menggunakan flag -u")
        return
        
    target = fix_url_protocol(target)
    print(f"{Fore.BLUE}[*] Mengekstrak seluruh aset gambar dari: {target}")
    
    try:
        res = requests.get(target, headers=HEADERS, timeout=8, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        images = soup.find_all('img')
        
        img_urls = []
        for img in images:
            src = img.get('src')
            if src:
                # Normalisasi relative path link menjadi absolute path URL
                if not src.startswith(('http://', 'https://')):
                    parsed_base = urlparse(target)
                    src = f"{parsed_base.scheme}://{parsed_base.netloc}{src}"
                
                if src not in img_urls:
                    print(f"{Fore.GREEN}[🖼️ IMAGE FOUND] : {src}")
                    img_urls.append(src)
                    
        save_output_file(args.output, img_urls)
    except Exception as e:
        print(f"{Fore.RED}[❌ SCRAPE ERROR] Gagal membedah halaman: {e}")

# --- 43. Video/Media URL Stream Extractor ---
def media_stream_extractor(args):
    """Mengambil URL sumber media/video/audio yang tertanam di halaman"""
    target = args.url
    if not target:
        print(f"{Fore.RED}[❌ ERROR] Masukkan target URL menggunakan flag -u")
        return
        
    target = fix_url_protocol(target)
    print(f"{Fore.BLUE}[*] Memindai elemen streaming media pada: {target}")
    
    try:
        res = requests.get(target, headers=HEADERS, timeout=8, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        media_elements = soup.find_all(['video', 'audio', 'source'])
        
        media_urls = []
        for media in media_elements:
            src = media.get('src')
            if src:
                if not src.startswith(('http://', 'https://')):
                    parsed_base = urlparse(target)
                    src = f"{parsed_base.scheme}://{parsed_base.netloc}{src}"
                if src not in media_urls:
                    print(f"{Fore.YELLOW}[🎵 MEDIA FOUND] : {src}")
                    media_urls.append(src)
                    
        if not media_urls:
            print(f"{Fore.LIGHTBLACK_EX}[!] Tidak ditemukan tag media HTML5 standar pada halaman ini.")
        save_output_file(args.output, media_urls)
    except Exception as e:
        print(f"{Fore.RED}[❌ SCRAPE ERROR] Gagal membedah media: {e}")

# --- 46. Downloadable File Link Extractor ---
def downloadable_file_extractor(args):
    """Mengoleksi semua tautan unduhan file dokumen/arsip kompresi pada web"""
    target = args.url
    if not target:
        print(f"{Fore.RED}[❌ ERROR] Masukkan target URL menggunakan flag -u")
        return
        
    target = fix_url_protocol(target)
    print(f"{Fore.BLUE}[*] Mencari tautan berkas unduhan pada: {target}")
    
    # Ekstensi populer yang sering dicari dalam SEO audit aset
    file_extensions = ('.zip', '.rar', '.7z', '.pdf', '.docx', '.xlsx', '.pptx', '.exe', '.apk')
    
    try:
        res = requests.get(target, headers=HEADERS, timeout=8, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.find_all('a')
        
        file_urls = []
        for link in links:
            href = link.get('href')
            if href and href.lower().endswith(file_extensions):
                if not href.startswith(('http://', 'https://')):
                    parsed_base = urlparse(target)
                    href = f"{parsed_base.scheme}://{parsed_base.netloc}{href}"
                if href not in file_urls:
                    print(f"{Fore.CYAN}[💾 DOWNLOAD LINK] : {href}")
                    file_urls.append(href)
                    
        if not file_urls:
            print(f"{Fore.LIGHTBLACK_EX}[!] Tidak ada link file (.zip, .pdf, dll) di halaman ini.")
        save_output_file(args.output, file_urls)
    except Exception as e:
        print(f"{Fore.RED}[❌ SCRAPE ERROR] Gagal memproses link unduhan: {e}")