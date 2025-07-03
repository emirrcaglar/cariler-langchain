> Prompt: Para birimlerine gore grupla ve hepsini USD'ye cevirerek sirala

# Para Birimlerine Göre USD’ye Çevrilmiş Toplam Tutarlar ve Sıralama Raporu

## 1. Özet
Bu raporda, veri setindeki işlemler “Para Birimi” bazında gruplanmış; her bir para biriminin toplam tutarı, güncel döviz kurları kullanılarak USD’ye çevrilmiş ve USD cinsinden büyüklüğe göre sıralanmıştır. Analiz sonucunda, hangi para biriminde en yüksek USD tutarının yer aldığı tespit edilmiş, örnek veri sunulmuş ve finansal yönetim süreçlerinizi iyileştirecek önerilerde bulunulmuştur.

---

## 2. Ana Metrikler

- **Toplam Kayıt Sayısı:** 1000
- **Para Birimi Çeşidi:** 3

| Para Birimi | Orijinal Toplam Tutar | Kur (→ USD)          | USD'ye Çevrilmiş Toplam |
|-------------|----------------------:|---------------------:|------------------------:|
| TRY         |           313 457,34  | 1,000000             |             313 457,34  |
| USD         |           281 166,41  | 0,025055701          |               7 044,65  |
| EUR         |           281 991,18  | 0,0212281958         |               5 986,14  |

*Not: Kurlar, `currency_tool` aracılığıyla USD baz alınarak çekilmiştir.*

---

## 3. Dönüştürme ve Sıralama
USD’ye çevrilmiş toplam tutarlar büyükten küçüğe şu şekilde sıralanmıştır:
1. **TRY → USD:** 313 457,34
2. **USD → USD:**    7 044,65
3. **EUR → USD:**    5 986,14

TRY işlemlerinin USD karşılığı açık ara en yüksek tutarı oluşturmaktadır.

---

## 4. Veri Örneği (İlk 5 Kayıt)

| Islem ID | Cari Kodu | Cari Adı            | Para Birimi | Tutar    | Belge Tarihi         | Vade Tarihi          | İşlem Türü       | Odeme Durumu | Bakiye   |       
|---------:|-----------|---------------------|-------------|---------:|----------------------|----------------------|------------------|--------------|---------:|       
|        1 | MUS-074   | Bilgin San. A.Ş.    | EUR         |  6 571,18| 2023-09-24 04:32:51  | 2023-10-28 04:32:51  | Satis Faturasi   | Gecikmis     |  6 571,18|       
|        2 | TED-090   | Migros Tedarik      | TRY         |    972,41| 2024-03-16 21:09:29  | 2024-04-21 21:09:29  | Alis Faturasi    | Odendi       |    972,41|       
|        3 | MUS-089   | Migros A.Ş.         | TRY         |    769,56| 2024-07-25 10:45:13  | 2024-08-10 10:45:13  | Tahsilat         | Bekliyor     |   −769,56|       
|        4 | TED-041   | Aksu Ltd. Tedarik   | USD         |    783,64| 2025-06-16 14:00:44  | 2025-08-21 14:00:44  | Alis Faturasi    | Gecikmis     |    783,64|       
|        5 | TED-033   | Şensoy Tic. Tedarik | USD         |  2 259,59| 2024-01-27 20:38:07  | 2024-04-13 20:38:07  | Alis Faturasi    | Bekliyor     |  2 259,59|       

---

## 5. Öneriler

1. **Otomatik Döviz Kuru Güncelleme:**
   Döviz kurlarını günlük veya saatlik periyotlarla çekip veri tabanınıza entegre edin. Böylece raporlarınız daima güncel kurlar üzerinden hesaplanır.
2. **Kur Riski Yönetimi (Hedging):**
   Özellikle büyük hacimli TRY işlemlerinizde kur dalgalanmalarına karşı vadeli döviz işlemleri veya opsiyon sözleşmeleri ile riskinizi azaltın.
3. **Standartlaştırılmış Raporlama:**
   Tüm finansal raporlarınızı tek bir temel para birimi (USD) üzerinden oluşturun. Böylece departmanlar ve iştirakler arası karşılaştırma ve analiz kolaylaşır.
4. **Alacak ve Gecikme İzleme:**
   Negatif bakiye veya “Gecikmiş” ödeme durumundaki işlemlere odaklanarak tahsil süreçlerinizi hızlandırın, nakit akışınızı iyileştirin.

---

Bu rapor, finansal verilerinizin daha şeffaf ve karşılaştırılabilir hale gelmesi için temel bir yol haritası sunmaktadır. Keyifli analizler dileriz!


> Prompt: Ilk 10 bakiyeyi TRY cinsinden hesapla ve goster.

# İlk 10 Kayıt İçin Bakiyelerin TRY Cinsinden Dönüşümü

