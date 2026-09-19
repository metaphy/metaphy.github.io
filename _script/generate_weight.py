HEIGHT = 1.78  # meters
CURRENT_YEAR = "2026"

def generate_weight_html():
    src = """ 
8/31 161.9
9/1 162
9/2 162.1
9/3 162.4
9/4 161.9
9/5 161.3
9/6 161.3
9/7 161.4
9/8 162.4
9/9 161.5
9/10 162.2
9/11 162.0
9/12 162.1
9/13 161.6
9/14 162.2
9/15 162.1
9/16 161.9
9/17 162.1
9/18 162.0
9/19 161.1
"""
    
    lines = src.strip().splitlines()
    prev_weight = None
    month_entries = {}

    for line in lines:
        parts = line.split()
        date_str, weight = parts[0], float(parts[1])
        month, day = date_str.split('/')
        month_entries.setdefault(month, []).append(weight)

        format_date = f"{CURRENT_YEAR}-{int(month):02d}-{int(day):02d}"
        bmi = (weight / 2) / (HEIGHT ** 2)

        if prev_weight is None:
            prev_weight = weight
            continue

        delta = weight - prev_weight
        if delta > 0:
            arrow = f'<span class="arrow-up">&#x25B2; +{delta:.1f}</span>'
        elif delta < 0:
            arrow = f'<span class="arrow-down">&#x25BC; {delta:.1f}</span>'
        else:
            arrow = '<span class="arrow-flat">&#x25C0; 0.0</span>'

        if int(day) == 1:
            print(f'<tr><td colspan="4" class="month-header">{CURRENT_YEAR}年{int(month)}月&nbsp;&nbsp;当月减重：__斤</td></tr>')

        print(f'<tr><td>{format_date}</td><td>{weight:.1f}</td><td>{bmi:.1f}</td><td>{arrow}</td></tr>')
        prev_weight = weight


if __name__ == '__main__':
    generate_weight_html()
