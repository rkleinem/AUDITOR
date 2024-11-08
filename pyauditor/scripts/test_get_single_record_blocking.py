#!/usr/bin/env python3

import datetime

from tzlocal import get_localzone

from pyauditor import AuditorClientBuilder, Record


def main():
    local_tz = get_localzone()
    print("LOCAL TIMEZONE: " + str(local_tz))

    client = (
        AuditorClientBuilder().address("127.0.0.1", 8000).timeout(10).build_blocking()
    )

    print("Testing /health_check endpoint")
    health = client.health_check()
    assert health

    print("get should not return anything because there are not records in Auditor yet")
    empty_array = client.get()
    assert len(empty_array) == 0

    print("Adding a records to Auditor")

    for i in range(0, 24):
        record_id = f"record-{i:02d}"

        # datetimes sent to auditor MUST BE in UTC.
        start = datetime.datetime(2022, 8, 8, i, 0, 0, 0, tzinfo=datetime.timezone.utc)
        stop = datetime.datetime(2022, 8, 9, i, 0, 0, 0, tzinfo=datetime.timezone.utc)
        record = Record(record_id, start).with_stop_time(stop)

        client.add(record)

    print("Check if all records made it to Auditor")

    records = client.get()
    assert len(records) == 24

    records = sorted(records, key=lambda x: x.record_id)

    for i in range(0, 24):
        assert records[i].record_id == f"record-{i:02d}"

    record = client.get_single_record("record-03")
    assert records[3].record_id == record.record_id


if __name__ == "__main__":
    import time

    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
