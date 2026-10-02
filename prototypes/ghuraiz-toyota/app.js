(() => {
  document.documentElement.classList.add('js');
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const rtl = () => document.documentElement.dir === 'rtl';

  /* ---------- translations ---------- */
  const T = {
    ar: {
      title:"تويوتا الغريز | مركز صيانة وقطع غيار", btn:"EN",
      brand:"تويوتا الغريز", brand_sub:"مركز صيانة وقطع غيار",
      nav_services:"الخدمات", nav_process:"كيف نعمل", nav_why:"لماذا نحن", nav_contact:"تواصل معنا", nav_book:"احجز موعد",
      intro_name:'تويوتا الغريز', intro_tag:"مركز صيانة وقطع غيار", skip:"تخطي ›",
      hero_kicker:"متخصصون في تويوتا", hero_t1:"عناية تليق", hero_t2:"بسيارتك",
      hero_sub:"صيانة دورية، ميكانيكا وكهرباء، سمكرة ودهان، وقطع غيار — بأيدي فنيين متخصصين في سيارات تويوتا.",
      hero_cta1:"احجز موعد الآن", hero_cta2:"استعرض الخدمات", hint:"اسحب لتدوير السيارة",
      st1:"سنة خبرة", st2:"سيارة تمت صيانتها", st3:"أقسام متخصصة", st4:"عملاء راضون",
      svc_kicker:"خدماتنا", svc_title:"كل ما تحتاجه سيارتك في مكان واحد", svc_sub:"من الصيانة الدورية إلى الإصلاحات الدقيقة، نتعامل مع كل التفاصيل بخبرة وشفافية.",
      s1t:"صيانة دورية", s1d:"تغيير زيوت وفلاتر وفحص شامل حسب جدول الصيانة الرسمي لكل موديل.",
      s2t:"ميكانيكا ومحركات", s2d:"تشخيص وإصلاح المحرك والجيربوكس وناقل الحركة بأحدث الأدوات.",
      s3t:"كهرباء وكمبيوتر", s3d:"فحص بالكمبيوتر وإصلاح الأعطال الكهربائية وأنظمة الإضاءة والتكييف.",
      s4t:"سمكرة ودهان", s4d:"إصلاح الحوادث ودهان بالفرن بمطابقة دقيقة للون الأصلي.",
      s5t:"فرامل وتعليق", s5d:"فحص وتغيير الفرامل والمساعدين والمقصات لقيادة آمنة ومريحة.",
      s6t:"قطع غيار", s6d:"قطع أصلية وبديلة عالية الجودة لكل موديلات تويوتا مع ضمان.",
      pr_kicker:"رحلة سيارتك معنا", pr_title:"من الاستقبال إلى التسليم",
      p1t:"استقبال وفحص", p1d:"نستمع لمشكلتك ونفحص السيارة بالكمبيوتر.",
      p2t:"تقدير واضح", p2d:"تكلفة ومدة محددتان قبل أي عمل — بلا مفاجآت.",
      p3t:"إصلاح متقن", p3d:"فنيون متخصصون وقطع مضمونة.",
      p4t:"تسليم وضمان", p4d:"اختبار قيادة نهائي وضمان على الشغل.",
      why_kicker:"لماذا الغريز؟", why_title:"خبرة تويوتا في كل تفصيلة", why_badge:"سنة من الثقة",
      w1t:"ضمان على الشغل", w1d:"نضمن الإصلاح وقطع الغيار المستبدلة.",
      w2t:"فنيون متخصصون", w2d:"فريق يعمل على تويوتا فقط منذ سنوات.",
      w3t:"أسعار شفافة", w3d:"تقدير مكتوب قبل البدء، بدون بنود مخفية.",
      w4t:"التزام بالمواعيد", w4d:"نحترم وقتك ونسلّم السيارة في الموعد.",
      t_kicker:"آراء العملاء", t_title:"عملاؤنا يتكلمون",
      q1:"شغل نضيف وأمانة في التعامل. السيارة رجعت زي الجديدة.", a1:"أحمد س.", a1i:"أ", a1c:"لاند كروزر",
      q2:"حددوا العطل بسرعة وبسعر واضح من أول مرة.", a2:"محمود ع.", a2i:"م", a2c:"فورتشنر",
      q3:"سمكرة ودهان بمستوى الوكالة وبدون تأخير.", a3:"كريم ه.", a3i:"ك", a3c:"كورولا",
      b_kicker:"احجز الآن", b_title:"احجز موعد صيانة", b_sub:"اترك بياناتك وسنتواصل معك لتأكيد الموعد.",
      c_addr:"العنوان", c_addr_v:"[ العنوان هنا ]", c_phone:"الهاتف", c_hours:"مواعيد العمل", c_hours_v:"السبت – الخميس، ٩ ص – ٦ م",
      f_name:"الاسم", f_phone:"رقم الهاتف", f_car:"الموديل", f_srv:"الخدمة", f_msg:"ملاحظات", f_submit:"أرسل الطلب",
      m1:"لاند كروزر", m2:"فورتشنر", m3:"هايلكس", m4:"كورولا", m5:"كامري", m6:"يارس", m7:"أخرى",
      ok:"تم استلام طلبك ✓ سنتواصل معك قريباً", need:"من فضلك أدخل الاسم ورقم الهاتف",
      map:"مكان الخريطة — أضف Google Maps هنا", foot:"© ٢٠٢٦ تويوتا الغريز — نموذج أولي", replay:"إعادة تشغيل المقدمة"
    },
    en: {
      title:"Toyota Al-Ghuraiz | Service & Parts Center", btn:"عربي",
      brand:"Toyota Al-Ghuraiz", brand_sub:"Service & Parts Center",
      nav_services:"Services", nav_process:"How we work", nav_why:"Why us", nav_contact:"Contact", nav_book:"Book a visit",
      intro_name:'Toyota Al-Ghuraiz', intro_tag:"SERVICE & PARTS CENTER", skip:"Skip ›",
      hero_kicker:"Toyota specialists", hero_t1:"The care your", hero_t2:"Toyota deserves",
      hero_sub:"Periodic maintenance, mechanical & electrical repair, body & paint, and genuine parts — by technicians who live and breathe Toyota.",
      hero_cta1:"Book a visit now", hero_cta2:"View services", hint:"Drag to rotate the car",
      st1:"Years of experience", st2:"Cars serviced", st3:"Specialist departments", st4:"Happy customers",
      svc_kicker:"Our services", svc_title:"Everything your car needs, under one roof", svc_sub:"From routine servicing to precision repairs, we handle every detail with expertise and transparency.",
      s1t:"Periodic maintenance", s1d:"Oil, filters and a full inspection following the official schedule for your model.",
      s2t:"Engine & mechanical", s2d:"Diagnosis and repair of engines, gearboxes and drivetrains with modern tools.",
      s3t:"Electrical & diagnostics", s3d:"Computer scan and repair of electrical faults, lighting and A/C systems.",
      s4t:"Body & paint", s4d:"Collision repair and oven-baked paint with an exact colour match.",
      s5t:"Brakes & suspension", s5d:"Brakes, shocks and control arms checked or replaced for a safe, smooth ride.",
      s6t:"Spare parts", s6d:"Genuine and high-quality alternative parts for all Toyota models, warrantied.",
      pr_kicker:"Your car's journey", pr_title:"From drop-off to hand-over",
      p1t:"Reception & scan", p1d:"We listen to your concern and scan the car.",
      p2t:"Clear estimate", p2d:"Fixed cost and timing before any work — no surprises.",
      p3t:"Quality repair", p3d:"Specialist technicians and guaranteed parts.",
      p4t:"Hand-over & warranty", p4d:"Final road test and a warranty on the work.",
      why_kicker:"Why Al-Ghuraiz?", why_title:"Toyota know-how in every detail", why_badge:"years of trust",
      w1t:"Warranty on work", w1d:"Repairs and replaced parts are guaranteed.",
      w2t:"Specialist technicians", w2d:"A team that has worked on Toyotas for years.",
      w3t:"Transparent pricing", w3d:"A written estimate up front, no hidden items.",
      w4t:"On-time delivery", w4d:"We respect your time and deliver as promised.",
      t_kicker:"Testimonials", t_title:"What our customers say",
      q1:"Clean work and honest dealing. The car came back like new.", a1:"Ahmed S.", a1i:"A", a1c:"Land Cruiser",
      q2:"They found the fault fast and gave a clear price from the start.", a2:"Mahmoud A.", a2i:"M", a2c:"Fortuner",
      q3:"Dealership-level body and paint, with no delays.", a3:"Karim H.", a3i:"K", a3c:"Corolla",
      b_kicker:"Book now", b_title:"Book a service visit", b_sub:"Leave your details and we'll call to confirm your slot.",
      c_addr:"Address", c_addr_v:"[ Address here ]", c_phone:"Phone", c_hours:"Opening hours", c_hours_v:"Sat – Thu, 9 AM – 6 PM",
      f_name:"Name", f_phone:"Phone number", f_car:"Model", f_srv:"Service", f_msg:"Notes", f_submit:"Send request",
      m1:"Land Cruiser", m2:"Fortuner", m3:"Hilux", m4:"Corolla", m5:"Camry", m6:"Yaris", m7:"Other",
      ok:"Request received ✓ We'll contact you soon", need:"Please enter your name and phone number",
      map:"Map placeholder — embed Google Maps here", foot:"© 2026 Toyota Al-Ghuraiz — prototype", replay:"Replay intro"
    }
  };
  const MODELS = ['m1','m2','m3','m4','m5','m6'];
  let lang = 'ar';

  const nf = () => new Intl.NumberFormat(lang === 'ar' ? 'ar-EG' : 'en-US');
  function renderCounts(){ $$('[data-count]').forEach(el => { if (el.dataset.done) el.textContent = nf().format(+el.dataset.count); }); }

  function setLang(l){
    lang = l; const d = T[l];
    const h = document.documentElement; h.lang = l; h.dir = l === 'ar' ? 'rtl' : 'ltr';
    document.title = d.title;
    $$('[data-i18n]').forEach(el => { if (d[el.dataset.i18n] != null) el.textContent = d[el.dataset.i18n]; });
    $$('[data-i18n-html]').forEach(el => { el.innerHTML = d[el.dataset.i18nHtml]; });
    $('#lang').textContent = d.btn;
    $('#mq').innerHTML = [...MODELS, ...MODELS, ...MODELS, ...MODELS].map(k => `<span>${d[k]}</span>`).join('');
    renderCounts();
    try { localStorage.setItem('lang', l); } catch (e) {}
  }


  /* ---------- sky + clouds (photo-style) ---------- */
  const CLOUDS = [
    { l: '-4%', t: '6%',  w: 520, h: 120, o: .95, T: 120, dl: -20 },
    { l: '30%', t: '20%', w: 380, h: 90,  o: .85, T: 150, dl: -90 },
    { l: '62%', t: '4%',  w: 560, h: 130, o: .95, T: 135, dl: -60 },
    { l: '10%', t: '38%', w: 300, h: 70,  o: .7,  T: 170, dl: -120 },
    { l: '78%', t: '30%', w: 340, h: 80,  o: .8,  T: 160, dl: -30 },
  ];
  $$('[data-sky]').forEach(sky => {
    sky.innerHTML = CLOUDS.map(c => `<div class="cloud-w" style="left:${c.l};top:${c.t};--t:${c.T}s;--dl:${c.dl}s"><div class="cloud" style="width:${c.w}px;height:${c.h}px;--o:${c.o}"></div></div>`).join('');
  });

  /* ---------- 3D stages ---------- */
  const mk = (el, o) => { try { return window.LC3D ? LC3D.createStage(el, o) : null; } catch (e) { console.warn('3D unavailable', e); return null; } };
  const fitWidth = (st, meters, minH) => (w, h, aspect) => {   // distance so the car spans `meters` of frame width
    const t = Math.tan(st.cam.fov * Math.PI / 360);
    st.cam.dist = Math.max(meters / 2 / (t * aspect), minH / 2 / t);
  };

  /* ----- intro ----- */
  const intro = $('#intro');
  let introStage = null, timers = [];
  function startIntroScene() {
    if (introStage) { introStage.dispose(); introStage = null; }
    introStage = mk($('#introStage'), { fov: 30, shadow: .28, maxDt: .25 });
    if (!introStage) return;
    const st = introStage, car = st.car, T = 2.5;
    let started = false, done = false;
    const d = rtl() ? 1 : -1;                           // nose points toward the text side
    st.onResize = fitWidth(st, 7.4, 3.6);
    st.cam.target.set(0, 0.85, 0); st.cam.el = 0.1;
    car.group.rotation.y = d > 0 ? 0 : Math.PI;
    let lastX = -14 * d;
    car.group.position.x = lastX; car.lights(false);
    st.onFrame = (e) => {                                // timeline runs on rendered time, not wall-clock
      if (!started) { started = true; intro.classList.add('drive'); }
      if (e > T && !intro.classList.contains('park')) intro.classList.add('park');
      if (e > 3 && !hero) initHero();
      if (e > 4.3 && !done) { done = true; finishIntro(); }
      const p = clamp(e / T, 0, 1), ease = 1 - Math.pow(1 - p, 3);
      const x = -14 * d * (1 - ease);
      car.group.position.x = x; car.roll(Math.abs(x - lastX)); lastX = x;
      const k = Math.max(0, e - T);                     // brake nose-dip, then settle
      car.group.rotation.z = (p < 1 ? -0.035 * Math.pow(p, 6) : -0.035 * Math.exp(-k * 4) * Math.cos(k * 11)) * d;
      car.body.position.y = Math.sin(e * 22) * 0.004 * (1 - p);
      st.cam.az = d * (0.62 + e * 0.05);
      if (e > 1.5) car.lights(true);
    };
  }
  function finishIntro() {
    timers.forEach(clearTimeout); timers = [];
    initHero();
    intro.classList.add('open'); document.body.classList.remove('intro-on');
    setTimeout(() => document.body.classList.add('ready'), 250);
    setTimeout(() => { intro.style.display = 'none'; if (introStage) { introStage.dispose(); introStage = null; } }, 1100);
  }
  function playIntro() {
    timers.forEach(clearTimeout);
    intro.style.display = ''; intro.className = 'intro';
    document.body.classList.add('intro-on'); document.body.classList.remove('ready');
    window.scrollTo(0, 0);
    if (reduce) { finishIntro(); return; }
    startIntroScene();
    if (!introStage) { timers.push(setTimeout(finishIntro, 600)); return; }
    timers.push(setTimeout(finishIntro, 20000));          // safety net only
  }
  $('#skip').onclick = finishIntro;
  $('#replay').onclick = playIntro;

  /* ----- hero ----- */
  const heroEl = $('#hero'), heroBox = $('#heroStage');
  let hero = null;
  let scrollP = 0, drag = 0, dragging = false, px = 0, py = 0, spx = 0, spy = 0, lastY = scrollY;
  function alignGround(st, box, host) {
    if (!st) return;
    const f = st.groundFrac(), r = box.getBoundingClientRect(), h = host.getBoundingClientRect();
    host.style.setProperty('--gy', (r.top - h.top + f * r.height).toFixed(1) + 'px');
  }
  function initHero() {
  if (hero) return;
  hero = mk(heroBox, { fov: 26 });
  if (hero) {
    hero.cam.target.set(0, 0.95, 0); hero.car.lights(true);
    hero.onResize = (w, h, a) => { fitWidth(hero, 7.4, 3.8)(w, h, a); alignGround(hero, heroBox, heroEl); };
    hero.onFrame = (t, dt) => {
      const d = rtl() ? 1 : -1;
      if (!dragging) drag *= Math.pow(0.04, dt);
      spx += (px - spx) * Math.min(1, dt * 4); spy += (py - spy) * Math.min(1, dt * 4);
      const sway = reduce ? 0 : Math.sin(t * 0.45) * 0.09;
      hero.car.group.rotation.y = (d > 0 ? 0 : Math.PI) + d * (sway + drag + scrollP * 1.15);
      hero.cam.az = d * (0.78 - spx * 0.09);
      hero.cam.el = 0.13 + spy * 0.03;
      hero.car.body.position.y = reduce ? 0 : Math.sin(t * 2.1) * 0.004;
      hero.car.roll((scrollY - lastY) * 0.014); lastY = scrollY;
    };
    let lx = 0;
    heroBox.addEventListener('pointerdown', e => { dragging = true; lx = e.clientX; heroBox.setPointerCapture(e.pointerId); });
    heroBox.addEventListener('pointermove', e => { if (dragging) { drag = clamp(drag + (e.clientX - lx) * 0.008, -1.6, 1.6); lx = e.clientX; } });
    ['pointerup', 'pointercancel'].forEach(n => heroBox.addEventListener(n, () => { dragging = false; }));
    heroEl.addEventListener('pointermove', e => { px = (e.clientX / innerWidth - .5) * 2; py = (e.clientY / innerHeight - .5) * 2; });
  } else { $('.hint').style.display = 'none'; }
  }

  /* ----- journey (car drives as you scroll) ----- */
  const track = $('#track'), trackBox = $('#trackStage'), steps = $$('.step');
  let jr = null;
  let jp = 0, jHalf = 8.5;
  function initJourney() {
  if (jr) return;
  jr = mk(trackBox, { fov: 12, shadow: .26 });
  if (jr) {
    jr.cam.target.set(0, 1.25, 0); jr.cam.el = 0.07; jr.cam.az = 0.12;
    jr.onResize = (w, h, a) => {
      const t = Math.tan(jr.cam.fov * Math.PI / 360);
      jr.cam.dist = 8.5 / (t * a); jHalf = 8.5;
      alignGround(jr, trackBox, track);
    };
    jr.car.lights(true);
    let jx = 0;
    jr.onFrame = () => {
      const d = rtl() ? -1 : 1;                         // travel in reading direction
      const x = d * (-1 + 2 * jp) * (jHalf - 2.9);
      jr.car.group.rotation.y = d > 0 ? 0 : Math.PI;
      jr.car.group.position.x = x;
      jr.car.roll((x - jx) * d); jx = x;
    };
  }
  }
  new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { initJourney(); o.disconnect(); } }, { rootMargin: '500px' }).observe(track);

  /* ---------- reveal + counters ---------- */
  function countUp(el) {
    if (el.dataset.done) return;
    const to = +el.dataset.count, t0 = performance.now(), dur = 1600;
    const tick = now => {
      const p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = nf().format(Math.round(to * e));
      if (p < 1) requestAnimationFrame(tick); else el.dataset.done = 1;
    };
    requestAnimationFrame(tick);
  }
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add('in'); io.unobserve(e.target);
    $$('[data-count]', e.target).forEach(countUp);
    if (e.target.matches('[data-count]')) countUp(e.target);
  }), { threshold: .18 });
  $$('[data-reveal]').forEach(el => io.observe(el));

  /* ---------- scroll effects ---------- */
  const nav = $('#nav'), prog = $('.progress i');
  let ticking = false;
  function onScroll() {
    ticking = false;
    const y = scrollY, max = document.documentElement.scrollHeight - innerHeight;
    prog.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
    nav.classList.toggle('solid', y > 40);
    scrollP = clamp(y / (innerHeight * 0.9), 0, 1);
    heroBox.style.setProperty('--so', (1 - scrollP * 0.95).toFixed(3));
    if (document.body.classList.contains('ready')) heroBox.style.opacity = (1 - scrollP * 0.95).toFixed(3);
    const r = track.getBoundingClientRect(), vh = innerHeight;
    jp = clamp((vh * .9 - r.top) / (vh * .75), 0, 1);
    steps.forEach(s => s.classList.toggle('on', jp >= +s.dataset.at));
  }
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  addEventListener('resize', () => { onScroll(); alignGround(hero, heroBox, heroEl); alignGround(jr, trackBox, track); });

  /* ---------- nav / lang / form ---------- */
  $('#lang').onclick = () => setLang(lang === 'ar' ? 'en' : 'ar');
  $('#burger').onclick = () => $('#links').classList.toggle('open');
  $$('#links a').forEach(a => a.addEventListener('click', () => $('#links').classList.remove('open')));
  const toast = $('#toast');
  $('#form').addEventListener('submit', e => {
    e.preventDefault();
    const ok = $('#f_name').value.trim() && $('#f_phone').value.trim();
    toast.textContent = T[lang][ok ? 'ok' : 'need'];
    toast.classList.add('show'); setTimeout(() => toast.classList.remove('show'), 3200);
    if (ok) e.target.reset();
  });

  /* ---------- boot ---------- */
  const qs = new URLSearchParams(location.search);
  let saved = 'ar'; try { saved = localStorage.getItem('lang') || 'ar'; } catch (e) {}
  if (qs.get('lang')) saved = qs.get('lang');
  setLang(T[saved] ? saved : 'ar');
  if (qs.has('nointro')) { intro.style.display = 'none'; document.body.classList.remove('intro-on'); document.body.classList.add('ready'); initHero(); }
  else playIntro();
  onScroll();
  [300, 1200].forEach(ms => setTimeout(() => { alignGround(hero, heroBox, heroEl); alignGround(jr, trackBox, track); }, ms));
})();
