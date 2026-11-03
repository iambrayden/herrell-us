#!/usr/bin/env python3
"""Build the project pages for herrell.us.

Edit PROJECTS below, then run:  python3 scripts/build_projects.py
It writes public/projects/<slug>/index.html for every project, plus
public/projects/index.html. Screenshots live in public/projects/<slug>/.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "projects"
GH = "https://github.com/iambrayden/"

GROUPS = ["Infrastructure & networking", "Software", "Game projects"]

# Each project: slug, title, group, summary (one or two sentences), about
# (paragraphs), features (list of (name, text)), tech, repo (public GitHub
# URL or None), site (public domain or None), shots (list of (file, caption)).
PROJECTS = [
    dict(
        slug="vn-vpn", title="VN-VPN", group=GROUPS[0],
        summary="A self-hosted WireGuard VPN service you can sell: a management panel, server agents, a customer portal, and Stripe billing.",
        about=[
            "VN-VPN turns any number of Linux servers into one VPN service. The panel runs in a single container; each server runs a small agent that installs WireGuard, registers with the panel, and syncs its peer list every 15 seconds without dropping connected tunnels.",
            "Every device gets its own key pair and can use every location. Agents only allow devices that are paid up and within their plan's connection limit, and servers keep running on their last config if the panel goes down.",
        ],
        features=[
            ("Node agent", "One command turns a fresh VPS into a VPN node. The server's private key is generated on the server and never leaves it."),
            ("Customer portal", "Sign-up, a guided setup for each device type, and location picks by flag with live load and a recommended server."),
            ("Subscriptions", "Stripe Checkout, plan upgrades, and the Stripe Customer Portal. Basic allows one device at a time, Pro allows five."),
            ("Monitoring", "CPU, memory, disk, bandwidth, and connected devices per server, with 1h / 24h / 7d charts and Discord or Slack alerts."),
            ("Leak protection", "IPv6 is routed into the tunnel and dropped, MTU is set to 1380, and servers clamp TCP MSS."),
            ("Provisioning API", "Other systems can create, suspend, and delete users and grant plans."),
        ],
        tech=["WireGuard", "FastAPI", "SQLite", "Stripe", "Docker", "Linux"],
        repo=GH + "vn-vpn",
        shots=[("portal.jpg", "Customer portal"), ("admin.jpg", "Admin dashboard"), ("add-server.jpg", "Add-server wizard")],
    ),
    dict(
        slug="postbound", title="Postbound", group=GROUPS[0],
        summary="A managed SMTP relay for support teams sending tickets, replies, and invoices.",
        about=[
            "Postbound gives a team its own outbound mail service with the deliverability pieces handled: DKIM keys are generated per domain, the dashboard walks you through SPF, DKIM, and DMARC records, and it checks DNS until the domain verifies.",
            "It runs on a single Debian or Ubuntu server with an installer, stores everything in SQLite, and can optionally hand mail off to SendGrid, Amazon SES, or another upstream relay.",
        ],
        features=[
            ("SMTP and HTTP", "SMTP on port 587 with STARTTLS and user logins, plus an HTTP send API with API keys."),
            ("Domain setup", "Automatic DKIM key pairs, an SPF / DKIM / DMARC record wizard, and live verification status."),
            ("Activity log", "A searchable, filterable log of every message sent."),
            ("Suppression list", "Stops sending to addresses that bounced or unsubscribed."),
            ("Limits and keys", "Multiple SMTP users with daily limits, and API keys restricted to specific domains."),
            ("Dashboard", "A dark-mode web UI with live stats and charts."),
        ],
        tech=["SMTP", "DKIM / SPF / DMARC", "Node.js", "SQLite"],
        repo=None,
    ),
    dict(
        slug="waymail-security", title="WayMail Security", group=GROUPS[0],
        summary="A white-label client console for a Proxmox Mail Gateway.",
        about=[
            "WayMail Security puts a clean, branded dashboard in front of a mail security gateway. Clients manage their own quarantine, lists, and policies, while the gateway behind it stays invisible: no upstream branding, cookies, headers, or hostnames ever reach the browser.",
            "There are no config files. A setup wizard connects the console to the gateway on first launch, and it installs with one line on any server with Docker.",
        ],
        features=[
            ("Dashboard", "Mail volume, spam and virus counts, greylisting, per-domain traffic, and a 24-hour flow chart."),
            ("Quarantine", "Browse spam, virus, and attachment quarantine and preview messages."),
            ("Message tracking", "Search the delivery log by sender or recipient."),
            ("Filtering", "Sender allow and block lists, and filter rules you can create, enable, and disable."),
            ("Domains and routing", "Protected domains, delivery routes, and trusted networks."),
            ("Accounts", "Client logins with Client, Manager, Auditor, and Administrator roles."),
        ],
        tech=["Email security", "Proxmox Mail Gateway", "Docker"],
        repo=None,
    ),
    dict(
        slug="blockserver", title="BlockServer", group=GROUPS[0],
        summary="A central IP blocklist shared across servers, fed by CrowdSec.",
        about=[
            "BlockServer keeps one blocklist for a whole fleet. A small API holds blocked IPv4 and IPv6 addresses and subnets in nftables sets, and each client server runs CrowdSec and reports its bans back, so an attacker blocked on one server is blocked on all of them.",
        ],
        features=[
            ("Shared blocklist", "IPv4 and IPv6 addresses and whole subnets, stored in nftables sets."),
            ("Ban reporting", "Client servers running CrowdSec report their bans to the central server automatically."),
            ("Allow list", "Protected addresses and clients that can never be blocked."),
            ("Installers", "One script sets up the server and one sets up each client."),
        ],
        tech=["nftables", "CrowdSec", "Python", "Flask"],
        repo=None,
    ),
    dict(
        slug="fortigate-cve-scanner", title="FortiGate CVE-2024-23113 scanner", group=GROUPS[0],
        summary="Checks a list of client IPs for FortiGate devices exposed to CVE-2024-23113.",
        about=[
            "CVE-2024-23113 is a critical FortiOS vulnerability in the fgfmd daemon. This script takes a list of client addresses, checks each one, and writes out the ones that look exposed, so an MSP can find and patch affected firewalls quickly.",
            "It's meant for scanning your own IP space or your clients' with permission.",
        ],
        features=[
            ("Bulk check", "Reads every client IP from a text file and checks them in one run."),
            ("Report", "Writes the vulnerable addresses to a separate file to work from."),
        ],
        tech=["Python", "Fortinet", "Security"],
        repo=GH + "CVE-2024-23113",
    ),
    dict(
        slug="arin-waitlist-monitor", title="ARIN waitlist monitor", group=GROUPS[0],
        summary="Tracks your place on ARIN's IPv4 waiting list and emails you when it moves.",
        about=[
            "ARIN's IPv4 waiting list is rendered in the browser, so it can't be scraped with a simple request. The monitor loads the page in headless Chromium, reads the table, finds your request by its exact timestamp, and emails your current position.",
            "It remembers the previous position so you can see progress over time, and it's meant to run on a schedule.",
        ],
        features=[
            ("Headless browser", "Uses Playwright and Chromium to read the rendered waiting list."),
            ("Position tracking", "Finds your entry by its date and time added, and compares it with the last run."),
            ("Email alerts", "SMTP with STARTTLS or SMTPS, to one or more recipients."),
            ("One-line install", "Sets up the system packages, a Python virtual environment, and the browser."),
        ],
        tech=["Python", "Playwright", "ARIN", "SMTP"],
        repo=GH + "arin-waitlist-monitor",
    ),
    dict(
        slug="bgp-toolkit", title="BGP toolkit", group=GROUPS[0],
        summary="Sets up a Debian server to speak BGP.",
        about=[
            "A starting point for running BGP on Linux. One script installs the tools I use on every router and enables IPv4 forwarding.",
        ],
        features=[
            ("bgpq4", "Generates prefix lists from IRR data."),
            ("BIRD", "The BGP daemon."),
            ("Pathvector", "Generates and manages routing policy for BIRD."),
            ("Forwarding", "Turns on IPv4 forwarding so the box can route."),
        ],
        tech=["BGP", "BIRD", "Pathvector", "Debian"],
        repo=GH + "BGP",
    ),
    dict(
        slug="dns-block-lists", title="DNS block lists", group=GROUPS[0],
        summary="Valor Node's curated DNS block lists.",
        about=[
            "Block lists for DNS resolvers and filters such as Pi-hole and AdGuard, each published as a raw file you can subscribe to.",
        ],
        features=[
            ("All", "Domains tied to malware, scams, spam, adware, and tracking."),
            ("Malicious", "Domains known to be malicious."),
            ("New domains", "Domains registered in the last 30 days."),
            ("Adult content", "Explicit sites."),
        ],
        tech=["DNS", "Security"],
        repo=GH + "dns",
    ),
    dict(
        slug="proxui", title="ProxUI", group=GROUPS[0],
        summary="A better way to manage Proxmox.",
        about=["A cleaner interface for managing Proxmox virtual machines and hosts."],
        features=[],
        tech=["Proxmox", "Virtualization"],
        repo=GH + "ProxUI",
    ),
    dict(
        slug="ridgecad", title="RidgeCAD", group=GROUPS[1],
        summary="Computer-aided dispatch for search and rescue, roadside assistance, and security teams.",
        about=[
            "RidgeCAD is a dispatch system with two sides: a console where dispatchers create and run incidents, and a mobile app for field units. Every change is pushed to every connected dispatcher instantly.",
        ],
        features=[
            ("Dispatcher console", "Create, prioritize, and track incidents with a full narrative log and address search."),
            ("Live map", "Field units' GPS positions and incidents on one map."),
            ("Dispatch", "Assign and release units, with statuses that update automatically."),
            ("Field app", "An installable mobile app that shares GPS, shows the active call, and opens turn-by-turn navigation."),
            ("Incident types", "Search and rescue, roadside, defense, and medical, each with detailed subtypes."),
            ("Admin", "User accounts with Admin, Supervisor, Dispatcher, and Field Unit roles, scoped by division."),
        ],
        tech=["React", "Node.js", "Socket.io", "PostgreSQL", "Mapbox"],
        repo=None,
    ),
    dict(
        slug="msp-pricing-calculator", title="MSP pricing calculator", group=GROUPS[1],
        summary="Builds MSP quotes from real vendor costs and turns them into a client proposal.",
        about=[
            "Pick services from a catalog of vendor costs (Microsoft 365 plans and other common MSP line items), set quantities and markup, and the calculator works out pricing and margin, then produces a proposal for the client.",
        ],
        features=[
            ("Service catalog", "Vendor costs, units, and suggested markups for common MSP services."),
            ("Margins", "Per-line and total cost, price, and margin."),
            ("Proposal", "A client-ready proposal built from the quote."),
        ],
        tech=["JavaScript", "Vite"],
        repo=None,
    ),
    dict(
        slug="settlementfinder", title="SettlementFinder", group=GROUPS[1],
        summary="Finds class action settlements you're eligible to claim.",
        about=[
            "SettlementFinder collects class action settlements and matches them to your profile. A scraper runs every hour and a notification job follows it, so new matches reach you the same hour they're found.",
            "It deploys with one command on a Linux server, on Vercel, or as a Docker container.",
        ],
        features=[
            ("Aggregation", "An hourly scraper collects open settlements."),
            ("Matching", "Settlements are matched against your profile."),
            ("Notifications", "Email alerts for new matches."),
        ],
        tech=["Next.js", "PostgreSQL", "Docker"],
        repo=None,
    ),
    dict(
        slug="chargemyev", title="ChargeMyEV", group=GROUPS[1],
        summary="Finds EV chargers that actually fit your car.",
        about=[
            "Add your EV and the adapters you carry, and ChargeMyEV shows the chargers you can use out of more than 100,000 real stations.",
        ],
        features=[
            ("Map", "Charging stations from Open Charge Map on an OpenStreetMap map."),
            ("Compatibility", "Connector types are detected from your car (NACS, CCS1, CHAdeMO, J1772), and adapters unlock more stations."),
            ("Trip planner", "Plan road trips with charging stops."),
            ("Community", "Reviews, check-ins, and favorites."),
            ("Accounts", "Sign-up and multiple vehicles per user."),
        ],
        tech=["Next.js", "TypeScript", "Supabase", "Leaflet"],
        repo=None,
    ),
    dict(
        slug="blaine-county-sheriff", title="Blaine County Sheriff's Office", group=GROUPS[2],
        summary="The department website for the Last Chance Roleplay community.",
        about=[
            "A public website and staff portal for an in-game sheriff's department, styled after a real government site.",
        ],
        features=[
            ("Public site", "News, the roster, standard operating procedures, FAQ, and records requests."),
            ("Recruiting", "Application information and the path to joining."),
            ("Training", "Training modules behind a staff login, and a field training officer section."),
            ("Staff tools", "Leave requests, a deputy portal, and an admin panel."),
        ],
        tech=["Node.js", "Express"],
        repo=None, site="blainecountyso.org",
        shots=[("home.jpg", "Homepage")],
    ),
    dict(
        slug="san-andreas-state-police", title="San Andreas State Police", group=GROUPS[2],
        summary="The agency website for the Last Chance Roleplay community, with bodycam storage on Cloudflare.",
        about=[
            "An agency website for an in-game state police department, plus a Cloudflare Worker that stores and serves bodycam footage from R2.",
        ],
        features=[
            ("Agency site", "Mission and values, divisions, careers, policies and updates, and contact."),
            ("Bodycam storage", "A Cloudflare Worker in front of an R2 bucket for uploading and viewing footage."),
        ],
        tech=["HTML / CSS", "Cloudflare Workers", "R2"],
        repo=None, site="sasp.lcrpp.net",
        shots=[("home.jpg", "Homepage")],
    ),
    dict(
        slug="bdev-restaurant", title="bdev-restaurant", group=GROUPS[2],
        summary="Player-owned restaurants for Qbox FiveM servers, built to work in any restaurant interior.",
        about=[
            "Admins walk into any restaurant interior, create a restaurant, and place every station with an in-game tool. Owners then run the business: buy stock that arrives as crates, cook every dish through minigames, serve customers, keep the place clean, hire staff, and survive health inspections.",
        ],
        features=[
            ("Any interior", "No coordinates in config. Every station is placed in-game."),
            ("Supply chain", "Ingredients arrive as crates at the dock and spoil over time."),
            ("Cooking", "14 dishes and 11 different minigames, timed and checked by the server."),
            ("Service", "NPC customers queue, order, and sit; players order from a menu board."),
            ("Staff and payroll", "Hire players or NPCs, with wages, roles, and upkeep each cycle."),
            ("Inspections", "Random health inspections grade the restaurant A, B, or C."),
        ],
        tech=["Lua", "FiveM", "Qbox", "ox_lib"],
        repo=GH + "bdev-restaurant",
        shots=[("01-overview.jpg", "Management tablet"), ("02-kitchen.jpg", "Live kitchen"), ("03-menu.jpg", "Menu and pricing"), ("06-finances.jpg", "Finances")],
    ),
    dict(
        slug="bdev-trucking-company", title="bdev-trucking-company", group=GROUPS[2],
        summary="Player-owned trucking companies for Qbox FiveM servers.",
        about=[
            "Buy a depot by the docks, build out the office, hire NPC and player staff, train and certify them, buy and insure a fleet, win loads on a bid board shared by every company, and hand the busywork to dispatchers.",
        ],
        features=[
            ("Company tablet", "Dashboard, finances, bid board, loads, staff, hiring, fleet, and dispatch."),
            ("Bid board", "Shared across companies, with cert and reputation gates."),
            ("Training", "Real-time certification courses: CDL Class A, HAZMAT, Tanker, Oversize, Dispatch."),
            ("Fleet and insurance", "Trucks track wear and mileage; insurance pays claims automatically."),
            ("Drivers", "Simulated NPC drivers or real players driving the route."),
            ("Dispatchers", "NPC dispatchers bid on loads and assign drivers automatically."),
        ],
        tech=["Lua", "FiveM", "Qbox", "ox_lib"],
        repo=GH + "bdev-trucking-company",
        shots=[("01-dashboard.jpg", "Company tablet"), ("03-bid-board.jpg", "Shared bid board"), ("08-fleet.jpg", "Fleet"), ("11-dispatch.jpg", "Dispatch")],
    ),
    dict(
        slug="hearth", title="Hearth", group=GROUPS[2],
        summary="A location-sharing app for the in-game phone, built for families and friend groups.",
        about=[
            "Players form private circles, see each other on a live map, get alerts when someone arrives at or leaves a saved place, check in, and send an SOS. It also detects hard crashes and alerts the circle.",
        ],
        features=[
            ("Circles", "Invite by code or text message, with admin roles."),
            ("Live map", "Member pins with status like “Driving · 54 mph on Route 68”."),
            ("Places", "Saved places with arrive and leave alerts that ignore GPS jitter."),
            ("SOS and crashes", "Press-and-hold SOS and automatic crash and downed alerts."),
            ("History", "The last 60 minutes of a member's trail."),
        ],
        tech=["Lua", "FiveM", "Qbox", "JavaScript"],
        repo=GH + "bdev-hearth",
    ),
    dict(
        slug="ledger", title="LEDGER", group=GROUPS[2],
        summary="A read-only dashboard for auditing a FiveM server's economy.",
        about=[
            "LEDGER connects to a server's database and shows every citizen's money, transactions, shared accounts, property, and vehicles, then flags suspicious activity for staff to investigate.",
        ],
        features=[
            ("Overview", "Total money in the economy, the richest citizens, and trends."),
            ("Citizens", "A searchable list and a page per citizen."),
            ("Audit flags", "Suspicious transactions surfaced automatically."),
            ("Cases", "Investigation files with snapshotted evidence, notes, status, and printable reports."),
            ("Access control", "Roles, per-user permission overrides, and table access per role."),
        ],
        tech=["Web", "MySQL"],
        repo=GH + "bdev-bank-site",
    ),
]

HEAD = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta name="theme-color" content="#0B1220">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/styles.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>

  <header class="top wrap">
    <a class="mark" href="/">Brayden Herrell</a>
    <nav aria-label="Primary">
      <ul>
        <li><a href="/#networks">Networks</a></li>
        <li><a href="/#experience">Experience</a></li>
        <li><a href="/projects/">Projects</a></li>
        <li><a href="/#certifications">Certifications</a></li>
        <li><a href="/#contact">Contact</a></li>
      </ul>
    </nav>
  </header>
"""

