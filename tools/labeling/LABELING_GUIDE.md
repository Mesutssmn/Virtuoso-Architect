# 🏷️ MIDI Etiketleme Rehberi

## Kategori Belirleme Kuralları

### 0️⃣ FAR REACH (Geniş El Açıklığı)
**Ne zaman seçilir:**
- max_stretch > 15-20 (büyük aralıklar)
- max_chord_size büyük (6+)
- Rachmaninoff, Liszt gibi geniş el gerektiren eserler

**Örnek:** max_stretch: 50 → Far Reach

---

### 1️⃣ DOUBLE THIRDS (Üçlü Diziler)
**Ne zaman seçilir:**
- thirds_frequency > 0.20-0.25 (çok üçlü var)
- note_density yüksek (hızlı notalar)
- Chopin Etudes gibi teknik çalışmalar

**Örnek:** thirds_frequency: 0.28 → Double Thirds

---

### 2️⃣ MULTIPLE VOICES (Polifoni)
**Ne zaman seçilir:**
- poly_voice_count > 2-3 (çok ses)
- polyrhythm_score yüksek
- Bach Fugues gibi çok sesli eserler

**Örnek:** poly_voice_count: 4.5 → Multiple Voices

---

### 3️⃣ ADVANCED CHORDS (Yoğun Akorlar)
**Ne zaman seçilir:**
- max_chord_size > 7-8 (büyük akorlar)
- note_density yüksek
- Brahms, Scriabin gibi yoğun armoni

**Örnek:** max_chord_size: 10 → Advanced Chords

---

### 4️⃣ ADVANCED COUNTERPOINT (Hassasiyet/Bağımsızlık)
**Ne zaman seçilir:**
- left_hand_activity dengeli (~0.4-0.5)
- octave_jump_frequency yüksek
- Mozart, Haydn gibi klasik dönem

**Örnek:** left_hand_activity: 0.45 ve octave_jump_frequency: 0.35 → Advanced Counterpoint

---

## 📊 HIZLI KARAR TABLOSU

```
┌─────────────────────────┬─────────────┬───────────────┬─────────────────┬─────────────────┬──────────────┐
│ Feature                 │ Far Reach   │ Double Thirds │ Multiple Voices │ Advanced Chords │ Counterpoint │
├─────────────────────────┼─────────────┼───────────────┼─────────────────┼─────────────────┼──────────────┤
│ max_stretch             │   >20 ★     │    10-15      │     10-15       │     15-20       │    10-15     │
├─────────────────────────┼─────────────┼───────────────┼─────────────────┼─────────────────┼──────────────┤
│ thirds_frequency        │  0.15-0.20  │   >0.25 ★     │    0.15-0.20    │    0.15-0.20    │   0.18-0.22  │
├─────────────────────────┼─────────────┼───────────────┼─────────────────┼─────────────────┼──────────────┤
│ poly_voice_count        │    1-2      │     1-2       │      >3 ★       │      2-3        │     2-3      │
├─────────────────────────┼─────────────┼───────────────┼─────────────────┼─────────────────┼──────────────┤
│ max_chord_size          │    6-8      │     4-6       │      4-6        │      >8 ★       │     4-6      │
├─────────────────────────┼─────────────┼───────────────┼─────────────────┼─────────────────┼──────────────┤
│ left_hand_activity      │  0.3-0.4    │   0.3-0.4     │    0.35-0.45    │    0.35-0.45    │  0.4-0.5 ★   │
├─────────────────────────┼─────────────┼───────────────┼─────────────────┼─────────────────┼──────────────┤
│ octave_jump_frequency   │  0.2-0.3    │   0.2-0.3     │    0.25-0.35    │    0.25-0.35    │  0.3-0.4 ★   │
└─────────────────────────┴─────────────┴───────────────┴─────────────────┴─────────────────┴──────────────┘

★ = En önemli indicator (dominant feature)
```

---

## 💡 PRATIK İPUÇLARI

1. **Dominant Feature'a bak**: Hangi feature en çok öne çıkıyor?
2. **Dosya adına bak**: Besteci adı ipucu verebilir
3. **Tutarlı ol**: Benzer feature'lara benzer etiket ver
4. **Emin değilsen**: En yakın kategoriyi seç, sonra düzeltebilirsin

---

## 🎯 ÖRNEK KARARLAR

**Örnek 1:**
```
max_stretch: 45.2
thirds_frequency: 0.18
poly_voice_count: 1.8
max_chord_size: 7
left_hand_activity: 0.35
```
→ **Far Reach** (max_stretch çok yüksek!)

---

**Örnek 2:**
```
max_stretch: 12.5
thirds_frequency: 0.32
poly_voice_count: 1.5
max_chord_size: 5
left_hand_activity: 0.38
```
→ **Double Thirds** (thirds_frequency dominant!)

---

**Örnek 3:**
```
max_stretch: 14.0
thirds_frequency: 0.19
poly_voice_count: 4.2
max_chord_size: 6
left_hand_activity: 0.42
```
→ **Multiple Voices** (poly_voice_count yüksek!)

---

**Örnek 4:**
```
max_stretch: 18.0
thirds_frequency: 0.17
poly_voice_count: 2.5
max_chord_size: 11
left_hand_activity: 0.40
```
→ **Advanced Chords** (max_chord_size çok büyük!)

---

**Örnek 5:**
```
max_stretch: 13.0
thirds_frequency: 0.20
poly_voice_count: 2.8
max_chord_size: 5
left_hand_activity: 0.48
octave_jump_frequency: 0.38
```
→ **Advanced Counterpoint** (dengeli, octave jumps yüksek!)

---

## 🚀 BAŞLARKEN

1. İlk 10-20 dosyayı etiketle
2. Pattern'i yakala
3. Hızlan!
4. Emin olmadığın dosyaları atlayabilirsin (→ tuşu ile)

**Keyboard Shortcuts:**
- 1-5: Kategori seç
- →: Sonraki dosya
- ←: Önceki dosya

İyi etiketlemeler! 🎹
