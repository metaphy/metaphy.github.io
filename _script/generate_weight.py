HEIGHT = 1.78  # meters
CURRENT_YEAR = "2026"

def generate_weight_html():
    src = """ 
10/31 158.2
11/1 158.8
11/2 158.5
11/3 159.7
11/4 159.1
11/5 159.5
11/6 160.8
11/7 161.4
11/8 160.4
11/9 160.0
11/10 159.8
11/11 159.2
11/12 159.1
11/13 159.7
11/14 159.4
11/15 160.4
11/16 159.9
11/17 159.4
11/18 159.4
11/19 159.6
11/20 159.9
11/21 161.0
11/22 160.3
11/23 159.8
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
