from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker('tr_TR')

sirketler = [fake.company() + ' A.Ş.' for _ in range(20)]
tedarikciler = [fake.company() + ' Tedarik' for _ in range(10)]

def rastgele_tarih():
    return fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')

data = {
    'Islem ID': [],
    'Cari Kodu': [],
    'Cari Adi': [],
    'Cari Tipi': [],
    'Belge No': [],
    'Belge Tarihi': [],
    'Vade Tarihi': [],
    'Islem Turu': [],
    'Tutar': [],
    'Para Birimi': [],
    'Aciklama': [],
    'Odeme Durumu': [],
    'Bakiye': []
}

for i in range(1, 201):
    cari_tipi = random.choice(['Musteri', 'Tedarikci'])
    
    if cari_tipi == 'Musteri':
        cari_adi = random.choice(sirketler)  
        islem_turu = random.choice(['Satis Faturasi', 'Satis Irsaliyesi', 'Tahsilat'])
        cari_kodu = f"MUS-{sirketler.index(cari_adi)+1:03d}"  
    else:
        cari_adi = random.choice(tedarikciler)  
        islem_turu = random.choice(['Alis Faturasi', 'Alis Irsaliyesi', 'Odeme'])
        cari_kodu = f"TED-{tedarikciler.index(cari_adi)+1:03d}"  
    
    belge_tarihi = rastgele_tarih()
    vade_tarihi = (datetime.strptime(belge_tarihi, '%Y-%m-%d %H:%M:%S') + 
                  timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d %H:%M:%S')
    
    tutar = round(random.uniform(100, 10000), 2)
    
    if islem_turu in ['Satis Faturasi', 'Alis Faturasi']:
        bakiye = tutar
    else:
        bakiye = -tutar
    
    data['Islem ID'].append(i)
    data['Cari Kodu'].append(cari_kodu)
    data['Cari Adi'].append(cari_adi)
    data['Cari Tipi'].append(cari_tipi)
    data['Belge No'].append(f"BEL-{fake.unique.random_number(digits=5)}")
    data['Belge Tarihi'].append(belge_tarihi)
    data['Vade Tarihi'].append(vade_tarihi)
    data['Islem Turu'].append(islem_turu)
    data['Tutar'].append(tutar)
    data['Para Birimi'].append(random.choice(['TRY', 'USD', 'EUR']))
    data['Aciklama'].append(fake.sentence())
    data['Odeme Durumu'].append(random.choice(['Odendi', 'Bekliyor', 'Gecikmis']))
    data['Bakiye'].append(bakiye)

df = pd.DataFrame(data)

import os

if not os.path.exists('data'):
    os.makedirs('data')

output_path = 'data/cari_hesap_hareketleri.csv'
df.to_csv(output_path, index=False)

print(f"CSV dosyası başarıyla oluşturuldu: {output_path}")
print(f"Toplam {len(sirketler)} müşteri ve {len(tedarikciler)} tedarikçi kullanıldı.")
print("Her bir şirket ortalama", round(200/(len(sirketler)+len(tedarikciler)), 1), "kez tekrar etti.")