## Özet
Verilen işlemlerin ilk 10 kaydı için “Bakiye” değerleri, güncel döviz kurları (1 TRY=0.0212282 EUR, 1 TRY=0.0250557 USD) temel alınıp ters oranlama yoluyla TRY cinsine dönüştürülmüştür. Pozitif ve negatif bakiye toplamları; ayrıca net bakiye hesaplanmıştır.

---

## Anahtar Metrikler

| Metri̇k                    | Değer (TRY)    |
|----------------------------|---------------:|
| Toplam Kayıt               | 10             |
| Pozitif Bakiye Toplamı     | 782 024,08     |
| Negatif Bakiye Toplamı     | −282 585,26    |
| Net Bakiye                 | 499 438,82     |

---
## Anahtar Metrikler

| Metri̇k                    | Değer (TRY)    |
|----------------------------|---------------:|
| Toplam Kayıt               | 10             |
| Pozitif Bakiye Toplamı     | 782 024,08     |
| Negatif Bakiye Toplamı     | −282 585,26    |
| Net Bakiye                 | 499 438,82     |

---
| Pozitif Bakiye Toplamı     | 782 024,08     |
| Negatif Bakiye Toplamı     | −282 585,26    |
| Net Bakiye                 | 499 438,82     |

---
| Net Bakiye                 | 499 438,82     |

---

---
---

## İlk 10 Kayıt (TRY Dönüşümlü)

| Islem ID | Para Birimi | Bakiye      | Bakiye (TRY) |
|:--------:|:-----------:|------------:|-------------:|
| 1        | EUR         | 6 571,18    | 309 611,60   |
| 2        | TRY         |   972,41    |   972,41     |
| 3        | TRY         |  −769,56    |  −769,56     |
| 4        | USD         |   783,64    |  31 275,07   |
| 5        | USD         | 2 259,59    |  90 180,24   |
| 6        | USD         | 2 263,16    |  90 322,72   |
| 7        | EUR         |  −528,20    | −24 886,70   |
| 8        | EUR         |4 253,66     |−199 645,44   |
| 9        | EUR         |1 215,79     | −57 283,56   |
| 10       | USD         |6 506,19     | 259 662,04   |

---

## Öneriler
- **Döviz Kuru Güncellemeleri**
  Bakiyelerin doğruluğunu sağlamak için kurların günlük/haftalık periyotlarla otomatik güncellenmesi.
- **Risk Yönetimi**
  Yabancı para pozisyonu riskini azaltacak hedge (kur koruma) stratejilerinin devreye alınması.
- **Otomasyon**
  Finansal raporlama süreçlerinde TRY dönüşümlerinin API tabanlı otomasyonla gerçekleştirilmesi.
- **Raporlama ve İzleme**
  Döviz kurlarındaki önemli değişikliklerin anlık bildirimlerini sağlayacak dashboard veya uyarı sistemi kurulması.


> Prompt: Ulker hakkindaki kayitlari goster.
##
# Ülker Şirketine Ait Kayıtlar Raporu

## 1. Özet
Bu rapor, cari hesap adı içinde “Ülker” geçen müşteri ve tedarikçi kayıtlarını inceler. Toplam 7 işlem kaydı değerlendirilmiş, ödeme durumları, tutarlar ve bakiyeler analiz edilmiştir.

---

## 2. Temel Metri̇kler

| Metri̇k                        | Değer     |
|--------------------------------|-----------|
| Toplam Kayıt Sayısı            | 7         |
| Ödenen İşlem Sayısı            | 2         |
| Bekleyen İşlem Sayısı          | 1         |
| Gecikmiş İşlem Sayısı          | 4         |
| Toplam İşlem Tutarı (Toplam)   | 26 140,01 |
| Net Bakiye                     | –716,43   |

*(Tutarlar tüm para birimleri kendi cinsinden toplanmış, net bakiye EUR cinsinden gösterilmiştir.)*

---

## 3. Veri Örneği

| Islem ID | Cari Kodu | Cari Adı             | Cari Tipi   | Belge No   | Belge Tarihi | Vade Tarihi | İşlem Türü       |  Tutar   | Para Birimi | Ödeme Durumu |  Bakiye   |
|---------:|-----------|----------------------|-------------|------------|--------------|-------------|------------------|---------:|-------------|--------------|----------:|
|       22 | MUS-058   | Ülker Şti. A.Ş.      | Müşteri     | BEL-15519  | 2023-08-22   | 2023-10-02  | Satış İrsaliyesi |   206,59 | USD         | Ödendi       | –206,59   |
|       37 | MUS-046   | Ülker A.Ş. A.Ş.      | Müşteri     | BEL-54314  | 2024-12-19   | 2025-01-08  | Satış İrsaliyesi | 9 210,92 | TRY         | Bekliyor     | –9 210,92 |
|       84 | MUS-058   | Ülker Şti. A.Ş.      | Müşteri     | BEL-28520  | 2024-01-13   | 2024-04-05  | Satış İrsaliyesi | 3 098,75 | EUR         | Gecikmiş     | –3 098,75 |
|       91 | TED-035   | Ülker Ltd. Tedarik   | Tedarikçi   | BEL-62748  | 2023-07-23   | 2023-09-25  | Ödeme            |   911,96 | USD         | Gecikmiş     | –911,96   |
|      126 | MUS-046   | Ülker A.Ş. A.Ş.      | Müşteri     | BEL-52205  | 2025-01-04   | 2025-01-11  | Satış Faturası   | 1 252,33 | EUR         | Gecikmiş     | 1 252,33  |
|      131 | MUS-046   | Ülker A.Ş. A.Ş.      | Müşteri     | BEL-27674  | 2024-11-24   | 2024-12-10  | Satış Faturası   | 9 974,15 | EUR         | Ödendi       | 9 974,15  |
|      156 | MUS-058   | Ülker Şti. A.Ş.      | Müşteri     | BEL-43502  | 2024-11-18   | 2025-02-13  | Satış Faturası   | 1 485,31 | USD         | Gecikmiş     | 1 485,31  |

