import json,subprocess,datetime,html,xml.etree.ElementTree as ET
from pathlib import Path
ET.register_namespace('', 'http://www.w3.org/2000/svg')
root=Path(__file__).resolve().parents[1]
config_path=root/'scripts/profile-config.json'
if not config_path.exists(): config_path=Path('work/profile-config.json')
config=json.loads(config_path.read_text())
query='query { user(login:"Luk4sy") { contributionsCollection { contributionCalendar { weeks { contributionDays { date contributionCount contributionLevel weekday } } } } } }'
p=subprocess.run(['gh','api','graphql','-f','query='+query],capture_output=True,text=True,check=True)
data=json.loads(p.stdout)
if data.get('errors'): raise RuntimeError(data['errors'])
weeks=data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
assert 50 <= len(weeks) <= 54
parts=['''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="835" viewBox="0 0 900 835" role="img" aria-labelledby="title desc">
<title id="title">Lukasy | Education, Tech Stack and GitHub Contributions</title>
<desc id="desc">Software Engineering at Tianjin University of Technology. MScTP at The Hong Kong University of Science and Technology (Guangzhou). Full-stack technologies, AI coding tools and a GitHub contribution calendar.</desc>
<rect x="1" y="1" width="898" height="833" rx="14" fill="#0d1117" stroke="#30363d"/>
<path d="M15 1H885A14 14 0 0 1 899 15V43H1V15A14 14 0 0 1 15 1Z" fill="#161b22"/>
<path d="M1 43H899" stroke="#30363d"/>
<circle cx="23" cy="22" r="5" fill="#ff5f57"/><circle cx="42" cy="22" r="5" fill="#febc2e"/><circle cx="61" cy="22" r="5" fill="#28c840"/>
<g font-family="'SFMono-Regular',Consolas,'Liberation Mono',monospace">
<text x="450" y="27" text-anchor="middle" fill="#8b949e" font-size="12">luk4sy ~ / profile</text>
''']
def text(x,y,value,color='#c9d1d9',size=13,extra=''):
 parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{html.escape(value)}</text>')
def command(y,value):
 text(34,y,'❯','#7ee787',14);text(55,y,value,'#c9d1d9',14)
command(81,'whoami')
text(34,126,"Hi, I'm Lukasy",'#f0f6fc',34,'font-weight="700"');text(325,126,'_','#58a6ff',34)
text(35,156,'Exploring software engineering, full-stack development and AI.','#8b949e',13)
command(198,'cat education.txt')
text(35,225,'Software Engineering · Tianjin University of Technology','#c9d1d9',13)
text(35,250,'MScTP · The Hong Kong University of Science and Technology (Guangzhou)','#c9d1d9',12)
text(35,279,'contact → luk4sy@gmail.com','#58a6ff',12)
parts.append('<path d="M34 303H866" stroke="#21262d"/>')
command(336,'cat tech-stack.json')
brand_colors = {'typescript': '#3178C6', 'react': '#61DAFB', 'nextdotjs': '#FFFFFF', 'vuedotjs': '#4FC08D', 'tailwindcss': '#38BDF8', 'go': '#00ADD8', 'gin': '#00ADD8', 'openjdk': '#ED8B00', 'springboot': '#6DB33F', 'python': '#FFD43B', 'fastapi': '#00C7B7', 'nodedotjs': '#5FA04E', 'mysql': '#4EA9D6', 'postgresql': '#699ECA', 'redis': '#FF4438', 'docker': '#2496ED', 'linux': '#FCC624', 'codex': '#FFFFFF', 'claude': '#D97757', 'cursor': '#FFFFFF', 'dsh': '#6C8CFF'}
for i,(label,items) in enumerate(config['rows']):
 y=359+i*55
 text(35,y+15,label,'#8b949e',11)
 x=173
 for name,key in items:
  width=round(len(name)*6.0+ (34 if key in config['icons'] else 20))
  parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="27" rx="5" fill="#161b22" stroke="#30363d"/>')
  if key in config['icons']:
   brand_color=brand_colors.get(key,'#c9d1d9')
   icon=ET.fromstring(config['icons'][key]); icon.set('x',str(x+8));icon.set('y',str(y+6));icon.set('width','14');icon.set('height','14'); icon.set('fill',brand_color);icon.set('color',brand_color)
   for node in icon.iter():
    for attr in ['fill','stroke']:
     val=node.get(attr)
     if val and val!='none': node.set(attr,brand_color)
   parts.append(ET.tostring(icon,encoding='unicode'))
  text(x+(28 if key in config['icons'] else 10),y+17,name,'#e6edf3',10)
  x+=width+7
 assert x<880,(label,x)
parts.append('<path d="M34 588H866" stroke="#21262d"/>')
command(620,'git log --contributions')
text(35,645,'Recent Contributions','#f0f6fc',14)
text(865,645,'PAST 12 MONTHS','#8b949e',10,'text-anchor="end"')
colors={'NONE':'#161b22','FIRST_QUARTILE':'#0e4429','SECOND_QUARTILE':'#006d32','THIRD_QUARTILE':'#26a641','FOURTH_QUARTILE':'#39d353'}
for day,label in [(1,'Mon'),(3,'Wed'),(5,'Fri')]:text(34,690+day*15,label,'#8b949e',9)
lastmonth=None
for wi,week in enumerate(weeks):
 for day in week['contributionDays']:
  date=datetime.date.fromisoformat(day['date']); x=70+wi*15; y=678+day['weekday']*15
  if date.day<=7 and date.month!=lastmonth:
   text(x,668,date.strftime('%b'),'#8b949e',10);lastmonth=date.month
  color=colors[day['contributionLevel']]
  parts.append(f'<rect x="{x}" y="{y}" width="11" height="11" rx="2" fill="{color}"><title>{day["date"]}: {day["contributionCount"]} contributions</title></rect>')
text(35,808,'Updated '+datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')+' UTC','#8b949e',10)
text(700,808,'Less','#8b949e',10)
for i,color in enumerate(colors.values()):parts.append(f'<rect x="{733+i*17}" y="798" width="11" height="11" rx="2" fill="{color}"/>')
text(825,808,'More','#8b949e',10)
parts.append('</g></svg>')
svg=''.join(parts);ET.fromstring(svg)
out=root/'assets/profile.svg'
if not (root/'scripts').exists():out=Path('work/profile.svg')
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(svg)
print('Generated',len(weeks),'weeks into',out)
