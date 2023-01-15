with open("input.txt") as f:
    data = f.read().split("\n")
data.append("")  # This ensures the last value in data is counted

totals = []
total = 0
for calories in data:
    if calories:
        total += int(calories)
    else:
        totals.append(total)
        total = 0

top_three = sorted(totals, reverse=True)[:3]

print(f"Answer = {sum(top_three)}")
