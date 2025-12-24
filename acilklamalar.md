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
   - Batimetri verilerini NetCDF'den okuma
   - Kesit profilleri oluşturma ve karşılaştırma
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

### Satır 21-71: LANDING PAGE (Ana Sayfa)

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
- `width='stretch'`: Resmi tam genişlikte göster (eski `use_container_width=True` yerine)

#### Satır 30-32: Başlık ve Alt Başlık

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

#### Satır 45-67: Sağ Sütun - Proje Başlatma Formu

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

#### Satır 69-71: Footer

```python
# Footer at the bottom
st.markdown("---")
st.caption("© 2025 Coastal Engineering Solutions | Ağlayankaya Beach Nourishment Project")
```

**Ne yapıyor?** Alt bilgi yazısı. (Not: Kullanıcı tercihine göre bu footer kaldırılabilir)

---

### Satır 73-158: PROJECT PAGE (Proje Sayfası)

#### Satır 74: Sayfa Kontrolü

```python
elif st.session_state.page == 'project':
```

**Ne yapıyor?** "Yoksa eğer project sayfasındaysak" diye kontrol ediyor.

#### Satır 76-83: Üst Çubuk

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
- Bu fonksiyon harita, batimetri, kesit profilleri ve grafikleri gösterir

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

### Satır 1-6: Kütüphaneler

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

### Satır 9-24: Batimetri Verisi Yükleme Fonksiyonu

```python
@st.cache_data
def load_bathymetry():
    try:
        import os
        file_name = "Mean depth in multi colour (no land).nc"
        if os.path.exists(file_name):
            file_path = os.path.abspath(file_name)
        else:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        
        try:
            return xr.open_dataset(file_path, engine='netcdf4')
        except:
            return xr.open_dataset(file_path, engine='scipy')
    except Exception as e:
        return None
```

**Ne yapıyor?**
- `@st.cache_data`: Veriyi bir kez yükle, sonra hafızada tut (her seferinde yeniden yükleme)
- `os.path.exists()`: Dosya var mı kontrol et
- `xr.open_dataset()`: NetCDF dosyasını aç
- İlk `netcdf4` motorunu dene, olmazsa `scipy` motorunu kullan

---

### Satır 26-78: Derinlik Profili Çıkarma Fonksiyonu

```python
def extract_depth_profile(ds, point1, point2, num_points=50):
```

**Ne yapıyor?** İki nokta arasındaki derinlik profilini çıkarır.

**İçinde:**
1. **Satır 30-31:** İki nokta arasında düz çizgi çiz (lat/lon interpolasyonu)
2. **Satır 33-41:** Haversine formülü ile mesafeleri hesapla (dünya yuvarlak olduğu için)
3. **Satır 43-50:** NetCDF'deki derinlik değişkenini bul
4. **Satır 56-62:** Her noktadaki derinliği NetCDF'den oku
5. **Satır 66-71:** Eksik veriler varsa interpolasyon yap
6. **Satır 73-74:** Derinlik pozitifse negatif yap (deniz seviyesinin altında)

**Döndürür:** Mesafe listesi ve derinlik listesi

---

### Satır 80-92: Session State Başlatma (Modül Seviyesi)

```python
if 'sections' not in st.session_state:
    st.session_state.sections = {
        'A': {'points': [], 'bathy_dist': [], 'bathy_depth': [], 'user_dist': [], 'user_depth': [], 'completed': False},
        'B': {'points': [], 'bathy_dist': [], 'bathy_depth': [], 'user_dist': [], 'user_depth': [], 'completed': False},
        'C': {'points': [], 'bathy_dist': [], 'bathy_depth': [], 'user_dist': [], 'user_depth': [], 'completed': False}
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
  - `user_dist`, `user_depth`: Kullanıcının girdiği tasarım profili
  - `completed`: Bu kesit tamamlandı mı?
- `current_section`: Şu anda hangi kesitte çalışıyoruz (A, B, C veya ALL)
- `coord_version`: Koordinat widget'larını yenilemek için versiyon numarası

**Not:** `render_profile_section()` fonksiyonunun içinde de aynı kontroller yapılır (güvenlik için çift kontrol)

---

### Satır 94-377: render_profile_section() Fonksiyonu

Bu fonksiyon kesit analizi arayüzünü oluşturur.

#### Satır 94-111: Başlangıç ve Session State Kontrolü

```python
def render_profile_section():
    # Ensure session state is initialized
    if 'current_section' not in st.session_state:
        st.session_state.current_section = 'A'
    if 'sections' not in st.session_state:
        st.session_state.sections = {
            'A': {'points': [], 'bathy_dist': [], 'bathy_depth': [], 'user_dist': [], 'user_depth': [], 'completed': False},
            'B': {...},
            'C': {...}
        }
    if 'coord_version' not in st.session_state:
        st.session_state.coord_version = 0
    
    bathymetry_ds = load_bathymetry()
    st.markdown("---")
    current = st.session_state.current_section
