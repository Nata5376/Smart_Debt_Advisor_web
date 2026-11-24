from django.db import models
from django.contrib.auth.models import User

class DebtSimulation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pemasukan = models.FloatField()
    total_hutang = models.FloatField()
    tenor_bulan = models.IntegerField()
    pengeluaran_pokok = models.FloatField()
    tanggal_jatuh_tempo = models.IntegerField(default=25)
    
    # Hasil Feature Engineering & Prediksi ML
    dti_ratio = models.FloatField(default=0)
    disposable_income = models.FloatField(default=0)
    risiko_rf = models.CharField(max_length=50, default='Medium Risk')
    risiko_xgb = models.CharField(max_length=50, default='Medium Risk')
    rekomendasi_cicilan = models.FloatField(default=0)
    sudah_bayar_bulan_ini = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Simulasi Hutang Rp {self.total_hutang:,.0f} ({self.tenor_bulan} bln)"