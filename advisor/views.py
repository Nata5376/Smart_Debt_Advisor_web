from datetime import date
from django.shortcuts import render, redirect
from .utils.predictor import run_prediction
from .utils.exporters import export_excel_response

def index(request):
    if request.method == 'POST':
        pemasukan = float(request.POST.get('pemasukan', 3000000))
        total_hutang = float(request.POST.get('total_hutang', 10000000))
        tenor_bulan = int(request.POST.get('tenor_bulan', 12))
        pengeluaran_pokok = float(request.POST.get('pengeluaran_pokok', 1500000))
        jatuh_tempo = int(request.POST.get('tanggal_jatuh_tempo', 25))

        hasil = run_prediction(pemasukan, total_hutang, tenor_bulan, pengeluaran_pokok)
        hasil['input'] = {
            'pemasukan': pemasukan,
            'total_hutang': total_hutang,
            'tenor_bulan': tenor_bulan,
            'pengeluaran_pokok': pengeluaran_pokok,
            'tanggal_jatuh_tempo': jatuh_tempo,
        }
        request.session['last_simulation'] = hasil
        return redirect('dashboard')

    return render(request, 'index.html')

def dashboard(request):
    hasil = request.session.get('last_simulation')
    if not hasil:
        # Default simulasi contoh awal (Hutang 10jt, Tenor 12 bln, Gaji 3jt)
        hasil = run_prediction(3000000, 10000000, 12, 1500000)
        hasil['input'] = {
            'pemasukan': 3000000, 'total_hutang': 10000000,
            'tenor_bulan': 12, 'pengeluaran_pokok': 1500000, 'tanggal_jatuh_tempo': 25
        }
    return render(request, 'dashboard.html', {'hasil': hasil})

def history(request):
    hasil = request.session.get('last_simulation')
    hari_ini = date.today().day
    jatuh_tempo = hasil['input']['tanggal_jatuh_tempo'] if hasil else 25
    butuh_reminder = abs(jatuh_tempo - hari_ini) <= 3
    return render(request, 'history.html', {
        'hasil': hasil,
        'butuh_reminder': butuh_reminder,
        'jatuh_tempo': jatuh_tempo
    })

def export_excel(request):
    hasil = request.session.get('last_simulation') or run_prediction(3000000, 10000000, 12, 1500000)
    return export_excel_response(hasil)