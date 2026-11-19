from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'public' / 'assets'
OUT.mkdir(parents=True, exist_ok=True)

PALETTES = [
    ('#e9dfca', '#233f4b', '#a44939', '#c3a36d', '#758276'),
    ('#e8e0d2', '#5c3133', '#263d49', '#b89a65', '#9a7462'),
    ('#e5e7df', '#304f47', '#a95943', '#d1b477', '#7d9181'),
    ('#eee2ce', '#263c55', '#aa4c3f', '#bd9464', '#697b8b'),
    ('#e7ded4', '#493d52', '#a4483c', '#c4a570', '#817485'),
    ('#e6e3d5', '#2e4c50', '#a65640', '#c2a26e', '#6e8c86'),
]

def art(i, name, portrait=True):
    paper, ink, red, gold, soft = PALETTES[i % len(PALETTES)]
    shift = (i % 3 - 1) * 24
    figure = ''
    if portrait:
        figure = f'''
        <g transform="translate({shift} 0)">
          <path d="M420 690 C390 554 425 443 502 401 C571 363 646 399 665 484 C683 566 659 640 696 738 L341 738 C370 715 400 710 420 690Z" fill="{ink}" opacity=".96"/>
          <path d="M465 401 C436 337 453 247 523 222 C587 199 647 244 650 310 C653 367 624 414 568 430 C520 443 484 430 465 401Z" fill="#d9b9a0"/>
          <path d="M458 337 C430 276 468 198 540 197 C617 195 663 254 650 336 C620 318 611 278 591 251 C563 291 516 315 458 337Z" fill="{ink}"/>
          <path d="M605 222 C660 250 688 315 673 393 C661 456 681 498 706 525 C639 498 608 449 622 378 C640 293 620 260 605 222Z" fill="{ink}"/>
          <path d="M470 368 C454 436 418 479 379 502 C409 444 417 378 447 324Z" fill="{ink}"/>
          <path d="M509 336 Q526 327 542 336" stroke="{ink}" stroke-width="3" fill="none"/>
          <path d="M578 334 Q594 326 608 333" stroke="{ink}" stroke-width="3" fill="none"/>
          <path d="M546 388 Q565 398 583 384" stroke="{red}" stroke-width="4" fill="none"/>
          <path d="M484 435 C520 475 581 473 622 429 L606 518 L532 556 L469 503Z" fill="#eee4d4"/>
          <path d="M492 469 L555 584 L609 468 C647 489 669 527 679 590 L627 738 L410 738 L398 578 C411 520 440 487 492 469Z" fill="{red}" opacity=".88"/>
          <path d="M555 584 L527 738 M555 584 L602 738" stroke="{gold}" stroke-width="5" opacity=".8"/>
          <path d="M467 512 Q410 560 397 665 M624 510 Q674 559 686 648" stroke="{gold}" stroke-width="3" fill="none"/>
          <circle cx="629" cy="258" r="11" fill="{gold}"/><path d="M630 266 L651 313" stroke="{gold}" stroke-width="3"/>
        </g>'''
    else:
        figure = f'''
        <path d="M80 635 Q225 412 343 578 Q470 340 602 566 Q725 424 830 637Z" fill="{soft}" opacity=".55"/>
        <path d="M55 681 Q240 471 380 646 Q512 449 688 655 Q769 559 850 684Z" fill="{ink}" opacity=".88"/>
        <path d="M60 708 Q263 566 422 700 Q607 558 839 710Z" fill="{red}" opacity=".68"/>
        <path d="M70 732 Q302 662 497 726 T850 719" stroke="{gold}" stroke-width="5" fill="none" opacity=".7"/>
        <path d="M214 243 Q254 222 294 243 M235 263 Q274 242 314 263" stroke="{ink}" stroke-width="4" fill="none"/>
        <path d="M706 330 Q731 309 757 330 M723 349 Q748 328 774 349" stroke="{ink}" stroke-width="3" fill="none"/>
        '''
    botanical = f'''
      <g stroke="{ink}" fill="none" stroke-width="3" opacity=".72">
        <path d="M100 740 Q104 498 221 352 Q274 287 294 174"/>
        <path d="M124 575 Q74 536 78 479 Q130 503 143 547 M154 476 Q204 450 226 395 Q170 404 143 445 M209 362 Q155 337 157 282 Q208 301 226 334 M250 271 Q300 249 311 207 Q267 211 241 245"/>
      </g>
      <g fill="{red}" opacity=".8"><circle cx="78" cy="478" r="14"/><circle cx="226" cy="394" r="12"/><circle cx="157" cy="282" r="13"/><circle cx="311" cy="207" r="11"/></g>
    '''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1100">
      <defs>
        <filter id="grain"><feTurbulence baseFrequency=".65" numOctaves="3" stitchTiles="stitch"/><feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 .09 0"/></filter>
        <radialGradient id="wash"><stop stop-color="{gold}" stop-opacity=".55"/><stop offset="1" stop-color="{paper}" stop-opacity="0"/></radialGradient>
        <linearGradient id="bg" x2="1" y2="1"><stop stop-color="{paper}"/><stop offset="1" stop-color="#f8f4eb"/></linearGradient>
      </defs>
      <rect width="900" height="1100" fill="url(#bg)"/>
      <circle cx="{680 - i*18}" cy="{220 + i*10}" r="168" fill="url(#wash)"/>
      <circle cx="{680 - i*18}" cy="{220 + i*10}" r="101" fill="{red}" opacity=".12"/>
      <path d="M0 810 Q230 690 405 804 T900 774 V1100 H0Z" fill="{soft}" opacity=".13"/>
      {botanical if i%2==0 else ''}{figure}
      <g opacity=".12" stroke="{ink}"><path d="M40 60 H210 M40 75 H155"/><path d="M690 1020 H860 M746 1035 H860"/></g>
      <rect width="900" height="1100" filter="url(#grain)" opacity=".7"/>
      <g transform="translate(735 820)"><rect width="90" height="90" rx="3" fill="{red}"/><text x="45" y="38" text-anchor="middle" fill="#f6ead8" font-size="29" font-family="serif">镜绘</text><text x="45" y="69" text-anchor="middle" fill="#f6ead8" font-size="18" font-family="serif">珍藏</text></g>
      <text x="72" y="105" fill="{ink}" font-size="20" letter-spacing="8" font-family="serif">JINGHUI · {name}</text>
    </svg>'''
    return svg

names = ['月下仕女', '朱砂旧梦', '青山如故', '青花映照', '敦煌遗韵', '松间清影', '云水谣', '东方意象']
for i, name in enumerate(names):
    (OUT / f'art-{i+1}.svg').write_text(art(i, name, portrait=i < 6), encoding='utf-8')

# AI / hand-painted comparison pair: same composition with different texture treatment.
(OUT / 'compare-ai.svg').write_text(art(3, 'AI 定稿', True), encoding='utf-8')
(OUT / 'compare-hand.svg').write_text(art(1, '画师亲绘', True).replace('opacity=".7"', 'opacity="1"'), encoding='utf-8')

products = [
    ('scroll', '宣纸卷轴', '#a94b3c'), ('fan', '团扇扇面', '#2e4858'),
    ('porcelain', '釉下瓷板', '#637b80'), ('canvas', '油画布框', '#8c5c4a'),
    ('screen', '双面绣屏', '#6b765b'), ('gift', '定制礼盒', '#9a7747')
]
for slug, title, color in products:
    if slug == 'fan':
        shape = '<circle cx="300" cy="260" r="175" fill="#eee5d2" stroke="#b59461" stroke-width="10"/><path d="M300 435 V555" stroke="#7a5138" stroke-width="24"/><path d="M300 435 V555" stroke="#c29c67" stroke-width="7"/>'
    elif slug == 'porcelain':
        shape = '<rect x="150" y="70" width="300" height="420" rx="150" fill="#edf0ea" stroke="#b8c5c0" stroke-width="8"/><path d="M175 430 Q300 340 425 430" stroke="#2e4858" stroke-width="7" fill="none"/>'
    elif slug == 'canvas':
        shape = '<rect x="120" y="75" width="360" height="440" fill="#eee2cd" stroke="#8a674e" stroke-width="24"/><rect x="145" y="100" width="310" height="390" fill="none" stroke="#b59461" stroke-width="2"/>'
    elif slug == 'screen':
        shape = '<rect x="95" y="105" width="410" height="345" rx="190" fill="#eee5d2" stroke="#6e4f3a" stroke-width="16"/><path d="M150 440 L120 530 M450 440 L480 530" stroke="#6e4f3a" stroke-width="20"/>'
    elif slug == 'gift':
        shape = '<rect x="110" y="180" width="380" height="300" rx="12" fill="#b69661"/><rect x="95" y="140" width="410" height="80" rx="8" fill="#c5aa7a"/><path d="M300 140 V480" stroke="#8e3f35" stroke-width="34"/><circle cx="300" cy="310" r="55" fill="#a94b3c"/>'
    else:
        shape = '<rect x="160" y="65" width="280" height="430" fill="#eee5d2" stroke="#b59461" stroke-width="3"/><path d="M130 65 H470 M130 495 H470" stroke="#74503b" stroke-width="25"/><path d="M130 50 V80 M470 50 V80 M130 480 V510 M470 480 V510" stroke="#b59461" stroke-width="10"/>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 650"><rect width="600" height="650" fill="#f2ecdf"/><circle cx="300" cy="280" r="210" fill="{color}" opacity=".06"/>{shape}<g transform="translate(300 275)"><circle r="95" fill="{color}" opacity=".15"/><path d="M-80 55 Q-20 -70 20 30 Q60 -45 90 60" fill="{color}" opacity=".8"/><circle cx="42" cy="-62" r="32" fill="{color}" opacity=".3"/></g><text x="300" y="595" text-anchor="middle" font-family="serif" font-size="25" letter-spacing="8" fill="#2e3532">{title}</text></svg>'''
    (OUT / f'product-{slug}.svg').write_text(svg, encoding='utf-8')

# Brand mark and subtle cloud ornament.
(OUT.parent / 'favicon.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect x="4" y="4" width="56" height="56" rx="7" fill="#a94b3c"/><rect x="9" y="9" width="46" height="46" rx="3" fill="none" stroke="#f6f2e9" stroke-width="1.5"/><text x="32" y="45" text-anchor="middle" font-family="serif" font-weight="700" font-size="38" fill="#f6f2e9">镜</text></svg>''', encoding='utf-8')
print(f'Generated {len(list(OUT.glob("*.svg")))} SVG assets in {OUT}')
