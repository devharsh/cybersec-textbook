import icons
names=list(icons.ICONS)
cols=7; s=130
rows=(len(names)+cols-1)//cols
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{cols*s}" height="{rows*(s+20)}" viewBox="0 0 {cols*s} {rows*(s+20)}">',
       '<rect width="100%" height="100%" fill="#fff"/>', icons.defs(names)]
for k,n in enumerate(names):
    x,y=(k%cols)*s,(k//cols)*(s+20)
    parts.append(f'<use href="#i-{n}" x="{x+10}" y="{y+5}" width="{s-20}" height="{s-20}"/>')
    parts.append(f'<text x="{x+s/2}" y="{y+s+8}" font-size="13" text-anchor="middle" font-family="Helvetica,Arial,sans-serif">{n}</text>')
parts.append('</svg>')
open('gallery.svg','w').write("\n".join(parts))