```

**Ne yapıyor?**
- Fonksiyonun başında session state'in başlatıldığından emin olur (güvenlik kontrolü)
- Eğer session state yoksa başlatır
- Batimetri verisini yükler ve mevcut kesiti alır
- **Neden önemli?** Bazı durumlarda (örneğin uygulama ilk açıldığında) session state henüz başlatılmamış olabilir. Bu kontrol hataları önler.

#### Satır 113-138: Navigasyon Butonları

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

#### Satır 140-219: ALL RESULTS VIEW

```python
if current == 'ALL':
    st.info("Viewing: **All Results Summary**")
    st.markdown("---")
    
    completed_sections = [name for name, data in st.session_state.sections.items() if data['completed']]
    
    if not completed_sections:
        st.warning("No sections completed yet. Please complete at least one section to view results.")
    else:
        st.markdown("## All Cross-Section Profiles")
        
        for sec_name in ['A', 'B', 'C']:
            sec_data = st.session_state.sections[sec_name]
            if sec_data['completed']:
                st.markdown(f"### Section {sec_name}-{sec_name}'")
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=sec_data['bathy_dist'], y=sec_data['bathy_depth'], ...))
                fig.add_trace(go.Scatter(x=sec_data['user_dist'], y=sec_data['user_depth'], ...))
                st.plotly_chart(fig)
                
                # Metrikler gösterilir
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Distance", f"{sec_data['bathy_dist'][-1]:.1f} m")
                col2.metric("Max Depth (Bathy)", f"{abs(min(sec_data['bathy_depth'])):.2f} m")
                col3.metric("Max Depth (Design)", f"{abs(min(sec_data['user_depth'])):.2f} m")
        
        st.markdown("## Combined View - All Sections")
        fig_combined = go.Figure()
        colors = {'A': '#2563EB', 'B': '#DC2626', 'C': '#FACC15'}
        # Tüm kesitler tek grafikte
```

**Ne yapıyor?**
- Tamamlanan tüm kesitlerin grafiklerini tek sayfada gösterir
- Her kesit için ayrı grafik: batimetri (mavi) vs tasarım (kırmızı, kesikli)
- Her kesit için metrikler: toplam mesafe, maksimum derinlikler
- En altta Combined View: Tüm kesitler tek grafikte (A: mavi, B: kırmızı, C: sarı)

#### Satır 221-388: SECTION EDITING VIEW

##### Satır 228-255: Harita ve Nokta Seçimi

```python
m = folium.Map(location=[41.175354, 29.626743], zoom_start=15)
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellite',
    overlay=False,
    control=True
).add_to(m)
map_colors = {'A': 'blue', 'B': 'green', 'C': 'orange'}

# Tüm kesitlerin noktalarını göster
for sec_name, sec_data in st.session_state.sections.items():
    if sec_data['points']:
        color = map_colors.get(sec_name, 'gray')
        for idx, pt in enumerate(sec_data['points']):
            folium.Marker([pt['lat'], pt['lon']], ...).add_to(m)
        if len(sec_data['points']) == 2:
            folium.PolyLine([...], color=color if sec_name == current else 'gray', ...).add_to(m)
