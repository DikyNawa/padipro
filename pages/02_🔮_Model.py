import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import pickle as pkl
from sklearn import preprocessing
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from io import BytesIO

# SET PAGE
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Model", page_icon=":crystal_ball:", layout="centered")

# SET TITLE
st.title('Model Prediksi Hasil Produksi Padi di Indonesia')

# DESCRIPTION
st.markdown('<div style="text-align: justify; font-size:160%"> Model prediksi ini menggunakan algoritma Regresi Linier dan dibuat dengan bahasa pemrograman Python. </div>',
            unsafe_allow_html=True)
st.write('')

# LOAD MODEL & DUMMY DATA
# Fungsi untuk menghitung prediksi berdasarkan persamaan regresi
def predict_production(data):
    coef_const = -78156610.23
    coef_provinsi = 4006.8334
    coef_tahun = 38533
    coef_curah_hujan = -0.3897
    coef_hama_penggerek_batang = -15.301
    coef_hama_batang_coklat = 5.7487
    coef_hama_tikus = -2.8053
    coef_hama_blas = -43.3541
    coef_hama_daun = 81.1937
    coef_hama_tungro = 16.6364
    coef_kelembapan = -92.7757
    coef_lama_penyinaran = 60490
    coef_luas_banjir = -3.1959
    coef_luas_kekeringan = 5.0543
    coef_npk_bersubsidi = 0.0060
    coef_sp36_bersubsidi = -0.2285
    coef_urea_bersubsidi = -0.0140
    coef_za_bersubsidi = 1.0121
    coef_irigasi = 0.9506
    coef_temperature = -17390
    coef_luas_panen = 5.0636
    coef_produktivitas = 9074.2263

    # Hitung prediksi berdasarkan persamaan regresi
    prediction = (
        coef_const +
        coef_provinsi * data['Provinsi'] +
        coef_tahun * data['Tahun'] +
        coef_curah_hujan * data['Curah_Hujan'] +
        coef_hama_penggerek_batang * data['Hama_Penggerek_Batang'] +
        coef_hama_batang_coklat * data['Hama_Batang_Coklat'] +
        coef_hama_tikus * data['Hama_Tikus'] +
        coef_hama_blas * data['Hama_Blas'] +
        coef_hama_daun * data['Hama_Daun'] +
        coef_hama_tungro * data['Hama_Tungro'] +
        coef_kelembapan * data['Kelembapan'] +
        coef_lama_penyinaran * data['Lama_Penyinaran'] +
        coef_luas_banjir * data['Luas_Banjir'] +
        coef_luas_kekeringan * data['Luas_Kekeringan'] +
        coef_npk_bersubsidi * data['NPK_Bersubsidi'] +
        coef_sp36_bersubsidi * data['SP36_Bersubsidi'] +
        coef_urea_bersubsidi * data['Urea_Bersubsidi'] +
        coef_za_bersubsidi * data['ZA_Bersubsidi'] +
        coef_irigasi * data['Irigasi'] +
        coef_temperature * data['Temperature'] +
        coef_luas_panen * data['Luas_Panen'] +
        coef_produktivitas * data['Produktivitas']
    )

    return prediction

@st.cache_resource
def load_data():
    data_dummy = pd.read_excel('Data_Contoh.xlsx')
    data_awal = pd.read_excel('prediksi_ok.xls')        
    return data_dummy, data_awal

data_dummy, data_awal = load_data()

# CHOOSE FILE
option = st.selectbox(
    'How would you like to do prediction?',
    ('Manual Input', 'Upload a File'))

# DICTIONARY MAPPING PROVINSI
provinsi_dict = {'Aceh': 1,
                 'SumateraUtara': 2,
                 'SumateraBarat': 3,
                 'Riau': 4,
                 'Jambi': 5,
                 'SumateraSelatan': 6,
                 'Bengkulu': 7,
                 'Lampung': 8,
                 'Kep.BangkaBelitung': 9,
                 'Kep.Riau': 10,
                 'DKIJakarta': 11,
                 'JawaBarat': 12,
                 'JawaTengah': 13,
                 'DIYogyakarta': 14,
                 'JawaTimur': 15,
                 'Banten': 16,
                 'Bali': 17,
                 'NusaTenggaraBarat': 18,
                 'NusaTenggaraTimur': 19,
                 'KalimantanBarat': 20,
                 'KalimantanTengah': 21,
                 'KalimantanSelatan': 22,
                 'KalimantanTimur': 23,
                 'KalimantanUtara': 24,
                 'SulawesiUtara': 25,
                 'SulawesiTengah': 26,
                 'SulawesiSelatan': 27,
                 'SulawesiTenggara': 28,
                 'Gorontalo': 29,
                 'SulawesiBarat': 30,
                 'Maluku': 31,
                 'MalukuUtara': 32,
                 'PapuaBarat': 33,
                 'Papua': 34}

