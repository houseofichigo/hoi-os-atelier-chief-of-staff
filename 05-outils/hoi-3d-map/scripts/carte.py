#!/usr/bin/env python3
"""HOI OS — hoi-3d-map (version dossier).

Construit carte.html, une carte 3D cliquable du wiki et des sources ingérées,
à partir des fichiers du dossier uniquement (wiki/ et .hoi/). Fonctionne sans internet.

  python3 skills/hoi-3d-map/scripts/carte.py verifier      # contrôle liens et citations, n'écrit rien
  python3 skills/hoi-3d-map/scripts/carte.py construire    # écrit carte.html à la racine du dossier
  options : --racine CHEMIN   --sortie carte.html   --sans-sources

Python 3.9+, bibliothèque standard uniquement.
"""
import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
VENDOR = SKILL / "vendor"
IGNORED_WIKI = {"index", "accueil", "readme"}

TYPE_ALIASES = {
    "client": "client", "clients": "client", "prospect": "client", "compte": "client", "entreprise": "client",
    "organisation": "client", "organization": "client",
    "personne": "personne", "personnes": "personne", "person": "personne", "people": "personne", "contact": "personne",
    "mission": "mission", "missions": "mission", "projet": "mission", "project": "mission", "opportunite": "mission",
    "engagement": "mission",
    "reunion": "reunion", "reunions": "reunion", "meeting": "reunion", "rendez-vous": "reunion", "rdv": "reunion",
    "decision": "decision", "decisions": "decision",
}
TROU_WORDS = ("trou", "gap", "illisible", "echec", "non lu", "non-lu", "erreur", "vide")

CITE_RE = re.compile(r"src-(\d{3,5})(?:\s*[,;:]?\s*¶\s*(\d+))?", re.I)
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]*))?\]\]")
PASSAGE_RE = re.compile(r"^\s*(?:[#>*\-]+\s*)*[\[(]?\**\s*¶\s*(\d+)\s*\**[\])]?\s*[:.\-—)]*\s*(.*)$")
HEADER_KV_RE = re.compile(r"^\s*[-*]?\s*\**\s*([A-Za-zÀ-ÿ_' ]{2,30}?)\s*\**\s*[:：]\s*\**\s*(.+?)\s*\**\s*$")


# ------------------------------------------------------------------ helpers
def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def slug(s):
    s = strip_accents(str(s)).lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def src_id(num):
    return f"src-{int(num):04d}"


def parse_frontmatter(text):
    """YAML-lite: key: value, key: [a, b], or key:\n  - a\n  - b. Returns (meta, body)."""
    if not text.lstrip().startswith("---"):
        return {}, text
    text = text.lstrip()
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta, current = {}, None
    for line in text[3:end].splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        m = re.match(r"^\s*-\s+(.*)$", line)
        if m and current:
            meta.setdefault(current, [])
            if isinstance(meta[current], list):
                meta[current].append(m.group(1).strip().strip("'\""))
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            k, v = slug(k).replace("-", "_"), v.strip()
            current = k
            if v.startswith("[") and v.endswith("]"):
                meta[k] = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
            elif v == "":
                meta[k] = []
            else:
                meta[k] = v.strip("'\"")
    return meta, text[end + 4:].lstrip("\n")


def header_block(text, max_lines=25):
    """Reads 'Clé : valeur' lines at the top of a file (used when there is no YAML frontmatter)."""
    meta = {}
    for line in text.splitlines()[:max_lines]:
        if PASSAGE_RE.match(line):
            break
        m = HEADER_KV_RE.match(line)
        if m:
            meta[slug(m.group(1)).replace("-", "_")] = m.group(2).strip()
    return meta


def first(meta, *keys, default=None):
    for k in keys:
        v = meta.get(k)
        if v not in (None, "", []):
            return v
    return default


def as_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v if str(x).strip()]
    return [x.strip() for x in re.split(r"[;,]", str(v)) if x.strip()]


