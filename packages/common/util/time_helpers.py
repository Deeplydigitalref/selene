from pyfuncify import chronos

def epoch_exp(seconds_from_now: int):
    return (int(chronos.time_now(tz=chronos.tz_utc(), apply=[chronos.epoch()])) + seconds_from_now)