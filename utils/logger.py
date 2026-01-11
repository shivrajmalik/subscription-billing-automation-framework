import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root

def take_full_page_screenshot(driver, name="full_screenshot"):
    from datetime import datetime
    import base64

    screenshot_dir = os.path.join(BASE_DIR, "reports", "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")

    try:
        # Use Chrome DevTools Protocol for full-page screenshot
        metrics = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
        width = metrics["contentSize"]["width"]
        height = metrics["contentSize"]["height"]

        driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
            "mobile": False,
            "width": width,
            "height": height,
            "deviceScaleFactor": 1,
        })

        screenshot = driver.execute_cdp_cmd("Page.captureScreenshot", {"fromSurface": True})
        with open(path, "wb") as f:
            f.write(base64.b64decode(screenshot["data"]))

        return path
    except Exception as e:
        print(f"[ERROR] Failed to take full-page screenshot: {e}")
        return None

def write_html_report(test_name, status, message, screenshot_path=None):
    report_dir = os.path.join(BASE_DIR, "reports")
    os.makedirs(report_dir, exist_ok=True)

    # Generate unique timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{test_name}_report_{timestamp}.html"
    report_path = os.path.join(report_dir, filename)

    with open(report_path, "w") as f:
        f.write("<html><head><title>Test Report</title></head><body>")
        f.write(f"<h2>Test Name: {test_name}</h2>")
        f.write(f"<p>Status: <strong>{status}</strong></p>")
        f.write(f"<p>Timestamp: {timestamp}</p>")
        f.write(f"<p>Message: {message}</p>")
        if screenshot_path:
            relative_path = os.path.relpath(screenshot_path, report_dir)
            f.write(f"<p><img src='{relative_path}' width='600'></p>")
        f.write("</body></html>")

    return report_path

