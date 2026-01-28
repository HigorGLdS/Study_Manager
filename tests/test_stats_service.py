from services.stats_service import weekly_stats
from datetime import datetime

def test_weekly_stats():
    materials = [
        {"progress": 100, "updated_at": datetime.now().isoformat()},
        {"progress": 50, "updated_at": datetime.now().isoformat()}
    ]

    avg, done = weekly_stats(materials)
    assert avg == 75
    assert done == 50
