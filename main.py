#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SPECTRA JSON REPAIR - ULTIMATE EDITION
AUTO DETECT: DAPODIK / BPJS / CSV / GENERIC JSON
BY: CELI SANTINEL
"""

import json
import re
import os
import sys
import csv
import shutil
from datetime import datetime

# ============ KONFIGURASI ============
VERSION = "SPECTRA-FIXER-v5.0"

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

# ============================================================
# BANNER
# ============================================================
def banner():
    print(f"""
{C.MAGENTA}{C.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║                   SPECTRA JSON REPAIR                         ║
║         AUTO DETECT: JENIS FILE JSON CSV / GENERIC            ║
║                    BY: CELI SANTINEL                          ║
╚═══════════════════════════════════════════════════════════════╝
{C.RESET}""")

# ============================================================
# AUTO DETECT TIPE DATA
# ============================================================
def detect_type(data):
    """Detect tipe data: dapodik / bpjs / csv / generic"""
    
    # Ambil sample pertama
    sample = None
    
    if isinstance(data, list) and data:
        sample = data[0]
    elif isinstance(data, dict):
        if "data" in data and isinstance(data["data"], list) and data["data"]:
            sample = data["data"][0]
        else:
            sample = data
    
    if not isinstance(sample, dict):
        return "generic", 0
    
    # Normalisasi keys (lowercase)
    keys = [k.lower() for k in sample.keys()]
    keys_str = " ".join(keys)
    
    # ===== DETEKSI DAPODIK =====
    dapodik_signature = ["nama", "jenis_kelamin", "nisn", "rombel", "tingkat"]
    dapodik_score = sum(1 for sig in dapodik_signature if sig in keys_str)
    
    if dapodik_score >= 3:
        return "dapodik", dapodik_score
    
    # ===== DETEKSI BPJS =====
    bpjs_signature = ["nik", "name", "gender", "birthdate", "phone", "address", "district"]
    bpjs_score = sum(1 for sig in bpjs_signature if sig in keys_str)
    
    if bpjs_score >= 3:
        return "bpjs", bpjs_score
    
    # ===== DETEKSI CSV-USER (CHINA) =====
    csv_signature = ["id", "group", "nickname", "mobile", "avatar", "logintime"]
    csv_score = sum(1 for sig in csv_signature if sig in keys_str)
    
    if csv_score >= 3:
        return "csv_user", csv_score
    
    return "generic", 0

# ============================================================
# LOAD FILE
# ============================================================
def load_json_file(filepath):
    """Load file JSON dengan berbagai metode"""
    print(f"{C.CYAN}📂 Memuat: {filepath}{C.RESET}")
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            raw = f.read()
    except FileNotFoundError:
        print(f"{C.RED}❌ File tidak ditemukan!{C.RESET}")
        return None
    except Exception as e:
        print(f"{C.RED}❌ Error baca file: {e}{C.RESET}")
        return None
    
    # ===== METODE 1: Parse langsung =====
    try:
        data = json.loads(raw)
        print(f"{C.GREEN}✅ JSON valid!{C.RESET}")
        return data
    except json.JSONDecodeError as e:
        print(f"{C.YELLOW}⚠️ JSON Error: {e}{C.RESET}")
        print(f"{C.CYAN}🔧 Mencoba repair...{C.RESET}")
    
    # ===== METODE 2: Fix trailing comma =====
    try:
        fixed = re.sub(r',(\s*[}\]])', r'\1', raw)
        data = json.loads(fixed)
        print(f"{C.GREEN}✅ JSON fixed (trailing comma)!{C.RESET}")
        return data
    except:
        pass
    
    # ===== METODE 3: Fix newline dalam string =====
    try:
        fixed = re.sub(r'(?<!\\)\n', ' ', raw)
        fixed = re.sub(r',(\s*[}\]])', r'\1', fixed)
        data = json.loads(fixed)
        print(f"{C.GREEN}✅ JSON fixed (newline)!{C.RESET}")
        return data
    except:
        pass
    
    # ===== METODE 4: Extract per object =====
    try:
        print(f"{C.CYAN}🔍 Ekstrak per object...{C.RESET}")
        
        # Cari pattern { ... }
        pattern = r'\{[^{}]*\}'
        matches = re.findall(pattern, raw)
        
        objects = []
        for match in matches:
            try:
                cleaned = re.sub(r',(\s*[}\]])', r'\1', match.strip())
                obj = json.loads(cleaned)
                objects.append(obj)
            except:
                continue
        
        if objects:
            print(f"{C.GREEN}✅ Berhasil ekstrak {len(objects)} objects!{C.RESET}")
            return objects
    except:
        pass
    
    print(f"{C.RED}❌ Gagal memperbaiki file!{C.RESET}")
    return None

# ============================================================
# CLEAN DAPODIK
# ============================================================
def clean_dapodik(data):
    """Bersihkan data Dapodik"""
    students = extract_list(data)
    cleaned = []
    
    for student in students:
        if not isinstance(student, dict):
            continue
        
        # Normalisasi keys (case-insensitive)
        norm = normalize_keys(student)
        
        cleaned.append({
            "nama": norm.get("nama", ""),
            "jenis_kelamin": fix_gender(norm.get("jenis_kelamin", "")),
            "tanggal_lahir": norm.get("tanggal_lahir", ""),
            "nik": fix_nik(norm.get("nik", "")),
            "nisn": norm.get("nisn", ""),
            "rombel": norm.get("rombel", ""),
            "tingkat": norm.get("tingkat", "")
        })
    
    return cleaned

# ============================================================
# CLEAN BPJS
# ============================================================
def clean_bpjs(data):
    """Bersihkan data BPJS"""
    records = extract_list(data)
    cleaned = []
    
    for item in records:
        if not isinstance(item, dict):
            continue
        
        norm = normalize_keys(item)
        
        cleaned.append({
            "nik": convert_nik(norm.get("nik (id card)") or norm.get("nik")),
            "nama": norm.get("name", ""),
            "gender": norm.get("gender", ""),
            "tanggal_lahir": norm.get("birthdate", ""),
            "no_hp": convert_phone(norm.get("phone number") or norm.get("phone")),
            "alamat": norm.get("address", ""),
            "kelurahan": norm.get("subdistrict", ""),
            "kecamatan": norm.get("district", ""),
            "kota": norm.get("city", "")
        })
    
    return cleaned

# ============================================================
# CLEAN CSV USER (CHINA)
# ============================================================
def clean_csv_user(data):
    """Bersihkan data CSV User China"""
    records = extract_list(data)
    cleaned = []
    
    for item in records:
        if not isinstance(item, dict):
            continue
        
        norm = normalize_keys(item)
        
        cleaned.append({
            "id": norm.get("id", ""),
            "group": clean_html(norm.get("group", "")),
            "nickname": clean_html(norm.get("nickname", "")),
            "mobile": norm.get("mobile", ""),
            "avatar": extract_avatar(norm.get("avatar", "")),
            "logintime": norm.get("logintime", ""),
            "jointime": norm.get("jointime", ""),
            "status": clean_html(norm.get("status", ""))
        })
    
    return cleaned

# ============================================================
# CLEAN GENERIC
# ============================================================
def clean_generic(data):
    """Bersihkan data generic"""
    records = extract_list(data)
    cleaned = []
    
    for item in records:
        if not isinstance(item, dict):
            continue
        
        new_item = {}
        for key, value in item.items():
            if value is None:
                new_item[key] = ""
            elif isinstance(value, (int, float)):
                new_item[key] = value
            elif isinstance(value, str):
                new_item[key] = value.strip()
            else:
                new_item[key] = str(value)
        
        cleaned.append(new_item)
    
    return cleaned

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def extract_list(data):
    """Extract list dari berbagai format"""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list) and value:
                return value
        return [data]
    return []

def normalize_keys(item):
    """Normalisasi keys — lowercase"""
    return {k.lower().strip(): v for k, v in item.items()}

def clean_html(text):
    """Hapus HTML tag"""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', str(text))
    return re.sub(r'\s+', ' ', text).strip()

def extract_avatar(text):
    """Extract URL avatar dari HTML"""
    if not text:
        return ""
    match = re.search(r'src="([^"]+)"', str(text))
    return match.group(1) if match else ""

def convert_nik(nik_raw):
    """Convert NIK dari scientific notation"""
    if not nik_raw:
        return ""
    if isinstance(nik_raw, float):
        nik_str = f"{nik_raw:.0f}"
    else:
        nik_str = str(nik_raw)
    nik_str = re.sub(r'[^0-9]', '', nik_str)
    return nik_str if nik_str else ""

def convert_phone(phone_raw):
    """Convert Phone dari scientific notation"""
    if not phone_raw:
        return ""
    if isinstance(phone_raw, float):
        phone_str = f"{phone_raw:.0f}"
    else:
        phone_str = str(phone_raw)
    phone_str = re.sub(r'[^0-9]', '', phone_str)
    return phone_str if phone_str else ""

def fix_gender(gender):
    """Fix jenis kelamin"""
    g = str(gender).strip().upper()
    if g in ['L', 'LAKI-LAKI', 'LAKI', 'MALE', 'M']:
        return 'L'
    elif g in ['P', 'PEREMPUAN', 'FEMALE', 'F']:
        return 'P'
    return g

def fix_nik(nik):
    """Fix NIK jadi 16 digit"""
    if not nik:
        return ""
    nik = str(nik).strip()
    if nik.isdigit() and len(nik) < 16:
        return nik.zfill(16)
    return nik

# ============================================================
# SAVE FILE
# ============================================================
def save_json(data, original_path, data_type):
    """Simpan JSON yang sudah rapi"""
    base, ext = os.path.splitext(original_path)
    output_path = f"{base}_repaired.json"
    
    # Backup
    if os.path.exists(original_path):
        backup_path = f"{original_path}.backup"
        shutil.copy2(original_path, backup_path)
        print(f"{C.DIM}💾 Backup: {backup_path}{C.RESET}")
    
    # Wrap dengan metadata
    result = {
        "_metadata": {
            "repaired_by": "SPECTRA FIXER ULTIMATE",
            "version": VERSION,
            "type": data_type,
            "repaired_at": datetime.now().isoformat(),
            "total_entries": len(data),
            "status": "OK"
        },
        "data": data
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"{C.GREEN}✅ File disimpan: {output_path}{C.RESET}")
    return output_path

# ============================================================
# STATISTIK
# ============================================================
def print_stats(data, data_type):
    """Tampilkan statistik"""
    total = len(data)
    
    if total == 0:
        print(f"{C.YELLOW}⚠️ Tidak ada data{C.RESET}")
        return
    
    print(f"""
{C.BLUE}{C.BOLD}📊 STATISTIK DATA:{C.RESET}
  ├─ Tipe Data       : {C.MAGENTA}{data_type.upper()}{C.RESET}
  ├─ Total Records   : {C.CYAN}{total}{C.RESET}
""")
    
    if data_type == "dapodik":
        l_count = sum(1 for s in data if s.get('jenis_kelamin', '').upper() == 'L')
        p_count = total - l_count
        print(f"  ├─ Laki-laki       : {C.BLUE}{l_count}{C.RESET}")
        print(f"  └─ Perempuan       : {C.MAGENTA}{p_count}{C.RESET}")
    
    elif data_type == "bpjs":
        pria = sum(1 for x in data if x.get('gender', '').lower() == 'laki-laki')
        wanita = sum(1 for x in data if x.get('gender', '').lower() == 'perempuan')
        print(f"  ├─ Pria            : {C.BLUE}{pria}{C.RESET}")
        print(f"  └─ Wanita          : {C.MAGENTA}{wanita}{C.RESET}")
    
    elif data_type == "csv_user":
        with_avatar = sum(1 for x in data if x.get('avatar'))
        print(f"  └─ Punya Avatar    : {C.GREEN}{with_avatar}{C.RESET}")

# ============================================================
# MAIN
# ============================================================
def main():
    banner()
    
    print(f"\n{C.CYAN}📁 Masukkan path file JSON:{C.RESET}")
    print(f"{C.DIM}  (contoh: data.json / data.csv.json){C.RESET}")
    
    filepath = input("> ").strip().strip('"').strip("'")
    
    if not filepath:
        print(f"{C.YELLOW}⚠️ Path kosong!{C.RESET}")
        return
    
    # Load
    data = load_json_file(filepath)
    if data is None:
        return
    
    # ===== AUTO DETECT =====
    print(f"\n{C.CYAN}🔍 Auto-detect tipe data...{C.RESET}")
    data_type, score = detect_type(data)
    print(f"{C.GREEN}✅ Terdeteksi: {C.MAGENTA}{data_type.upper()}{C.RESET} {C.DIM}(score: {score}){C.RESET}")
    
    # ===== CLEAN SESUAI TIPE =====
    print(f"{C.CYAN}🔧 Membersihkan data...{C.RESET}")
    
    if data_type == "dapodik":
        cleaned = clean_dapodik(data)
    elif data_type == "bpjs":
        cleaned = clean_bpjs(data)
    elif data_type == "csv_user":
        cleaned = clean_csv_user(data)
    else:
        cleaned = clean_generic(data)
    
    if not cleaned:
        print(f"{C.RED}❌ Gagal membersihkan data!{C.RESET}")
        return
    
    # Statistik
    print_stats(cleaned, data_type)
    
    # Simpan
    print(f"\n{C.YELLOW}💾 Simpan hasil? (y/n){C.RESET}")
    choice = input("> ").strip().lower()
    
    if choice in ['y', 'yes']:
        output = save_json(cleaned, filepath, data_type)
        print(f"\n{C.GREEN}{C.BOLD}✨ SELESAI!{C.RESET}")
        print(f"  {C.CYAN}{output}{C.RESET}")
        print(f"\n{C.GREEN}📁 Total {len(cleaned)} records berhasil direpair!{C.RESET}")
    else:
        print(f"{C.CYAN}ℹ️ Data tidak disimpan.{C.RESET}")

# ============================================================
# QUICK REPAIR (CLI ARG)
# ============================================================
def quick_repair(filepath):
    banner()
    data = load_json_file(filepath)
    if not data:
        return
    
    data_type, score = detect_type(data)
    print(f"{C.GREEN}✅ Terdeteksi: {C.MAGENTA}{data_type.upper()}{C.RESET}")
    
    if data_type == "dapodik":
        cleaned = clean_dapodik(data)
    elif data_type == "bpjs":
        cleaned = clean_bpjs(data)
    elif data_type == "csv_user":
        cleaned = clean_csv_user(data)
    else:
        cleaned = clean_generic(data)
    
    if cleaned:
        print_stats(cleaned, data_type)
        output = save_json(cleaned, filepath, data_type)
        print(f"\n{C.GREEN}✅ Selesai! File: {output}{C.RESET}")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        quick_repair(sys.argv[1])
    else:
        main()
