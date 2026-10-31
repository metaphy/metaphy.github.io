HEIGHT = 1.78  # meters
CURRENT_YEAR = "2026"

def generate_weight_html():
    src = """
9/30 161.7
10/1 162.2
10/2 162.0
10/3 161.5
10/4 161.6
10/5 162.2
10/6 161.4
10/7 162.0 
10/8 162.5
10/9 161.6 
10/10 161.0
10/11 160.3
10/12 159.6
10/13 160.7
10/14 160.2
10/15 160.7
10/16 160.1
10/17 159.8
10/18 159.6
10/19 159.7
10/20 160.1
10/21 160.4
10/22 159.9
10/23 160.7
10/24 159.6
10/25 160.2
10/26 159.4
10/27 160.2
10/28 160.1
10/29 158.8
10/30 158.1
10/31 158.2
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
