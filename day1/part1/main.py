with open("input.txt") as f:
    data = f.read().split("\n")

totals = []
total = 0
for calories in data:
    if not calories:
        totals.append(total)
        total = 0
    else:
        total += int(calories)

print(f"Answer: {max(totals)}")