# ------------------------------------------------------------------ sources
def load_manifest(root):
    for name in ("manifeste.json", "manifest.json"):
        p = root / ".hoi" / name
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                print(f"⚠ {p.relative_to(root)} n'est pas un JSON valide : {e}", file=sys.stderr)
                return {}
            if isinstance(data, dict):
                for key in ("sources", "fichiers", "entries", "items", "documents"):
                    if isinstance(data.get(key), list):
                        data = data[key]
                        break
                else:
                    data = [dict(v, id=k) if isinstance(v, dict) else {"id": k} for k, v in data.items()
                            if str(k).lower().startswith("src")]
            out = {}
            for e in data if isinstance(data, list) else []:
                if not isinstance(e, dict):
                    continue
                e = {slug(k).replace("-", "_"): v for k, v in e.items()}
                raw = first(e, "id", "identifiant", "source_id", "src")
                m = CITE_RE.search(str(raw or ""))
                if m:
                    out[src_id(m.group(1))] = e
            return out
    return {}


def parse_passages(body):
    passages, cur, buf = {}, None, []
    for line in body.splitlines():
        m = PASSAGE_RE.match(line)
        if m:
            if cur is not None:
                passages[cur] = "\n".join(buf).strip()
            cur, buf = int(m.group(1)), [m.group(2)]
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        passages[cur] = "\n".join(buf).strip()
    return passages


def load_sources(root):
    manifest = load_manifest(root)
    sources = {}
    extract_dirs = [d for d in (root / ".hoi" / "extraits", root / ".hoi" / "extracted") if d.exists()]
    files = {}
    for d in extract_dirs:
        for p in sorted(d.glob("*.md")):
            m = CITE_RE.search(p.stem)
            if m:
                files[src_id(m.group(1))] = p
    for sid in sorted(set(manifest) | set(files)):
        e = manifest.get(sid, {})
        meta, body, passages = {}, "", {}
        if sid in files:
            text = files[sid].read_text(encoding="utf-8", errors="replace")
            fm, body = parse_frontmatter(text)
            meta = {**header_block(body), **fm}
            passages = parse_passages(body)
        info = {**{k: v for k, v in meta.items()}, **e}
        status = str(first(info, "statut", "statut_lecture", "status", "lecture", "extraction", default="")).lower()
        trou = any(w in strip_accents(status) for w in TROU_WORDS) or (sid in files and not passages)
        path = str(first(info, "chemin", "chemin_original", "chemin_source", "path", "source_path", "fichier_source",
                         default="") or "")
        if path and not (root / path).exists():
            hits = list(root.glob(f"sources/**/{Path(path).name}"))
            path = hits[0].relative_to(root).as_posix() if hits else path
        sources[sid] = {
            "id": sid, "kind": "source", "type": "source",
            "title": str(first(info, "nom_d_origine", "nom_origine", "nom", "original_name", "fichier", "name",
                               default=Path(path).name or sid)),
            "provenance": str(first(info, "provenance", "app", "origine", default="")),
            "date": str(first(info, "date_du_document", "date_document", "document_date", "date", default="") or ""),
            "client": str(first(info, "client", default="") or ""),
            "path": path, "trou": trou, "status": status or ("trou" if trou else "lu"),
            "reason": str(first(info, "raison", "motif", "gap", "trou", "note", default="") or ""),
            "passages": [[k, v] for k, v in sorted(passages.items())],
            "extract": files[sid].relative_to(root).as_posix() if sid in files else "",
        }
    return sources


# ------------------------------------------------------------------ wiki
def page_type(meta, path, root):
    t = slug(str(first(meta, "type", "categorie", "category", default="")))
    if t in TYPE_ALIASES:
        return TYPE_ALIASES[t]
    for part in path.relative_to(root / "wiki").parts[:-1]:
        if slug(part) in TYPE_ALIASES:
            return TYPE_ALIASES[slug(part)]
    return "autre"


def load_wiki(root):
    pages, duplicates = {}, []
    wiki = root / "wiki"
    if not wiki.exists():
        return pages, duplicates
    for p in sorted(wiki.rglob("*.md")):
        if p.name.startswith(".") or slug(p.stem) in IGNORED_WIKI:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_frontmatter(text)
        meta = fm or header_block(body)
        h1 = re.search(r"^#\s+(.+)$", body, re.M)
        title = str(first(meta, "titre", "title", default=h1.group(1).strip() if h1 else p.stem))
        key = slug(p.stem)
        if key in pages:
            duplicates.append((pages[key]["path"], p.relative_to(root).as_posix()))
            continue
        pages[key] = {
            "id": key, "kind": "page", "type": page_type(meta, p, root), "title": title,
            "status": str(first(meta, "statut", "status", default="brouillon")),
            "aliases": as_list(first(meta, "alias", "aliases", default=[])),
            "updated": str(first(meta, "mise_a_jour", "mis_a_jour", "date_de_mise_a_jour", "updated", "date", default="")),
            "path": p.relative_to(root).as_posix(), "body": body,
        }
    return pages, duplicates


