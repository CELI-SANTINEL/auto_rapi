#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SPECTRA DAPODIK JSON REPAIR - ULTIMATE EDITION
KHUSUS UNTUK JSON SISWA DAPODIK DENGAN 1700+ DATA
AUTO DETECT, REPAIR, DAN RAPIKAN
"""

import json
import re
import os
import sys
from datetime import datetime

# ============ KONFIGURASI ============
VERSION = "SPECTRA-DAPODIK-FIXER-v4.0"

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

C = Colors()

# ============ FUNGSI KHUSUS DAPODIK ============

def banner():
    print(f"""
{C.RED}{C.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║  🔥 SPECTRA DAPODIK JSON REPAIR v4.0 ULTIMATE 🔥           ║
║  ☠️  KHUSUS UNTUK JSON SISWA DAPODIK 1700+ DATA            ║
║  👑  BY: MOMMY DARK WORM AI                                ║
╚═══════════════════════════════════════════════════════════════╝
{C.RESET}""")


def load_dapodik_json(filepath):
    """Load file dengan berbagai metode"""
    
    print(f"{C.CYAN}📂 Memuat: {filepath}{C.RESET}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            raw = f.read()
    except FileNotFoundError:
        print(f"{C.RED}❌ File tidak ditemukan!{C.RESET}")
        return None
    except Exception as e:
        print(f"{C.RED}❌ Error baca file: {e}{C.RESET}")
        return None
    
    # ====== METODE 1: Parse langsung ======
    try:
        data = json.loads(raw)
        print(f"{C.GREEN}✅ JSON valid!{C.RESET}")
        return data
    except json.JSONDecodeError as e:
        print(f"{C.YELLOW}⚠️ JSON Error: {e}{C.RESET}")
        print(f"{C.CYAN}🔧 Mencoba repair...{C.RESET}")
    
    # ====== METODE 2: Ekstrak semua data siswa ======
    try:
        print(f"{C.CYAN}🔍 Mencari data siswa...{C.RESET}")
        
        # Cari semua object siswa
        # Pola: { "nama": "...", "jenis_kelamin": "...", ... }
        students = []
        
        # Pattern untuk mendeteksi satu siswa
        pattern = r'\{[^{}]*"nama"\s*:\s*"[^"]*"[^{}]*\}'
        matches = re.findall(pattern, raw)
        
        if matches:
            print(f"{C.CYAN}🔍 Ditemukan {len(matches)} object siswa{C.RESET}")
            
            for i, match in enumerate(matches):
                try:
                    # Coba parse setiap object
                    # Bersihkan dulu
                    cleaned = match.strip()
                    # Fix trailing comma
                    cleaned = re.sub(r',\s*}', '}', cleaned)
                    cleaned = re.sub(r',\s*]', ']', cleaned)
                    
                    # Parse
                    student = json.loads(cleaned)
                    students.append(student)
                except:
                    continue
            
            if students:
                print(f"{C.GREEN}✅ Berhasil mengekstrak {len(students)} siswa!{C.RESET}")
                return {"data": students}
        
    except Exception as e:
        print(f"{C.YELLOW}⚠️ Metode 2 gagal: {e}{C.RESET}")
    
    # ====== METODE 3: Ekstrak per baris ======
    try:
        print(f"{C.CYAN}🔍 Mencoba ekstrak per baris...{C.RESET}")
        
        students = []
        lines = raw.split('\n')
        
        # Cari baris yang mengandung "nama"
        for line in lines:
            if '"nama"' in line and '"jenis_kelamin"' in line:
                try:
                    # Bersihkan line
                    clean_line = line.strip()
                    if clean_line.startswith('{') and clean_line.endswith('}'):
                        student = json.loads(clean_line)
                        students.append(student)
                except:
                    continue
        
        if students:
            print(f"{C.GREEN}✅ Berhasil mengekstrak {len(students)} siswa dari baris!{C.RESET}")
            return {"data": students}
            
    except Exception as e:
        print(f"{C.YELLOW}⚠️ Metode 3 gagal: {e}{C.RESET}")
    
    # ====== METODE 4: Ekstrak manual ======
    try:
        print(f"{C.CYAN}🔍 Mencoba ekstrak manual...{C.RESET}")
        
        students = []
        
        # Cari semua field yang diperlukan
        names = re.findall(r'"nama"\s*:\s*"([^"]*)"', raw)
        genders = re.findall(r'"jenis_kelamin"\s*:\s*"([^"]*)"', raw)
        birthdates = re.findall(r'"tanggal_lahir"\s*:\s*"([^"]*)"', raw)
        nik = re.findall(r'"nik"\s*:\s*"([^"]*)"', raw)
        nisn = re.findall(r'"nisn"\s*:\s*"([^"]*)"', raw)
        rombel = re.findall(r'"rombel"\s*:\s*"([^"]*)"', raw)
        tingkat = re.findall(r'"tingkat"\s*:\s*"([^"]*)"', raw)
        
        # Ambil jumlah minimum
        min_len = min(len(names), len(genders), len(birthdates))
        
        if min_len > 0:
            print(f"{C.CYAN}🔍 Ditemukan {min_len} data siswa{C.RESET}")
            
            for i in range(min_len):
                student = {
                    "nama": names[i] if i < len(names) else "",
                    "jenis_kelamin": genders[i] if i < len(genders) else "",
                    "tanggal_lahir": birthdates[i] if i < len(birthdates) else "",
                    "nik": nik[i] if i < len(nik) else "",
                    "nisn": nisn[i] if i < len(nisn) else "",
                    "rombel": rombel[i] if i < len(rombel) else "",
                    "tingkat": tingkat[i] if i < len(tingkat) else ""
                }
                students.append(student)
            
            if students:
                print(f"{C.GREEN}✅ Berhasil mengekstrak {len(students)} siswa secara manual!{C.RESET}")
                return {"data": students}
            
    except Exception as e:
        print(f"{C.YELLOW}⚠️ Metode 4 gagal: {e}{C.RESET}")
    
    print(f"{C.RED}❌ Gagal memperbaiki file!{C.RESET}")
    return None


def clean_dapodik_data(data):
    """Bersihkan data siswa"""
    if not data:
        return None
    
    # Pastikan formatnya punya key "data"
    if isinstance(data, list):
        students = data
    elif isinstance(data, dict) and "data" in data:
        students = data["data"]
    elif isinstance(data, dict):
        # Coba cari array di dalam dict
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0:
                students = value
                break
        else:
            students = []
    else:
        students = []
    
    # Bersihkan tiap siswa
    cleaned = []
    required_keys = ['nama', 'jenis_kelamin', 'tanggal_lahir', 'nisn']
    
    for i, student in enumerate(students):
        if not isinstance(student, dict):
            continue
        
        # Pastikan semua field ada
        for key in required_keys:
            if key not in student:
                student[key] = ""
        
        # Bersihkan nilai
        for key in student:
            if student[key] is None:
                student[key] = ""
            elif isinstance(student[key], (int, float)):
                student[key] = str(student[key])
            elif isinstance(student[key], str):
                student[key] = student[key].strip()
        
        # Fix NIK (16 digit)
        if 'nik' in student and student['nik']:
            nik = str(student['nik']).strip()
            if len(nik) < 16 and nik.isdigit():
                student['nik'] = nik.zfill(16)
        
        # Fix jenis_kelamin
        if 'jenis_kelamin' in student:
            jk = str(student['jenis_kelamin']).strip().upper()
            if jk in ['L', 'LAKI-LAKI', 'LAKI']:
                student['jenis_kelamin'] = 'L'
            elif jk in ['P', 'PEREMPUAN']:
                student['jenis_kelamin'] = 'P'
            else:
                student['jenis_kelamin'] = jk
        
        cleaned.append(student)
    
    # Tambahkan metadata
    result = {
        "data": cleaned,
        "_metadata": {
            "repaired_by": "SPECTRA DAPODIK FIXER ULTIMATE",
            "version": VERSION,
            "repaired_at": datetime.now().isoformat(),
            "total_entries": len(cleaned),
            "status": "OK"
        }
    }
    
    return result


def save_json(data, original_path):
    """Simpan JSON yang sudah rapi"""
    base, ext = os.path.splitext(original_path)
    output_path = f"{base}_repaired.json"
    
    # Backup
    if os.path.exists(original_path):
        backup_path = f"{original_path}.backup"
        import shutil
        shutil.copy2(original_path, backup_path)
        print(f"{C.DIM}💾 Backup: {backup_path}{C.RESET}")
    
    # Simpan
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)
    
    print(f"{C.GREEN}✅ File disimpan: {output_path}{C.RESET}")
    return output_path


def print_stats(data):
    """Tampilkan statistik"""
    students = data.get("data", [])
    total = len(students)
    
    if total == 0:
        print(f"{C.YELLOW}⚠️ Tidak ada data{C.RESET}")
        return
    
    l_count = sum(1 for s in students if s.get('jenis_kelamin', '').upper() == 'L')
    p_count = total - l_count
    
    kelas = sorted(set(s.get('rombel', '') for s in students if s.get('rombel')))
    
    print(f"""
{C.BLUE}{C.BOLD}📊 STATISTIK DATA:{C.RESET}
  ├─ Total Siswa      : {C.CYAN}{total}{C.RESET}
  ├─ Laki-laki        : {C.BLUE}{l_count}{C.RESET}
  ├─ Perempuan        : {C.MAGENTA}{p_count}{C.RESET}
  └─ Kelas            : {C.YELLOW}{', '.join(kelas[:5])}{'...' if len(kelas)>5 else ''}{C.RESET}
    """)


def main():
    banner()
    
    # Input file
    print(f"\n{C.CYAN}📁 Masukkan path file JSON:{C.RESET}")
    print(f"{C.DIM}  (contoh: db_siswa.json){C.RESET}")
    
    filepath = input("> ").strip().strip('"').strip("'")
    
    if not filepath:
        print(f"{C.YELLOW}⚠️ Path kosong!{C.RESET}")
        return
    
    # Load data
    data = load_dapodik_json(filepath)
    
    if data is None:
        print(f"{C.RED}❌ Gagal memuat data!{C.RESET}")
        return
    
    # Clean data
    print(f"{C.CYAN}🔍 Membersihkan data...{C.RESET}")
    cleaned = clean_dapodik_data(data)
    
    if cleaned is None:
        print(f"{C.RED}❌ Gagal membersihkan data!{C.RESET}")
        return
    
    # Tampilkan statistik
    print_stats(cleaned)
    
    # Simpan
    print(f"\n{C.YELLOW}💾 Simpan hasil? (y/n){C.RESET}")
    choice = input("> ").strip().lower()
    
    if choice == 'y' or choice == 'yes':
        output = save_json(cleaned, filepath)
        print(f"\n{C.GREEN}{C.BOLD}✨ SELESAI! File JSON sudah rapi:{C.RESET}")
        print(f"  {C.CYAN}{output}{C.RESET}")
        print(f"\n{C.GREEN}📁 Total {cleaned.get('_metadata', {}).get('total_entries', 0)} siswa berhasil direpair!{C.RESET}")
    else:
        print(f"{C.CYAN}ℹ️ Data tidak disimpan.{C.RESET}")


def quick_repair(filepath):
    """Repair cepat tanpa interaksi"""
    banner()
    data = load_dapodik_json(filepath)
    if data:
        cleaned = clean_dapodik_data(data)
        if cleaned:
            print_stats(cleaned)
            output = save_json(cleaned, filepath)
            print(f"\n{C.GREEN}✅ Selesai! File: {output}{C.RESET}")
        else:
            print(f"{C.RED}❌ Gagal repair!{C.RESET}")
    else:
        print(f"{C.RED}❌ Gagal memuat!{C.RESET}")


# ============ MAIN ============
if __name__ == "__main__":
    if len(sys.argv) > 1:
        quick_repair(sys.argv[1])
    else:
        main()
