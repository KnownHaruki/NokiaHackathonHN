from pathlib import Path

def next_magic_num(n: str) -> str:
    num_len = len(n)

    candidates = {str(10**num_len + 1)}

    prefix_len = (num_len + 1) // 2
    prefix = int(n[:prefix_len])

    for i in [0, 1]:
        new_prefix = str(prefix + i)

        if num_len % 2 == 0:
            candidate = new_prefix + new_prefix[::-1]
        else:
            candidate = new_prefix + new_prefix[:-1][::-1]

        candidates.add(candidate)

    original_num = int(n)
    valid_candidates = [int(c) for c in candidates if int(c) > original_num]

    return str(min(valid_candidates))

def parse_input_line(line: str) -> str:
    if "^" in line:
        base, exponent = line.split("^")
        return str(int(base) ** int(exponent))
    return line

def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    print(data, end="")

    print("\nOutput:")
    for line in data.splitlines():
        print(next_magic_num(parse_input_line(line)))

if __name__ == "__main__":
    main()