FOOT = """
  <footer class="foot wrap">
    <span>© <span id="year">2026</span> Brayden Herrell</span>
    <span>St. Louis, MO</span>
  </footer>

  <script src="/assets/main.js" defer></script>
</body>
</html>
"""


def e(s):
    return escape(s, quote=True)


def tags(items):
    return '<ul class="tags">' + "".join(f"<li>{e(t)}</li>" for t in items) + "</ul>"


def where(p):
    if p.get("repo"):
        return "GitHub"
    if p.get("site"):
        return p["site"]
    return "Private"


def card(p):
    return f"""          <li class="project">
            <div class="project-head"><h4><a href="/projects/{p['slug']}/">{e(p['title'])}</a></h4><span class="where">{e(where(p))}</span></div>
            <p>{e(p['summary'])}</p>
            {tags(p['tech'])}
          </li>
"""


def cards_by_group(heading_tag="h3"):
    out = []
    for g in GROUPS:
        items = [p for p in PROJECTS if p["group"] == g]
        cls = "projects two" if len(items) % 3 == 1 and len(items) % 2 == 0 else "projects"
        out.append(f"""      <div class="proj-group">
        <{heading_tag}>{e(g)}</{heading_tag}>
        <ul class="{cls}">
{''.join(card(p) for p in items)}        </ul>
      </div>
""")
    return "\n".join(out)


