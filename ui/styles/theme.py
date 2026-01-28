from utils.path import resource_path


def load_theme(app, theme_name):
    qss_path = resource_path(f"ui/styles/{theme_name}.qss")
    with open(qss_path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())