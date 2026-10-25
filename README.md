# py-log-sample

Sample repetitive log lines while always keeping the first and last.

```python
from py_log_sample import LogSampler

sampler = LogSampler()
result = sampler.sample([
    "connection reset",
    "connection reset",
    "connection reset",
    "reconnect attempted",
    "connection reset",
])
# result == [
#     ("connection reset", 3),
#     ("reconnect attempted", 1),
#     ("connection reset", 1),
# ]
```

## Why

Log files frequently contain long runs of identical lines (a flapping service, a stuck retry). Reading the raw output is noisy; seeing only unique lines loses the fact that a line repeated and loses the last line — which is often the one that matters for understanding final state.

This library reduces a sequence to one entry per maximal group of consecutive duplicates, paired with the repetition count. The first line of each group is kept, and because every line in a group is equal, the last line of each group (and thus the last line of the input) is always represented in the output.

## Edge case

Only **consecutive** duplicates are grouped. If a line appears, disappears, and reappears, that is two groups, each with its own count. This is the intended behaviour: interleaved distinct lines genuinely break a run, and merging non-adjacent duplicates would hide ordering information that matters in logs.

Equality is exact string equality (`==`). Lines that differ only in whitespace or timestamp are treated as distinct. If you need to ignore timestamps, strip them before passing lines in.
