class Frequency():
    opted_out = 0
    one_hours = 1
    six_hours = 2
    twelve_hours = 4
    one_days = 8
    three_days = 16
    five_days = 32
    one_weeks = 64
    two_weeks = 128
    one_month = 256

async def checkFlags(flag: int): #check flags that we have assigned
    flags = []
    if flag & Frequency.one_hours: flags.append(1)
    if flag & Frequency.six_hours: flags.append(2)
    if flag & Frequency.twelve_hours: flags.append(4)
    if flag & Frequency.one_days: flags.append(8)
    if flag & Frequency.three_days: flags.append(16)
    if flag & Frequency.five_days: flags.append(32)
    if flag & Frequency.one_weeks: flags.append(64)
    if flag & Frequency.two_weeks: flags.append(128)
    if flag & Frequency.one_month: flags.append(256)

    return flags