# list of expected column names and their corresponding data types
EXPECTED_COLUMNS = [
    ('Provinsi', object),
    ('Tahun', int),
    ('Curah_Hujan', float),
    ('Hama_Penggerek_Batang', float),
    ('Hama_Batang_Coklat', float),
    ('Hama_Tikus', float),
    ('Hama_Blas', float),
    ('Hama_Daun', float),
    ('Hama_Tungro', float),
    ('Kelembapan', float),
    ('Lama_Penyinaran', float),
    ('Luas_Banjir', float),
    ('Luas_Kekeringan', float),
    ('NPK_Bersubsidi', float),
    ('SP36_Bersubsidi', float),
    ('Urea_Bersubsidi', float),
    ('ZA_Bersubsidi', float),
    ('Irigasi', float),
    ('Temperature', float),
    ('Luas_Panen', float),
    ('Produktivitas', float)
]

# KALAU USER PILIH UPLOAD FILE
if option == 'Upload a File':
    # give warning message to users
    st.error("WARNING : PASTIKAN FILE EXCEL MEMILIKI FORMAT SEBAGAI BERIKUT!!! ")
    # display dataframe
    st.dataframe(data_dummy)
    try:
        # read the user uploaded Excel file
        uploaded_file = st.file_uploader("Choose an Excel file", type=["xls", "xlsx"])

        if uploaded_file is not None:
            # read the Excel file into a Pandas dataframe
            df = pd.read_excel(uploaded_file)

            # check if the dataframe has the expected columns and data types
            column_names = set(df.columns)
            expected_column_names = set([col[0] for col in EXPECTED_COLUMNS])
            if column_names != expected_column_names:
                raise ValueError(
                    f"Column names do not match. Expected {expected_column_names}, but got {column_names}.")

            for col, dtype in EXPECTED_COLUMNS:
                if col in df.select_dtypes(include=[int, float]).columns:
                    if not pd.api.types.is_integer_dtype(df[col]) and not pd.api.types.is_float_dtype(df[col]):
                        raise ValueError(
                            f"Column '{col}' has wrong data type. Expected {dtype}, but got {df[col].dtype}.")

            # if everything is OK, then predict it
            df_model = df.copy()
            df_model['Provinsi'] = df_model['Provinsi'].map(provinsi_dict)
            df['Hasil_Prediksi'] = predict_production(df_model)
            df['Hasil_Prediksi'] = df['Hasil_Prediksi'].apply(lambda x: max(0, x))

            # if everything is OK, display the dataframe
            st.write(df)

            # output
            # create a BytesIO object to hold the Excel data
            excel_data = BytesIO()

            # write the DataFrame to the BytesIO object as an Excel file
            df.to_excel(excel_data, index=False)

            # create a download button for the Excel file
            button = st.download_button(
                label="Download file",
                data=excel_data.getvalue(),
                file_name="Hasil_Prediksi.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

            # Agregasi per tahun
            df_agg = df.groupby('Tahun')['Hasil_Prediksi'].sum().reset_index()
            
            # Membuat line chart interaktif dengan Plotly
            fig = px.line(df_agg, x='Tahun', y='Hasil_Prediksi', title='Total Jumlah Prediksi per Tahun (dalam Ton)')
            fig.update_xaxes(title='Tahun')
            fig.update_yaxes(title='Jumlah Prediksi')
            
            # Menampilkan chart
            st.plotly_chart(fig)

    # throw exception error
    except ValueError as e:
        st.warning(str(e))
    except Exception as e:
        st.error(str(e))

else:
    #  CREATE INPUT FORM
    provinsi = st.selectbox('Dari mana asal provinsi tempat padi tersebut diproduksi?',
                            ('Aceh', 'SumateraUtara', 'SumateraBarat', 'Riau', 'Jambi',
                             'SumateraSelatan', 'Bengkulu', 'Lampung', 'Kep.BangkaBelitung',
                             'Kep.Riau', 'DKIJakarta', 'JawaBarat', 'JawaTengah',
                             'DIYogyakarta', 'JawaTimur', 'Banten', 'Bali', 'NusaTenggaraBarat',
                             'NusaTenggaraTimur', 'KalimantanBarat', 'KalimantanTengah',
                             'KalimantanSelatan', 'KalimantanTimur', 'KalimantanUtara',
                             'SulawesiUtara', 'SulawesiTengah', 'SulawesiSelatan',
                             'SulawesiTenggara', 'Gorontalo', 'SulawesiBarat', 'Maluku',
                             'MalukuUtara', 'PapuaBarat', 'Papua'))
    tahun = st.number_input(label = 'Pada tahun berapa padi diproduksi?', min_value=2011,
                            max_value=10000, step=1, key='1')
    curah_hujan = st.number_input(label = 'Berapa curah hujan pada saat diproduksi? (mm) ',
                                  min_value=0.00, step=0.01, key='2')
    hama_penggerek_batang = st.number_input(label='Berapa jumlah hama penggerek batang pada saat diproduksi? (Hektar) ',
                                            min_value=0.00, step=0.01, key='3')
    hama_batang_coklat = st.number_input(label='Berapa jumlah hama batang coklat pada saat diproduksi? (Hektar) ',
                                         min_value=0.00, step=0.01, key='4')
    hama_tikus = st.number_input(label='Berapa jumlah hama tikus pada saat diproduksi? (Hektar) ',
                                 min_value=0.00, step=0.01, key='5')
    hama_blas = st.number_input(label='Berapa jumlah hama blas pada saat diproduksi? (Hektar) ',
                                min_value=0.00, step=0.01, key='6')
    hama_daun = st.number_input(label='Berapa jumlah hama daun pada saat diproduksi? (Hektar) ',
                                min_value=0.00, step=0.01, key='7')
    hama_tungro = st.number_input(label='Berapa jumlah hama tungro pada saat pada diproduksi? (Hektar) ',
                                  min_value=0.00, step=0.01, key='8')
    kelembapan = st.number_input(label='Berapa kelembapan pada saat diproduksi? (Persentase) ',
                                  min_value=0.00, step=0.01, key='9')
    lama_sinar = st.number_input(label='Berapa lama penyinaran matahari pada saat diproduksi? (Jam) ',
                                  min_value=0.00, step=0.01, key='10')
    luas_banjir = st.number_input(label='Berapa luas lahan terkena banjir pada saat diproduksi? (Hektar) ',
                                  min_value=0.00, step=0.01, key='11')
    luas_kekeringan = st.number_input(label='Berapa luas lahan terkena kekeringan pada saat diproduksi? (Hektar) ',
                                  min_value=0.00, step=0.01, key='12')
    npk_subsidi = st.number_input(label='Berapa jumlah NPK bersubsidi pada saat diproduksi? (Hektar) ',
                                  min_value=0.00, step=0.01, key='13')
    sp36_subsidi = st.number_input(label='Berapa jumlah SP36 bersubsidi pada saat diproduksi? (Hektar) ',
                                  min_value=0.00, step=0.01, key='14')
    urea_subsidi = st.number_input(label='Berapa jumlah urea bersubsidi pada saat diproduksi? (Hektar) ',
                                  min_value=0.00, step=0.01, key='15')
    za_subsidi = st.number_input(label='Berapa jumlah ZA bersubsidi pada saat diproduksi? (Hektar) ',
                                  min_value=0.00, step=0.01, key='16')
    irigasi = st.number_input(label='Berapa jumlah irigasi pada saat diproduksi? (Hektar) ',
                                  min_value=0.00, step=0.01, key='17')
    suhu = st.number_input(label='Berapa suhu / temperatur pada saat diproduksi? (Celcius) ',
                                  min_value=0.00, step=0.01, key='18')
    luas_panen = st.number_input(label='Berapa luas panen didapat pada saat diproduksi? (Hektar) ',
                                  min_value=0.00, step=0.01, key='19')
    produktivitas = st.number_input(label='Berapa tingkat produktivitas pada saat diproduksi? (Kuintal/Hektar) ',
                                  min_value=0.00, step=0.01, key='20')

    # CREATE SUBMIT BUTTON
    submit = st.button('Submit', use_container_width=True)

    if submit:
        # Store data to DataFrame
        df_result = pd.DataFrame({'Provinsi':[provinsi],
                                  'Tahun':[tahun],
                                  'Curah_Hujan':[curah_hujan],
                                  'Hama_Penggerek_Batang':[hama_penggerek_batang],
                                  'Hama_Batang_Coklat':[hama_batang_coklat],
                                  'Hama_Tikus':[hama_tikus],
                                  'Hama_Blas':[hama_blas],
                                  'Hama_Daun':[hama_daun],
                                  'Hama_Tungro':[hama_tungro],
                                  'Kelembapan':[kelembapan],
                                  'Lama_Penyinaran':[lama_sinar],
                                  'Luas_Banjir':[luas_banjir],
                                  'Luas_Kekeringan':[luas_kekeringan],
                                  'NPK_Bersubsidi':[npk_subsidi],
                                  'SP36_Bersubsidi':[sp36_subsidi],
                                  'Urea_Bersubsidi':[urea_subsidi],
                                  'ZA_Bersubsidi':[za_subsidi],
                                  'Irigasi':[irigasi],
                                  'Temperature':[suhu],
                                  'Luas_Panen':[luas_panen],
                                  'Produktivitas':[produktivitas]})

        # Mapping provinsi
        df_result['Provinsi'] = df_result['Provinsi'].map(provinsi_dict)

        # Predict
        result = predict_production(df_result)
                
        df_linechart = data_awal[data_awal['Provinsi'] == provinsi]
        df_linechart = df_linechart[['Provinsi' ,'Tahun', 'Produksi']]

        df_res_linechart = pd.DataFrame({'Provinsi':[provinsi],
                                         'Tahun':[tahun],
                                         'Produksi':[result.values]})
        
        df_linechart = df_linechart.append(df_res_linechart, ignore_index=True)
        st.dataframe(df_linechart)
        st.dataframe(df_res_linechart)
        # Show it
        if result[0] < 0:
            text_res = 'Jumlah Produksi : 0' + 'Ton'
            st.success(text_res)
        else:
            text_res = 'Jumlah Produksi :' + str(result[0]) + 'Ton'
            st.success(text_res)
