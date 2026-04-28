import matplotlib.pyplot as plt
import numpy as np

def plot_bimodal_demand(p_basis, p_peak1, mu1, sigma1, p_peak2, mu2, sigma2, start=6, end=23):
    # 1. Hochauflösende Zeitachse für eine glatte Kurve (z.B. 200 Punkte)
    t_smooth = np.linspace(start, end, 200)
    
    # 2. Stündliche Zeitpunkte für die Balken (deine eigentlichen Daten)
    t_hourly = np.arange(start, end + 1)
    
    # Hilfsfunktion für die Berechnung (interne Logik)
    def calc_curve(t):
        peak1 = p_peak1 * np.exp(-((t - mu1)**2) / (2 * sigma1**2))
        peak2 = p_peak2 * np.exp(-((t - mu2)**2) / (2 * sigma2**2))
        return p_basis + peak1 + peak2

    # Daten berechnen
    curve_smooth = calc_curve(t_smooth)
    demand_hourly = np.round(calc_curve(t_hourly)).astype(int)

    # Plot erstellen
    plt.figure(figsize=(12, 6))
    
    # Die stündlichen Erwartungswerte als Balken
    plt.bar(t_hourly, demand_hourly, alpha=0.3, color='blue', label='Stündliche Erwartungswerte (Diskret)')
    
    # Die kontinuierliche Modell-Kurve
    plt.plot(t_smooth, curve_smooth, color='red', linewidth=2, label='Mathematisches Modell (Kontinuierlich)')
    
    # Punkte auf den Stundenmarken setzen
    plt.scatter(t_hourly, demand_hourly, color='darkblue', zorder=3)

    # Styling
    plt.title(f"Nachfrageverlauf von {start:02d}:00 bis {end:02d}:00 Uhr", fontsize=14)
    plt.xlabel("Uhrzeit [h]", fontsize=12)
    plt.ylabel("Anzahl Personen", fontsize=12)
    plt.xticks(t_hourly)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.show()

def plot_plateau_demand(p_basis, p_plateau, mu_plat, sigma_plat, p_dip, mu_dip, sigma_dip, start=6, end=23):
    """Visualisiert die Plateau-Nachfrage mit Mittagsdelle."""
    
    # 1. Zeitachsen erstellen
    t_smooth = np.linspace(start, end, 500)  # Für die glatte Modelllinie
    t_hourly = np.arange(start, end + 1)     # Für die tatsächlichen Stundenbalken
    
    # 2. Mathematische Funktionen
    def get_values(t):
        # Super-Gauß für das Plateau (Potenz 8 macht die Kanten steil)
        plateau = p_plateau * np.exp(-0.5 * ((t - mu_plat) / sigma_plat)**8)
        # Gauß für die Delle (Dip)
        dip = p_dip * np.exp(-((t - mu_dip)**2) / (2 * sigma_dip**2))
        # Basis + Plateau - Delle
        return p_basis + plateau - dip

    # 3. Daten berechnen
    curve_smooth = get_values(t_smooth)
    demand_hourly = np.round(np.maximum(get_values(t_hourly), 0)).astype(int)

    # 4. Plot erstellen
    plt.figure(figsize=(12, 6))
    
    # Balken für die diskreten Stundenwerte
    plt.bar(t_hourly, demand_hourly, alpha=0.3, color='orange', label='Stündliche Werte (Simuliert)')
    
    # Glatte Modell-Linie
    plt.plot(t_smooth, curve_smooth, color='darkorange', linewidth=2, label='Plateau-Modell (Super-Gauß)')
    
    # Markierungspunkte
    plt.scatter(t_hourly, demand_hourly, color='red', zorder=3, s=20)

    # Styling
    plt.title("Samstags-Nachfrageverlauf (Plateau & Mittags-Dip)", fontsize=14)
    plt.xlabel("Uhrzeit [h]", fontsize=12)
    plt.ylabel("Anzahl Personen", fontsize=12)
    plt.xticks(t_hourly)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.legend()
    
    plt.show()

# Aufruf mit deinen Parametern
# plot_bimodal_demand(50, 175, 11, 4, 215, 18, 2)
# plot_plateau_demand(50, 175, 14, 5.5, 50, 13, 0.8)