def project_page(i, p):
    prev_p = PROJECTS[i - 1] if i > 0 else None
    next_p = PROJECTS[i + 1] if i + 1 < len(PROJECTS) else None

    links = []
    if p.get("repo"):
        links.append(f'<a class="btn primary" href="{e(p["repo"])}">View source on GitHub ↗</a>')
    if p.get("site"):
        links.append(f'<span class="note">Live at {e(p["site"])}</span>')
    if not p.get("repo"):
        links.append('<span class="note">Source code is private</span>')

    shots = p.get("shots") or []
    gallery = ""
    if shots:
        first, rest = shots[0], shots[1:]
        figs = [f"""        <figure class="shot lead">
          <img src="{e(first[0])}" alt="{e(p['title'])}: {e(first[1])}" loading="eager">
          <figcaption>{e(first[1])}</figcaption>
        </figure>"""]
        for f, cap in rest:
            figs.append(f"""        <figure class="shot">
          <img src="{e(f)}" alt="{e(p['title'])}: {e(cap)}" loading="lazy">
          <figcaption>{e(cap)}</figcaption>
        </figure>""")
        gallery = '      <div class="gallery">\n' + "\n".join(figs) + "\n      </div>\n"

    about = "\n".join(f"        <p>{e(t)}</p>" for t in p["about"])
    features = ""
    if p["features"]:
        items = "\n".join(f"          <li><strong>{e(n)}.</strong> {e(t)}</li>" for n, t in p["features"])
        features = f"""
      <section class="detail-block" aria-labelledby="features">
        <h2 id="features">What it does</h2>
        <ul class="features">
{items}
        </ul>
      </section>
"""

    pager = '      <nav class="pager" aria-label="More projects">\n'
    pager += (f'        <a class="prev" href="/projects/{prev_p["slug"]}/"><span>Previous</span>{e(prev_p["title"])}</a>\n' if prev_p else "        <span></span>\n")
    pager += (f'        <a class="next" href="/projects/{next_p["slug"]}/"><span>Next</span>{e(next_p["title"])}</a>\n' if next_p else "        <span></span>\n")
    pager += "      </nav>\n"

    body = f"""
  <main id="main" class="wrap detail">
    <p class="crumb"><a href="/projects/">← All projects</a></p>
    <header class="detail-head">
      <p class="eyebrow">{e(p['group'])}</p>
      <h1>{e(p['title'])}</h1>
      <p class="lede">{e(p['summary'])}</p>
      <div class="detail-meta">
        {tags(p['tech'])}
        <div class="detail-links">{' '.join(links)}</div>
      </div>
    </header>

{gallery}
      <section class="detail-block" aria-labelledby="about">
        <h2 id="about">About</h2>
{about}
      </section>
{features}
{pager}  </main>
"""
    return HEAD.format(title=e(f"{p['title']} — Brayden Herrell"), desc=e(p["summary"])) + body + FOOT


