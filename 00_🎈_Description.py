import streamlit as st
from PIL import Image

# SET PAGE
# pageicon = Image.open("aset_batik_icon.png")
st.set_page_config(page_title="PadiPro Web App", layout="centered")

# SET TITLE AND LOGO IMAGE
intro_col_left, intro_col_right = st.columns(2)
# intro_col_left.image('Bata Baca.png')
st.markdown('<div style="text-align: justify; font-size:250%"> <b>PadiPro : Web App Dashboard dan Prediksi Produksi Padi</b> </div>',
            unsafe_allow_html=True)

# DESCRIPTION
st.markdown('<div style="text-align: justify; font-size:160%; text-indent: 4em;"> PadiPro adalah sebuah Web App yang dikembangkan untuk memudahkan pengguna dalam menganalisis dan memprediksi produksi padi di Indonesia. Web App ini memiliki dua fitur utama, yaitu Dashboard dan Prediksi, yang memungkinkan pengguna untuk mempelajari karakteristik produksi padi di Indonesia dan melakukan prediksi produksi padi yang dihasilkan. </div>',
            unsafe_allow_html=True)
st.markdown('<div style="text-align: justify; font-size:160%; text-indent: 4em;"> Fitur Dashboard pada PadiPro memungkinkan pengguna untuk melihat informasi mengenai data produksi padi di Indonesia yang telah diproses sebelumnya. Fitur ini akan menampilkan distribusi produksi padi berdasarkan provinsi, curah hujan, dan hama penggerek batang, serta visualisasi hubungan antara variabel-variabel tersebut dengan produksi padi. Dashboard pada PadiPro dirancang untuk memudahkan pengguna dalam memahami dan menganalisis data produksi padi di Indonesia. </div>',
            unsafe_allow_html=True)
st.markdown('<div style="text-align: justify; font-size:160%; text-indent: 4em;"> Fitur Prediksi pada PadiPro memungkinkan pengguna untuk memasukkan nilai-nilai dari variabel-variabel yang menjadi faktor dalam produksi padi, seperti curah hujan, kelembapan, dan lama penyinaran, dan melakukan prediksi mengenai produksi padi yang dihasilkan. Hasil prediksi tersebut akan ditampilkan pada halaman yang sama, bersamaan dengan informasi mengenai nilai-nilai dari variabel yang dimasukkan pengguna. Fitur ini akan membantu pengguna dalam memprediksi produksi padi di masa depan dan membuat keputusan yang lebih baik dalam mengelola pertanian padi. </div>',
            unsafe_allow_html=True)
st.markdown('<div style="text-align: justify; font-size:160%; text-indent: 4em;"> Dengan adanya PadiPro, pengguna dapat dengan mudah menganalisis dan memprediksi produksi padi di Indonesia secara interaktif dan cepat melalui antarmuka web yang sederhana dan mudah digunakan. PadiPro dapat digunakan oleh petani, peneliti, dan siapa saja yang tertarik dalam mempelajari atau berinvestasi di bidang pertanian padi di Indonesia. </div>',
            unsafe_allow_html=True)