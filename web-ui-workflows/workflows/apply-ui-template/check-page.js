// Browser expression: the runner supplies only trusted local rules and bindings.
// No aesthetic defaults. Each result describes one declared rule and its samples.
(input) => {
  const visible = (el) => {
    if (typeof el.checkVisibility !== 'function') throw new Error('Browser visibility API unavailable');
    return el.checkVisibility({checkOpacity: true, checkVisibilityCSS: true, contentVisibilityAuto: true})
      && [...el.getClientRects()].some(r => r.width > 0 && r.height > 0);
  };
  // Element identity without page text (text may contain personal data).
  const describe = (el) => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '')
    + [...el.classList].slice(0, 4).map((c) => '.' + c).join('');
  const ownText = (el) => [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
  // Outermost descendants that extend past the container and are not clipped by an inner scroller.
  const overflowCulprits = (box) => {
    const limit = box.getBoundingClientRect().left + box.clientWidth + 1;
    const clipped = (el) => {
      for (let p = el.parentElement; p && p !== box; p = p.parentElement)
        if (getComputedStyle(p).overflowX !== 'visible') return true;
      return false;
    };
    const wide = [...box.querySelectorAll('*')].filter((el) => el.getBoundingClientRect().right > limit && visible(el) && !clipped(el));
    return wide.filter((el) => !wide.some((o) => o !== el && o.contains(el))).slice(0, 5)
      .map((el) => ({element: describe(el), width: Math.round(el.getBoundingClientRect().width), right: Math.round(el.getBoundingClientRect().right)}));
  };
  return input.rules.map((rule) => {
    const binding = input.bindings[rule.role];
    const base = {rule: rule.id, role: rule.role, source: rule.source, samples: 0};
    const result = (status, detail, extra = {}) => ({...base, status, detail, ...extra});
    if (input.exclude[rule.id]) return result('NA', input.exclude[rule.id]);
    if (rule.kind === 'manual') return result('UNCHECKED', 'Requires reading or visual inspection: ' + rule.description);
    if (!binding) return result('UNCHECKED', 'No project binding for this role');
    try {
      if (rule.kind === 'predicate') {
        if (!binding.expression) return result('UNCHECKED', 'No project assertion adapter');
        const observed = Function('"use strict"; return (' + binding.expression + ')')();
        if (!observed || typeof observed.pass !== 'boolean' || !Number.isInteger(observed.samples) || observed.samples < 1)
          return result('UNCHECKED', 'Adapter must return {pass:boolean, samples:positive integer, detail:string}');
        return result(observed.pass ? 'PASS' : 'FAIL', String(observed.detail || ''), {samples: observed.samples});
      }
      if (!binding.selector) return result('UNCHECKED', 'No selector');
      let nodes = [...document.querySelectorAll(binding.selector)].filter(visible);
      if (binding.exclude) nodes = nodes.filter((el) => !el.closest(binding.exclude));
      if (rule.kind === 'allowed-values') {
        if (rule.own_text) nodes = nodes.filter(ownText);
        if (!nodes.length) return result('UNCHECKED', 'No rendered samples for selector');
        const allowed = new Set(rule.allowed);
        const outliers = new Map();
        for (const el of nodes) {
          const value = getComputedStyle(el).getPropertyValue(rule.property).trim();
          if (allowed.has(value)) continue;
          const entry = outliers.get(value) || {observed: value, count: 0, elements: []};
          entry.count += 1;
          if (entry.elements.length < 3) entry.elements.push(describe(el));
          outliers.set(value, entry);
        }
        const failures = [...outliers.values()].sort((a, b) => b.count - a.count);
        const off = failures.reduce((n, f) => n + f.count, 0);
        return result(off ? 'FAIL' : 'PASS', `${nodes.length - off}/${nodes.length} rendered samples use an allowed value; ${failures.length} other values`, {
          samples: nodes.length, selector: binding.selector, expected: rule.allowed, failures
        });
      }
      if (rule.kind === 'count') {
        return result(nodes.length === rule.expected ? 'PASS' : 'FAIL', `Visible count ${nodes.length}; expected ${rule.expected}`, {samples: nodes.length});
      }
      if (!nodes.length) return result('UNCHECKED', 'No rendered samples for selector');
      const values = nodes.map((el) => {
        switch (rule.kind) {
          case 'style': return getComputedStyle(el).getPropertyValue(rule.property).trim();
          case 'attribute': return el.getAttribute(rule.property);
          case 'text': return el.innerText;
          case 'no-horizontal-overflow': return el.scrollWidth <= el.clientWidth + 1;
          default: throw new Error('Unsupported check');
        }
      });
      const ok = (value) => rule.kind === 'no-horizontal-overflow' ? value === true
        : rule.kind === 'text' ? (rule.match === 'contains' ? value.includes(rule.expected) : value === rule.expected)
        : value === rule.expected;
      const failures = values.flatMap((value, index) => ok(value) ? [] : [rule.kind === 'no-horizontal-overflow'
        ? {index, observed: value, element: describe(nodes[index]), culprits: overflowCulprits(nodes[index])}
        : {index, observed: value}]);
      // Text may contain personal data: keep it out of artifacts. The assertion still uses it.
      const evidence = rule.kind === 'text' ? failures.map(({index}) => ({index})) : failures;
      return result(failures.length ? 'FAIL' : 'PASS', `${values.length - failures.length}/${values.length} rendered samples match`, {
        samples: values.length, selector: binding.selector, expected: rule.expected,
        failures: evidence, limitation: rule.kind === 'no-horizontal-overflow'
          ? 'Element scroll geometry only; excludes canvas pixels, occlusion and intentional clipping' : undefined
      });
    } catch (_) { return result('UNCHECKED', 'Selector or assertion evaluation failed'); }
  });
}
