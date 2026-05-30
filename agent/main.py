import subprocess

def run_coral_query(sql: str) -> str:
    result = subprocess.run(
        ["coral", "sql", sql],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return ""
    return result.stdout or ""

def parse_table(output: str):
    rows = []
    lines = output.strip().split('\n')
    data_lines = [l for l in lines if l.startswith('|') and '---' not in l]
    if len(data_lines) < 2:
        return [], []
    headers = [h.strip() for h in data_lines[0].split('|')[1:-1]]
    for line in data_lines[1:]:
        values = [v.strip() for v in line.split('|')[1:-1]]
        if values:
            rows.append(values)
    return headers, rows

def generate_html(videos_data, tweets_data, cross_data):
    v_headers, v_rows = videos_data
    t_headers, t_rows = tweets_data
    c_headers, c_rows = cross_data

    def table_html(headers, rows, empty_msg="No data"):
        if not rows:
            return f'<p class="empty">{empty_msg}</p>'
        html = '<table><thead><tr>'
        for h in headers:
            html += f'<th>{h}</th>'
        html += '</tr></thead><tbody>'
        for row in rows:
            html += '<tr>'
            for cell in row:
                html += f'<td>{cell}</td>'
            html += '</tr>'
        html += '</tbody></table>'
        return html

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Creator Command Center</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #0a0a0f;
    --surface: #12121a;
    --card: #1a1a26;
    --border: #2a2a40;
    --coral: #ff6b4a;
    --coral-dim: #ff6b4a22;
    --teal: #00d4aa;
    --teal-dim: #00d4aa22;
    --gold: #ffd166;
    --text: #e8e8f0;
    --muted: #6b6b8a;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'JetBrains Mono', monospace;
    min-height: 100vh;
    overflow-x: hidden;
  }}

  /* Grid background */
  body::before {{
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(var(--border) 1px, transparent 1px),
      linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 40px 40px;
    opacity: 0.3;
    pointer-events: none;
    z-index: 0;
  }}

  .container {{
    position: relative;
    z-index: 1;
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 20px;
  }}

  /* Header */
  header {{
    text-align: center;
    margin-bottom: 60px;
    animation: fadeDown 0.8s ease both;
  }}

  .skull {{
    font-size: 48px;
    display: block;
    margin-bottom: 16px;
    animation: float 3s ease-in-out infinite;
  }}

  @keyframes float {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-8px); }}
  }}

  h1 {{
    font-family: 'Syne', sans-serif;
    font-size: clamp(28px, 5vw, 52px);
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(135deg, var(--coral), var(--gold), var(--teal));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
  }}

  .subtitle {{
    color: var(--muted);
    font-size: 13px;
    letter-spacing: 3px;
    text-transform: uppercase;
  }}

  .badge {{
    display: inline-block;
    margin-top: 16px;
    padding: 4px 16px;
    background: var(--coral-dim);
    border: 1px solid var(--coral);
    border-radius: 20px;
    color: var(--coral);
    font-size: 11px;
    letter-spacing: 2px;
  }}

  /* Stats bar */
  .stats-bar {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 40px;
    animation: fadeUp 0.8s 0.2s ease both;
  }}

  .stat {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
  }}

  .stat:hover {{ border-color: var(--coral); }}

  .stat::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--coral), var(--teal));
  }}

  .stat-num {{
    font-family: 'Syne', sans-serif;
    font-size: 36px;
    font-weight: 800;
    color: var(--coral);
    display: block;
  }}

  .stat-label {{
    color: var(--muted);
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
  }}

  /* Cards */
  .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin-bottom: 24px;
    animation: fadeUp 0.8s 0.4s ease both;
  }}

  .card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    transition: transform 0.3s, border-color 0.3s;
  }}

  .card:hover {{
    transform: translateY(-2px);
    border-color: var(--teal);
  }}

  .card-full {{
    grid-column: 1 / -1;
    animation: fadeUp 0.8s 0.6s ease both;
  }}

  .card-header {{
    padding: 20px 24px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .card-icon {{
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
  }}

  .icon-yt {{ background: #ff000022; }}
  .icon-tw {{ background: #1d9bf022; }}
  .icon-cross {{ background: var(--coral-dim); }}

  .card-title {{
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 15px;
    color: var(--text);
  }}

  .card-tag {{
    margin-left: auto;
    font-size: 10px;
    padding: 3px 10px;
    border-radius: 20px;
    background: var(--teal-dim);
    color: var(--teal);
    border: 1px solid var(--teal);
    letter-spacing: 1px;
  }}

  .card-body {{ padding: 20px 24px; }}

  /* Table */
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}

  th {{
    text-align: left;
    color: var(--muted);
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 8px 12px;
    border-bottom: 1px solid var(--border);
    font-weight: 400;
  }}

  td {{
    padding: 12px;
    border-bottom: 1px solid var(--border)44;
    color: var(--text);
  }}

  tr:last-child td {{ border-bottom: none; }}

  tr:hover td {{ background: var(--surface); }}

  .num {{ color: var(--coral); font-weight: 600; }}
  .platform-yt {{ color: #ff4444; }}
  .platform-tw {{ color: #1d9bf0; }}

  .empty {{
    color: var(--muted);
    text-align: center;
    padding: 40px;
    font-size: 13px;
  }}

  /* Bar chart */
  .bar-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
  }}

  .bar-label {{
    font-size: 12px;
    color: var(--muted);
    width: 180px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex-shrink: 0;
  }}

  .bar-track {{
    flex: 1;
    height: 8px;
    background: var(--border);
    border-radius: 4px;
    overflow: hidden;
  }}

  .bar-fill {{
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, var(--coral), var(--gold));
    transition: width 1s ease;
  }}

  .bar-val {{
    font-size: 12px;
    color: var(--gold);
    width: 40px;
    text-align: right;
    flex-shrink: 0;
  }}

  /* Footer */
  footer {{
    text-align: center;
    margin-top: 60px;
    padding-top: 30px;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-size: 11px;
    letter-spacing: 2px;
    animation: fadeUp 0.8s 0.8s ease both;
  }}

  footer span {{ color: var(--coral); }}

  @keyframes fadeDown {{
    from {{ opacity: 0; transform: translateY(-20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  @keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  @media (max-width: 768px) {{
    .grid {{ grid-template-columns: 1fr; }}
    .stats-bar {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<div class="container">

  <header>
    <span class="skull">🏴‍☠️</span>
    <h1>Creator Command Center</h1>
    <p class="subtitle">Powered by Coral — Query Everything as SQL</p>
    <span class="badge">🐠 Pirates of the Coral-bean Hackathon</span>
  </header>

  <div class="stats-bar">
    <div class="stat">
      <span class="stat-num">{len(v_rows)}</span>
      <span class="stat-label">YouTube Videos</span>
    </div>
    <div class="stat">
      <span class="stat-num">{len(t_rows)}</span>
      <span class="stat-label">Tweets Tracked</span>
    </div>
    <div class="stat">
      <span class="stat-num">3</span>
      <span class="stat-label">Sources Connected</span>
    </div>
  </div>

  <div class="grid">

    <div class="card">
      <div class="card-header">
        <div class="card-icon icon-yt">🎬</div>
        <span class="card-title">YouTube Videos</span>
        <span class="card-tag">LIVE</span>
      </div>
      <div class="card-body">
        {table_html(v_headers, v_rows, "No videos found")}
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-icon icon-tw">🐦</div>
        <span class="card-title">Top Tweets by Likes</span>
        <span class="card-tag">MOCK</span>
      </div>
      <div class="card-body">
        {"".join([f'<div class="bar-row"><span class="bar-label">{r[0]}</span><div class="bar-track"><div class="bar-fill" style="width:{min(int(r[1] or 0)*100//100, 100)}%"></div></div><span class="bar-val">{r[1]}</span></div>' for r in t_rows]) if t_rows else '<p class="empty">No tweets found</p>'}
      </div>
    </div>

    <div class="card card-full">
      <div class="card-header">
        <div class="card-icon icon-cross">⚡</div>
        <span class="card-title">Cross-Platform Engagement</span>
        <span class="card-tag">SQL JOIN</span>
      </div>
      <div class="card-body">
        {table_html(c_headers, c_rows, "No cross-platform data")}
      </div>
    </div>

  </div>

  <footer>
    Built with <span>Coral</span> · YouTube · Twitter · Discord · 
    <span>WeMakeDevs Hackathon 2026</span>
  </footer>

</div>
</body>
</html>"""

if __name__ == "__main__":
    print("🏴‍☠️ Creator Command Center — Generating Dashboard...\n")

    print("📊 Fetching YouTube videos...")
    v_out = run_coral_query("SELECT title, views, likes FROM youtube_local.videos ORDER BY views DESC LIMIT 5")
    videos = parse_table(v_out)

    print("🐦 Fetching tweets...")
    t_out = run_coral_query("SELECT text, likes, retweets FROM twitter_local.tweets ORDER BY likes DESC LIMIT 5")
    tweets = parse_table(t_out)

    print("⚡ Running cross-platform query...")
    c_out = run_coral_query("""
        SELECT 'YouTube' AS platform, title AS content, likes AS engagement
        FROM youtube_local.videos
        UNION ALL
        SELECT 'Twitter' AS platform, text AS content, likes AS engagement
        FROM twitter_local.tweets
        ORDER BY engagement DESC
        LIMIT 10
    """)
    cross = parse_table(c_out)

    html = generate_html(videos, tweets, cross)

    with open("/app/dashboard.html", "w") as f:
        f.write(html)

    print("\n✅ Dashboard generated at /app/dashboard.html")
    print("📂 Open it in your browser from Windows!")