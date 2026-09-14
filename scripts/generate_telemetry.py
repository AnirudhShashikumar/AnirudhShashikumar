"""Refresh an honest public GitHub snapshot. All data is fetched before files change."""
from collections import Counter
from datetime import datetime, timedelta, timezone
from html import escape
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from build_visuals import document, frame, path, text

ROOT = Path(__file__).resolve().parents[1]
OWNER = 'AnirudhShashikumar'
API = f'https://api.github.com/users/{OWNER}/repos'
SOURCE = f'https://github.com/{OWNER}?tab=repositories'
START, END = '<!-- telemetry:start -->', '<!-- telemetry:end -->'
WINDOW_DAYS = 90
SCOPE = 'Public, non-fork, non-archived, enabled, non-empty repositories owned by AnirudhShashikumar; profile repository excluded.'
NAME = re.compile(r'^[A-Za-z0-9_.-]{1,100}$')


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError('GitHub returned an invalid push timestamp')
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        raise ValueError('Push timestamp lacks a timezone')
    return dt.astimezone(timezone.utc)


def request_page(page):
    headers = {'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2026-03-10', 'User-Agent': 'AnirudhShashikumar-profile-telemetry'}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = 'Bearer ' + token
    url = f'{API}?type=owner&sort=full_name&per_page=100&page={page}'
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return json.load(response)


def fetch_repositories(fetch=request_page):
    result, names = [], set()
    for page in range(1, 101):
        batch = fetch(page)
        if not isinstance(batch, list) or len(batch) > 100:
            raise ValueError('Invalid GitHub repository response; keeping prior snapshot')
        for repo in batch:
            if not isinstance(repo, dict) or not NAME.fullmatch(repo.get('name', '')):
                raise ValueError('Invalid repository identity')
            name = repo['name'].casefold()
            if name in names:
                # Pagination can shift while repos change. Fail closed rather than undercount.
                raise ValueError('Duplicate repository across pages; retry the snapshot')
            names.add(name)
            result.append(repo)
        if len(batch) < 100:
            return result
    raise ValueError('Pagination limit reached; refusing a partial repository count')


def snapshot(repositories, now):
    if now.tzinfo is None:
        raise ValueError('Snapshot time must be timezone-aware')
    now = now.astimezone(timezone.utc)
    selected = []
    required = ['fork', 'archived', 'disabled', 'private']
    for repo in repositories:
        if not isinstance(repo, dict) or not NAME.fullmatch(repo.get('name', '')):
            raise ValueError('Invalid repository identity')
        if any(not isinstance(repo.get(k), bool) for k in required):
            raise ValueError('Incomplete repository visibility/lifecycle metadata')
        if not isinstance(repo.get('size'), int) or repo['size'] < 0:
            raise ValueError('Missing repository size')
        owner = repo.get('owner', {}).get('login', '')
        if not owner:
            raise ValueError('Missing repository owner')
        if owner.casefold() != OWNER.casefold() or repo['name'].casefold() == OWNER.casefold():
            continue
        if any(repo[k] for k in required) or repo['size'] == 0:
            continue
        language = repo.get('language')
        if language is not None and (not isinstance(language, str) or len(language) > 100):
            raise ValueError('Invalid primary-language metadata')
        pushed = repo.get('pushed_at')
        dt = timestamp(pushed) if pushed is not None else None
        if dt is not None and dt > now + timedelta(minutes=5):
            raise ValueError('Push timestamp is unexpectedly in the future')
        selected.append({'name': repo['name'], 'url': f'https://github.com/{OWNER}/{repo["name"]}', 'primary_language': language, 'pushed_at': pushed})
    selected.sort(key=lambda r: r['name'].casefold())
    latest = sorted((r for r in selected if r['pushed_at']), key=lambda r: (timestamp(r['pushed_at']), r['name']), reverse=True)
    active = [r for r in latest if now - timedelta(days=WINDOW_DAYS) <= timestamp(r['pushed_at']) <= now]
    counts = Counter(r['primary_language'] for r in selected if r['primary_language'])
    languages = sorted(counts, key=lambda name: (-counts[name], name))
    return {'generated_at': now.isoformat(timespec='seconds').replace('+00:00', 'Z'), 'source': SOURCE, 'api': API, 'scope': SCOPE, 'window_days': WINDOW_DAYS, 'public_project_count': len(selected), 'recently_pushed_count': len(active), 'primary_languages': languages, 'recent_projects': latest[:2], 'repositories': selected}


def compact(value, limit=24):
    return value if len(value) <= limit else value[:limit-1] + '…'


