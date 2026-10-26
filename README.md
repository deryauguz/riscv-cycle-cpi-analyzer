# RISC-V Komut Çevrim ve CPI Analiz Motoru

## Proje Hakkında

Bu proje, RISC-V mimarisine ait temel komut kümesi (RV32I/RV64I) talimatlarının yürütme dinamiklerini incelemek, çevrim maliyetlerini (Cycle Costs) modellemek ve ortalama çevrim başına komut (Cycles Per Instruction - CPI) değerini hesaplamak amacıyla Python ile geliştirilmiş bir analiz ve profil çıkarma aracıdır.

Herhangi bir harici kütüphane bağımlılığı bulunmayan araç, girdi olarak verilen sembolik RISC-V kodlarını sözdizimsel olarak ayrıştırır (parsing), talimatları mimari kategorilerine göre sınıflandırır ve işlemci performansına ilişkin ayrıntılı bir yürütme raporu oluşturur.

---

## Temel Özellikler

* **Komut Sınıflandırma ve Ayrıştırma:**
  * Kod satırlarındaki etiketler, boşluklar ve yorum satırları (`#`, `;`) düzenli ifadeler (regex) ile temizlenir[cite: 9].
  * Opcode belirteçleri incelenerek talimatlar ALU, LOAD, STORE, BRANCH, JUMP veya OTHER kategorilerine ayrılır[cite: 9].
* **Mimari Çevrim Maliyet Modellemesi:**
  * İşlemci mimarisi gecikme süreleri baz alınarak her kategoriye özgü donanım yürütme maliyeti (Cycle Cost) atanır[cite: 9]:
    * **ALU (1 Çevrim):** `add`, `sub`, `and`, `or`, `xor`, `addi`, `sll` vb[cite: 9].
    * **LOAD (4 Çevrim):** `lw`, `lh`, `lb`, `lbu`, `lhu`[cite: 9]
    * **STORE (4 Çevrim):** `sw`, `sh`, `sb`[cite: 9]
    * **BRANCH (3 Çevrim):** `beq`, `bne`, `blt`, `bge`, `bltu`, `bgeu`[cite: 9]
    * **JUMP (3 Çevrim):** `jal`, `jalr`[cite: 9]
* **Performans ve Maliyet Raporlama:**
  * Toplam işlenen komut adedi (Instruction Count) hesaplanır[cite: 9].
  * Toplam yürütme çevrimi (Total Cycles) ve işlemcinin ortalama CPI değeri matematiksel olarak raporlanır[cite: 9].
  * Komut bazında satır satır izleme günlüğü (Trace Log) dökümü sunulur[cite: 9].

---

## Örnek Rapor Çıktısı

Uygulama çalıştırıldığında terminale aşağıdaki formatta yapılandırılmış analiz dökümü sunulmaktadır[cite: 9]:

```text
=================================================================
          RISC-V PERFORMANS VE MALİYET ANALİZ RAPORU
=================================================================
Toplam Komut Sayısı (Instruction Count) : 9
Toplam Hesaplanan Maliyet (Total Cycles): 21 Cycle
Ortalama Komut Başına Döngü (CPI)      : 2.33
-----------------------------------------------------------------

[1] KOMUT GRUBU MALİYET DAĞILIMI:
Kategori   | Birim Maliyet  | Komut Adedi  | Toplam Maliyet (Cycle)
-----------------------------------------------------------------
ALU        | 1              | 4            | 4
LOAD       | 4              | 2            | 8
STORE      | 4              | 1            | 4
BRANCH     | 3              | 1            | 3
JUMP       | 3              | 1            | 3

[2] AYRINTILI KOMUT İZLEME (TRACE LOG):
Satır/Komut                    | Grubu    | Maliyet
--------------------------------------------------
addi x5, x0, 5                 | ALU      | 1 Cycle
addi x6, x0, 10                | ALU      | 1 Cycle
add  x7, x5, x6                | ALU      | 1 Cycle
lw   x10, 0(x5)                | LOAD     | 4 Cycle
lw   x11, 4(x5)                | LOAD     | 4 Cycle
sw   x10, 0(x6)                | STORE    | 4 Cycle
beq  x5, x6, 12                | BRANCH   | 3 Cycle
jal  x1, 100                   | JUMP     | 3 Cycle
sub  x7, x7, x5                | ALU      | 1 Cycle
=================================================================
