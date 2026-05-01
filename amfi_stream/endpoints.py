from datetime import date

SCHEME_MASTER_URL = "https://portal.amfiindia.com/DownloadSchemeData_Po.aspx?mf=0"
LATEST_NAV_URL = "https://portal.amfiindia.com/spages/NAVAll.txt"
HISTORICAL_NAV_URL = "https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx"


def scheme_master_url() -> str:
    return SCHEME_MASTER_URL


def latest_nav_url() -> str:
    return LATEST_NAV_URL


def historical_nav_url(from_date: date, to_date: date) -> str:
    return (
        f"{HISTORICAL_NAV_URL}"
        f"?frmdt={from_date.strftime('%d-%b-%Y')}"
        f"&todt={to_date.strftime('%d-%b-%Y')}"
    )
