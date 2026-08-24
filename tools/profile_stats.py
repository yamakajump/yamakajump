# -*- coding: utf-8 -*-
"""Génère les cartes de statistiques du profil GitHub.

Les données viennent de la page publique de contributions, qui reflète déjà le
réglage « inclure les contributions privées ». Aucun token n'est donc nécessaire,
et la carte affiche les mêmes chiffres que le graphe visible sur le profil.
"""

import datetime as dt
import html
import os
import re
import urllib.request

USER = os.environ.get("PROFILE_USER", "yamakajump")
OUT_DIR = os.environ.get("OUT_DIR", "dist")
SOURCE = f"https://github.com/users/{USER}/contributions"

THEMES = {
    "light": dict(bg="#ffffff", border="#d0d7de", title="#0f2027",
                  label="#57606a", value="#0f2027", accent="#2c5364",
                  bar="#40c463", bar_dim="#d8dee4"),
    "dark": dict(bg="#0d1117", border="#30363d", title="#e6edf3",
                 label="#8b949e", value="#e6edf3", accent="#58a6ff",
                 bar="#3fb950", bar_dim="#21262d"),
}

LOCALES = {
    "en": dict(title="Contributions over the last year",
               total="Total", current="Current streak", longest="Longest streak",
               active="Active days", unit_day="day", unit_days="days",
               source="from the public contribution graph"),
    "fr": dict(title="Contributions sur l'année écoulée",
               total="Total", current="Série en cours", longest="Plus longue série",
               active="Jours actifs", unit_day="jour", unit_days="jours",
               source="d'après le graphe public de contributions"),
}


def fetch_days():
    """Retourne la liste (date, nombre) triée par date croissante."""
    req = urllib.request.Request(SOURCE, headers={"User-Agent": "profile-stats"})
    page = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")

    # Chaque case du calendrier porte son identifiant et sa date.
    cells = dict(re.findall(
        r'<td[^>]*id="(contribution-day-component-[\d-]+)"[^>]*data-date="(\d{4}-\d{2}-\d{2})"',
        page))
    # Variante d'ordre des attributs selon les rendus GitHub.
    cells.update({cid: date for date, cid in re.findall(
        r'<td[^>]*data-date="(\d{4}-\d{2}-\d{2})"[^>]*id="(contribution-day-component-[\d-]+)"',
        page)})

    # L'infobulle liée porte le compte exact.
    counts = {}
    for cid, text in re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>',
                                page, re.S):
        m = re.match(r"\s*(?:(\d+)|No)\s+contribution", html.unescape(text))
        if m:
            counts[cid] = int(m.group(1) or 0)

    days = [(dt.date.fromisoformat(date), counts.get(cid, 0))
            for cid, date in cells.items()]
    if not days:
        raise SystemExit("aucune case de calendrier trouvée, le format a changé")
    return sorted(days)


def compute(days):
    """Calcule total, série en cours, plus longue série et jours actifs."""
    total = sum(n for _, n in days)
    active = sum(1 for _, n in days if n > 0)

    longest = run = 0
    for _, n in days:
        run = run + 1 if n > 0 else 0
        longest = max(longest, run)

    # La série en cours tolère une journée d'aujourd'hui encore vide.
    current = 0
    for date, n in reversed(days):
        if n > 0:
            current += 1
        elif date == days[-1][0]:
            continue
        else:
            break

    return dict(total=total, active=active, longest=longest, current=current)


def weekly(days, buckets=52):
    """Agrège en semaines pour l'histogramme de fond."""
    weeks, cur, start = [], 0, days[0][0]
    for date, n in days:
        if (date - start).days >= 7:
            weeks.append(cur)
            cur, start = 0, date
        cur += n
    weeks.append(cur)
    return weeks[-buckets:]


def render(stats, weeks, theme, locale):
    c, t = THEMES[theme], LOCALES[locale]
    W, H = 880, 200
    peak = max(weeks) or 1

    bars = []
    bw = (W - 80) / len(weeks)
    for i, v in enumerate(weeks):
        h = 4 + (v / peak) * 52
        x = 40 + i * bw
        colour = c["bar"] if v else c["bar_dim"]
        bars.append(f'<rect x="{x:.1f}" y="{H - 28 - h:.1f}" width="{bw - 2:.1f}" '
                    f'height="{h:.1f}" rx="2" fill="{colour}" opacity="0.85" />')

    cells = [(t["total"], f"{stats['total']:,}".replace(",", " ")),
             (t["current"], f"{stats['current']} "
                            f"{t['unit_day'] if stats['current'] == 1 else t['unit_days']}"),
             (t["longest"], f"{stats['longest']} "
                            f"{t['unit_day'] if stats['longest'] == 1 else t['unit_days']}"),
             (t["active"], f"{stats['active']} / {len(weeks) * 7}")]

    blocks = []
    for i, (label, value) in enumerate(cells):
        x = 40 + i * ((W - 80) / 4)
        blocks.append(
            f'<text x="{x:.0f}" y="86" font-size="30" font-weight="700" '
            f'fill="{c["value"]}">{value}</text>'
            f'<text x="{x:.0f}" y="108" font-size="13" fill="{c["label"]}">{label}</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{t["title"]}">
  <style>text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}</style>
  <rect width="{W}" height="{H}" rx="10" fill="{c["bg"]}" stroke="{c["border"]}" />
  <text x="40" y="46" font-size="15" font-weight="600" fill="{c["title"]}">{t["title"]}</text>
  <circle cx="{W - 44}" cy="41" r="4" fill="{c["accent"]}" />
  {"".join(blocks)}
  {"".join(bars)}
  <text x="40" y="{H - 10}" font-size="10" fill="{c["label"]}">{t["source"]}</text>
</svg>
'''


def main():
    days = fetch_days()
    stats = compute(days)
    weeks = weekly(days)
    os.makedirs(OUT_DIR, exist_ok=True)
    for locale in LOCALES:
        for theme in THEMES:
            path = os.path.join(OUT_DIR, f"stats-{locale}-{theme}.svg")
            with open(path, "w", encoding="utf-8") as f:
                f.write(render(stats, weeks, theme, locale))
            print(f"  {path}")
    print(f"  total={stats['total']} serie={stats['current']} "
          f"record={stats['longest']} actifs={stats['active']}")


if __name__ == "__main__":
    main()
