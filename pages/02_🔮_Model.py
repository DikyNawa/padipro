import streamlit as st
import pandas as pd
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
filename_model = 'finalized_model_linreg.sav'

@st.cache_resource
def load_files():
    # Load large model
    model = pkl.load(open(filename_model, 'rb'))
    data_dummy = pd.read_excel('Data_Contoh.xlsx')
    return model, data_dummy

model, data_dummy = load_files()

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
            prediksi = model.predict(df_model.values)
            df['Hasil_Prediksi'] = prediksi

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
    curah_hujan = st.number_input(label = 'Berapa curah hujan pada saat diproduksi? ',
                                  min_value=0.0, step=0.1, key='2')
    hama_penggerek_batang = st.number_input(label='Berapa jumlah hama penggerek batang pada saat diproduksi? ',
                                            min_value=0, max_value=10000, step=1000, key='3')
    hama_batang_coklat = st.number_input(label='Berapa jumlah hama batang coklat pada saat diproduksi? ',
                                         min_value=0, max_value=10000, step=1000, key='4')
    hama_tikus = st.number_input(label='Berapa jumlah hama tikus pada saat diproduksi? ',
                                 min_value=0, max_value=10000, step=1000, key='5')
    hama_blas = st.number_input(label='Berapa jumlah hama blas pada saat diproduksi? ',
                                min_value=0, max_value=10000, step=1000, key='6')
    hama_daun = st.number_input(label='Berapa jumlah hama daun pada saat diproduksi? ',
                                min_value=0, max_value=10000, step=1000, key='7')
    hama_tungro = st.number_input(label='Berapa jumlah hama tungro pada saat pada diproduksi? ',
                                  min_value=0, max_value=10000, step=1000, key='8')
    kelembapan = st.number_input(label='Berapa kelembapan pada saat diproduksi? ',
                                  min_value=0, max_value=1000, step=10, key='9')
    lama_sinar = st.number_input(label='Berapa lama penyinaran matahari pada saat diproduksi? ',
                                  min_value=0, max_value=1000, step=10, key='10')
    luas_banjir = st.number_input(label='Berapa luas lahan terkena banjir pada saat diproduksi? ',
                                  min_value=0, max_value=1000, step=100, key='11')
    luas_kekeringan = st.number_input(label='Berapa luas lahan terkena kekeringan pada saat diproduksi? ',
                                  min_value=0, max_value=10000, step=100, key='12')
    npk_subsidi = st.number_input(label='Berapa jumlah NPK bersubsidi pada saat diproduksi? ',
                                  min_value=0, max_value=10000, step=100, key='13')
    sp36_subsidi = st.number_input(label='Berapa jumlah SP36 bersubsidi pada saat diproduksi? ',
                                  min_value=0, max_value=10000, step=100, key='14')
    urea_subsidi = st.number_input(label='Berapa jumlah urea bersubsidi pada saat diproduksi? ',
                                  min_value=0, max_value=10000, step=100, key='15')
    za_subsidi = st.number_input(label='Berapa jumlah ZA bersubsidi pada saat diproduksi? ',
                                  min_value=0, max_value=10000, step=100, key='16')
    irigasi = st.number_input(label='Berapa jumlah irigasi pada saat diproduksi? ',
                                  min_value=0, max_value=10000, step=10, key='17')
    suhu = st.number_input(label='Berapa suhu / temperatur pada saat diproduksi? ',
                                  min_value=0, max_value=10000, step=10, key='18')
    luas_panen = st.number_input(label='Berapa luas panen didapat pada saat diproduksi? ',
                                  min_value=0, max_value=10000, step=1000, key='19')
    produktivitas = st.number_input(label='Berapa tingkat produktivitas pada saat diproduksi? ',
                                  min_value=0, max_value=10000, step=1000, key='20')

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
        result = model.predict(df_result.values)

        # Show it
        st.success(result)