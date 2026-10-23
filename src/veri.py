"""UCI Statlog (German Credit) verisini indirir ve Türkçe etiketlerle yükler.

Kaynak: Hofmann, H. (1994). Statlog (German Credit Data). UCI Machine Learning Repository.
https://doi.org/10.24432/C5NC77 (CC BY 4.0)
"""

from pathlib import Path

import pandas as pd
import requests

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data"
DOSYA = Path(__file__).resolve().parent.parent / "veri" / "german.data"

SUTUNLAR = [
    "hesap_durumu", "vade_ay", "kredi_gecmisi", "amac", "tutar", "birikim", "calisma_suresi",
    "taksit_gelir_orani", "medeni_durum_cinsiyet", "kefil", "ikamet_suresi", "mulk", "yas",
    "diger_taksitler", "konut", "mevcut_kredi_sayisi", "meslek", "bakmakla_yukumlu",
    "telefon", "yabanci_calisan", "hedef",
]

ETIKETLER = {
    "hesap_durumu": {"A11": "eksi bakiye", "A12": "0–200 DM", "A13": "200+ DM", "A14": "vadesiz hesap yok"},
    "kredi_gecmisi": {"A30": "hiç kredi yok / hepsi ödendi", "A31": "bu bankadakiler ödendi",
                      "A32": "mevcutlar düzenli ödeniyor", "A33": "geçmişte gecikme",
                      "A34": "kritik hesap / başka bankada kredi"},
    "amac": {"A40": "sıfır araç", "A41": "ikinci el araç", "A42": "mobilya / ekipman",
             "A43": "radyo / TV", "A44": "beyaz eşya", "A45": "tamir", "A46": "eğitim",
             "A48": "yeniden eğitim", "A49": "iş", "A410": "diğer"},
    "birikim": {"A61": "<100 DM", "A62": "100–500 DM", "A63": "500–1000 DM", "A64": "1000+ DM",
                "A65": "bilinmiyor / yok"},
    "calisma_suresi": {"A71": "işsiz", "A72": "<1 yıl", "A73": "1–4 yıl", "A74": "4–7 yıl", "A75": "7+ yıl"},
    "medeni_durum_cinsiyet": {"A91": "erkek: boşanmış/ayrı", "A92": "kadın: boşanmış/ayrı/evli",
                              "A93": "erkek: bekâr", "A94": "erkek: evli/dul", "A95": "kadın: bekâr"},
    "kefil": {"A101": "yok", "A102": "ortak başvuran", "A103": "kefil"},
    "mulk": {"A121": "gayrimenkul", "A122": "birikim / hayat sigortası", "A123": "araç / diğer",
             "A124": "bilinmiyor / yok"},
    "diger_taksitler": {"A141": "banka", "A142": "mağaza", "A143": "yok"},
    "konut": {"A151": "kira", "A152": "kendi evi", "A153": "ücretsiz"},
    "meslek": {"A171": "işsiz / vasıfsız (yerleşik değil)", "A172": "vasıfsız", "A173": "vasıflı çalışan",
               "A174": "yönetici / serbest / yüksek vasıflı"},
    "telefon": {"A191": "yok", "A192": "var"},
    "yabanci_calisan": {"A201": "evet", "A202": "hayır"},
}


def yukle() -> pd.DataFrame:
    """Veriyi yükler; `temerrut` sütunu 1 = kötü kredi (geri ödenmedi), 0 = iyi."""
    if not DOSYA.exists():
        DOSYA.parent.mkdir(exist_ok=True)
        DOSYA.write_text(requests.get(URL, timeout=60).text)
    df = pd.read_csv(DOSYA, sep=" ", header=None, names=SUTUNLAR)
    for sutun, harita in ETIKETLER.items():
        df[sutun] = df[sutun].map(harita)
    df["temerrut"] = (df.pop("hedef") == 2).astype(int)
    return df