```

**Ne yapıyor?**
- Folium haritası oluştur (Şile Ağlayankaya koordinatları)
- Esri uydu görüntüsü katmanı ekle (satellite view)
- Tüm kesitlerin seçilen noktalarını göster (aktif kesit renkli, diğerleri gri)
- Aktif kesit için çizgi kalın, diğerleri ince
- Kullanıcı haritaya tıklayarak 2 nokta seçebilir

##### Satır 257-274: Harita Tıklamalarını İşleme

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

##### Satır 276-310: Manuel Koordinat Formu

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
    lon2 = st.number_input("Longitude ", value=default_lon2, format="%.6f", key=f"lon2_{current}_{v}")

col_apply, col_reset = st.columns(2)
with col_apply:
    if st.button("Apply Coordinates", key=f"apply_{current}", use_container_width=True):
        section['points'] = [{'lat': lat1, 'lon': lon1}, {'lat': lat2, 'lon': lon2}]
        st.rerun()
with col_reset:
    if st.button("Reset Points", key=f"reset_{current}", use_container_width=True):
        section['points'] = []
        section['completed'] = False
        # Tüm verileri temizle
        st.rerun()
```

**Ne yapıyor?**
- Kullanıcı koordinatları manuel olarak da girebilir
- İki sütun: Point A ve Point A' için ayrı ayrı
- Haritadan seçilen koordinatlar otomatik yansır (versiyon numarası sayesinde widget yenilenir)
- "Apply Coordinates" butonu ile manuel girilen koordinatları uygula
- "Reset Points" butonu ile noktaları ve tüm kesit verilerini sıfırla

##### Satır 312-336: Batimetri Profili

```python
if len(section['points']) == 2:
    st.success("Both points selected!")
else:
    st.warning("Select 2 points on the map or enter manually")

st.markdown("---")

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
```

**Ne yapıyor?**
- 2 nokta seçildiğinde yeşil başarı mesajı göster
- 2 nokta yoksa uyarı mesajı göster
- 2 nokta seçildiğinde otomatik olarak batimetri profili çıkarılır
- NetCDF dosyasından derinlik verileri okunur
- Grafik çizilir (mesafe vs derinlik, mavi çizgi)
- Toplam mesafe metrik olarak gösterilir

##### Satır 338-357: Tasarım Profili

```python
st.markdown(f"### Step 3: Design Profile")

num_pts = st.number_input("Number of points", min_value=2, max_value=20, value=5, key=f"npts_{current}")

if not section['user_dist'] or len(section['user_dist']) != num_pts:
    max_dist = section['bathy_dist'][-1]
    # Noktaları eşit aralıklarla dağıt
    section['user_dist'] = [float(i * max_dist / (num_pts - 1)) for i in range(num_pts)]
    # Başlangıç derinliklerini batimetri profilinden interpolasyon ile al
    section['user_depth'] = [float(np.interp(d, section['bathy_dist'], section['bathy_depth'])) for d in section['user_dist']]

st.markdown("**Distance (m) | Depth (m)**")

for i in range(num_pts):
    c1, c2 = st.columns(2)
    with c1:
        new_dist = st.number_input(f"D{i+1}", value=section['user_dist'][i], step=1.0, key=f"ud_{current}_{i}", label_visibility="collapsed")
        section['user_dist'][i] = new_dist
    with c2:
        new_depth = st.number_input(f"H{i+1}", value=section['user_depth'][i], step=0.1, key=f"uh_{current}_{i}", label_visibility="collapsed")
        section['user_depth'][i] = new_depth
```

