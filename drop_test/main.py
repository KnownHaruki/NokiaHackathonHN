from pathlib import Path

def min_num_of_drops(device_num: int, max_floors: int) -> int:
    if max_floors == 0:
        return 0
    if device_num == 1:
        return max_floors

    covered_floors = [0] * (device_num + 1)
    
    while covered_floors[device_num] < max_floors:
        for i in range(device_num, 0, -1):
            covered_floors[i] = covered_floors[i] + covered_floors[i - 1] + 1
            
    return covered_floors[1]

def main():
    data = Path("input.txt").read_text(encoding="utf-8")

    for line in data.splitlines():
        parts = line.split(',')
        print(min_num_of_drops(int(parts[0].strip()), int(parts[1].strip())))


if __name__ == "__main__":
    main()