def resolver(pages):
    idx = {}
    for key, p in pages.items():
        for name in [key, p["title"], *p["aliases"], Path(p["path"]).stem]:
            idx.setdefault(slug(name), key)
    return idx


# ------------------------------------------------------------------ analysis
def analyse(root, with_sources=True):
    pages, duplicates = load_wiki(root)
    sources = load_sources(root)
    resolve = resolver(pages)
    links, seen, problems = [], set(), {"liens": [], "citations": [], "trous_cites": [], "sans_citation": [],
                                        "doublons": duplicates}
    cited_by = {}
    for key, p in pages.items():
        body = p["body"]
        p["links"], p["cites"] = [], []
        for target, _label in LINK_RE.findall(body):
            t = resolve.get(slug(target))
            if not t:
                problems["liens"].append((p["path"], f"[[{target.strip()}]]"))
                continue
            if t != key and t not in p["links"]:
                p["links"].append(t)
            pair = tuple(sorted((key, t)))
            if t != key and pair not in seen:
                seen.add(pair)
                links.append({"source": key, "target": t, "kind": "lien"})
        cites = [(src_id(n), int(par) if par else None) for n, par in CITE_RE.findall(body)]
        if not cites:
            problems["sans_citation"].append(p["path"])
        for sid, par in cites:
            s = sources.get(sid)
            if not s:
                problems["citations"].append((p["path"], f"{sid} (source inconnue)"))
                continue
            if s["trou"] and par is not None:
                problems["trous_cites"].append((p["path"], f"{sid} ¶{par} (source illisible : aucun passage ne peut être cité)"))
            elif not s["trou"] and par is not None and par not in dict(s["passages"]):
                problems["citations"].append((p["path"], f"{sid} ¶{par} (passage inexistant)"))
            if sid not in p["cites"]:
                p["cites"].append(sid)
                cited_by.setdefault(sid, []).append(key)
                if with_sources:
                    links.append({"source": key, "target": sid, "kind": "citation"})
    for sid, s in sources.items():
        s["cited_by"] = cited_by.get(sid, [])
    nodes = list(pages.values()) + (list(sources.values()) if with_sources else [])
    return {"nodes": nodes, "links": links, "pages": len(pages), "sources": len(sources),
            "trous": sum(1 for s in sources.values() if s["trou"])}, problems


def report(problems, data):
    print(f"Wiki : {data['pages']} pages · Sources : {data['sources']} ({data['trous']} trous)")
    labels = [("liens", "Liens [[...]] cassés"), ("citations", "Citations invalides"),
              ("trous_cites", "Passages cités dans une source illisible (trou)"), ("doublons", "Pages en double (même nom)"),
              ("sans_citation", "Pages sans aucune citation")]
    defects = 0
    for key, label in labels:
        items = problems[key]
        print(f"\n{label} : {len(items)}")
        for it in items[:40]:
            print("  - " + (" → ".join(it) if isinstance(it, tuple) else it))
        if key in ("liens", "citations", "trous_cites", "doublons"):
            defects += len(items)
    print(f"\n{'OK : aucun défaut bloquant.' if not defects else f'{defects} défaut(s) à corriger dans le wiki avant de construire la carte.'}")
    return defects


