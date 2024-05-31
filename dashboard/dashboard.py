import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

hoursDf = pd.read_csv('dashboard/hours-new.csv')
daysDf = pd.read_csv('dashboard/days-new.csv')

# Fungsi Helper
# RATA-RATA
def avgYearByMonth(df, year):
    # Menambahkan kondisi tahun yang dipilih
    if year == '2011':
        df = df[df['yr'] == 0]
    elif year == '2012':
        df = df[df['yr'] == 1]
    
    # Agregasi data peminjam berdasarkan bulan
    groupedByMonth = df.groupby('mnth').agg({
        'casual': ['std', 'mean', 'sum'],
        'registered': ['std', 'mean', 'sum']
    }).round().astype(int)
    
    #Melakukan reset index
    groupedByMonth = groupedByMonth.reset_index()
    
    #Mengubah nama kolom
    groupedByMonth.rename(columns={
        'mnth': 'month',
        'registered': 'Registered',
        'casual': 'Casual'
    }, inplace=True)
    
    return groupedByMonth, year

# Visualisasi data berdasarkan tahun perbulannya
def visualAvgYearByMonth(table, dside, year):
    #Membuat kondisi warna berbeda pada tiap tahun
    if year == '2011':
        color = 'red'
    elif year == '2012':
        color = 'blue'
    
    #Membuat kanvas
    fig, ax = plt.subplots(figsize=(20,12))
    # Plotting menggunakan Bar Plot
    sns.barplot(y=table[dside]['mean'], x=table['month'], data=table, color=color)
    #Buat dan ubah ukuran font
    ax.tick_params(axis='x', labelsize=24) 
    ax.tick_params(axis='y', labelsize=24)
    ax.set_xlabel('Month(s)', fontsize=24) 
    ax.set_ylabel('Mean', fontsize=24) 
    #Buat judul visualisasi
    ax.set_title('Mean Bicycle Loaners ' + dside + ' in ' + year, fontsize=24)
    # Tampilkan VIsualisasi
    st.pyplot(fig)

# visualisasi data berdarkan tahun keseluruhan
def visualAvgBothYear(df, dside):
    df2011 = df[df['yr'] == 0]
    df2012 = df[df['yr'] == 1]
    
    # Data 2011
    df2011 = df2011.groupby('mnth').agg({
        'casual': ['std', 'mean', 'sum'],
        'registered': ['std', 'mean', 'sum']
    }).round().astype(int)
    
    df2011 = df2011.reset_index()
    
    df2011.rename(columns={
        'mnth': 'month',
        'registered': 'Registered',
        'casual': 'Casual'
    }, inplace=True)
    
    #Data 2012
    df2012 = df2012.groupby('mnth').agg({
        'casual': ['std', 'mean', 'sum'],
        'registered': ['std', 'mean', 'sum']
    }).round().astype(int)
    
    df2012 = df2012.reset_index()
    
    df2012.rename(columns={
        'mnth': 'month',
        'registered': 'Registered',
        'casual': 'Casual'
    }, inplace=True)
    
    fig, ax = plt.subplots(figsize=(20,12))
    ax.plot(
        df2011['month'],
        df2011[dside]['mean'],
        marker='o',
        color='red'
    )
    ax.plot(
        df2012['month'],
        df2012[dside]['mean'],
        marker='o',
        color='blue'
    )
    
    ax.tick_params(axis='x', labelsize=24) 
    ax.tick_params(axis='y', labelsize=24)
    ax.set_xlabel('Month(s)', fontsize=24) 
    ax.set_ylabel('Mean', fontsize=24) 
    ax.set_title('Mean Bicycle Loaners ' + dside + ' in Both Year', fontsize=24)
    
    st.pyplot(fig)


st.markdown("<h1 style='text-align: center;'>Dashboard Bicycle Rent</h1>", unsafe_allow_html=True)

# Membuat 2 tab
tab1, tab2 = st.tabs(['Averages', 'Another Factors'])

css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.5rem;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)
with tab1:
    st.subheader('Averages Loaner by Year')
        
    me1, me2 = st.columns(2)
    
    # Kolom 1 : Pilihan Tahun
    with me1:
        year = st.selectbox(
            label="Pick the year",
            options=('2011', '2012')
        )
    # Kolom 2 : Pilihan Tipe Pengguna
    with me2:
        dataSide = st.selectbox(
            label="Pick the data side",
            options=('Registered', 'Casual')
        )
    
    #Mempersiapkan data untuk divisualisasikan
    groupedByMonth, year = avgYearByMonth(daysDf, year)
    # Visualisasi data berdasarkan tahun perbulannya
    visualAvgYearByMonth(groupedByMonth, dataSide, year=year)
    
    #visualisasi data berdarkan tahun keseluruhan
    st.header('Averages Loaner by Both Year')
    visualAvgBothYear(daysDf, dataSide)

with tab2:
    # Faktor 1
    st.subheader('Range Times Factor')
    #Filtering berdasarkan Range Waktu
    groupedByRangeTimes = hoursDf.groupby(by='range_times').range_times.count().sort_values(ascending=False)
    
    # Visualisasi Berdasarkan Range Waktu
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.pie(
        x=groupedByRangeTimes.values,
        labels=groupedByRangeTimes.index,
        autopct='%1.1f%%',
        colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
        textprops={'fontsize': 20} 
    )
    ax.set_title('Total Count By Range Times', fontsize=20)
    st.pyplot(fig)
    
    # Faktor 2
    st.subheader('Day Type Factor')
    # Filtering berdasarkan tipe hari
    groupedByDayType = hoursDf.groupby('day_type').cnt.sum().sort_values(ascending=False).round().astype(int)
    # Membulatkan rata-rata mean dan mengubah tipe data menjadi integer
    
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.pie(
        x=groupedByDayType.values,
        labels=groupedByDayType.index,
        autopct='%1.1f%%',
        colors=['red', 'orange'],
        explode=[0.1, 0],
        textprops={'fontsize': 20} 
    )
    ax.set_title('Total Count By Day Type', fontsize=20)
    st.pyplot(fig)
    
    # Faktor 3
    st.subheader('Weather Situation Factor')
    # Filtering berdasarkan cuaca
    groupedByWeather = hoursDf.groupby('weather_situation').cnt.count().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(18, 12))
    plt.bar(x=groupedByWeather.index, height=groupedByWeather.values)
    plt.title('Total Loaners By Weather Situation', fontsize=24)
    ax.tick_params(axis='x', labelsize=24) 
    ax.tick_params(axis='y', labelsize=24)
    ax.set_xlabel('Weather', fontsize=24) 
    ax.set_ylabel('Counts', fontsize=24) 
    st.pyplot(fig)
    
    # Faktor 4
    st.subheader('Season Type Factor')
    # Filtering berdasarkan musim
    groupedBySeason = hoursDf.groupby('season_type').cnt.mean().sort_values(ascending=False).round()
    groupedBySeason.sort_values(ascending=False, inplace=True)
    
    fig, ax = plt.subplots(figsize=(18, 12))
    plt.bar(x=groupedBySeason.index, height=groupedBySeason.values, color=['green', 'blue', 'blue', 'blue'], width=0.6)
    plt.title('Total Loaners By Season Type', fontsize=24)
    ax.tick_params(axis='x', labelsize=24) 
    ax.tick_params(axis='y', labelsize=24)
    ax.set_xlabel('Season Type', fontsize=24)
    ax.set_ylabel('Counts', fontsize=24) 
    st.pyplot(fig)