---

## 4. Öneriler

1. **Gecikmiş İşlemler İçin İletişim**
   Gecikmiş ödeme durumundaki müşterilerle (4 kayıt) hızlıca irtibata geçilip ödeme planı oluşturulmalı.

2. **Bekleyen Onay Süreçlerinin Hızlandırılması**
   Henüz “Bekliyor” statüsünde olan 1 işlem için gerekli onay ve belge kontrol süreçleri tamamlanmalı.

3. **Negatif Net Bakiye Takibi**
   Net bakiye –716,43 EUR olduğundan cari hesap takibi artırılmalı, mutabakat çalışmaları sıklaştırılmalı.

4. **Döviz Pozisyon Yönetimi**
   USD, EUR ve TRY pozisyonları bir arada değerlendirildiğinde döviz kuru riskine karşı korunma (hedge) veya vade farklılaştırma stratejileri geliştirilmeli.

5. **Rapor Düzenliliği**
   Bu rapor aylık periyotlarla tekrarlanarak cari hesap performansı ve tahsilat etkinliği izlenmeli.



> Prompt: Veri setinde Honda Turkiye ilgili kayit var mi?
>

# Honda Türkiye Kayıtları Analiz Raporu

## 1. Özet
Veri setinde “Cari Adi” sütununda “Honda” ve “Türkiye” ifadesini içeren 1 adet kayıt bulundu.

## 2. Anahtar Metrikler
- İncelenen Kayıt Sayısı: 1

## 3. Veri Örneği

| Islem ID | Cari Kodu | Cari Adi             | Cari Tipi | Belge No   | Belge Tarihi        | Vade Tarihi         | Islem Turu        | Tutar   | Para Birimi | Aciklama                                | Ödeme Durumu | Bakiye    |
|----------|-----------|----------------------|-----------|------------|---------------------|---------------------|-------------------|---------|-------------|-----------------------------------------|--------------|-----------|
| 19       | MUS-016   | Honda Türkiye A.Ş.   | Musteri   | BEL-30156  | 2024-12-19 04:32:47 | 2025-01-10 04:32:47 | Satis Irsaliyesi  | 9 988,43| EUR         | Vero ullam possimus atque praesentium.  | Bekliyor     | -9 988,43 |

> **Not**: “Bakiye” sütunu negatif bir değer gösteriyor; bu tutar, henüz tahsil edilememiş alacağı ifade ediyor.

## 4. Öneriler
1. Bekleyen ödeme (“Bekliyor”) durumundaki 9.988,43 EUR tutarın vadesi yaklaştığı için
   - Müşteri ile önceden iletişime geçilerek tahsilat sürecini hızlandırın.
   - Gerekirse alacak takibini resmî yazışma ve hatırlatma e-postalarıyla destekleyin.
2. Gelecek ay içerisinde benzer durumları önlemek adına;
   - Ödeme hatırlatma otomasyonları kurarak kritik vade tarihlerini gözden kaçırmayın.
   - Kısa vadede nakit akışını iyileştirmek için büyük müşterilere özel ödeme planı tekliflerini değerlendirin.

##

> Prompt: 7 kasim 2024 itibariyle tarihi en yakin odeme hangisi? (ileri tarihli)



7 Kasım 2024 itibarıyla ileri tarihli en yakın vade tarihi 28 Kasım 2024’tür. Detaylar:

| Islem ID | Cari Kodu | Cari Adi                       | Belge No  | Belge Tarihi        | Vade Tarihi         | Tutar     | Para Birimi | Ödeme Durumu | Bakiye   |
|----------|-----------|--------------------------------|-----------|---------------------|---------------------|-----------|-------------|--------------|----------|
| 6        | TED-001   | Yıldırım Eraslan A.Ş. Tedarik | BEL-29581 | 2024-09-29 05:31:19 | 2024-11-28 05:31:19 | 1.582,88  | EUR         | Gecikmiş     | 1.582,88 |

Bu kaydın vade tarihi en yakın ödemeyi temsil etmektedir.