# Bike Analysis 

## Deskripsi
Analisis ini bertujuan untuk mendapatkan *insight* dari dataset yang sudah disediakan.

Terdapat 2 dataset yaitu:
1. Hours Dataset, berisi rekam peminjaman sepeda berdasarkan jam dalam hari.
1. Days Dataset, berisi rekam peminjaman sepeda berdasarkan hari dalam tahun.

## Setup Environment

```
    conda create --name submission python=3.9
    conda activate submission
    pip install numpy pandas scipy matplotlib seaborn jupyter streamlit scikit-learn 
```

atau dapat juga menggunakan perintah di bawah untuk menginstall library

```
    pip install -r requirements.txt
```

## Run Streamlit Dashboard
```
    streamlit run dashboard/dashboard.py
```