def index_page():
    body = f"""
  <main id="main" class="wrap detail">
    <header class="detail-head">
      <p class="eyebrow">Brayden Herrell</p>
      <h1>Projects</h1>
      <p class="lede">Networks, infrastructure, and software I've built. Pick one to see what it does and how it's built.</p>
    </header>

    <section class="section" aria-label="Projects">
{cards_by_group()}
    </section>
  </main>
"""
    return HEAD.format(title="Projects — Brayden Herrell", desc="Networks, infrastructure, and software built by Brayden Herrell.") + body + FOOT


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for i, p in enumerate(PROJECTS):
        d = OUT / p["slug"]
        d.mkdir(exist_ok=True)
        for f, _ in p.get("shots") or []:
            if not (d / f).exists():
                raise SystemExit(f"missing screenshot: {d / f}")
        (d / "index.html").write_text(project_page(i, p))
    (OUT / "index.html").write_text(index_page())

    # Refresh the project cards on the homepage between the markers.
    home = ROOT / "public" / "index.html"
    s = home.read_text()
    start, end = "<!-- projects:start -->", "<!-- projects:end -->"
    if start in s and end in s:
        a, b = s.index(start) + len(start), s.index(end)
        s = s[:a] + "\n" + cards_by_group() + "      " + s[b:]
        home.write_text(s)
    print(f"built {len(PROJECTS)} project pages")


if __name__ == "__main__":
    main()
