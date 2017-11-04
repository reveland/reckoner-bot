import numpy as np
bill = {}
bill['end'] = float(1485907200)
bill['start'] = float(1483228800)
start = float(1483228800)
end = bill['start'] + (bill['end'] - bill['start']) / 2

whole_interval = bill["end"] - bill["start"]
print('whole_interval', whole_interval)
start_interval = start - bill["start"]
print('start_interval', start_interval)
end_interval = bill["end"] - end
print('end_interval',end_interval)
if start < bill["start"]:
    start_interval = 0
if end > bill["end"]:
    end_interval = 0
print('start_interval', start_interval)
print('end_interval',end_interval)
valuable_interval = whole_interval - start_interval - end_interval
print('whole_interval',whole_interval)
valuable_percent = valuable_interval / whole_interval
print('valuable_percent',valuable_percent)
if start > bill["end"]:
    valuable_percent = 0
if end < bill["start"]:
    valuable_percent = 0
print(valuable_percent, start, end, bill['start'], bill['end'])