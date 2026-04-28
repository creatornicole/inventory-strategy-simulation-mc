CONFIG = {
    "runs": {
        "label": "Monte-Carlo-Durchläufe",
        "min": 1000,
        "max": 20000,
        "default": 10000,
        "step": 1000
    },
    "w_range": {
        "label": "Anzahl Waggons (Min-Max)",
        "min": 1,
        "max": 10,
        "default": (1, 4),
        "step": 1
    },
    "lambda_param": {
        "label": "Unzufriedenheitskosten (in €)",
        "min": 1,
        "max": 10000,
        "default": 1000,
        "step": 50,
        "help": "Strafkosten für die Unzufriedenheit der Fahrgäste bei überfüllten Zügen"
    },
    "overflow_costs": {
        "label": "Kosten pro abgewiesenem Fahrgast (in €)",
        "min": 0,
        "max": 10000,
        "default": 100,
        "step": 10,
        "help": "Kosten, die entstehen, wenn Fahrgäste aufgrund voller Züge nicht befördert werden können"
    },
    "cost_up": {
        "label": "Kosten pro Waggon hinzufügen (in €)",
        "min": 0,
        "max": 10000,
        "default": 300,
        "step": 10,
        "help": "Kosten für das Anfügen eines zusätzlichen Waggons zur Kapazitätserhöhung"
    },
    "cost_down": {
        "label": "Kosten pro Waggon entfernen (in €)",
        "min": 0,
        "max": 10000,
        "default": 100,
        "step": 10,
        "help": "Kosten für das Abkoppeln eines Waggons zur Kapazitätsreduktion"
    }
}