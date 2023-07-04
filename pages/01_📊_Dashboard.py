# IMPORT LIBRARY
import pandas as pd
import numpy as np
import scipy.stats as sci_stats
import streamlit as st
from streamlit_lottie import st_lottie
import plotly.express as px
import plotly.graph_objs as go
import requests
from PIL import Image
import matplotlib.pyplot as plt

# SET PAGE
st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")

# IMPORT DATASET
@st.cache_resource
def load_data():
    df = pd.read_excel('prediksi_ok.xls')
    df['ZA_Bersubsidi'] = df['ZA_Bersubsidi'].str.replace('46.72.40', '0')
    df['ZA_Bersubsidi'] = df['ZA_Bersubsidi'].str.replace('7.384.00', '7.384')
    df['ZA_Bersubsidi'] = df['ZA_Bersubsidi'].astype('float')
    return df

df = load_data()

# ---- LOAD ASSETS ----
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_ajzyv37m.json")

# HEADER
intro_column_left, intro_column_right = st.columns(2)
with st.container():
    with intro_column_left:
        # st.title(":bar_chart: Dashboard")
        st.markdown('<div style="text-align: justify; font-size:210%; line-height: 150%; margin-top: 10px;"> <b><br>Dashboard Data Produksi Padi di Indonesia</b> </div>',
            unsafe_allow_html=True)
    with intro_column_right:
        st_lottie(lottie_coding, height=250, key="dashboard")

# st.markdown("##")
st.markdown('<hr>', unsafe_allow_html=True)

# TOP KPI's
# total produksi
sum_produksi = np.round(df['Produksi'].sum(),2)
# rata-rata produktivitas
avg_produktivitas = np.round(df['Produktivitas'].mean(),2)
# persentase perubahan produksi
tahun_terakhir = df['Tahun'].max()
tahun_sebelumnya = tahun_terakhir - 1
produksi_tahun_terakhir = df[df['Tahun'] == tahun_terakhir]['Produksi'].sum()
produksi_tahun_sebelumnya = df[df['Tahun'] == tahun_sebelumnya]['Produksi'].sum()
persen_perubahan_produksi = ((produksi_tahun_terakhir - produksi_tahun_sebelumnya) / produksi_tahun_sebelumnya) * 100
# persentase penggunaan pupuk bersubsidi
total_pupuk_bersubsidi = df['NPK_Bersubsidi'].sum() + df['SP36_Bersubsidi'].sum() + df['Urea_Bersubsidi'].sum() + df['ZA_Bersubsidi'].sum()
persentase_pupuk_bersubsidi = (total_pupuk_bersubsidi / df['Produksi'].sum()) * 100
# persentase Luas Banjir dan Kekeringan terhadap Luas Panen
luas_banjir_kekeringan = df['Luas_Banjir'].sum() + df['Luas_Kekeringan'].sum()
luas_panen = df['Luas_Panen'].sum()
persentase_banjir_kekeringan_terhadap_panen = luas_banjir_kekeringan / luas_panen * 100
# persentase kerugian hama dan penyakit
total_kerugian_hama_penyakit = df['Hama_Penggerek_Batang'].sum() + df['Hama_Batang_Coklat'].sum() + df['Hama_Tikus'].sum() + df['Hama_Blas'].sum() + df['Hama_Daun'].sum() + df['Hama_Tungro'].sum()
total_produksi = df['Produksi'].sum()
persentase_kerugian_hama_penyakit = (total_kerugian_hama_penyakit / total_produksi) * 100

# KPI BARIS 1
kpi_column1, kpi_column2, kpi_column3 = st.columns(3)
with kpi_column1:
    st.subheader("Total Jumlah Hasil Produksi")
    st.write(sum_produksi, 'Ton')
with kpi_column2:
    st.subheader("Rata-rata Jumlah Produktivitas")
    st.write(avg_produktivitas, 'Kuintal/Hektar')
with kpi_column3:
    st.subheader("Persentase Perubahan Produksi")
    st.write(np.round(persen_perubahan_produksi,2), "%")

# KPI BARIS 2
kpi_column4, kpi_column5, kpi_column6 = st.columns(3)
with kpi_column4:
    st.subheader("Persentase Penggunaan Pupuk Bersubsidi terhadap Hasil Produksi")
    st.write(np.round(persentase_pupuk_bersubsidi,2), "%")
with kpi_column5:
    st.subheader("Persentase Banjir dan Kekeringan terhadap Luas Panen")
    st.write(np.round(persentase_banjir_kekeringan_terhadap_panen,2), "%")
with kpi_column6:
    st.subheader("Persentase Kerugian Hama dan Penyakit terhadap Hasil Produksi")
    st.write(np.round(persentase_kerugian_hama_penyakit,2), "%")

