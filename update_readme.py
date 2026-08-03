import requests
import re
import time

url = 'https://api.github.com/users/RiteshGenAI/repos?sort=updated&per_page=50'
response = requests.get(url)
repos = response.json()

if not isinstance(repos, list):
    print('Error fetching repos:', repos)
    exit(1)

filtered = [r for r in repos if r['name'].lower() != 'riteshgenai' and not r['fork']]

filtered.sort(key=lambda r: (r.get('stargazers_count', 0), r.get('updated_at', '')), reverse=True)

top_repos = filtered[:4]

html = '<p align="center">\n'
for repo in top_repos:
    name = repo['name']
    html += f'  <a href="https://github.com/RiteshGenAI/{name}">\n'
    html += f'    <img src="https://gh-readme-stats.vercel.app/api/pin/?username=RiteshGenAI&repo={name}&theme=calm" height="120" />\n'
    html += '  </a>\n'
html += '</p>'

cache_bust = int(time.time())
streak_html = (
    '<p align="center">\n'
    f'  <img src="https://streak-stats.demolab.com/?user=RiteshGenAI&theme=calm&{cache_bust}"'
    ' alt="GitHub Streak" />\n'
    '</p>'
)

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

pattern_repos = r'<!-- RECENT_REPOS_START -->.*?<!-- RECENT_REPOS_END -->'
replacement_repos = f'<!-- RECENT_REPOS_START -->\\n{html}\\n<!-- RECENT_REPOS_END -->'
new_content = re.sub(pattern_repos, replacement_repos, content, flags=re.DOTALL)

pattern_streak = r'<!-- STREAK_START -->.*?<!-- STREAK_END -->'
replacement_streak = f'<!-- STREAK_START -->\\n{streak_html}\\n<!-- STREAK_END -->'
new_content = re.sub(pattern_streak, replacement_streak, new_content, flags=re.DOTALL)

pattern_cards = r'<!-- GITHUB_DATA_START -->.*?<!-- GITHUB_DATA_END -->'
replacement_cards = (
    '<!-- GITHUB_DATA_START -->\n'
    '<p align="center">\n'
    '  <img src="./profile-3d-contrib/profile-night-green.svg" alt="GitHub 3D Contribution Graph" />\n'
    '</p>\n'
    '<!-- GITHUB_DATA_END -->'
)
new_content = re.sub(pattern_cards, replacement_cards, new_content, flags=re.DOTALL)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_content)