# ------------------------------------------------------------------ build
def build(root, out, with_sources):
    data, problems = analyse(root, with_sources)
    payload = {"nodes": data["nodes"], "links": data["links"], "counts": {k: data[k] for k in ("pages", "sources", "trous")},
               "generated": datetime.now().strftime("%d/%m/%Y %H:%M"), "root": root.name}
    graph_js = (VENDOR / "3d-force-graph.min.js").read_text(encoding="utf-8")
    marked_js = (VENDOR / "marked.umd.js").read_text(encoding="utf-8")
    html = (TEMPLATE.replace("/*__GRAPH__*/", graph_js.replace("</script", "<\\/script"))
            .replace("/*__MARKED__*/", marked_js.replace("</script", "<\\/script"))
            .replace("__DATA__", json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")))
    out.write_text(html, encoding="utf-8")
    n_bad = len(problems["liens"]) + len(problems["citations"])
    print(f"Carte écrite : {out.relative_to(root) if out.is_relative_to(root) else out} — {data['pages']} pages, "
          f"{data['sources'] if with_sources else 0} sources ({data['trous']} trous), {len(data['links'])} liens."
          + (f" ⚠ {n_bad} lien(s)/citation(s) invalide(s) affiché(s) en rouge." if n_bad else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["verifier", "construire"])
    ap.add_argument("--racine", default=None, help="dossier de travail (par défaut : le dossier qui contient skills/)")
    ap.add_argument("--sortie", default="carte.html")
    ap.add_argument("--sans-sources", action="store_true")
    a = ap.parse_args()
    root = Path(a.racine).resolve() if a.racine else SKILL.parent.parent
    if not (root / "wiki").exists():
        sys.exit(f"Pas de dossier wiki/ dans {root}. Construisez d'abord le wiki (hoi-wiki-author).")
    if a.action == "verifier":
        data, problems = analyse(root)
        sys.exit(1 if report(problems, data) else 0)
    build(root, root / a.sortie, not a.sans_sources)


TEMPLATE = r"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Carte des connaissances</title>
<style>
:root{--bg:#0d1117;--panel:#161b22;--panel2:#1c2330;--line:#30363d;--text:#e6edf3;--muted:#8b949e;--accent:#58a6ff;--warn:#d29922;--bad:#f85149;--ok:#3fb950}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:var(--bg);color:var(--text);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif}
#app{display:grid;grid-template-columns:280px minmax(0,1fr) 440px;height:100vh}
#side,#panel{background:var(--panel);overflow:auto}
#side{border-right:1px solid var(--line);padding:16px}
#panel{border-left:1px solid var(--line);padding:18px 22px}
h1{font-size:15px;margin:0 0 2px}.sub{color:var(--muted);font-size:12px;margin-bottom:12px}
input[type=search]{width:100%;padding:8px 10px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--text);font:inherit}
.legend{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0 4px}
.chip{display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border-radius:999px;border:1px solid var(--line);font-size:12px;cursor:pointer;user-select:none;background:transparent;color:var(--text);font-family:inherit}
.chip.off{opacity:.35}.dot{width:9px;height:9px;border-radius:50%;flex:none}
.group{margin-top:14px}.group h3{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:0 0 4px}
.item{display:flex;justify-content:space-between;gap:8px;width:100%;text-align:left;padding:5px 8px;border-radius:6px;color:var(--text);background:none;border:0;cursor:pointer;font:inherit}
.item:hover,.item.active{background:var(--panel2)}.item small{color:var(--muted);flex:none}
#graph{position:relative;min-width:0;overflow:hidden}#canvas{position:absolute;inset:0}
#tools{position:absolute;right:12px;top:12px;z-index:2;display:flex;gap:6px}
#hint{position:absolute;left:14px;bottom:12px;color:var(--muted);font-size:12px;pointer-events:none}
.btn{padding:6px 12px;border-radius:8px;border:1px solid var(--line);background:var(--panel);color:var(--text);cursor:pointer;font:inherit}
.btn:disabled{opacity:.4;cursor:default}
.badge{display:inline-block;font-size:11px;padding:1px 8px;border-radius:999px;border:1px solid var(--line);margin:0 6px 4px 0;color:var(--muted)}
.badge.brouillon{color:var(--warn);border-color:var(--warn)}.badge.ok{color:var(--ok);border-color:var(--ok)}.badge.trou{color:var(--bad);border-color:var(--bad)}
#panel h2{font-size:20px;margin:6px 0 4px}#panel .meta{color:var(--muted);font-size:12px;margin-bottom:14px}
#panel h3{font-size:13px;margin:18px 0 6px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
#panel a{color:var(--accent);text-decoration:none;cursor:pointer}#panel a:hover{text-decoration:underline}
a.cite{font-size:12px;background:var(--panel2);padding:0 5px;border-radius:4px;white-space:nowrap}
a.cite.bad,span.broken{color:var(--bad)!important}
#panel table{border-collapse:collapse;width:100%;font-size:13px}#panel td,#panel th{border:1px solid var(--line);padding:4px 6px;text-align:left;vertical-align:top}
#panel blockquote{margin:8px 0;padding:4px 12px;border-left:3px solid var(--line);color:var(--muted)}
.passage{padding:8px 10px;border-left:3px solid var(--line);margin:8px 0;white-space:pre-wrap;font-size:13px;border-radius:0 6px 6px 0}
.passage.hit{border-color:var(--accent);background:#132035}.pn{display:block;color:var(--muted);font-size:11px;margin-bottom:2px}
.empty{color:var(--muted)}.alert{color:var(--bad);background:#2a1215;border:1px solid #5a1d22;padding:8px 10px;border-radius:6px;font-size:13px}
@media (max-width:1000px){#app{grid-template-columns:1fr;grid-template-rows:auto 55vh auto;height:auto}#side,#panel{border:0}}
</style></head>
<body><div id="app">
<aside id="side"><h1>Carte des connaissances</h1><div class="sub" id="stats"></div>
<input type="search" id="q" placeholder="Rechercher une page, une source, un mot…" aria-label="Rechercher">
<div class="legend" id="legend"></div><div id="list"></div></aside>
<div id="graph"><div id="canvas"></div>
<div id="tools"><button class="btn" id="back" disabled>← Retour</button><button class="btn" id="fit">Vue d'ensemble</button></div>
<div id="hint">Glisser pour pivoter · molette pour zoomer · clic droit pour se déplacer · clic sur un nœud pour l'ouvrir</div></div>
<section id="panel"><p class="empty">Cliquez sur un nœud de la carte ou sur un élément de la liste.</p></section>
</div>
<script>/*__GRAPH__*/</script>
<script>/*__MARKED__*/</script>
<script id="data" type="application/json">__DATA__</script>
<script>
const DATA=JSON.parse(document.getElementById('data').textContent);
const COLORS={client:'#58a6ff',personne:'#f778ba',mission:'#3fb950',reunion:'#d29922',decision:'#a371f7',autre:'#39c5cf',source:'#8b949e'};
const LABELS={client:'Clients',personne:'Personnes',mission:'Missions',reunion:'Réunions',decision:'Décisions',autre:'Autres',source:'Sources'};
const ORDER=['client','mission','reunion','personne','decision','autre','source'];
const byId=Object.fromEntries(DATA.nodes.map(n=>[n.id,n]));
const pagesIndex={};DATA.nodes.filter(n=>n.kind==='page').forEach(n=>[n.id,n.title,...(n.aliases||[]),n.path.split('/').pop().replace(/\.md$/,'')].forEach(k=>{pagesIndex[slug(k)]??=n.id}));
const hidden=new Set();let selected=null;const history=[];
function slug(s){return String(s).normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')}
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const color=n=>n.kind==='source'?(n.trou?'#f85149':COLORS.source):(COLORS[n.type]||COLORS.autre);
const typeOf=n=>n.kind==='source'?'source':n.type;
document.getElementById('stats').textContent=`${DATA.counts.pages} pages · ${DATA.counts.sources} sources (${DATA.counts.trous} illisibles) · générée le ${DATA.generated}`;
const degree={};DATA.links.forEach(l=>{degree[l.source]=(degree[l.source]||0)+1;degree[l.target]=(degree[l.target]||0)+1});
const container=document.getElementById('canvas');
const Graph=ForceGraph3D()(container).backgroundColor('#0d1117').showNavInfo(false)
 .graphData({nodes:DATA.nodes.map(n=>({...n})),links:DATA.links.map(l=>({...l}))})
 .nodeId('id').nodeRelSize(3.4)
 .nodeLabel(n=>`<div style="background:#161b22;padding:4px 8px;border-radius:6px;border:1px solid #30363d;font:13px sans-serif">${esc(n.title)}<br><small style="color:#8b949e">${n.kind==='source'?esc(n.id)+(n.trou?' · illisible':''):esc(LABELS[n.type]||n.type)}</small></div>`)
 .nodeColor(color).nodeOpacity(.95)
 .nodeVal(n=>n.kind==='source'?1.3:2.5+Math.min(9,(degree[n.id]||0)*.6))
 .nodeVisibility(n=>!hidden.has(typeOf(n)))
 .linkVisibility(l=>{const s=byId[l.source.id||l.source],t=byId[l.target.id||l.target];return s&&t&&!hidden.has(typeOf(s))&&!hidden.has(typeOf(t))})
 .linkColor(l=>l.kind==='citation'?'rgba(139,148,158,.28)':'rgba(220,226,235,.75)')
 .linkWidth(l=>l.kind==='citation'?0:1.4).linkOpacity(.6)
 .linkDirectionalParticles(l=>l.kind==='lien'?2:0).linkDirectionalParticleWidth(1.4)
 .onNodeClick(n=>open(n.id,null));
const resize=()=>Graph.width(container.clientWidth).height(container.clientHeight);
window.addEventListener('resize',resize);resize();
document.getElementById('fit').onclick=()=>Graph.zoomToFit(700,50);
document.getElementById('back').onclick=()=>{history.pop();const prev=history.pop();if(prev)open(prev.id,prev.p)};
setTimeout(()=>Graph.zoomToFit(900,50),1800);
function focus(id){const n=Graph.graphData().nodes.find(x=>x.id===id);if(!n||n.x===undefined)return;const r=1+220/Math.hypot(n.x||1,n.y||1,n.z||1);Graph.cameraPosition({x:n.x*r,y:n.y*r,z:n.z*r},n,900)}
function renderBody(md){
 md=md.replace(/^---[\s\S]*?\n---\n/,'');
 md=md.replace(/\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]*))?\]\]/g,(m,t,label)=>{const id=pagesIndex[slug(t)];return id?`<a data-open="${esc(id)}">${esc(label||byId[id].title)}</a>`:`<span class="broken" title="Page introuvable">${esc(label||t)} ⚠</span>`});
 md=md.replace(/\[((?:\s*src-\d{3,5}(?:\s*[,;:]?\s*¶\s*\d+)?\s*[,;]?)+)\]/gi,'$1');
 md=md.replace(/src-(\d{3,5})(?:\s*[,;:]?\s*¶\s*(\d+))?/gi,(m,num,p)=>{const id='src-'+String(+num).padStart(4,'0');const s=byId[id];const ok=s&&(!p||(s.passages||[]).some(x=>String(x[0])===p));return `<a class="cite${ok?'':' bad'}" data-open="${id}" data-p="${p||''}" title="${ok?'Voir le passage':'Citation invalide'}">${id}${p?' ¶'+p:''}</a>`});
 return marked.parse(md);
}
function pageLinks(ids){return ids.map(i=>byId[i]?`<a data-open="${esc(i)}">${esc(byId[i].title)}</a>`:'').filter(Boolean).join(' · ')}
function open(id,para){
 const n=byId[id];if(!n)return;selected=id;history.push({id,p:para});document.getElementById('back').disabled=history.length<2;
 const panel=document.getElementById('panel');
 if(n.kind==='page'){
  const related=[...new Set([...(n.links||[]),...DATA.links.filter(l=>l.kind==='lien'&&l.target===id).map(l=>l.source)])].filter(x=>x!==id);
  const st=/brouillon|draft/i.test(n.status)?'brouillon':'ok';
  panel.innerHTML=`<span class="badge" style="color:${color(n)};border-color:${color(n)}">${esc(LABELS[n.type]||n.type)}</span><span class="badge ${st}">${esc(n.status||'brouillon')}</span>
  <h2>${esc(n.title)}</h2><div class="meta">${esc(n.path)}${n.updated?' · mis à jour '+esc(n.updated):''}${n.aliases?.length?' · aussi : '+esc(n.aliases.join(', ')):''}</div>
  <div>${renderBody(n.body)}</div>
  ${related.length?`<h3>Pages liées</h3><p>${pageLinks(related)}</p>`:''}
  ${(n.cites||[]).length?`<h3>Sources citées</h3><p>${n.cites.map(s=>`<a class="cite${byId[s]?.trou?' bad':''}" data-open="${s}">${s}</a> ${esc(byId[s]?.title||'')}`).join('<br>')}</p>`:''}`;
 }else{
  const href=n.path?encodeURI(n.path):'';
  panel.innerHTML=`<span class="badge">source${n.provenance?' · '+esc(n.provenance):''}</span><span class="badge ${n.trou?'trou':'ok'}">${n.trou?'illisible (trou)':'lue'}</span>
  <h2>${esc(n.id)}</h2><div class="meta">${esc(n.title)}${n.date&&!/inconnu|unknown|^none$/i.test(n.date)?' · document du '+esc(n.date):''}${n.client?' · '+esc(n.client):''}<br>
  ${href?`<a href="${href}" target="_blank">Ouvrir le fichier original</a> (preuve, lecture seule)`:'Chemin du fichier original inconnu'}${n.extract?` · <a href="${encodeURI(n.extract)}" target="_blank">texte extrait</a>`:''}</div>
  ${n.trou?`<p class="alert">Aucun texte n'a pu être lu dans ce fichier${n.reason?' : '+esc(n.reason):''}. Son contenu n'est pas dans la base : ne rien en déduire.</p>`:''}
  ${para&&!(n.passages||[]).some(x=>String(x[0])===String(para))?`<p class="alert">Le passage ¶${esc(para)} cité n'existe pas dans cette source.</p>`:''}
  ${(n.passages||[]).map(([k,v])=>`<div class="passage${String(k)===String(para)?' hit':''}"><span class="pn">¶${k}</span>${esc(v)}</div>`).join('')}
  ${(n.cited_by||[]).length?`<h3>Citée par</h3><p>${pageLinks(n.cited_by)}</p>`:'<h3>Citée par</h3><p class="empty">Aucune page du wiki ne cite cette source.</p>'}`;
  const hit=panel.querySelector('.passage.hit');if(hit)setTimeout(()=>hit.scrollIntoView({block:'center',behavior:'smooth'}),60);else panel.scrollTop=0;
 }
 if(n.kind==='page')panel.scrollTop=0;
 panel.querySelectorAll('a[data-open]').forEach(a=>a.onclick=e=>{e.preventDefault();open(a.dataset.open,a.dataset.p||null)});
 focus(id);renderList();
}
function renderLegend(){
 const present=ORDER.filter(t=>DATA.nodes.some(n=>typeOf(n)===t));
 const el=document.getElementById('legend');
 el.innerHTML=present.map(t=>`<button class="chip ${hidden.has(t)?'off':''}" data-t="${t}" title="Afficher / masquer"><span class="dot" style="background:${COLORS[t]}"></span>${LABELS[t]} (${DATA.nodes.filter(n=>typeOf(n)===t).length})</button>`).join('')
  +(DATA.counts.trous?`<span class="chip" style="cursor:default"><span class="dot" style="background:#f85149"></span>Source illisible</span>`:'');
 el.querySelectorAll('button.chip').forEach(c=>c.onclick=()=>{const t=c.dataset.t;hidden.has(t)?hidden.delete(t):hidden.add(t);Graph.nodeVisibility(Graph.nodeVisibility());Graph.linkVisibility(Graph.linkVisibility());renderLegend();renderList()});
}
function renderList(){
 const q=slug(document.getElementById('q').value.trim());
 const hay=n=>slug([n.title,n.id,n.body||'',(n.aliases||[]).join(' '),(n.passages||[]).map(p=>p[1]).join(' ')].join(' '));
 const groups={};DATA.nodes.filter(n=>!hidden.has(typeOf(n))&&(!q||hay(n).includes(q))).forEach(n=>(groups[typeOf(n)] ||= []).push(n));
 document.getElementById('list').innerHTML=ORDER.filter(t=>groups[t]).map(t=>`<div class="group"><h3>${LABELS[t]} (${groups[t].length})</h3>${groups[t].sort((a,b)=>(a.kind==='source'?a.id:a.title).localeCompare(b.kind==='source'?b.id:b.title)).map(n=>`<button class="item ${n.id===selected?'active':''}" data-id="${esc(n.id)}"><span>${esc(n.kind==='source'?n.id+' · '+n.title:n.title)}</span>${n.trou?'<small style="color:#f85149">illisible</small>':(/brouillon|draft/i.test(n.status||'')?'<small>brouillon</small>':'')}</button>`).join('')}</div>`).join('')||'<p class="empty">Aucun résultat.</p>';
 document.querySelectorAll('#list .item').forEach(b=>b.onclick=()=>open(b.dataset.id,null));
}
document.getElementById('q').addEventListener('input',renderList);
renderLegend();renderList();
</script></body></html>
"""

if __name__ == "__main__":
    main()
