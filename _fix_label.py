with open('index.html', 'r') as f:
    html = f.read()

old = 'html += \'<div class="dash-section-title"><i class="ri-tv-line"></i> 最近剧集</div>\';\n\t    const recent = eps.slice(-5).reverse();'
new = 'html += \'<div class="dash-section-title"><i class="ri-tv-line"></i> 当前项目</div>\';\n\t    const recent = [...eps].reverse();'

html = html.replace(old, new)

with open('index.html', 'w') as f:
    f.write(html)

print('Done')
