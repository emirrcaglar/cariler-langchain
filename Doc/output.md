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