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

async def checkFlags(flag: int):
    flags = []
    
    if flag & Frequency.one_hours: flags.append(1)

    return flags