import math
from datetime import datetime
from pathlib import Path

def calc_fee(secs, per_min=False):
    days, remaining = divmod(secs, 86400)
    mins = math.ceil(remaining / 60)

    if mins <= 30:
        f = 0
    elif mins <= 210:
        f = (mins - 30) * 5 if per_min else math.ceil((mins - 30) / 60) * 300
    else:
        f = 900 + (mins - 210) * (500 / 60) if per_min else 900 + math.ceil((mins - 210) / 60) * 500
        
    return int(days * 10000 + min(f, 10000))

def main():
    lines = Path("input.txt").read_text(encoding="utf-8").splitlines()[2:]
    out = []

    for line in lines:
        if not line.strip(): continue
        split_line = line.split()
        arr = datetime.strptime(f"{split_line[1]} {split_line[2]}", "%Y-%m-%d %H:%M:%S")
        dep = datetime.strptime(f"{split_line[3]} {split_line[4]}", "%Y-%m-%d %H:%M:%S")

        all_secs = (dep - arr).total_seconds()

        if all_secs < 0:
            out.append(f"{split_line[0]:<10} | >> HIBA: A TÁVOZÁS KORÁBBI, MINT A BELÉPÉS! <<")
            continue

        std_fee = calc_fee(all_secs, per_min=False)
        min_fee = calc_fee(all_secs, per_min=True)

        day, remaining = divmod(all_secs, 86400)
        hours, mins = divmod(remaining, 3600)
        time_parts = []
        if day > 0: time_parts.append(f"{int(day)} nap")
        if hours > 0: time_parts.append(f"{int(hours)} óra")
        if mins // 60 > 0: time_parts.append(f"{int(mins // 60)} perc")
        duration = " ".join(time_parts) if time_parts else "0 perc"

        #out.append(f"{split_line[0]:<10} | {duration:<20} | Alap: {std_fee:>5} Ft | Percre: {min_fee:>5} Ft")
        out.append(f"{split_line[0]} -> {std_fee} forint")

    result_text = "\n".join(out)
    with open("out.txt", "w", encoding="utf-8") as f:
        f.write(result_text)
    print(result_text)

if __name__ == "__main__":
    main()
