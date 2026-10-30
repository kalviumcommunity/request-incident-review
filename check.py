import json
from formatter import format_event
from support import load, require, main


def records():
    for event in load('fixtures/events.json'):
        line = format_event(event)
        require(len(line.splitlines()) == 1, 'Emit one JSON object per line.')
        parsed = json.loads(line)
        require(parsed == event, 'Preserve timestamp, level, request_id, message with exact names and values.')
        print(line)


def trace():
    records_to_show = [e for e in load('fixtures/events.json') if e['request_id'] == 'r17']
    print('Filter: request_id=r17 (JSON field, not a Loki label)')
    for event in records_to_show:
        parsed = json.loads(format_event(event))
        require(parsed == event, 'Repair formatter before investigating request fields.')
        print(json.dumps(parsed, separators=(',', ':')))
    print('Chronological incident evidence (provided recording, not a live outage):')
    for event in load('fixtures/events.json'):
        if event['request_id'] in ('monitor', 'incident', 'verify'):
            print(event['timestamp'], event['level'], event['message'])
    print('Timeline accuracy is manually graded against these events.')


def review():
    print((__import__('pathlib').Path(__file__).parent / 'fixtures/change-record.md').read_text())
    print('Written causal chain and actions require human review; no keyword-based PASS.')


if __name__ == '__main__':
    raise SystemExit(main(dict(records=records, trace=trace, review=review)))
