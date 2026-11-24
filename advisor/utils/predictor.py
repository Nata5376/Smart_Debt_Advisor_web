import os
import joblib
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'advisor', 'ml_models', 'debt_advisor.joblib')

def run_prediction(pemasukan: float, total_hutang: float, tenor_bulan: int, pengeluaran_pokok: float) -> dict:
    # Tahap Feature Engineering
    cicilan_standar = round(total_hutang / max(tenor_bulan, 1))
    dti_ratio = round((cicilan_standar / max(pemasukan, 1)) * 100, 2)
    eir_ratio = round((pengeluaran_pokok / max(pemasukan, 1)) * 100, 2)
    disposable_income = round(pemasukan - (pengeluaran_pokok + cicilan_standar))

    # Jika file .joblib dari Anggota 2 sudah tersedia, muat model asli di sini:
    if os.path.exists(MODEL_PATH):
        model_bundle = joblib.load(MODEL_PATH)
        # TODO (Anggota 2 & 3): Sesuaikan inferensi dari model_bundle

    # Kontrak Output Default (Dummy terkalibrasi sebelum model final digabung)
    if dti_ratio > 40 or disposable_income < 0:
        risiko_rf, prob_rf = "High Risk", 84.5
        risiko_xgb, prob_xgb = "High Risk", 87.2
        saran_teks = "Rasio cicilan melebihi 40% pemasukan. Disarankan restrukturisasi tenor menjadi lebih panjang dan pangkas pengeluaran non-esensial minimal 15%."
    elif dti_ratio > 25:
        risiko_rf, prob_rf = "Medium Risk", 68.0
        risiko_xgb, prob_xgb = "Medium Risk", 71.4
        saran_teks = "Kondisi masih terkendali namun ruang dana darurat sempit. Pertahankan pengeluaran pokok dan alokasikan sisa dana untuk pelunasan dipercepat."
    else:
        risiko_rf, prob_rf = "Low Risk", 91.2
        risiko_xgb, prob_xgb = "Low Risk", 93.0
        saran_teks = "Kesehatan kas sangat aman. Anda dapat menambah cicilan akselerasi agar hutang lunas lebih cepat dari tenor awal."

    rekomendasi_cicilan = cicilan_standar
    rekomendasi_tabungan = max(0, round(disposable_income * 0.4))
    sisa_bebas = max(0, disposable_income - rekomendasi_tabungan)

    # Data deret waktu untuk grafik Chart.js
    labels_bulan = [f"Bln {i}" for i in range(1, tenor_bulan + 1)]
    saldo_standar = [max(0, round(total_hutang - (cicilan_standar * i))) for i in range(1, tenor_bulan + 1)]
    akselerasi = cicilan_standar + round(rekomendasi_tabungan * 0.5)
    saldo_akselerasi = [max(0, round(total_hutang - (akselerasi * i))) for i in range(1, tenor_bulan + 1)]

    return {
        "dti_ratio": dti_ratio,
        "eir_ratio": eir_ratio,
        "disposable_income": disposable_income,
        "risiko_rf": risiko_rf,
        "prob_rf": prob_rf,
        "risiko_xgb": risiko_xgb,
        "prob_xgb": prob_xgb,
        "rekomendasi_cicilan": rekomendasi_cicilan,
        "rekomendasi_kebutuhan": pengeluaran_pokok,
        "rekomendasi_tabungan": rekomendasi_tabungan,
        "sisa_bebas": sisa_bebas,
        "saran_teks": saran_teks,
        "chart_data": {
            "labels": labels_bulan,
            "saldo_standar": saldo_standar,
            "saldo_akselerasi": saldo_akselerasi,
            "alokasi": [rekomendasi_cicilan, pengeluaran_pokok, rekomendasi_tabungan + sisa_bebas]
        }
    }