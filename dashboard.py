import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


data_sewa_sepeda = pd.read_csv('day.csv')
data_sewa_sepeda['dteday'] = pd.to_datetime(data_sewa_sepeda['dteday'])
st.title("Dashboard Penyewaan Sepeda 🚴")
st.sidebar.header("Filter Data")


min_date = data_sewa_sepeda['dteday'].min().date()
max_date = data_sewa_sepeda['dteday'].max().date()
tanggal_pilih = st.sidebar.date_input('Pilih Rentang Tanggal', [min_date, max_date], min_value=min_date, max_value=max_date)

if isinstance(tanggal_pilih, list) and len(tanggal_pilih) == 2:
    tanggal_mulai, tanggal_selesai = tanggal_pilih
else:
    tanggal_mulai, tanggal_selesai = min_date, max_date

data_filtered = data_sewa_sepeda[(data_sewa_sepeda['dteday'].dt.date >= tanggal_mulai) & 
                                 (data_sewa_sepeda['dteday'].dt.date <= tanggal_selesai)]

st.sidebar.header("Pengaturan Visualisasi")
tema_warna = st.sidebar.selectbox("Pilih Tema Warna Visualisasi", ["Blues", "Greens", "Reds", "Purples"])

waktu_tersibuk = data_filtered.groupby('weekday')['cnt'].mean()

pengaruh_cuaca = data_filtered.groupby('weathersit')['cnt'].mean()

cuaca_label = {1: 'Cerah', 2: 'Hujan ringan', 3: 'Kabut'}
pengaruh_cuaca.index = pengaruh_cuaca.index.map(cuaca_label)

st.markdown("## 📅 Rata-rata Penyewaan Sepeda Per Hari dalam Seminggu")
fig, ax = plt.subplots()
sns.lineplot(x=waktu_tersibuk.index, y=waktu_tersibuk.values, marker='o', color='blue', ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda Per Hari', fontsize=14)
ax.set_ylabel('Rata-rata Jumlah Penyewaan')
ax.set_xlabel('Hari dalam Seminggu')
ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
ax.set_xticklabels(['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
ax.grid(True)
st.pyplot(fig)

st.markdown("## ☁️ Pengaruh Kondisi Cuaca terhadap Jumlah Penyewaan Sepeda")
fig, ax = plt.subplots()
sns.barplot(x=pengaruh_cuaca.index, y=pengaruh_cuaca.values, palette=tema_warna, ax=ax)
ax.set_title('Pengaruh Cuaca terhadap Penyewaan Sepeda', fontsize=14)
ax.set_ylabel('Rata-rata Jumlah Penyewaan')
ax.set_xlabel('Kondisi Cuaca')
st.pyplot(fig)

st.sidebar.write("📅 **Tanggal Data**: ", min_date.strftime("%Y-%m-%d"), " s/d ", max_date.strftime("%Y-%m-%d"))
st.sidebar.write("🔍 **Total Baris dalam Dataset**: ", len(data_sewa_sepeda))
