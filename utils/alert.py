def generate_alert(event):
    alerts = {
        "multi_face": "Multiple faces detected",
        "no_face": "No face detected",
        "tab_switch": "Tab switched",
        "noise": "Background noise detected"
    }

    return alerts.get(event, "Unknown alert")