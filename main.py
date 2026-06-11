#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SeoTools - All-in-One SEO CLI Framework
Developed by: Mr.Rm19
GitHub: https://github.com/Rm19x
Version: 1.0.0 (Core Engine)
"""

import sys
import argparse
from colorama import Fore, Style, init

# Inisialisasi colorama untuk dukungan warna di lintas platform (Windows/Linux/Mac)
init(autoreset=True)

def print_banner():
    """Menampilkan banner utama identitas pembuat (Mr.Rm19)"""
    banner = f"""
{Fore.CYAN}====================================================================
{Fore.GREEN} ⚡ SeoTools ⚡
{Fore.YELLOW} Coded by : Mr.Rm19
{Fore.YELLOW} GitHub   : https://github.com/Rm19x
{Fore.CYAN}====================================================================
    """
    print(banner)

def main():
    print_banner()
    
    # Inisialisasi Argument Parser
    parser = argparse.ArgumentParser(
        description=f"{Fore.GREEN}SeoTools: Toolkit otomatisasi & analisis SEO modular by Mr.Rm19.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Definisikan Argumen Utama
    parser.add_argument("-i", "--input", help="Path ke file teks input (contoh: list.txt atau domain.txt)")
    parser.add_argument("-u", "--url", help="Target URL tunggal untuk analisis spesifik")
    parser.add_argument("-o", "--output", help="Path ke file output hasil analisis (opsional)")
    
    # Kelompokkan Fitur berdasarkan kategori dalam argumen --mode
    mode_help = """Pilih mode/fitur yang ingin dijalankan:

[ KATEGORI 1: PONDASI UTAMA & CRAWLER ]
  status-checker      : Bulk Status Code Checker (v3 Multi-threading)
  redirect-tracker    : Redirect Chain Tracker (301/302)
  broken-finder       : Broken Link Finder (404 Crawler)
  subdomain-finder    : Subdomain Finder / Enumerator
  sitemap-validator   : Robots.txt & Sitemap Validator
  da-fetcher          : Domain Authority (DA) Fetcher

[ KATEGORI 2: EXTRACTOR & DEEP ANALYSIS ]
  tld-filter          : TLD Filter & Extractor
  regex-extractor     : Regex-Based URL Pattern Extractor
  query-stripper      : Mass Query String Stripper
  protocol-stripper   : Protocol Stripper (Removes http/https/www)
  port-stripper       : Port Stripper/Extractor
  ext-finder          : File Extension Finder in URL
  uuid-detector       : UUID/Hash URL Detector
  reverse-dns         : IP Address Domain Finder (Reverse DNS)
  dns-extractor       : DNS Record Extractor (A, AAAA, MX, TXT)
  ns-auditor          : Nameserver (NS) Auditor & Grouper
  cf-detector         : Cloudflare / WAF Detector
  domain-avail        : Domain Availability Bulk Checker
  malware-scanner     : Malware/Phishing URL Scanner (Safe Browsing)
  banned-checker      : Banned Domain Checker (Search Engine Deindex)
  expiry-timer        : Domain Expiry Countdown Timer (WHOIS)
  img-extractor       : Image URL Extractor & Auditor
  media-extractor     : Video/Media URL Stream Extractor
  download-extractor  : Downloadable File Link Extractor

[ KATEGORI 3: FITUR TAMBAHAN BARU ]
  domain-extractor    : Base Domain Extractor
  url-cleaner-http    : URL List Cleaner & Add HTTP (Otomatis HTTP jika tanpa protokol)
  url-cleaner-https   : URL List Cleaner & Add HTTPS (Otomatis HTTPS jika tanpa protokol)
"""
    
    parser.add_argument("-m", "--mode", help=mode_help, required=True)
    
    # Parsing argumen yang masuk
    args = parser.parse_args()
    
    # Import modul fitur secara dinamis untuk efisiensi memori
    try:
        import modules
    except ImportError:
        print(f"{Fore.RED}[❌ ERROR] Gagal memuat file 'modules.py'. Pastikan file tersebut berada di folder yang sama dengan main.py.")
        sys.exit(1)
        
    # Pemetaan Mode ke Fungsi di modules.py
    mode_mapping = {
        # Kategori 1
        "status-checker": modules.bulk_status_checker,
        "redirect-tracker": modules.redirect_chain_tracker,
        "broken-finder": modules.broken_link_finder,
        "subdomain-finder": modules.subdomain_finder,
        "sitemap-validator": modules.sitemap_validator,
        "da-fetcher": modules.domain_authority_fetcher,
        
        # Kategori 2
        "tld-filter": modules.tld_filter_extractor,
        "regex-extractor": modules.regex_pattern_extractor,
        "query-stripper": modules.mass_query_stripper,
        "protocol-stripper": modules.protocol_stripper,
        "port-stripper": modules.port_stripper_extractor,
        "ext-finder": modules.file_extension_finder,
        "uuid-detector": modules.uuid_hash_detector,
        "reverse-dns": modules.reverse_dns_finder,
        "dns-extractor": modules.dns_record_extractor,
        "ns-auditor": modules.nameserver_auditor,
        "cf-detector": modules.cloudflare_detector,
        "domain-avail": modules.domain_availability_checker,
        "malware-scanner": modules.malware_phishing_scanner,
        "banned-checker": modules.banned_domain_checker,
        "expiry-timer": modules.domain_expiry_timer,
        "img-extractor": modules.image_url_extractor,
        "media-extractor": modules.media_stream_extractor,
        "download-extractor": modules.downloadable_file_extractor,
        
        # Kategori 3
        "domain-extractor": modules.base_domain_extractor,
        "url-cleaner-http": lambda a: modules.url_list_cleaner_protocol(a, "http"),
        "url-cleaner-https": lambda a: modules.url_list_cleaner_protocol(a, "https")
    }

    # Validasi dan Eksekusi Driver Mode
    if args.mode in mode_mapping:
        print(f"{Fore.BLUE}[*] Memulai mode: {Fore.YELLOW}{args.mode}")
        # Menjalankan fungsi target dengan melemparkan objek argumen CLI
        mode_mapping[args.mode](args)
    else:
        print(f"{Fore.RED}[❌ ERROR] Mode '{args.mode}' tidak dikenali. Gunakan -h atau --help untuk melihat daftar mode.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[⚠️] Proses dihentikan paksa oleh pengguna (Ctrl+C).")
        sys.exit(0)