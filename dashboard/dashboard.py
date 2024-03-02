import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# membaca dataset hour
df = pd.read_csv("hour.csv")
df.head()

# Menghapus kolom yang tidak diperlukan
drop_col = ['windspeed']

for col in df.columns:
    if col in drop_col:
        df.drop(labels=col, axis=1, inplace=True)

# kolom season
df['season'] = df['season'].map({
    1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})

# kolom yr (YEAR)
df ['yr'] = df['yr'].map({
    0 : 2011 , 1 : 2012
})

# kolom mnth (MONTH)
df['mnth'] = df['mnth'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})

# kolom weekday
df['weekday'] = df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})

# kolom weathersit
df['weathersit'] = df['weathersit'].map({
    1: 'Clear',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# membuat func untuk dataframe

# func dataframe sepeda harian
def create_df_pengguna_sepeda_harian(df) :
    df_harian = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return df_harian

# func dataframe pengguna sepeda harian 'casual'
def create_df_pengguna_casual_harian(df):
    df_casual_harian = df.groupby(by = 'dteday').agg({
        'casual' : 'sum'
    }).reset_index()
    return df_casual_harian

# func dataframe pengguna sepeda harian 'registered'
def create_df_pengguna_registered_harian(df):
    df_registered_harian = df.groupby(by = 'dteday').agg({
        'registered' : 'sum'
    }).reset_index()
    return df_registered_harian
    
# func dataframe pengguna sepeda berdasarkan musim
def create_df_season(df):
    df_season = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return df_season

# func dataframe pengguna sepeda berdasarkan bulan
def create_df_bulan(df):
    df_monthly = df.groupby(by='mnth').agg({
        'cnt': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    df_monthly = df_monthly.reindex(ordered_months, fill_value=0)
    return df_monthly

# func dataframe pengguna weeekday
def create_df_weekday(df):
    df_weekday = df.groupby(by='weekday').agg({
        'cnt': 'sum'
    }).reset_index()
    # ordered_day = [
    #     'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri','Sat'
    # ]
    # df_weekday = df_weekday.reindex(ordered_day, fill_value=0)
    return df_weekday

# func dataframe holiday
def create_df_holiday(df):
    df_holiday = df.groupby(by='holiday')['cnt'].sum()
    return df_holiday

# func dataframe berdasarkan cuaca
def create_df_cuaca(df):
    df_cuaca = df.groupby(by='weathersit').agg({
        'cnt': 'sum'
    })
    return df_cuaca

# func dataframe berdasarkan jam
def create_df_pengguna_perjam(df):
    df_perjam = df.groupby('hr')['cnt'].sum().reset_index()
    return df_perjam


# widget filter dataframe
min_date = pd.to_datetime(df['dteday']).dt.date.min()
max_date = pd.to_datetime(df['dteday']).dt.date.max()

# sidebar widget
with st.sidebar:
    st.image('cycling.png')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

# inisialisasi dataframe berdasarkan rentang waktu
df_home = df[(df['dteday'] >= str(start_date)) & 
                (df['dteday'] <= str(end_date))]

# mengaplikasikan dataframe ke dalam fungsi
pengguna_harian = create_df_pengguna_sepeda_harian(df_home)
pengguna_casual_harian = create_df_pengguna_casual_harian(df_home)
pengguna_registered_harian = create_df_pengguna_registered_harian(df_home)
pengguna_tiap_musim = create_df_season(df_home)
pengguna_tiap_bulan = create_df_bulan(df_home)
pengguna_weekday= create_df_weekday(df_home)
pengguna_holiday= create_df_holiday(df_home)
pengguna_berdasarkan_cuaca = create_df_cuaca(df_home)
pengguna_berdasarkan_jam = create_df_pengguna_perjam(df_home)

# Dashboard 

# Title.header
st.header('Bike Rental Dashboard :sparkles:')

# Menampilkan jumlah penyewaan harian
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    pengguna_casual = pengguna_casual_harian['casual'].sum()
    st.metric('Casual Users', value= pengguna_casual)

with col2:
    pengguna_registered = pengguna_registered_harian['registered'].sum()
    st.metric('Registered Users', value= pengguna_registered)

with col3:
    total_pengguna = pengguna_harian['cnt'].sum()
    st.metric('Total Users', value= total_pengguna)

# Menampilkan jumlah pengguna sepeda bulanan
st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    pengguna_tiap_bulan.index,
    pengguna_tiap_bulan['cnt'],
    marker='o', 
    linewidth=2,
)

for index, row in enumerate(pengguna_tiap_bulan['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# Menampilkan jumlah pengguna sepeda berdasarkan musim
st.subheader('Seasonly Rentals')

fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='season',
    y='registered',
    data=pengguna_tiap_musim,
    label='Registered',
    color=sns.color_palette("viridis")[1],
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=pengguna_tiap_musim,
    label='Casual',
    color=sns.color_palette("viridis")[5],
    ax=ax
)

for index, row in pengguna_tiap_musim.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah pengguna sepeda')
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

# Menampilkan jumlah pengguna sepeda berdasarkan kondisi cuaca
st.subheader('Weatherly Rentals')

fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x=pengguna_berdasarkan_cuaca.index,
    y=pengguna_berdasarkan_cuaca['cnt'],
    palette="viridis",
    ax=ax
)

for index, row in enumerate(pengguna_berdasarkan_cuaca['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel("Cuaca", fontsize=20)
ax.set_ylabel("Jumlah Pengguna Sepeda", fontsize=15)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Menampilkan jumlah pengguna sepeda berdasarkan weekday
st.subheader("Weekday Rentals")
fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x=pengguna_weekday['weekday'],
    y=pengguna_weekday['cnt'],
    palette="viridis",
    ax=ax
)

for index, row in enumerate(pengguna_weekday['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel("Hari", fontsize=20)
ax.set_ylabel("Jumlah Pengguna Sepeda", fontsize=15)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Menampilkan Persentase Pengguna Sepeda Holiday vs Not Holiday
st.subheader("Percentage of User in Holiday vs Not Holiday")
fig, ax = plt.subplots(figsize=(8, 8))

sns.set_palette("viridis")
ax.pie(
    x=pengguna_holiday,
    labels=df_home['holiday'].unique(),
    autopct='%1.1f%%'
)
ax.set_title("Persentase Pengguna Pada Hari Libur")

st.pyplot(fig)

# Menampilkan Pengguna Berdasarkan Jam 
st.subheader('Number of Users by Hour')

fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(pengguna_berdasarkan_jam['hr'], pengguna_berdasarkan_jam['cnt'], marker=".", label='Count', color='navy')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Sepeda Disewa')
ax.set_title('Penggunaan Sepeda per Jam')
ax.set_xticks(range(24))
ax.grid(True)

st.pyplot(fig)