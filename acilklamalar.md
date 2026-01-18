# Kod Açıklamaları - Beach Nourishment Design Tool

Bu belge, `app.py` ve `profile_module.py` dosyalarındaki kodları hiç Python veya Streamlit bilmeyen birine anlatmak için hazırlanmıştır.

---

## 📋 GENEL YAPISI

Uygulama iki ana dosyadan oluşur:

1. **`app.py`** - Ana uygulama dosyası
   - Landing page (giriş sayfası)
   - Project page (proje veri giriş sayfası)
   - Dalga, sediman, yapısal elemanlar ve maliyet verilerini toplar

2. **`profile_module.py`** - Kesit analizi modülü
   - Harita ile nokta seçimi
   - Batimetri verilerini NetCDF'den okuma (`final_veri.nc` formatı)
   - **Otomatik tasarım profili oluşturma** (parabol formülü ile)
   - Kesit profilleri oluşturma ve karşılaştırma
   - Sill (eşik) konumu hesaplama ve görselleştirme
   - Grafikler ve görselleştirme

---

## 📁 app.py - ANA UYGULAMA DOSYASI

### Satır 1-2: Kütüphaneleri Yükleme

```python
import streamlit as st
import profile_module as profile
```

**Ne yapıyor?**
- `streamlit`: Web sayfası oluşturmak için kullanılan ana kütüphane
- `profile_module`: Kesit analizi için hazırladığımız modülü import ediyoruz
- `as profile`: Modülü kısaca "profile" olarak çağıracağız

**Basit anlatım:** Gerekli araçları çekmeceden çıkarıyoruz.

---

### Satır 4-7: Sayfa Ayarları

```python
st.set_page_config(
    page_title="Beach Nourishment Design Tool", 
    layout="wide", 
)
```

**Ne yapıyor?**
- `page_title`: Tarayıcı sekmesinde görünecek başlık
- `layout="wide"`: Sayfayı tam genişlikte aç (dar mod yerine)

**Önemli:** Bu satırlar her zaman kodun en başında olmalı!

---

### Satır 9-11: Sayfa Durumunu Takip Etme

```python
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
```

**Ne yapıyor?**
- `st.session_state`: Streamlit'in hafızası. Sayfa yenilendiğinde bile bilgileri saklar.
- `'page'`: Hangi sayfada olduğumuzu tutan değişken
- İlk açılışta `'landing'` (ana sayfa) olarak ayarlıyoruz

**Neden önemli?** Kullanıcı "Start Project" butonuna bastığında farklı sayfa göstermemiz lazım.

---

### Satır 13-19: Sayfa Geçiş Fonksiyonları

```python
def switch_to_project():
    st.session_state.page = 'project'

def reset_project():
    st.session_state.page = 'landing'
```

**Ne yapıyor?**
- `def`: Fonksiyon tanımlıyoruz (tekrar kullanılabilir kod parçası)
- `switch_to_project()`: Proje sayfasına geç
- `reset_project()`: Ana sayfaya geri dön

**Basit anlatım:** Sayfa değiştirmek için kısayollar oluşturuyoruz.

---

### Satır 21-70: LANDING PAGE (Ana Sayfa)

#### Satır 22: Sayfa Kontrolü

```python
if st.session_state.page == 'landing':
```

**Ne yapıyor?** "Eğer şu anda landing sayfasındaysak" diye kontrol ediyor.

#### Satır 24-28: Hero Resmi

```python
try:
    st.image("images/bg.jpg", width='stretch')
except:
    st.warning("Background image not found.")
```

**Ne yapıyor?**
- `try/except`: Hata yakalama. Eğer resim bulunamazsa uyarı göster.
- `st.image()`: Resim göster
- `width='stretch'`: Resmi tam genişlikte göster

#### Satır 30-33: Başlık ve Alt Başlık

```python
st.title("Beach Nourishment Design Tool")
st.subheader("Professional solution for coastal engineering calculations...")
st.markdown("---")
```

**Ne yapıyor?**
- `st.title()`: En büyük başlık
- `st.subheader()`: Alt başlık
- `st.markdown("---")`: Yatay çizgi (ayırıcı)

#### Satır 35-36: Sütunlara Bölme

```python
col_map, col_form = st.columns([1, 1])
```

**Ne yapıyor?** Sayfayı 2 eşit sütuna böl (`[1, 1]` = 1:1 oranında).

#### Satır 38-43: Sol Sütun - Harita

```python
with col_map:
    st.components.v1.iframe(
        "https://www.google.com/maps/embed?pb=...",
        height=410
    )
```

**Ne yapıyor?**
- `with col_map:`: Sol sütunun içinde çalış
- `st.components.v1.iframe()`: Google Maps'i sayfaya göm
- `height=410`: Haritanın yüksekliği

#### Satır 45-66: Sağ Sütun - Proje Başlatma Formu

```python
with col_form:
    st.markdown("### Start New Project")
    
    with st.form("entry_form"):
        project_name = st.text_input(
            "Enter Project Name:", 
            placeholder="e.g., Şile Ağlayankaya Beach Nourishment", 
            value="Şile Ağlayankaya Beach Nourishment"
        )
        submitted = st.form_submit_button("Start Project", type="primary", use_container_width=True)
        
        if submitted:
            if project_name:
                st.session_state.project_name = project_name
                switch_to_project()
                st.rerun()
            else:
                st.error("Please enter a project name to continue.")
```

