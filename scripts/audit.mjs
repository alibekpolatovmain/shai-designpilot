/* Браузерный аудит страницы. Вставить содержимое в javascript_tool на
   открытой странице; вернёт отчёт объектом.

   Проверено на живых дефектах — и на ложных срабатываниях, которых у первой
   версии было больше, чем находок:

   · Tailwind отдаёт полупрозрачный фон как `oklab(L a b / alpha)`. Наивный
     разбор брал первые три числа за RGB и объявлял чёрным белый фон: экран
     показывал нарушения там, где их нет.
   · Прозрачность нужно смешивать со слоями под ней, иначе линия из белого
     10% считается чистым белым и даёт 17:1 вместо 1.34:1.
   · Растянутая ссылка (`after:inset-0`) меряется по своему боксу, а не по
     области нажатия: её высота 20px — не дефект, и она помечается отдельно.

   Ничего не чинит. Только считает. */
(() => {
  const S = getComputedStyle

  /* ── цвет ─────────────────────────────────────────────── */
  const lin = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4 }
  const L = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
  const ratio = (a, b) => { const [x, y] = [L(a), L(b)].sort((m, n) => n - m); return (x + 0.05) / (y + 0.05) }

  const okl = (Lv, A, B) => {
    const l = (Lv + 0.3963377774 * A + 0.2158037573 * B) ** 3
    const m = (Lv - 0.1055613458 * A - 0.0638541728 * B) ** 3
    const s = (Lv - 0.0894841775 * A - 1.2914855480 * B) ** 3
    const f = (x) => { const c = x <= 0.0031308 ? 12.92 * x : 1.055 * Math.pow(Math.max(x, 0), 1 / 2.4) - 0.055
      return Math.max(0, Math.min(255, Math.round(c * 255))) }
    return [f(4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s),
            f(-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s),
            f(-0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)]
  }
  const parse = (v) => {
    const n = (v.match(/-?[\d.]+(?:e-?\d+)?/g) || []).map(Number)
    if (!n.length) return null
    if (v.startsWith('oklab')) return { rgb: okl(n[0], n[1], n[2]), a: n.length > 3 ? n[3] : 1 }
    const srgb = v.includes('color(srgb')
    return { rgb: n.slice(0, 3).map((x) => (srgb ? x * 255 : x)), a: n.length > 3 ? n[3] : 1 }
  }
  const over = (t, b) => { const a = t.a + b.a * (1 - t.a)
    return { rgb: t.rgb.map((v, i) => (v * t.a + b.rgb[i] * b.a * (1 - t.a)) / (a || 1)), a } }
  /* Градиент под текстом измерить нельзя: у фона там не цвет, а протяжённость.
     Первая версия шла мимо него к белому и выдавала 1.00 на белом тексте по
     тёмно-зелёному — то есть кричала о нарушении там, где его нет. Теперь
     такой случай возвращает null и попадает в «не измерено», а не в находки:
     ложная тревога стоит доверия ко всему отчёту. */
  const bgOf = (el) => { let n = el, acc = null
    while (n) { const c = S(n)
      if (c.backgroundImage && c.backgroundImage.includes('gradient')) return null
      const b = parse(c.backgroundColor)
      if (b && b.a > 0) { acc = acc ? over(acc, b) : b; if (acc.a >= 0.999) return acc.rgb }
      n = n.parentElement }
    const page = parse(S(document.body).backgroundColor) || { rgb: [255, 255, 255], a: 1 }
    return acc ? over(acc, page).rgb : page.rgb
  }

  /* ── сбор ─────────────────────────────────────────────── */
  const out = { контраст: [], наГрадиенте: [], безымянные: [], мелкиеЦели: [], растянутые: [],
                поля: [], картинки: [], заголовки: [], вкладки: [], итог: {} }
  const seen = new Set()
  const nameOf = (el) => (el.innerText || '').trim() || el.getAttribute('aria-label') ||
    el.getAttribute('title') || (el.getAttribute('aria-labelledby') &&
      (document.getElementById(el.getAttribute('aria-labelledby'))?.innerText || '').trim()) || ''

  document.querySelectorAll('body *').forEach((el) => {
    const cs = S(el)
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return
    const r = el.getBoundingClientRect()
    if (!r.width || !r.height) return

    const own = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim())
      .map((n) => n.textContent.trim()).join(' ')
    if (own) {
      const fg = parse(cs.color); const bg = bgOf(el)
      if (fg && !bg) out.наГрадиенте.push(`«${own.slice(0, 40)}» — измерить нельзя, под текстом градиент`)
      if (fg && bg) {
        const mix = fg.a < 1 ? fg.rgb.map((v, i) => v * fg.a + bg[i] * (1 - fg.a)) : fg.rgb
        const size = parseFloat(cs.fontSize)
        const need = size >= 24 || (size >= 18.66 && +cs.fontWeight >= 700) ? 3 : 4.5
        const got = ratio(mix, bg)
        const key = own.slice(0, 24) + got.toFixed(2)
        if (got < need && !seen.has(key)) { seen.add(key)
          out.контраст.push(`${got.toFixed(2)} < ${need} — «${own.slice(0, 48)}»`) }
      }
    }

    const role = el.getAttribute('role')
    const clickable = ['BUTTON', 'A', 'SUMMARY'].includes(el.tagName) ||
      ['button', 'link', 'checkbox', 'menuitem', 'tab', 'switch', 'radio', 'option'].includes(role)
    if (clickable) {
      const name = nameOf(el)
      if (!name) out.безымянные.push(`${el.tagName}${role ? `[${role}]` : ''} .${(el.className || '').toString().slice(0, 40)}`)
      /* растянутая ссылка накрывает всю строку — её бокс меньше цели */
      const stretched = [...el.querySelectorAll('*')].length === 0 &&
        (cs.getPropertyValue('--tw-content') || '').length === 0 && el.matches('a') &&
        S(el, '::after').position === 'absolute'
      if (r.width < 24 || r.height < 24) {
        (stretched ? out.растянутые : out.мелкиеЦели).push(`${Math.round(r.width)}×${Math.round(r.height)} ${name.slice(0, 28)}`)
      }
    }

    if (el.tagName === 'IMG' && el.getAttribute('alt') === null) out.картинки.push((el.getAttribute('src') || '').slice(0, 48))
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(el.tagName) && el.type !== 'hidden') {
      const named = el.getAttribute('aria-label') || el.getAttribute('aria-labelledby') ||
        (el.id && document.querySelector(`label[for="${CSS.escape(el.id)}"]`)) || el.closest('label')
      if (!named) out.поля.push(el.getAttribute('placeholder') || el.name || el.type)
    }
  })

  /* вкладка без панели — самый частый обман разметки */
  document.querySelectorAll('[role=tab]').forEach((t) => {
    const id = t.getAttribute('aria-controls')
    if (!id || !document.getElementById(id)) out.вкладки.push(`«${nameOf(t).slice(0, 24)}» без панели`)
  })

  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map((h) => +h.tagName[1])
  hs.forEach((lvl, i) => { if (i && lvl > hs[i - 1] + 1) out.заголовки.push(`h${hs[i - 1]} → h${lvl}`) })
  if (document.querySelectorAll('h1').length !== 1) out.заголовки.push(`h1 на странице: ${document.querySelectorAll('h1').length}`)

  out.итог = {
    адрес: location.pathname,
    тема: document.documentElement.dataset.theme || 'как в системе',
    нарушений: out.контраст.length + out.безымянные.length + out.мелкиеЦели.length +
      out.поля.length + out.картинки.length + out.заголовки.length + out.вкладки.length,
  }
  Object.keys(out).forEach((k) => { if (Array.isArray(out[k]) && !out[k].length) delete out[k] })
  return JSON.stringify(out, null, 1)
})()
