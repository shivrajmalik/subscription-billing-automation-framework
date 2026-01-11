import os
from datetime import datetime

def take_screenshot(driver, name="screenshot"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = "reports/screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    path = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
    driver.save_screenshot(path)
    return path

def write_html_report(test_name, status, message, screenshot_path=None):
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_path = os.path.join(report_dir, f"{test_name}_report.html")

    with open(report_path, "w") as f:
        f.write("<html><head><title>Test Report</title></head><body>")
        f.write(f"<h2>Test Name: {test_name}</h2>")
        f.write(f"<p>Status: <strong>{status}</strong></p>")
        f.write(f"<p>Timestamp: {timestamp}</p>")
        f.write(f"<p>Message: {message}</p>")
        if screenshot_path:
            f.write(f"<p><img src='{screenshot_path}' width='600'></p>")
        f.write("</body></html>")

    return report_path
