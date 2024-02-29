from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


def verileri_al(url, sayfa_sayisi):
    liste = []
    #Browse all pages
    for sayfa_numarasi in range(1, sayfa_sayisi + 1):
        r = requests.get(f"{url}?page={sayfa_numarasi}")
        if r.status_code != 200:
            print(f"İstek başarısız. Hata kodu: {r.status_code}")
            continue  # İstek başarısızsa bir sonraki sayfaya geç
        time.sleep(0.5)
        soup = BeautifulSoup(r.content, "lxml")
        st1 = soup.find("div", attrs={"id": "list"})
        st2 = st1.find("div", attrs={"class": "list-block"})
        #Get the details of the products
        for detaylar in st2:
            link = detaylar.a.get("href")

            r1 = requests.get(link)
            if r1.status_code != 200:
                print(f"İstek başarısız. Hata kodu: {r1.status_code}")
                continue  # İstek başarısızsa bir sonraki linki al
            time.sleep(0.5)
            soup1 = BeautifulSoup(r1.content, "lxml")

            try:
                first = soup1.find("div", attrs={"id": "auto_title"}).text
            except AttributeError:
                first = "Bilgi Yok"
            try:
                second = soup1.find("a", attrs={"class": "_pr_auto_link_make v3-c-btn-text link"}).text
            except AttributeError:
                second = "Bilgi Yok"
            try:
                third = soup1.find("a", attrs={"class": "_pr_auto_link_model v3-c-btn-text link"}).text
            except AttributeError:
                third = "Bilgi Yok"
            try:
                fourth = soup1.find("div", attrs={"data-view-unit": "KM"}).text.replace("km","")
            except AttributeError:
                fourth = "Bilgi Yok"
            try:
                fifth = soup1.find("div", attrs={"class": "specs-value specs-location"}).text
            except AttributeError:
                fifth = "Bilgi Yok"
            liste.append([first, second, thirst, fourth, fifth])
    df = pd.DataFrame(liste, columns=["first", "second", "thirst", "fourth", "fifth"])
    return df


# Fonksiyonu kullanarak verileri al
url = "YOUR URL"
sayfa_sayisi = 5  # Kaç sayfa veri almak istediğimiz
df = verileri_al(url, sayfa_sayisi)
df.to_excel("abc.xlsx")