**Ne yapıyor?**
- Kullanıcıdan kaç noktayla profil tanımlayacağını sorar (2-20 arası)
- Nokta sayısı değişirse veya henüz girilmemişse otomatik oluştur
- Mesafeleri eşit aralıklarla dağıt (0'dan maksimum mesafeye kadar)
- Başlangıç derinliklerini batimetri profilinden interpolasyon ile al
- Her nokta için mesafe (D1, D2, ...) ve derinlik (H1, H2, ...) girişi
- Kullanıcı değerleri değiştirdikçe session state'e kaydedilir

##### Satır 359-388: Karşılaştırma ve Kaydetme

```python
st.markdown("---")

if st.button("Compare & Save", type="primary", key=f"compare_{current}"):
    section['completed'] = True
    st.rerun()

if section['completed']:
    st.markdown(f"### Step 4: Comparison")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=section['bathy_dist'], y=section['bathy_depth'], mode='lines+markers', name='Bathymetry', line=dict(color='#0077B6', width=2)))
    fig2.add_trace(go.Scatter(x=section['user_dist'], y=section['user_depth'], mode='lines+markers', name='Design', line=dict(color='#FF6B6B', width=2, dash='dash')))
    fig2.update_layout(xaxis_title="Distance (m)", yaxis_title="Depth (m)", height=400, legend=dict(x=0.01, y=0.99))
    st.plotly_chart(fig2)
    
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
        if current in ['A', 'B']:
            next_sec = 'B' if current == 'A' else 'C'
            if st.button(f"Next ({next_sec}) >", key=f"next_{current}", use_container_width=True):
                st.session_state.current_section = next_sec
                st.rerun()
```

**Ne yapıyor?**
- "Compare & Save" butonuna basılınca kesit tamamlandı olarak işaretlenir
- Batimetri (mavi, düz çizgi) ve tasarım (kırmızı, kesikli çizgi) profilleri üst üste çizilir
- Yeşil başarı mesajı gösterilir
- "Previous" ve "Next" butonları ile kesitler arası geçiş (ortalanmış, tam genişlik)
- Previous sadece B ve C'de görünür, Next sadece A ve B'de görünür

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
- **Önemli:** Hem modül seviyesinde hem de fonksiyon içinde başlatılır (güvenlik için)

### 3. Folium Harita
- `folium.Map()`: Harita oluştur
- `folium.TileLayer()`: Katman ekle (uydu görüntüsü)
- `folium.Marker()`: İşaretçi ekle
- `folium.PolyLine()`: Çizgi çiz
- `st_folium()`: Streamlit'te göster

### 4. NetCDF ve xarray
- `.nc` dosyaları: Bilimsel veri formatı
- `xr.open_dataset()`: Dosyayı aç
- `.sel()`: Belirli koordinatları seç
- `.values`: Numpy dizisine çevir

### 5. Plotly Grafikleri
- `go.Figure()`: Boş grafik oluştur
- `go.Scatter()`: Çizgi/nokta grafiği ekle
- `.add_trace()`: Yeni çizgi ekle
- `.update_layout()`: Eksen isimleri, boyut ayarla

---

## 🎯 KODUN GENEL AKIŞI

1. **Uygulama açılır** → Landing page görünür
2. **"Start Project" butonu** → Project page'e geç
3. **Dalga ve sediman verileri gir** → Hs, T, d50, A, h_toe
4. **Section Navigation** → A, B, C veya All Results seç
5. **Haritada 2 nokta seç** → Kesit çizgisi belirlenir
6. **Batimetri profili çıkarılır** → NetCDF'den otomatik
7. **Tasarım profili gir** → Manuel değerler
8. **"Compare & Save"** → Grafikler karşılaştırılır, kesit kaydedilir
9. **"Next"** → Sonraki kesite geç
10. **Yapısal elemanlar ve maliyet gir** → Groin, Sill, maliyetler
11. **"START CALCULATIONS"** → Sonuçlar gösterilir (şu an dummy data)
12. **"← Home"** → Ana sayfaya geri dön

---

## 💡 İPUÇLARI

- Streamlit yukarıdan aşağıya çalışır
- Her buton tıklamasında sayfa yeniden çalışır (`st.rerun()`)
- Session state ile veriler korunur
- Haritada tıklama → koordinatlar otomatik forma yansır (coord_version sayesinde)
- NetCDF dosyası olmazsa uygulama hata verir
- Modüler yapı: `app.py` ana uygulama, `profile_module.py` kesit analizi
- `width='stretch'` kullanımı: `use_container_width=True` yerine (deprecation uyarısı önlemek için)

**En önemli kural:** Her şey `st.session_state` ile hafızada tutulur! Kesitler arası geçişte veriler kaybolmaz.