def render_svg(data, theme='dark', mobile=False):
    w,h=(480,290) if mobile else (960,210)
    b=frame(w,h)
    when=data['generated_at'].replace('T', ' ').replace('Z', ' UTC')
    digits=str(data['public_project_count']).zfill(2)
    count_size=48 if len(digits)<=2 else 32 if len(digits)==3 else 24
    languages=' · '.join(data['primary_languages'][:3]) or 'Not reported by GitHub'
    if len(data['primary_languages'])>3:languages += ' + more'
    if mobile:
        b+=text(24,30,'PUBLIC PROJECT SNAPSHOT',13,'var(--cyan)',mono=True)
        b+=text(24,53,when,13,'var(--muted)',mono=True)
        b+=text(23,112,digits,count_size,weight=600)
        b+=text(104,87,'SOURCE PROJECTS',14,'var(--muted)',mono=True)
        b+=text(104,111,f'{data["recently_pushed_count"]} pushed in {WINDOW_DAYS} days',18)
        b+=text(24,151,compact(languages,36),19,'var(--cyan)',mono=True)
        b+=path('M24 168H456','var(--border)')
        b+=text(24,194,'LATEST REPOSITORY PUSHES',12,'var(--muted)',mono=True)
        for i,repo in enumerate(data['recent_projects']):
            y=225+i*34
            b+=text(24,y,compact(repo['name'],22),19,weight=600,mono=True)
            b+=text(456,y,repo['pushed_at'][:10],14,'var(--muted)',mono=True,text_anchor='end')
        if not data['recent_projects']:b+=text(24,235,'No push dates reported.',18,'var(--muted)')
    else:
        b+=text(32,30,'PUBLIC PROJECT SNAPSHOT',12,'var(--cyan)',mono=True,letter_spacing=1)
        b+=text(928,30,when,12,'var(--muted)',mono=True,text_anchor='end')
        b+=text(30,101,digits,count_size+4,weight=600)
        b+=text(117,72,'SOURCE PROJECTS',13,'var(--muted)',mono=True)
        b+=text(117,97,f'{data["recently_pushed_count"]} pushed in the last {WINDOW_DAYS} days',17)
        b+=text(510,68,'PRIMARY REPOSITORY LANGUAGES',11,'var(--muted)',mono=True)
        b+=text(510,97,compact(languages,32),21,'var(--cyan)',mono=True)
        b+=path('M32 120H928','var(--border)')
        for i,repo in enumerate(data['recent_projects']):
            x=32+i*478
            b+=text(x,156,compact(repo['name'],30),21,weight=600,mono=True)
            b+=text(x,182,'PUSHED '+repo['pushed_at'][:10]+' UTC',12,'var(--muted)',mono=True)
        if not data['recent_projects']:b+=text(32,158,'No push dates reported.',18,'var(--muted)')
    desc=f'{data["public_project_count"]} source projects; {data["recently_pushed_count"]} with pushes in {WINDOW_DAYS} days. Primary repository languages: {languages}. Snapshot {when}. Repository activity, not deployment status.'
    return document(w,h,'Public GitHub telemetry — '+when,desc,b,theme)


def markdown(data):
    count,active=data['public_project_count'],data['recently_pushed_count']
    when=data['generated_at'].replace('T',' ').replace('Z',' UTC')
    languages=', '.join(data['primary_languages']) or 'not reported'
    alt=escape(f'Public snapshot: {count} source projects, {active} pushed in {WINDOW_DAYS} days. Primary languages: {languages}. Refreshed {when}. Full snapshot follows as text.',quote=True)
    rows='\n'.join(f'- [{r["name"]}]({r["url"]}) — last repository push: **{r["pushed_at"][:10]} UTC**.' for r in data['recent_projects']) or '- No push dates reported.'
    return f'''<a href="assets/generated/telemetry.json#gh-dark-mode-only">
  <picture>
    <source media="(max-width: 600px)" srcset="assets/generated/telemetry-mobile.svg">
    <img src="assets/generated/telemetry.svg" width="960" alt="{alt}">
  </picture>
</a>
<a href="assets/generated/telemetry.json#gh-light-mode-only">
  <picture>
    <source media="(max-width: 600px)" srcset="assets/generated/telemetry-mobile-light.svg">
    <img src="assets/generated/telemetry-light.svg" width="960" alt="{alt}">
  </picture>
</a>

<details>
<summary>Read the snapshot and its scope</summary>

**Snapshot:** {when} · **{count} public source projects** · **{active} pushed in the last {WINDOW_DAYS} days**.<br>
**Primary repository languages:** {escape(languages)}.

{rows}

{SCOPE} Primary language means GitHub's repository classification, not proficiency. Counts include all qualifying projects; the profile features a curated subset. These figures are a dated snapshot, not a live availability indicator.

[Machine-readable snapshot](assets/generated/telemetry.json) · [GitHub source]({SOURCE})

</details>'''


def prepare_outputs(data, readme):
    if readme.count(START)!=1 or readme.count(END)!=1:
        raise ValueError('Expected exactly one telemetry marker pair')
    start,end=readme.index(START)+len(START),readme.index(END)
    if start>end:
        raise ValueError('Reversed telemetry markers')
    outputs={'README.md': readme[:start]+'\n'+markdown(data)+'\n'+readme[end:]}
    for mobile in [False,True]:
        for theme in ['dark','light']:
            name='telemetry'+('-mobile' if mobile else '')+('-light' if theme=='light' else '')+'.svg'
            outputs['assets/generated/'+name]=render_svg(data,theme,mobile)
    outputs['assets/generated/telemetry.json']=json.dumps(data,indent=2,ensure_ascii=False)+'\n'
    return outputs


def refresh(root=ROOT, fetch=request_page, now=None):
    data=snapshot(fetch_repositories(fetch), now or datetime.now(timezone.utc))
    outputs=prepare_outputs(data,(root/'README.md').read_text())
    # Network, schema, and marker failures occur above; never publish partial API data.
    # Each filesystem replacement is atomic. CI commits the complete successful set.
    for relative,content in outputs.items():
        target=root/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        temporary=target.with_name(target.name+'.tmp')
        temporary.write_text(content)
        temporary.replace(target)
    print(f'Refreshed public snapshot: {data["public_project_count"]} source projects, {data["recently_pushed_count"]} with pushes in {WINDOW_DAYS} days.')
    return data


if __name__=='__main__':
    try:
        refresh()
    except (HTTPError,URLError,ValueError,KeyError,TypeError,OSError) as error:
        print(f'Telemetry refresh failed; no new snapshot should be committed: {error}',file=sys.stderr)
        raise SystemExit(1)