**Ne yapıyor?**
- `st.form()`: Form oluştur (birkaç input'u bir arada göndermek için)
- `st.text_input()`: Metin kutusu
  - `placeholder`: Gri renkle gösterilen örnek metin
  - `value`: Başlangıç değeri
- `st.form_submit_button()`: Form gönderme butonu
- `if submitted:`: Butona basıldıysa...
- `if project_name:`: Proje adı girildiyse...
  - `st.session_state.project_name`: Proje adını hafızaya kaydet
  - `switch_to_project()`: Proje sayfasına geç
  - `st.rerun()`: Sayfayı yenile
- `else:`: Proje adı boşsa hata göster

#### Satır 68-70: Footer

```python
# Footer at the bottom
st.markdown("---")
st.caption("© 2025 Coastal Engineering Solutions | Ağlayankaya Beach Nourishment Project")
```

**Ne yapıyor?** Alt bilgi yazısı.

---

### Satır 72-158: PROJECT PAGE (Proje Sayfası)

#### Satır 73: Sayfa Kontrolü

```python
elif st.session_state.page == 'project':
```

**Ne yapıyor?** "Yoksa eğer project sayfasındaysak" diye kontrol ediyor.

#### Satır 75-83: Üst Çubuk

```python
col_back, col_title = st.columns([1, 4])
with col_back:
    if st.button("← Home", use_container_width=True):
        reset_project()
        st.rerun()
with col_title:
    st.subheader(f"Project: {st.session_state.get('project_name', 'Untitled Project')}")
```

**Ne yapıyor?**
- `[1, 4]`: Sol 1 birim, sağ 4 birim (geri butonu dar, başlık geniş)
- `st.button()`: Buton oluştur
- `use_container_width=True`: Buton tam genişlikte
- `f"..."`: f-string (içine değişken yazabiliriz)
- `st.session_state.get('project_name', 'Untitled Project')`: Hafızadan proje adını getir, yoksa "Untitled Project" yaz

#### Satır 85-86: Bilgilendirme

```python
st.divider()
st.info("Please enter the required parameters for design calculations.")
```

**Ne yapıyor?**
- `st.divider()`: İnce yatay çizgi
- `st.info()`: Mavi bilgi kutusu

#### Satır 90-102: Bölüm 1 - Dalga ve Sediman Özellikleri

```python
st.markdown("### 1. Wave and Sediment Properties")

c1, c2 = st.columns(2)
with c1:
    Hs = st.number_input("Significant Wave Height (Hs) [m]", value=2.0, step=0.1, help="Design wave height for the project area")
    T = st.number_input("Wave Period (T) [s]", value=7.0, step=0.1, help="Peak wave period")
    L_coast = st.number_input("Total Coastline Length [m]", value=480.0, step=10.0, help="Total length of beach nourishment")
with c2:
    d50 = st.number_input("Median Grain Size (d₅₀) [mm]", value=0.25, step=0.01, help="Median sediment grain diameter")
    A_param = st.number_input("Sediment Scale Parameter (A)", value=0.09, step=0.01, help="Dean's parameter based on grain size")
    h_toe = st.number_input("Sill Depth (h) [m]", value=2.5, step=0.1, help="Target depth for sill placement")
```

**Ne yapıyor?**
- `st.number_input()`: Sayı girişi kutusu
  - `value`: Başlangıç değeri
  - `step`: Artırma/azaltma miktarı
  - `help`: Üzerine gelince gösterilen açıklama
- Her değişken (`Hs`, `T`, `d50`, vb.) kullanıcının girdiği değeri saklar

#### Satır 106-108: Bölüm 2 - Kesit Analizi

```python
profile.render_profile_section()
st.markdown("---")
```

**Ne yapıyor?**
- `profile.render_profile_section()`: `profile_module.py` dosyasındaki fonksiyonu çağır
- Bu fonksiyon harita, batimetri, **otomatik tasarım profili** ve grafikleri gösterir

#### Satır 110-135: Bölüm 3 - Yapısal Elemanlar

```python
st.markdown("### 3. Structural Elements (Optional)")

with st.expander("Groin Properties"):
    use_groin = st.toggle("Include Groin in Project", value=False)
    if use_groin:
        gc1, gc2 = st.columns(2)
        with gc1:
            groin_length = st.number_input("Groin Length (m)", value=28.3, key="gl")
            groin_width = st.number_input("Groin Width (m)", value=1.0, key="gw")
        with gc2:
            groin_depth = st.number_input("Groin Depth (m)", value=5.5, key="gd")
            groin_cost = st.number_input("Unit Cost ($/m³)", value=33.0, key="g_cost")
```

**Ne yapıyor?**
- `st.expander()`: Açılır kapanır kutu (başlığa tıklayınca açılır)
- `st.toggle()`: Switch (açık/kapalı)
- `if use_groin:`: Switch açıksa mahmuz bilgilerini göster
- `key="gl"`: Her input'a benzersiz isim (Streamlit ayırt etmek için kullanır)

**Aynı mantık Sill için de geçerli** (Satır 125-135).

#### Satır 139-145: Bölüm 4 - Maliyet Tahmini

```python
st.markdown("### 4. Cost Estimation")
cost1, cost2 = st.columns(2)
with cost1:
    sand_cost = st.number_input("Sand Unit Cost ($/m³)", value=20.0, step=1.0, help="Cost per cubic meter of fill material")
with cost2:
    transport_cost = st.number_input("Transport & Placement Cost ($/m³)", value=5.0, step=1.0, help="Additional costs for material placement")
```

**Ne yapıyor?** Kum ve taşıma maliyetlerini alıyoruz.

#### Satır 149-158: Hesaplama Butonu ve Sonuçlar

```python
if st.button("START CALCULATIONS", type="primary", use_container_width=True):
    st.success("Data received successfully. Processing results...")
    
    st.markdown("#### Results (Real calculations will be implemented)")
    col_res1, col_res2, col_res3 = st.columns(3)
    col_res1.metric("Estimated Sand Volume", "~12,345 m³")
    col_res2.metric("Total Material Cost", "$123,000")
    col_res3.metric("Project Total", "$123,456")
```

**Ne yapıyor?**
- `st.button()`: Buton oluştur
- `type="primary"`: Mavi renkli önemli buton
- `st.success()`: Yeşil başarı mesajı
- `st.metric()`: Büyük sayı kartları (metrik kartları)
- **Not:** Şu anda sahte (dummy) veriler gösteriliyor. Gerçek hesaplamalar daha sonra eklenecek.

---

## 📁 profile_module.py - KESİT ANALİZİ MODÜLÜ

### Satır 1-7: Kütüphaneler

```python
import streamlit as st
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import xarray as xr
import numpy as np
```

**Ne yapıyor?**
- `plotly`: İnteraktif grafikler için
- `folium`: Harita oluşturmak için
- `streamlit_folium`: Folium haritalarını Streamlit'te göstermek için
- `xarray`: NetCDF dosyalarını okumak için
- `numpy`: Matematiksel hesaplamalar için

---

### Satır 9-42: Yardımcı Fonksiyonlar

#### find_line_intersection() - İki Çizginin Kesişim Noktasını Bulma

```python
def find_line_intersection(p1, p2, p3, p4):
    """Find intersection point between two lines
    p1-p2: First line (section line)
    p3-p4: Second line (new shoreline or sill line)
    """
```

**Ne yapıyor?**
- İki çizginin kesişim noktasını hesaplar
- `p1-p2`: Kesit çizgisi (A-A', B-B' veya C-C')
- `p3-p4`: Yeni sahil çizgisi veya sill çizgisi
- Determinant hesaplaması ile kesişim noktasını bulur
- Eğer çizgiler paralelse veya kesişim noktası kesit çizgisinin dışındaysa `None` döner

**Kullanım:** Tasarım profili oluştururken kesit çizgisinin yeni sahil çizgisi ve sill çizgisi ile kesişim noktalarını bulmak için kullanılır.

#### calculate_distance() - İki Nokta Arası Mesafe Hesaplama

```python
def calculate_distance(point1, point2):
    """Calculate distance between two points (Haversine formula)"""
```

**Ne yapıyor?**
- Haversine formülü ile iki coğrafi koordinat arasındaki mesafeyi hesaplar
- Dünya yuvarlak olduğu için basit mesafe formülü yerine bu formül kullanılır
- Sonuç metre cinsinden döner

**Kullanım:** Kesit çizgisi üzerindeki noktaların mesafelerini hesaplamak için kullanılır.

---

### Satır 56-71: Batimetri Verisi Yükleme Fonksiyonu

```python
@st.cache_data
def load_bathymetry():
    try:
        import os
        file_name = "final_veri.nc"
        if os.path.exists(file_name):
            file_path = os.path.abspath(file_name)
        else:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        
        try:
            return xr.open_dataset(file_path, engine='netcdf4')
        except:
            return xr.open_dataset(file_path, engine='scipy')
    except:
        return None
```

**Ne yapıyor?**
- `@st.cache_data`: Veriyi bir kez yükle, sonra hafızada tut (her seferinde yeniden yükleme)
- `final_veri.nc`: Projeye özel NetCDF dosyası (1D nokta verisi formatında)
- `os.path.exists()`: Dosya var mı kontrol et
- `xr.open_dataset()`: NetCDF dosyasını aç
- İlk `netcdf4` motorunu dene, olmazsa `scipy` motorunu kullan
- Hata olursa `None` döner

**Önemli:** `final_veri.nc` dosyası `latitude`, `longitude` ve `label` değişkenlerini `data_vars` içinde tutar (standart NetCDF formatından farklı).

---

### Satır 73-141: Derinlik Profili Çıkarma Fonksiyonu

```python
def extract_depth_profile(ds, point1, point2, num_points=50):
```

**Ne yapıyor?** İki nokta arasındaki derinlik profilini çıkarır.

**İçinde:**
1. **Satır 77-78:** İki nokta arasında düz çizgi çiz (lat/lon interpolasyonu)
2. **Satır 80-88:** Haversine formülü ile mesafeleri hesapla (dünya yuvarlak olduğu için)
3. **Satır 90-96:** NetCDF'deki koordinatları bul (`data_vars` içinde `latitude` ve `longitude`)
4. **Satır 98-110:** Derinlik değişkenini bul (`label`, `depth` veya `elevation` içeren değişken)
5. **Satır 115-122:** Her noktadaki derinliği **en yakın komşu (nearest neighbor)** yöntemi ile bul
   - Euclidean mesafe ile en yakın noktayı bul
   - O noktanın derinlik değerini al
6. **Satır 126-132:** Eksik veriler varsa interpolasyon yap
7. **Satır 134-136:** Derinlik pozitifse negatif yap (deniz seviyesinin altında)

**Döndürür:** Mesafe listesi ve derinlik listesi

**Önemli:** `final_veri.nc` formatı 1D nokta verisi olduğu için grid interpolasyonu yerine nearest neighbor kullanılır.

---

### Satır 143-155: Session State Başlatma (Modül Seviyesi)

```python
if 'sections' not in st.session_state:
    st.session_state.sections = {
        'A': {'points': [], 'bathy_dist': [], 'bathy_depth': [], 'user_dist': [], 'user_depth': [], 'completed': False, 'sill_distance': None, 'sill_depth': None},
        'B': {...},
        'C': {...}
    }

if 'current_section' not in st.session_state:
    st.session_state.current_section = 'A'

if 'coord_version' not in st.session_state:
    st.session_state.coord_version = 0
```

**Ne yapıyor?**
- **Modül seviyesinde** session state başlatma (dosya yüklendiğinde çalışır)
- `sections`: Her kesit için verileri saklar
  - `points`: Haritada seçilen 2 nokta (lat/lon)
  - `bathy_dist`, `bathy_depth`: NetCDF'den okunan gerçek derinlik profili
  - `user_dist`, `user_depth`: **Otomatik oluşturulan** tasarım profili
  - `completed`: Bu kesit tamamlandı mı?
  - `sill_distance`, `sill_depth`: Sill (eşik) konumu ve derinliği
- `current_section`: Şu anda hangi kesitte çalışıyoruz (A, B, C veya ALL)
- `coord_version`: Koordinat widget'larını yenilemek için versiyon numarası

---

### Satır 157-161: Sill Çizgisi Koordinatları (Sabitler)

```python
NEW_SHORELINE_P1 = {'lat': 41.1775, 'lon': 29.6244}  # 41°10'39"N 29°37'28"E
NEW_SHORELINE_P2 = {'lat': 41.1747, 'lon': 29.6286}  # 41°10'29"N 29°37'43"E
SILL_P1 = {'lat': 41.1778, 'lon': 29.6253}  # 41°10'40"N 29°37'31"E
SILL_P2 = {'lat': 41.1750, 'lon': 29.6292}  # 41°10'30"N 29°37'45"E
```

**Ne yapıyor?**
- Yeni sahil çizgisi (doldurma başlangıcı) ve sill çizgisi (parabol sonu) koordinatlarını tanımlar
- Bu çizgiler tasarım profili oluştururken kullanılır
- Haritada yeşil çizgiler olarak gösterilir

---

### Satır 163-588: render_profile_section() Fonksiyonu

Bu fonksiyon kesit analizi arayüzünü oluşturur.

#### Satır 163-168: Başlangıç

```python
def render_profile_section():
    bathymetry_ds = load_bathymetry()
    st.markdown("---")
    current = st.session_state.current_section
```

**Ne yapıyor?**
- Batimetri verisini yükler
- Mevcut kesiti alır

#### Satır 170-195: Navigasyon Butonları

```python
st.markdown("### Section Navigation")
col_a, col_b, col_c, col_all = st.columns(4)

with col_a:
    label = "[Done] A-A'" if st.session_state.sections['A']['completed'] else "A-A'"
    if st.button(label, key="nav_a", use_container_width=True, type="primary" if current == 'A' else "secondary"):
        st.session_state.current_section = 'A'
        st.rerun()
```

**Ne yapıyor?**
- 4 buton: A-A', B-B', C-C' ve All Results
- Tamamlanan kesitlerin yanında "[Done]" yazıyor
- Aktif kesit mavi (primary), diğerleri gri (secondary)
- Butona basınca ilgili kesit açılıyor ve sayfa yenilenir
- "All Results" butonunda tamamlanan kesit sayısı gösterilir (örn: "All Results (2/3)")

#### Satır 197-330: ALL RESULTS VIEW

```python
if current == 'ALL':
    st.info("Viewing: **All Results Summary**")
    st.markdown("---")
    
    completed_sections = [name for name, data in st.session_state.sections.items() if data['completed']]
    
    if not completed_sections:
        st.warning("No sections completed yet. Please complete at least one section to view results.")
    else:
        # ===== VOLUME CALCULATION SUMMARY =====
        st.markdown("## 📊 Volume Calculation Summary")
        
        vol_results, error = calculate_total_volume()
        
        if error:
            st.warning(f"Volume calculation failed: {error}")
        else:
            # Main metrics
            col_total, col_ab, col_bc = st.columns(3)
            
            with col_total:
                st.metric("🏗️ Total Fill Volume", f"{vol_results['total']:,.0f} m³")
            with col_ab:
                st.metric("A-B Region Volume", f"{vol_results['volumes']['A-B']:,.0f} m³")
            with col_bc:
                st.metric("B-C Region Volume", f"{vol_results['volumes']['B-C']:,.0f} m³")
            
            # Section details
            st.markdown("#### Section Details")
            detail_cols = st.columns(3)
            for i, sec_name in enumerate(['A', 'B', 'C']):
                with detail_cols[i]:
                    st.markdown(f"**Section {sec_name}-{sec_name}'**")
                    st.write(f"Fill Area: **{vol_results['areas'][sec_name]:,.1f} m²**")
            
            # Inter-section distances
            st.markdown("#### Inter-Section Distances")
            dist_col1, dist_col2 = st.columns(2)
            with dist_col1:
                st.write(f"A ↔ B Distance: **{vol_results['distances']['A-B']:,.1f} m**")
            with dist_col2:
                st.write(f"B ↔ C Distance: **{vol_results['distances']['B-C']:,.1f} m**")
            
            # Calculation method explanation
            with st.expander("📐 Calculation Method"):
                st.markdown("""
                **Average End Area Method**
                
                ```
                V = (A₁ + A₂) / 2 × L
                ```
                
                - **A₁, A₂**: Fill areas of two sections (m²)
                - **L**: Distance between sections (m)
                - **V**: Volume (m³)
                """)
        
        st.markdown("---")
        
        st.markdown("## Combined View - All Sections")
        
        fig_combined = go.Figure()
        colors = {'A': '#2563EB', 'B': '#DC2626', 'C': '#FACC15'}
        sill_colors = {'A': '#006400', 'B': '#00FF00', 'C': '#90EE90'}
        
        for sec_name in ['A', 'B', 'C']:
            sec_data = st.session_state.sections[sec_name]
            if sec_data['completed']:
                # Add bathymetry and design traces
                # Add sill markers with different green shades
```

**Ne yapıyor?**
- **Volume Calculation Summary:** Tüm kesitler tamamlandığında otomatik olarak hacim hesaplaması yapılır
  - **Total Fill Volume:** A-B ve B-C bölgelerinin toplam hacmi
  - **A-B Region Volume:** A ve B kesitleri arasındaki hacim
  - **B-C Region Volume:** B ve C kesitleri arasındaki hacim
  - **Section Details:** Her kesit için dolgu alanı (m²)
  - **Inter-Section Distances:** Kesitler arası mesafeler
  - **Calculation Method:** Average End Area Method açıklaması (genişletilebilir bölüm)
- **Combined View:** Tüm kesitler tek grafikte
  - A: Mavi, B: Kırmızı, C: Sarı
  - Her kesit için sill marker'ları farklı yeşil tonlarda (A: koyu yeşil, B: normal yeşil, C: açık yeşil)

#### Satır 340-588: SECTION EDITING VIEW

##### Satır 347-377: Harita ve Sill Çizgileri

```python
m = folium.Map(location=[41.175354, 29.626743], zoom_start=15)
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellite',
    overlay=False,
    control=True
).add_to(m)

# Add sill lines to map
new_shoreline_coords = [[NEW_SHORELINE_P1['lat'], NEW_SHORELINE_P1['lon']], 
                        [NEW_SHORELINE_P2['lat'], NEW_SHORELINE_P2['lon']]]
sill_coords = [[SILL_P1['lat'], SILL_P1['lon']], 
               [SILL_P2['lat'], SILL_P2['lon']]]

folium.PolyLine(new_shoreline_coords, color='green', weight=3, opacity=0.8,
               popup='New Shoreline (Fill Start)').add_to(m)
folium.PolyLine(sill_coords, color='green', weight=3, opacity=0.8,
               dashArray='10, 5', popup='Parabola End (Sill Location)').add_to(m)

# Add markers to line start and end points
for coord, popup_text in [(new_shoreline_coords[0], 'New Shoreline Start'),
                          (new_shoreline_coords[1], 'New Shoreline End'),
                          (sill_coords[0], 'Sill Line Start'),
                          (sill_coords[1], 'Sill Line End')]:
    folium.Marker(coord, popup=popup_text,
                 icon=folium.Icon(color='green', icon='info-sign')).add_to(m)
```

**Ne yapıyor?**
- Folium haritası oluştur (Şile Ağlayankaya koordinatları)
- Esri uydu görüntüsü katmanı ekle (satellite view)
- **Yeni sahil çizgisi:** Yeşil düz çizgi (doldurma başlangıcı)
- **Sill çizgisi:** Yeşil kesikli çizgi (parabol sonu)
- Her çizginin başlangıç ve bitiş noktalarına yeşil marker ekle
- Tüm kesitlerin seçilen noktalarını göster (aktif kesit renkli, diğerleri gri)
- Aktif kesit için çizgi kalın, diğerleri ince

##### Satır 395-412: Harita Tıklamalarını İşleme

```python
m.add_child(folium.LatLngPopup())
map_data = st_folium(m, height=400, use_container_width=True, key=f"map_{current}")

if map_data and map_data.get('last_clicked'):
    lat = map_data['last_clicked']['lat']
    lon = map_data['last_clicked']['lng']
    
    if len(section['points']) < 2:
        new_point = True
        if section['points']:
            last = section['points'][-1]
            # Aynı noktaya tekrar tıklanmış mı kontrol et
            if abs(last['lat'] - lat) < 0.0001 and abs(last['lon'] - lon) < 0.0001:
                new_point = False
        
        if new_point:
            section['points'].append({'lat': lat, 'lon': lon})
            st.session_state.coord_version += 1
            st.rerun()
```

**Ne yapıyor?**
- `st_folium()` ile haritayı Streamlit'e göm
- Haritada tıklama algılandıysa koordinatları al
- Eğer 2'den az nokta varsa ve yeni bir nokta ise ekle
- Aynı noktaya tekrar tıklanmışsa yok say
- Koordinat versiyonunu artır (manuel koordinat formunu yenilemek için)
- Sayfayı yenile

##### Satır 414-448: Manuel Koordinat Formu

```python
st.markdown("#### Manual Coordinates")

v = st.session_state.coord_version
default_lat1 = section['points'][0]['lat'] if section['points'] else 41.175354
default_lon1 = section['points'][0]['lon'] if section['points'] else 29.626743
default_lat2 = section['points'][1]['lat'] if len(section['points']) > 1 else 41.175000
default_lon2 = section['points'][1]['lon'] if len(section['points']) > 1 else 29.627000

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Point {current}**")
    lat1 = st.number_input("Latitude", value=default_lat1, format="%.6f", key=f"lat1_{current}_{v}")
    lon1 = st.number_input("Longitude", value=default_lon1, format="%.6f", key=f"lon1_{current}_{v}")
with col2:
    st.markdown(f"**Point {current}'**")
    lat2 = st.number_input("Latitude ", value=default_lat2, format="%.6f", key=f"lat2_{current}_{v}")
    lon2 = st.number_input("Longitude ", value=default_lat2, format="%.6f", key=f"lon2_{current}_{v}")

col_apply, col_reset = st.columns(2)
with col_apply:
    if st.button("Apply Coordinates", key=f"apply_{current}", use_container_width=True):
        section['points'] = [{'lat': lat1, 'lon': lon1}, {'lat': lat2, 'lon': lon2}]
        st.rerun()
with col_reset:
    if st.button("Reset Points", key=f"reset_{current}", use_container_width=True):
        section['points'] = []
        section['completed'] = False
        section['bathy_dist'] = []
        section['bathy_depth'] = []
        section['user_dist'] = []
        section['user_depth'] = []
        st.session_state.coord_version += 1
        st.rerun()
```

**Ne yapıyor?**
- Kullanıcı koordinatları manuel olarak da girebilir
- İki sütun: Point A ve Point A' için ayrı ayrı
- Haritadan seçilen koordinatlar otomatik yansır (versiyon numarası sayesinde widget yenilenir)
- "Apply Coordinates" butonu ile manuel girilen koordinatları uygula
- "Reset Points" butonu ile noktaları ve tüm kesit verilerini sıfırla

##### Satır 450-520: Batimetri Profili ve Otomatik Tasarım Profili

```python
if len(section['points']) == 2:
    st.markdown(f"### Step 2: Bathymetry Profile")
    
    if not section['bathy_dist']:
        dist, depth = extract_depth_profile(bathymetry_ds, section['points'][0], section['points'][1])
        if dist and depth:
            section['bathy_dist'] = dist
            section['bathy_depth'] = depth
    
    if section['bathy_dist']:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=section['bathy_dist'], y=section['bathy_depth'], mode='lines+markers', name='Bathymetry', line=dict(color='#0077B6', width=2)))
        fig.update_layout(xaxis_title="Distance (m)", yaxis_title="Depth (m)", height=350)
        st.plotly_chart(fig)
        
        st.metric("Total Distance", f"{section['bathy_dist'][-1]:.1f} m")
        
        # Create automatic design profile
        # Parabola: y = 0.11 * x^0.67
        if not section['user_dist']:
            # Find intersection points with section line
            section_p1 = section['points'][0]
            section_p2 = section['points'][1]
            intersection_start = find_line_intersection(section_p1, section_p2, NEW_SHORELINE_P1, NEW_SHORELINE_P2)
            intersection_end = find_line_intersection(section_p1, section_p2, SILL_P1, SILL_P2)
            
            # Calculate distances to intersection points
            fill_distance = calculate_distance(section_p1, intersection_start) if intersection_start else 0.0
            parabol_end_distance = calculate_distance(section_p1, intersection_end) if intersection_end else float('inf')
            
            # Calculate sill depth once (used for constant depth after sill point)
            sill_depth = 0.0
            if parabol_end_distance < float('inf'):
                relative_x_end = parabol_end_distance - fill_distance
                if relative_x_end > 0:
                    sill_depth = -abs(0.11 * (relative_x_end ** 0.67))
                section['sill_distance'] = parabol_end_distance
                section['sill_depth'] = sill_depth
            else:
                section['sill_distance'] = None
                section['sill_depth'] = None
            
            # Calculate depth for each distance point using formula
            design_depths = []
            for x in bathy_dist_array:
                if x <= fill_distance:
                    # 0 meters up to first intersection point (filled area)
                    design_depths.append(0.0)
                elif x <= parabol_end_distance:
                    # Between first and second intersection points: Parabola
                    # y = 0.11 * (x - fill_distance)^0.67
                    relative_x = x - fill_distance
                    if relative_x > 0:
                        y = 0.11 * (relative_x ** 0.67)
                        design_depths.append(-abs(y))
                    else:
                        design_depths.append(0.0)
                else:
                    # After sill point: constant depth
                    design_depths.append(sill_depth)
            
            section['user_dist'] = bathy_dist_array.tolist()
            section['user_depth'] = design_depths
            section['completed'] = True
```

**Ne yapıyor?**
- 2 nokta seçildiğinde otomatik olarak batimetri profili çıkarılır
- NetCDF dosyasından derinlik verileri okunur
- Grafik çizilir (mesafe vs derinlik, mavi çizgi)
- Toplam mesafe metrik olarak gösterilir
- **Otomatik tasarım profili oluşturulur:**
  1. Kesit çizgisinin yeni sahil çizgisi ile kesişim noktası bulunur (`fill_distance`)
  2. Kesit çizgisinin sill çizgisi ile kesişim noktası bulunur (`parabol_end_distance`)
  3. Sill derinliği hesaplanır (parabol formülü ile)
  4. Her mesafe noktası için:
     - `x <= fill_distance`: 0 metre (doldurulmuş alan)
     - `fill_distance < x <= parabol_end_distance`: Parabol formülü `y = 0.11 * (x - fill_distance)^0.67`
     - `x > parabol_end_distance`: Sill derinliğinde sabit (parabol sonu)
  5. Tasarım profili otomatik olarak kaydedilir ve kesit tamamlandı olarak işaretlenir

**Önemli:** Kullanıcıdan tasarım profili alınmaz, otomatik olarak parabol formülü ile oluşturulur.

##### Satır 522-588: Karşılaştırma ve Navigasyon

```python
if section['completed']:
    st.markdown(f"### Step 3: Comparison")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=section['bathy_dist'], y=section['bathy_depth'], mode='lines+markers', name='Bathymetry', line=dict(color='#0077B6', width=2)))
    fig2.add_trace(go.Scatter(x=section['user_dist'], y=section['user_depth'], mode='lines+markers', name='Design', line=dict(color='#FF6B6B', width=2, dash='dash')))
    
    # Mark sill location (parabola end point)
    if section.get('sill_distance') is not None and section.get('sill_depth') is not None:
        # Sill marker (green diamond)
        fig2.add_trace(go.Scatter(
            x=[section['sill_distance']], 
            y=[section['sill_depth']], 
            mode='markers',
            name='Sill Location',
            marker=dict(
                symbol='diamond',
                size=15,
                color='#00FF00',
                line=dict(color='#006600', width=2)
            ),
            hovertemplate='Sill Location<br>Distance: %{x:.1f} m<br>Depth: %{y:.2f} m<extra></extra>'
        ))
        
        # Vertical line downward from sill (green)
        min_depth = min(min(section['bathy_depth']), min(section['user_depth']))
        fig2.add_shape(
            type="line",
            x0=section['sill_distance'],
            y0=section['sill_depth'],
            x1=section['sill_distance'],
            y1=min_depth - 1,
            line=dict(color='#00FF00', width=2, dash='dash')
        )
    
    fig2.update_layout(xaxis_title="Distance (m)", yaxis_title="Depth (m)", height=400, legend=dict(x=0.01, y=0.99))
    st.plotly_chart(fig2)
    
    # Show sill information
    if section.get('sill_distance') is not None and section.get('sill_depth') is not None:
        st.info(f"**Sill Location:** Distance = {section['sill_distance']:.1f} m, Depth = {abs(section['sill_depth']):.2f} m")
    
    st.success(f"Section {current}-{current}' saved!")
    
    # Previous ve Next butonları
    _, col_prev, col_next, _ = st.columns([1, 2, 2, 1])
    with col_prev:
        if current in ['B', 'C']:
            prev_sec = 'A' if current == 'B' else 'B'
            if st.button(f"< Previous ({prev_sec})", key=f"prev_{current}", use_container_width=True):
                st.session_state.current_section = prev_sec
                st.rerun()
    with col_next:
        if current == 'A':
            if st.button("Next (B) >", key=f"next_{current}", use_container_width=True):
                st.session_state.current_section = 'B'
                st.rerun()
        elif current == 'B':
            if st.button("Next (C) >", key=f"next_{current}", use_container_width=True):
                st.session_state.current_section = 'C'
                st.rerun()
        elif current == 'C':
            if st.button("All Results >", key=f"next_{current}", use_container_width=True):
                st.session_state.current_section = 'ALL'
                st.rerun()
```

**Ne yapıyor?**
- Batimetri (mavi, düz çizgi) ve tasarım (kırmızı, kesikli çizgi) profilleri üst üste çizilir
- **Sill konumu:** Yeşil elmas marker ve dikey kesikli çizgi ile gösterilir
- Sill bilgisi (mesafe ve derinlik) bilgi kutusunda gösterilir
- Yeşil başarı mesajı gösterilir
- "Previous" ve "Next" butonları ile kesitler arası geçiş
  - Previous sadece B ve C'de görünür
  - Next: A'da "Next (B)", B'de "Next (C)", C'de "All Results"

---

### Satır 586-694: VOLUME CALCULATION FUNCTIONS

#### calculate_fill_area() - Fill Area Calculation

```python
def calculate_fill_area(bathy_dist, bathy_depth, design_dist, design_depth, sill_distance=None):
    """
    Calculate fill area between bathymetry and design profiles.
    If sill_distance is provided, calculates only up to that distance
    """
```

**Ne yapıyor?**
- Bathymetry ve design profilleri arasındaki dolgu alanını hesaplar
- **Sill distance:** Verilirse sadece sill noktasına kadar olan kısmı hesaplar
- **Yöntem:**
  1. Design profili bathymetry profili mesafe noktalarına interpolasyon ile uyarlar
  2. Dolgu yüksekliğini hesaplar: `fill_height = design_depth - bathy_depth`
  3. Negatif değerleri sıfırlar (sadece dolgu alanı)
  4. Trapezoid yöntemi ile alanı hesaplar
- **Döndürür:** Dolgu alanı (m²)

#### calculate_section_midpoint() - Section Midpoint

```python
def calculate_section_midpoint(points):
    """
    Calculate the midpoint of a section line.
    """
```

**Ne yapıyor?**
- Kesit çizgisinin orta noktasını hesaplar
- İki noktanın lat/lon ortalamasını alır
- Kesitler arası mesafe hesaplamak için kullanılır

#### calculate_total_volume() - Total Volume Calculation

```python
def calculate_total_volume():
    """
    Calculate total fill volume between all sections.
    Uses Average End Area Method: V = (A1 + A2) / 2 * L
    """
```

**Ne yapıyor?**
- Tüm kesitler arasındaki toplam dolgu hacmini hesaplar
- **Average End Area Method:** `V = (A₁ + A₂) / 2 × L`
  - **A₁, A₂:** İki kesitin dolgu alanları (m²)
  - **L:** Kesitler arası mesafe (m)
  - **V:** Hacim (m³)
- **Adımlar:**
  1. Tüm kesitlerin tamamlanıp tamamlanmadığını kontrol eder
  2. Her kesit için dolgu alanını hesaplar (sill'e kadar)
  3. Kesit orta noktalarını hesaplar
  4. Kesitler arası mesafeleri hesaplar (Haversine formülü)
  5. A-B ve B-C bölgeleri için hacimleri hesaplar
  6. Toplam hacmi döndürür
- **Döndürür:** `(results_dict, error_message)`
  - `results_dict`: `areas`, `distances`, `volumes`, `total` içerir
  - `error_message`: Hata varsa mesaj, yoksa `None`

#### get_volume_results() - Get Volume Results

```python
def get_volume_results():
    """
    Get volume calculation results (called from app.py).
    """
```

**Ne yapıyor?**
- `app.py`'dan çağrılmak için wrapper fonksiyon
- `calculate_total_volume()` fonksiyonunu çağırır ve sonuçları döndürür

---

## 🔑 ÖNEMLİ KAVRAMLAR ÖZET

### 1. Streamlit Bileşenleri
- `st.title()`, `st.subheader()`, `st.markdown()`: Başlıklar ve metin
- `st.image()`: Resim gösterme
- `st.text_input()`, `st.number_input()`: Kullanıcı girişi
- `st.button()`, `st.toggle()`: Butonlar ve switch'ler
- `st.columns()`: Sütunlara bölme
- `st.form()`: Form oluşturma
- `st.metric()`: Metrik kartları
- `st.plotly_chart()`: Plotly grafiği gösterme
- `st.expander()`: Açılır kapanır kutu

### 2. Session State
- `st.session_state`: Verileri hafızada tutar
- Sayfa yenilendiğinde bile veriler korunur
- Kesitler arası geçişte veriler kaybolmaz
- **Önemli:** Modül seviyesinde başlatılır

### 3. Folium Harita
- `folium.Map()`: Harita oluştur
- `folium.TileLayer()`: Katman ekle (uydu görüntüsü)
- `folium.Marker()`: İşaretçi ekle
- `folium.PolyLine()`: Çizgi çiz
- `st_folium()`: Streamlit'te göster

### 4. NetCDF ve xarray
- `.nc` dosyaları: Bilimsel veri formatı
- `xr.open_dataset()`: Dosyayı aç
- `final_veri.nc`: 1D nokta verisi formatı (`latitude`, `longitude`, `label` `data_vars` içinde)
- `.values`: Numpy dizisine çevir
- **Nearest neighbor:** Grid interpolasyonu yerine en yakın nokta yöntemi kullanılır

### 5. Plotly Grafikleri
- `go.Figure()`: Boş grafik oluştur
- `go.Scatter()`: Çizgi/nokta grafiği ekle
- `.add_trace()`: Yeni çizgi ekle
- `.add_shape()`: Şekil ekle (dikey çizgi için)
- `.update_layout()`: Eksen isimleri, boyut ayarla

### 6. Otomatik Tasarım Profili
- **Parabol formülü:** `y = 0.11 * x^0.67`
- **Yeni sahil çizgisi:** Doldurma başlangıcı (0 metre derinlik)
- **Sill çizgisi:** Parabol sonu (sabit derinlik)
- **Üç bölge:**
  1. Doldurulmuş alan (0 metre)
  2. Parabol bölgesi (hızlı azalıp sonra yavaş azalan eğri)
  3. Sill sonrası (sabit derinlik)

### 7. Hacim Hesaplama
- **Average End Area Method:** `V = (A₁ + A₂) / 2 × L`
- **Dolgu alanı:** Bathymetry ve design profilleri arasındaki fark
- **Sill limiti:** Hesaplama sadece sill noktasına kadar yapılır
- **Kesitler arası mesafe:** Haversine formülü ile hesaplanır
- **Sonuçlar:** Toplam hacim, bölge hacimleri, dolgu alanları, mesafeler

---

## 🎯 KODUN GENEL AKIŞI

1. **Uygulama açılır** → Landing page görünür
2. **"Start Project" butonu** → Project page'e geç
3. **Dalga ve sediman verileri gir** → Hs, T, d50, A, h_toe
4. **Section Navigation** → A, B, C veya All Results seç
5. **Haritada 2 nokta seç** → Kesit çizgisi belirlenir
   - Haritada **yeşil çizgiler** görünür (yeni sahil ve sill çizgileri)
6. **Batimetri profili çıkarılır** → NetCDF'den otomatik (nearest neighbor yöntemi)
7. **Tasarım profili otomatik oluşturulur** → Parabol formülü ile
   - Yeni sahil çizgisi ile kesişim noktası bulunur
   - Sill çizgisi ile kesişim noktası bulunur
   - Parabol formülü ile derinlikler hesaplanır
8. **Karşılaştırma grafiği** → Batimetri vs Tasarım
   - **Sill konumu:** Yeşil elmas marker ve dikey çizgi
9. **"Next"** → Sonraki kesite geç (C'de "All Results")
10. **All Results** → Tüm kesitler tek sayfada
    - **Volume Calculation Summary:** Otomatik hacim hesaplaması
      - Toplam dolgu hacmi
      - A-B ve B-C bölge hacimleri
      - Her kesit için dolgu alanı
      - Kesitler arası mesafeler
      - Hesaplama yöntemi açıklaması
    - Combined view (tüm kesitler tek grafikte)
    - Sill marker'ları farklı yeşil tonlarda
11. **Yapısal elemanlar ve maliyet gir** → Groin, Sill, maliyetler
12. **"START CALCULATIONS"** → Sonuçlar gösterilir (şu an dummy data)
13. **"← Home"** → Ana sayfaya geri dön

---

## 💡 İPUÇLARI

- Streamlit yukarıdan aşağıya çalışır
- Her buton tıklamasında sayfa yeniden çalışır (`st.rerun()`)
- Session state ile veriler korunur
- Haritada tıklama → koordinatlar otomatik forma yansır (coord_version sayesinde)
- `final_veri.nc` dosyası olmazsa uygulama hata verir
- Modüler yapı: `app.py` ana uygulama, `profile_module.py` kesit analizi
- **Tasarım profili kullanıcıdan alınmaz, otomatik oluşturulur**
- Sill konumu her kesit için otomatik hesaplanır ve görselleştirilir
- Combined view'da sill marker'ları section'a göre farklı renklerde (A: koyu yeşil, B: normal yeşil, C: açık yeşil)

**En önemli kural:** Her şey `st.session_state` ile hafızada tutulur! Kesitler arası geçişte veriler kaybolmaz.

---

## 📝 ÖNEMLİ NOTLAR

### final_veri.nc Dosya Formatı
- **Format:** 1D nokta verisi (grid değil)
- **Koordinatlar:** `latitude` ve `longitude` `data_vars` içinde (standart NetCDF'den farklı)
- **Derinlik:** `label` değişkeni (veya `depth`/`elevation` içeren değişken)
- **Okuma yöntemi:** Nearest neighbor (en yakın nokta)

### Otomatik Tasarım Profili
- **Formül:** `y = 0.11 * x^0.67` (x: mesafe, y: derinlik)
- **Eğri şekli:** Hızlı azalıp sonra yavaş azalan
- **Üç bölge:**
  1. Doldurulmuş alan: 0 metre (yeni sahil çizgisine kadar)
  2. Parabol bölgesi: Formül ile hesaplanan derinlikler (sill çizgisine kadar)
  3. Sill sonrası: Sill derinliğinde sabit

### Sill (Eşik) Konumu
- **Tanım:** Parabol formülünün bittiği nokta
- **Hesaplama:** Sill çizgisi ile kesit çizgisinin kesişim noktası
- **Görselleştirme:**
  - Grafiklerde: Yeşil elmas marker + dikey kesikli çizgi
  - Haritada: Yeşil kesikli çizgi
  - Combined view'da: Section'a göre farklı yeşil tonlar