st.markdown('<hr>', unsafe_allow_html=True)

# GRAFIK BAR PLOT - JUMLAH PRODUKSI BERDASARKAN PROVINSI
sum_produksi_prov = df.groupby('Provinsi')['Produksi'].sum()
sum_produksi_prov = pd.DataFrame(sum_produksi_prov).sort_values(by='Produksi',
                                                                        ascending=False)

fig_sum_produksi_prov = px.bar(sum_produksi_prov,
                                   x=sum_produksi_prov.index,
                                   y="Produksi",
                                   title="<b>Jumlah Produksi berdasarkan<br>Provinsi</b>",
                                   color_discrete_sequence=["#0083B8"] * len(sum_produksi_prov),
                                   template="plotly_white",
)
fig_sum_produksi_prov.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# GRAFIK BAR PLOT - RATA-RATA PRODUKTIVITAS BERDASARKAN PROVINSI
avg_produktivitas_prov = df.groupby('Provinsi')['Produktivitas'].mean()
avg_produktivitas_prov = pd.DataFrame(avg_produktivitas_prov).sort_values(by='Produktivitas',
                                                                        ascending=False)

fig_avg_produktivitas_prov = px.bar(avg_produktivitas_prov,
                                   x=avg_produktivitas_prov.index,
                                   y="Produktivitas",
                                   title="<b>Rata-rata Produktivitas berdasarkan<br>Provinsi</b>",
                                   color_discrete_sequence=["#0083B8"] * len(avg_produktivitas_prov),
                                   template="plotly_white",
)
fig_avg_produktivitas_prov.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# GRAFIK LINE CHART - RATA-RATA CURAH HUJAN DAN TEMPERATUR PER TAHUN
df_mean = df.groupby("Tahun")[["Curah_Hujan", "Temperature"]].mean().reset_index()
fig_avg_hujan_suhu_tahun = px.line(df_mean, x="Tahun", y=["Curah_Hujan", "Temperature"],
                                   title="Rata-rata Curah Hujan dan Suhu Udara per Tahun")

# GRAFIK BAR CHART - JUMLAH MASING-MASING HAMA
hama_columns = ['Hama_Penggerek_Batang', 'Hama_Batang_Coklat', 'Hama_Tikus', 'Hama_Blas', 'Hama_Daun', 'Hama_Tungro']
jumlah_hama = df[hama_columns].sum()
fig_sum_hama = go.Figure(data=[go.Bar(x=hama_columns, y=jumlah_hama)])
fig_sum_hama.update_layout(title="Jumlah Hama pada Setiap Jenis Hama")

# GRAFIK BAR CHART - JUMLAH MASING-MASING PUPUK
pupuk_columns = ['NPK_Bersubsidi', 'SP36_Bersubsidi','Urea_Bersubsidi', 'ZA_Bersubsidi']
jumlah_pupuk = df[pupuk_columns].sum()
fig_sum_pupuk = go.Figure(data=[go.Bar(x=pupuk_columns, y=jumlah_pupuk)])
fig_sum_pupuk.update_layout(title="Jumlah Pupuk pada Setiap Jenis Pupuk")

# GRAFIK SCATTER PLOT - HUBUNGAN LUAS PANEN DENGAN PRODUKSI
fig_scatter_luas_produksi = px.scatter(df,
                                         x="Luas_Panen",
                                         y="Produksi",
                                         color="Provinsi",
                                         title="<b>Hubungan Luas Panen dengan Produksi</b>",
                                         labels={
                                             "Luas_Panen": "Luas Panen"
                                         },
                                         template="plotly_dark"
                                         )

# GRAFIK SCATTER PLOT - HUBUNGAN PRODUKTIVITAS DENGAN PRODUKSI
fig_scatter_produktiv_produksi = px.scatter(df,
                                         x="Produktivitas",
                                         y="Produksi",
                                         color="Provinsi",
                                         title="<b>Hubungan Produktivitas dengan Produksi</b>",
                                         template="plotly_dark"
                                         )

# DASHBOARD
left_column_chart_row1, right_column_chart_row1 = st.columns(2)
left_column_chart_row1.plotly_chart(fig_sum_produksi_prov, use_container_width=True)
right_column_chart_row1.plotly_chart(fig_avg_produktivitas_prov, use_container_width=True)

st.plotly_chart(fig_avg_hujan_suhu_tahun, use_container_width=True)
st.plotly_chart(fig_sum_hama, use_container_width=True)
st.plotly_chart(fig_sum_pupuk, use_container_width=True)

left_column_chart_row2, right_column_chart_row2 = st.columns(2)
left_column_chart_row2.plotly_chart(fig_scatter_luas_produksi, use_container_width=True)
right_column_chart_row2.plotly_chart(fig_scatter_produktiv_produksi, use_container_width=True)
