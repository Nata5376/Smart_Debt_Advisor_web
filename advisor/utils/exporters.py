import io
import pandas as pd
from django.http import HttpResponse

def export_excel_response(sim_data: dict) -> HttpResponse:
    df = pd.DataFrame({
        "Bulan": sim_data["chart_data"]["labels"],
        "Sisa Hutang (Standar)": sim_data["chart_data"]["saldo_standar"],
        "Sisa Hutang (Akselerasi ML)": sim_data["chart_data"]["saldo_akselerasi"],
    })
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Proyeksi_Pelunasan')
    buffer.seek(0)
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Laporan_Smart_Debt_Advisor.xlsx"'
    return response