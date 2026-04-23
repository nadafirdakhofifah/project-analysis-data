import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# page config
st.set_page_config(
    page_title="Air Quality Dashboard",
    page_icon="🌫️",
    layout="wide"
)

# load data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour
    return df

df = load_data()

# sidebar
st.sidebar.title("📌 Filter Dashboard")

selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    sorted(df['year'].unique()),
    default=sorted(df['year'].unique())
)

selected_month = st.sidebar.multiselect(
    "Pilih Bulan",
    sorted(df['month'].unique()),
    default=sorted(df['month'].unique())
)

# filter data
filtered_df = df[
    (df['year'].isin(selected_year)) &
    (df['month'].isin(selected_month))
]

# header
st.title("🌫️ Air Quality Dashboard")
st.markdown("### Analisis Kualitas Udara Wilayah Aotizhongxin (2013–2017)")
st.markdown("---")

# KPI
col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg PM2.5", round(filtered_df['PM2.5'].mean(),2))
col2.metric("Max PM2.5", round(filtered_df['PM2.5'].max(),2))
col3.metric("Avg Temp", round(filtered_df['TEMP'].mean(),2))
col4.metric("Total Records", len(filtered_df))

# chart 1 - per tahun
st.subheader("📈 Tren PM2.5 per Tahun")

yearly = filtered_df.groupby('year')['PM2.5'].mean()

fig, ax = plt.subplots(figsize=(10,4))
yearly.plot(marker='o', linewidth=3, ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("PM2.5")
ax.grid(True)
st.pyplot(fig)

# chart 2 - per bulan
st.subheader("📊 Rata-rata PM2.5 per Bulan")

monthly = filtered_df.groupby('month')['PM2.5'].mean()

fig, ax = plt.subplots(figsize=(10,4))
monthly.plot(kind='bar', ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("PM2.5")
st.pyplot(fig)

# heatmap
st.subheader("🔥 Korelasi Faktor Cuaca")

corr = filtered_df[['PM2.5','TEMP','PRES','DEWP','RAIN','WSPM']].corr()

fig, ax = plt.subplots(figsize=(8,5))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
st.pyplot(fig)

# chart arah angin
st.subheader("🌬️ Rata-rata PM2.5 Berdasarkan Arah Angin")

wind_pm25 = filtered_df.groupby('wd')['PM2.5'].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10,5))
wind_pm25.plot(kind='bar', ax=ax)

ax.set_xlabel("Arah Angin")
ax.set_ylabel("Rata-rata PM2.5")
ax.set_title("Pengaruh Arah Angin terhadap PM2.5")

st.pyplot(fig)

# kategori kualitas udara
st.subheader("🧩 Kategori Kualitas Udara")

bins = [0,50,100,150,1000]
labels = ['Good','Moderate','Unhealthy','Hazardous']

filtered_df['Category'] = pd.cut(
    filtered_df['PM2.5'],
    bins=bins,
    labels=labels
)

cat = filtered_df['Category'].value_counts()

fig, ax = plt.subplots(figsize=(8,4))
cat.plot(kind='pie', autopct='%1.1f%%', ax=ax)
ax.set_ylabel("")
st.pyplot(fig)

# download data
st.subheader("⬇️ Download Cleaned Dataset")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_air_quality.csv",
    mime="text/csv"
)

# insight
st.subheader("📌 Insight Utama")

st.info("""
1. PM2.5 tertinggi umumnya terjadi saat musim dingin.  
2. Kecepatan angin berpengaruh menurunkan polusi udara. 
3. Angin dari arah tertentu cenderung membawa polutan lebih tinggi,
sedangkan arah lain menunjukkan udara lebih bersih. 
4. Beberapa periode masuk kategori Unhealthy hingga Hazardous.
""")

# footer
st.markdown("---")
st.caption("Created by Nada Firda | Dicoding Data Scientist Submission")