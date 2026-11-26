from datetime import datetime


def iOrchid_clock(zone):
    """Write the current local hour for the zone."""
    path = f"{zone}/data_DO_NOT_MODIFY/time.txt"
    with open(path, "w", encoding="utf-8") as time_file:
        time_file.write(str(datetime.now().hour))


def iOrchid_seasonal_clock(zone):
    """
    Set the seasonal mode for the Southern Hemisphere.

    Summer: November through April (1)
    Winter: May through October (2)

    This matches the New Zealand/Larnaco seasonal convention used by
    the current iOrchid deployment, rather than Northern Hemisphere months.
    """
    month = datetime.now().month
    season = "1" if month in (11, 12, 1, 2, 3, 4) else "2"
    path = f"{zone}/data_DO_NOT_MODIFY/season(summer=1winter=2).txt"
    with open(path, "w", encoding="utf-8") as season_file:
        season_file.write(season)
