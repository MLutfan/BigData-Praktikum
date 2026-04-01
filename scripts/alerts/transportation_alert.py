def generate_alert(df):
    alerts = []
    
    # Memperbaiki typo dari modul: if len en(df)>100:
    if len(df) > 100:
        alerts.append("⚠️ High traffic volume")
        
    if df["fare"].max() > 90000:
        alerts.append("🚨 High fare detected")
        
    return alerts