// AI image library for blog articles.
//
// RULES (owner's standing instruction):
//  - Article covers are GENERATED images, never quarry photos and never
//    photos reused from the site. A quarry slab next to an article about
//    choosing material reads as a product ad, not an editorial illustration.
//  - Before generating anything, check this library: if an image already
//    fits the topic, REUSE it. Generate only when nothing fits.
//  - Every generated image is registered here, so the next article on the
//    same topic reuses instead of regenerating.
//
// SHAPE
//   slug      unique library key, used as the filename in /images/blog-ai/
//   file      path served by the site
//   scene     what is depicted, in Arabic — this is the alt text
//   prompt    the English prompt that produced it, kept so an image can be
//             regenerated or refined later with the same intent
//   topics    keywords an article is matched against when deciding reuse
//   usedBy    post slugs that currently use this image ("" = unused)
//
// Adding an image: append an entry and copy the file into
// public/images/blog-ai/<slug>.jpg — see scripts/blog_image_match.py.

export const BLOG_AI_DIR = '/images/blog-ai/';

export const BLOG_AI_IMAGES = [
  {
    slug: 'choosing-stone-countertop',
    file: '/images/blog-ai/choosing-stone-countertop.jpg',
    scene:
      'شخص يقارن بين عيّنتي حجر على طاولة معمل، إحداهما رخام والأخرى جرانيت، في مكتب تصميم داخلي',
    prompt:
      'A person comparing two stone samples on a desk in an interior design office, one marble one granite, warm daylight, professional editorial photography, shallow depth of field',
    topics: [
      'اختيار, مقارنة, رخام, جرانيت, سطح العمل, المطبخ',
    ],
    usedBy: [''],
  },
  {
    slug: 'travertine-facade-install',
    file: '/images/blog-ai/travertine-facade-install.jpg',
    scene:
      'رافعة تركّب ألواح ترافرتينو كبيرة على واجهة مبنى حديث، وعامل بمعدات سلامة، عند الغروب',
    prompt:
      'A construction crane installing large travertine facade panels on a modern building, worker in safety gear, golden hour, documentary photography',
    topics: [
      'واجهات, ترافرتينو, تركيب, خارجي, مبنى, رافعة',
    ],
    usedBy: [''],
  },
  {
    slug: 'spec-sheet-measuring',
    file: '/images/blog-ai/spec-sheet-measuring.jpg',
    scene:
      'حجار يقيس سماكة لوح حجر بكالبر رقمي على طاولة عمل مع ورقة مواصفات مطبوعة',
    prompt:
      'A stonemason using a digital caliper to measure the thickness of a stone slab on a workbench with a printed spec sheet, warm workshop light, close-up documentary photography',
    topics: [
      'مواصفات, قياس, سماكة, فحص, ورشة',
    ],
    usedBy: [''],
  },
  {
    slug: 'installation-tapping-check',
    file: '/images/blog-ai/installation-tapping-check.jpg',
    scene:
      'مركّب يطرق بلاطة أرضية كبيرة للتحقق من الفراغات، مستوى وفواصل على القاعدة',
    prompt:
      'An installer tapping a large stone floor tile checking for hollow spots, level and spacers on the subfloor, construction detail photography',
    topics: [
      'مركّب يطرق بلاطة أرضية كبيرة للتحقق من الفراغات، مستوى وفواصل على القاعدة',
    ],
    usedBy: [''],
  },
  {
    slug: 'riyadh-stone-villa',
    file: '/images/blog-ai/riyadh-stone-villa.jpg',
    scene:
      'داخل فيلا حديثة بجدران حجر جيري فاتح وإضاءة بعد الظهر الدافئة',
    prompt:
      'A modern residential villa interior with pale limestone walls and warm afternoon light, architectural interior photography, no people',
    topics: [
      'داخل فيلا حديثة بجدران حجر جيري فاتح وإضاءة بعد الظهر الدافئة',
    ],
    usedBy: [''],
  },
  {
    slug: 'basalt-facade-cladding',
    file: '/images/blog-ai/basalt-facade-cladding.jpg',
    scene:
      'تكسية جدار بازلت داكن على واجهة مبنى حديث، تفاصيل السطح المشقوق، إضاءة يومية',
    prompt:
      'A dark basalt stone wall cladding on a modern building exterior, split-face texture detail, overcast daylight, architectural close-up photography',
    topics: [
      'تكسية جدار بازلت داكن على واجهة مبنى حديث، تفاصيل السطح المشقوق، إضاءة يومية',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-care-routine',
    file: '/images/blog-ai/stone-care-routine.jpg',
    scene:
      'عامل صيانة ينظف أرضية حجر مصقولة كبيرة بممسحة ناعمة وصابون محايد',
    prompt:
      'A maintenance worker cleaning a large polished stone floor with a soft mop and neutral soap, warm interior light, documentary photography',
    topics: [
      'عامل صيانة ينظف أرضية حجر مصقولة كبيرة بممسحة ناعمة وصابون محايد',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-price-factors-medina',
    file: '/images/blog-ai/stone-price-factors-medina.jpg',
    scene:
      'مقاول ورب منزل يراجعان عرض سعر مكتوباً على مكتب مع عيّنات حجر وشريط قياس',
    prompt:
      'A contractor and a homeowner reviewing a written stone quotation on a desk with stone samples and a tape measure, warm office daylight, editorial photography',
    topics: [
      'سعر الحجر, عرض سعر رخام, مقارنة عروض, المدينة المنورة, تكلفة الحجر',
    ],
    usedBy: [''],
  },
  {
    slug: 'buying-natural-stone-checklist',
    file: '/images/blog-ai/buying-natural-stone-checklist.jpg',
    scene:
      'يد تقدم عيّنة حجر طبيعي كبيرة لعميل داخل معرض حجر في المدينة المنورة',
    prompt:
      'A shop assistant\'s hands presenting a large natural stone sample tile to a client inside a stone showroom, warm daylight from the side, editorial photography, shallow depth of field',
    topics: [
      'شراء الحجر, عيّنة رخام, معرض حجر, المدينة المنورة, سماكة الألواح',
    ],
    usedBy: [''],
  },
  {
    slug: 'calacatta-marble-guide',
    file: '/images/blog-ai/calacatta-marble-guide.jpg',
    scene:
      'لوح رخام كالاكاتا بعروق رمادية وذهبية داخل مستودع حجر مضاء، ويد تلمع السطح المصقول',
    prompt:
      'A large Calacatta marble slab with grey and gold veining standing in a bright stone warehouse, soft daylight, a hand resting on the polished surface, editorial photography',
    topics: [
      'كالاكاتا, رخام إيطالي, عروق الرخام, الرخام الأبيض, مستودع حجر',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-finishes-guide',
    file: '/images/blog-ai/stone-finishes-guide.jpg',
    scene:
      'ثلاث عيّنات حجر جنباً إلى جنب تُظهر تشطيباً مصقولاً وآخر مطفأً وثالثاً مجروشاً على طاولة ورشة',
    prompt:
      'Three stone sample tiles side by side showing polished, honed and textured finishes on a workshop table, soft daylight, editorial photography, macro detail',
    topics: [
      'تشطيبات الحجر, مصقول, مطفأ, ساندبلاست, عيّنات تشطيب',
    ],
    usedBy: [''],
  },
  {
    slug: 'medina-stone-facade-home-designs',
    file: '/images/blog-ai/medina-stone-facade-home-designs.jpg',
    scene:
      'منظر لواجهات منازل مغشاة بالحجر الطبيعي في حي سكني',
    prompt:
      'A quiet residential street with villas clad in natural stone, a different facade design per house, warm morning sunlight, wide architectural photography, no people, no text',
    topics: [
      'تصاميم واجهات, منازل, حجر طبيعي, المدينة المنورة, واجهات فلل',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-facade-annual-maintenance-cleaning',
    file: '/images/blog-ai/stone-facade-annual-maintenance-cleaning.jpg',
    scene:
      'تنظيف واجهة حجرية بفرشاة ناعمة وماء في الشمس',
    prompt:
      'A worker gently washing a natural stone facade with a soft brush and water from ground level, daylight, editorial photography, no text',
    topics: [
      'تنظيف واجهات, صيانة, حجر, فرشاة, حماية',
    ],
    usedBy: [''],
  },
  {
    slug: 'marble-kitchen-acids',
    file: '/images/blog-ai/marble-kitchen-acids.jpg',
    scene:
      'يد تمسح عصير حموض مسكوبا على سطح رخامي كريمي داخل مطبخ بإضاءة نافذة طبيعية، مع إظهار نسيج السطح ولمعته.',
    prompt:
      'Editorial photograph in a kitchen: a hand wiping spilled citrus juice from a creamy marble countertop with a soft cloth, close-up on surface texture and matte finish, natural window light, documentary style, no text or lettering.',
    topics: [
      'رخام المطبخ, تآكل الرخام, عزل الرخام, صقل الرخام, عناية يومية',
    ],
    usedBy: [''],
  },
  {
    slug: 'guest-washbasin-marble',
    file: '/images/blog-ai/guest-washbasin-marble.jpg',
    scene:
      'زاوية مغسل ضيافة ضيقة في منزل بالمدينة المنورة مع حوض رخام دائري على كونسول بسيط',
    prompt:
      'A narrow guest washbasin corner in a bright Medina home, a round marble basin on a simple console, warm side light from a window highlighting the stone veins, editorial interior photography',
    topics: [
      'مغاسل ضيافة, رخام الضيافة, حوض صغير, المدينة المنورة, تصميم داخلي',
    ],
    usedBy: [''],
  },
  {
    slug: 'granite-vs-travertine-vs-limestone-facades',
    file: '/images/blog-ai/granite-vs-travertine-vs-limestone-facades.jpg',
    scene:
      'ثلاث عيّنات حجر للواجهات معروضة تحت الشمس للمقارنة بينها',
    prompt:
      'Three large facade stone slabs leaning against a wall in a stone yard, grey granite beige travertine and pale limestone, soft daylight, editorial photography, no people, no text',
    topics: [
      'مقارنة, جرانيت, ترافرتينو, حجر جيري, واجهات, عينات',
    ],
    usedBy: [''],
  },
  {
    slug: 'sandstone-facades-cladding',
    file: '/images/blog-ai/sandstone-facades-cladding.jpg',
    scene:
      'نجار حجر يثبّت لوح حجر رملي مشطوف على واجهة فيلا بيديه ومطرقة مطاطية، وعامل آخر يفحص الاستواء بخيط، وغبار القطع في الضوء.',
    prompt:
      'Editorial scene: a mason carefully setting a rough-hewn sandstone panel onto a villa facade with a rubber mallet, a second worker checking alignment with a string line, dust from cutting visible in daylight, close-up of stone texture and shadow, no text',
    topics: [
      'واجهات حجر رملي, تثبيت الحجر, عزل الحجر, واجهات فلل, المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-facade-fixing-systems',
    file: '/images/blog-ai/stone-facade-fixing-systems.jpg',
    scene:
      'نجار حجر يركّب كلبًا من معدن مقاوم للصدأ في حافة لوح حجر جيري على سقالة، وعامل يثبت اللوح، وميزان ماء في المقدمة وغبار في ضوء النهار.',
    prompt:
      'Editorial scene: a stonemason fastening a stainless steel anchor bracket to the edge of a limestone panel on a scaffold, a helper holding the panel steady, level in the foreground, dust particles in warm daylight, close-up of the fixing detail, no text',
    topics: [
      'تثبيت الحجر, كلاليب معدنية, تركيب الواجهات, فواصل الحجر, المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-stain-removal',
    file: '/images/blog-ai/stone-stain-removal.jpg',
    scene:
      'يدان تضعان عجينة امتصاص بيضاء على بقعة زيتية داكنة في سطح رخامي داخل مطبخ بإضاءة دافئة.',
    prompt:
      'Editorial photograph: hands applying a thick off-white poultice paste on a dark oil stain on a marble countertop, plastic film at the side, close-up of working hands in warm kitchen light, documentary style, no text or lettering.',
    topics: [
      'تنظيف الرخام, بقع زيتية, ضمادة امتصاص, عزل الرخام, صقل الرخام',
    ],
    usedBy: [''],
  },
  {
    slug: 'hotel-stone-sinks-medina',
    file: '/images/blog-ai/hotel-stone-sinks-medina.jpg',
    scene:
      'فريق صيانة يفحص صفاً من المغاسل الحجرية في حمام فندق قيد التأثيث بالمدينة المنورة',
    prompt:
      'A maintenance team inspecting a row of stone washbasins in a hotel bathroom under renovation in Medina, tools on a towel, daylight from an open window, editorial photography',
    topics: [
      'مغاسل فنادق, رخام المدينة المنورة, صيانة المغاسل, حوض فندقي, توريد حجر',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-facade-cost-factors',
    file: '/images/blog-ai/stone-facade-cost-factors.jpg',
    scene:
      'مهندس ومقاول يراجعان نماذج حجر لواجهة على طاولة في مكتب موقع بناء بالمدينة المنورة، مع مقياس سماكة ومخطط واجهة على الطاولة، وضوء النهار من النافذة.',
    prompt:
      'Editorial scene: an architect and a contractor reviewing stone cladding samples on a table at a construction site office, calipers and a thickness gauge beside the samples, drawing of a facade elevation on the table, daylight through a window, no text',
    topics: [
      'تكلفة واجهات الحجر, سماكة الحجر, قطع الحجر, ميزانية الواجهة, المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 'natural-marble-washbasins',
    file: '/images/blog-ai/natural-marble-washbasins.jpg',
    scene:
      'يد نحّات حجر تلمّع الجزء الداخلي لمغسل رخام دائري في ورشة عمل مع ضوء جانبي',
    prompt:
      'A stonemason\'s hands polishing the interior of a round natural marble vessel sink in a workshop, water flowing over the stone, side daylight through a window, editorial photography, shallow depth of field',
    topics: [
      'مغاسل رخام',
      'أحواض حمام',
      'تشطيب الحجر',
      'المدينة المنورة',
      'ورشة حجر',
      'سماكة الألواح',
    ],
    usedBy: [''],
  },
  {
    slug: 'facade-slab-thickness-20-30-50mm',
    file: '/images/blog-ai/facade-slab-thickness-20-30-50mm.jpg',
    scene:
      'قياس سماكة لوح حجر بفركار على طاولة عمل قبل تجهيز واجهة',
    prompt:
      'Three natural stone wall panels of different thicknesses standing side by side in a stone workshop, a caliper measuring the panel edge, diffused daylight, editorial photography, no text',
    topics: [
      'سماكة ألواح',
      'قياس',
      'واجهات',
      'حجر',
      'مصنع',
    ],
    usedBy: [''],
  },
  {
    slug: 'villa-facades-medina',
    file: '/images/blog-ai/villa-facades-medina.jpg',
    scene:
      'مهندس على سقالة منخفضة يراجع واجهة فيلا مكتملة في المدينة المنورة مكسوة بحجر طبيعي متعدد الدرجات، يشرح بيده استواء الصفوف وعامل يحمل ميزان ماء على الحائط.',
    prompt:
      'Editorial scene: an architect standing on a low scaffold reviewing the facade of a completed Medina villa clad in mixed-tone natural stone, gesturing to the stone course alignment while a worker holds a level against the wall, late afternoon light, no text',
    topics: [
      'واجهات منازل',
      'المدينة المنورة',
      'حجر طبيعي',
      'تصميم واجهات',
      'تشطيب خارجي',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-facades-complete-selection-guide',
    file: '/images/blog-ai/stone-facades-complete-selection-guide.jpg',
    scene:
      'واجهة فيلا حديثة مغشاة بألواح ترافرتينو فاتحة تحت شمس المدينة المنورة',
    prompt:
      'Modern villa facade clad in large light beige travertine stone panels, bright direct sunlight, clear joints between stone slabs, architectural editorial photography',
    topics: [
      'واجهات حجر',
      'ترافرتينو',
      'فيلا',
      'المدينة المنورة',
      'تصميم واجهات',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-vessel-sinks',
    file: '/images/blog-ai/stone-vessel-sinks.jpg',
    scene:
      'مصمم يثبّت حوضاً حجرياً فوق سطح طاولة في معرض حجر مضاء بالمدينة المنورة',
    prompt:
      'A designer gently lowering a heavy natural stone vessel sink onto a bathroom counter in a bright stone showroom, hands steadying the basin, morning sunlight from the side, editorial photography',
    topics: [
      'أحواض حمام',
      'مغاسل حجر',
      'رخام الحمام',
      'المدينة المنورة',
      'تصميم حمام',
      'تشطيب الحجر',
    ],
    usedBy: [''],
  },
  {
    slug: 'granite-exterior-facades',
    file: '/images/blog-ai/granite-exterior-facades.jpg',
    scene:
      'عاملان يثبّتان ألواح جرانيت داكنة على واجهة فيلا حديثة بالمدينة المنورة، مع ضبط كلب معدني بميزان ماء وإضاءة عصر دافئة.',
    prompt:
      'Editorial scene: two workers in workwear installing large dark granite cladding panels on a modern villa exterior wall in Medina, adjusting a stainless steel angle bracket with a spirit level, warm afternoon daylight, construction dust in the air, close-up facade detail, no text',
    topics: [
      'واجهات جرانيت',
      'تثبيت الألواح',
      'واجهات فلل',
      'جرانيت مطفأ',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 'marble-basins-buying-guide',
    file: '/images/blog-ai/marble-basins-buying-guide.jpg',
    scene:
      'يد تختار بين مغسلتي رخام في معرض حجر بإضاءة نهارية دافئة',
    prompt:
      'A customer\'s hands choosing between two marble vessel sinks in a stone showroom, warm daylight, editorial photography',
    topics: [
      'مغاسل حجر',
      'أحواض حمام',
      'رخام',
      'المدينة المنورة',
      'الحمامات',
    ],
    usedBy: [''],
  },
  {
    slug: 'travertine-facades-design-installation-maintenance',
    file: '/images/blog-ai/travertine-facades-design-installation-maintenance.jpg',
    scene:
      'تفصيل قريب لألواح ترافرتينو مثبتة على واجهة مبنى تحت شمس المدينة المنورة',
    prompt:
      'A close view of a travertine stone facade on a modern house, warm beige tones, sunlight casting soft shadows on the stone texture, architectural photography, no people, no text',
    topics: [
      'واجهات ترافرتينو',
      'تركيب',
      'مدن',
      'حجر طبيعي',
      'فواصل',
    ],
    usedBy: [''],
  },
  {
    slug: 'granite-kitchen-countertops',
    file: '/images/blog-ai/granite-kitchen-countertops.jpg',
    scene:
      'يدان تقيسان سماكة لوح جرانيت رمادي داكن لسطح مطبخ باستخدام فراقة رقمية في ورشة إضاءتها دافئة.',
    prompt:
      'Editorial photograph inside a stone fabrication workshop: two pairs of hands measuring the thickness of a dark grey granite kitchen countertop slab with a digital caliper, slab resting on wooden trestles, warm workshop lighting, shallow depth of field, documentary style, no text or lettering.',
    topics: [
      'أسطح عمل الجرانيت',
      'مطابخ الحجر',
      'سماكة اللوح',
      'ورشة قص الحجر',
      'أسطح مطبخ',
    ],
    usedBy: [''],
  },
  {
    slug: 'interior-stone-floors',
    file: '/images/blog-ai/interior-stone-floors.jpg',
    scene:
      'يدان بقفازات تثبتان بلاطة ترافرتينو كبيرة في ملاط لاصق فوق قاعدة إسمنتية باستخدام مجرفة مسنونة ومسافات بلاستيكية.',
    prompt:
      'Editorial photograph: gloved hands setting a large travertine floor tile into fresh mortar on a concrete slab, notched trowel and plastic spacers beside the tile, low working light in a quiet interior space, documentary detail shot, sharp focus, high detail, professional photography, crisp, clear.',
    topics: [
      'أرضيات الحجر',
      'تركيب البلاط',
      'تثبيت الحجر',
      'فواصل الأرضيات',
      'عزل الرطوبة',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-facade-waterproofing',
    file: '/images/blog-ai/stone-facade-waterproofing.jpg',
    scene:
      'عامل يرش عازلًا شفافًا على صف من الحجر الجيري في واجهة حديثة، وشمس تنعكس على سطح الحجر الرطب، وعامل آخر يفحص قاعدة الواجهة بأداة تسوية.',
    prompt:
      'Editorial scene: a worker applying a transparent stone sealer with a low-pressure sprayer across a freshly installed limestone facade course, sunlight reflecting off the wet stone surface, second worker inspecting the base course with a trowel, no text',
    topics: [
      'عزل الحجر',
      'عزل مائي',
      'معالجة الواجهات',
      'أملاح بيضاء',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 'surface-vs-undermount-basins',
    file: '/images/blog-ai/surface-vs-undermount-basins.jpg',
    scene:
      'طاولة حمام بمغسلة مدمجة بجانب عيّنة مغسى سطحية أثناء المقارنة',
    prompt:
      'A bathroom counter with an undermount stone basin next to a vessel sink sample, a designer comparing the two, editorial photography',
    topics: [
      'مغاسل حجر',
      'أحواض حمام',
      'رخام',
      'المدينة المنورة',
      'الحمامات',
    ],
    usedBy: [''],
  },
  {
    slug: 'facade-fixing-clips-mortar-joints',
    file: '/images/blog-ai/facade-fixing-clips-mortar-joints.jpg',
    scene:
      'تثبيت قضبان معدنية وتعليق لوح حجر بالكلالات على واجهة مبنى',
    prompt:
      'A construction worker installing a vertical stainless steel fixing bar on a building facade wall, then hanging a beige travertine stone cladding panel with metal fixing clips, light scaffolding, natural daylight, documentary photography',
    topics: [
      'كلاليس',
      'تثبيت',
      'واجهات',
      'قضبان',
      'تركيب حجر',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-scratch-repair',
    file: '/images/blog-ai/stone-scratch-repair.jpg',
    scene:
      'يدان تعملان في ترميم الحجر تصقلان لوحا رخاميا بآلة صقل كهربائية مع رش ماء داخل فراغ داخلي مضاء.',
    prompt:
      'Editorial photograph: a stone restorer\'s hands polishing a marble floor slab with an electric polishing machine and water spray in a bright interior space, protective gloves, close-up documentary style, no text or lettering.',
    topics: [
      'ترميم الحجر',
      'صقل الرخام',
      'خدوش الرخام',
      'حشو الحجر',
      'عزل بعد الصقل',
    ],
    usedBy: [''],
  },
  {
    slug: 'madinah-stone-installation',
    file: '/images/blog-ai/madinah-stone-installation.jpg',
    scene:
      'عمالة ماهرة تركّب ألواح حجر جيري طبيعي بلون بيج/كريمي على واجهة مبنى حديث في المدينة المنورة',
    prompt:
      'Professional construction photograph: skilled stone masons installing natural beige/cream limestone cladding tiles on a modern building exterior wall in Madinah, Saudi Arabia, trowel and level, visible stone veining, bright daylight, precise grout lines, workers in white uniforms and hard hats, authentic construction site, 4k photo style',
    topics: [
      'تركيب حجر',
      'المدينة المنورة',
      'واجهات',
      'حجر جيري',
      'ديارنا الحديثة',
    ],
    usedBy: [''],
  },
  {
    slug: 's1-2026-10-21-stone-crema-marfil-classic',
    file: '/images/blog-ai/s1-2026-10-21-stone-crema-marfil-classic.jpg',
    scene:
      'رخام كريما مارفيل كلاسيك مصقول بسطح كريمي مصفر وعروق طبيعية خفيفة',
    prompt:
      'Crema Marfil Classic Marble slab, polished cream beige surface with subtle natural veining, professional architectural photography, soft daylight, high detail',
    topics: [
      'رخام',
      'حجر طبيعي',
      'كريما مارفيل',
      'واجهات',
      'أرضيات',
    ],
    usedBy: [''],
  },
  {
    slug: 's2-2026-10-21-equip-01',
    file: '/images/blog-ai/s2-2026-10-21-equip-01.jpg',
    scene:
      'رافعة شوكية صفراء ترفع منصة داخل مستودع',
    prompt:
      'A yellow forklift truck inside a warehouse aisle lifting a pallet, professional industrial photography, real logistics warehouse, warm daylight, high detail',
    topics: [
      'رافعة شوكية',
      'معدات ثقيلة',
      'مستودع',
      'تأجير معدات',
    ],
    usedBy: [''],
  },
  {
    slug: 's3-2026-10-21-stone-bianco-carrara-marble',
    file: '/images/blog-ai/s3-2026-10-21-stone-bianco-carrara-marble.jpg',
    scene:
      'مشهد تصويري لواجهة فيلا بكسل رخام بيانكو كرارة قبل وبعد التجديد بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Bianco Carrara Marble villa facade cladding, before and after comparison of a building exterior, worn plain concrete wall transforming into an elegant white marble-clad facade, professional architectural photography, soft daylight, high detail',
    topics: [
      'رخام_بيانكو_كرارة',
      'واجهات_حجرية',
      'واجهات_رخام',
      'حجر_طبيعي',
      'تشطيب_واجهات',
    ],
    usedBy: [''],
  },
  {
    slug: 's1-2026-10-22-stone-arabescato-marble',
    file: '/images/blog-ai/s1-2026-10-22-stone-arabescato-marble.jpg',
    scene:
      'مشهد تصويري لـرخام أرابيسكاتو بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Arabescato Marble marble, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'رخام',
      'أرابيسكاتو',
      'واجهات',
      'أرضيات',
      'حجر طبيعي',
      'مصقول',
    ],
    usedBy: [''],
  },
  {
    slug: 'basin-materials-carrara-travertine',
    file: '/images/blog-ai/basin-materials-carrara-travertine.jpg',
    scene:
      'أربع عيّنات مغاسل من خامات مختلفة: رخام كرارة وترافرتينو وجرانيت وحجر جيري',
    prompt:
      'Four stone basin samples of different materials, Carrara marble travertine granite and limestone, arranged on a table, editorial photography',
    topics: [
      'مغاسل حجر',
      'أحواض حمام',
      'رخام',
      'المدينة المنورة',
      'الحمامات',
    ],
    usedBy: [''],
  },
  {
    slug: 's2-2026-10-22-equip-03',
    file: '/images/blog-ai/s2-2026-10-22-equip-03.jpg',
    scene:
      'مشهد تصويري لـمان لفت في موقع عمل بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'A heavy forklift moving an industrial machine in a port, professional industrial photography, real construction site, warm daylight, dust in the air, sharp focus, high detail, no text, no watermark',
    topics: [
      'مان لفت',
      'heavy forklift',
      'معدات ثقيلة',
      'موقع عمل',
      'port',
      'construction site',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-facade-cost-per-meter',
    file: '/images/blog-ai/stone-facade-cost-per-meter.jpg',
    scene:
      'مخطط واجهة وعيّنتا حجر على طاولة عمل قبل تسعير المشروع',
    prompt:
      'An architect and a homeowner reviewing natural stone facade samples and a printed building elevation drawing on a site office desk, calculator, pencil, two cut stone sample blocks, warm daylight from a window, editorial documentary photography, no text',
    topics: [
      'تكلفة',
      'عرض سعر',
      'واجهات حجر',
      'عينات',
      'مقاسات',
    ],
    usedBy: [''],
  },
  {
    slug: 's3-2026-10-22-stone-giallo-siena-marble',
    file: '/images/blog-ai/s3-2026-10-22-stone-giallo-siena-marble.jpg',
    scene:
      'واجهة مبنى تجاري قبل وبعد التجديد بكسوة رخام جيلو سيينا الذهبي - ديارنا الحديثة',
    prompt:
      'Modern commercial building exterior facade after renovation, newly clad in polished Giallo Siena yellow-gold Italian marble slabs with crisp clean joints, bright daylight, completed premium project',
    topics: [
      'رخام جيلو سيينا',
      'واجهات حجرية',
      'كسوة رخام',
      'تجديد واجهات',
      'رخام أصفر',
      'ديارنا الحديثة',
      'حجر طبيعي',
      'تشطيب مباني',
    ],
    usedBy: [''],
  },
  {
    slug: 's3-2026-10-22-stone-giallo-siena-ig',
    file: '/images/blog-ai/s3-2026-10-22-stone-giallo-siena-ig.jpg',
    scene:
      'واجهة مبنى تجاري قبل وبعد التجديد بكسوة رخام جيلو سيينا الذهبي - ديارنا الحديثة',
    prompt:
      'Modern commercial building exterior facade after renovation, newly clad in polished Giallo Siena yellow-gold Italian marble slabs with crisp clean joints, bright daylight, completed premium project',
    topics: [
      'رخام جيلو سيينا',
      'واجهات حجرية',
      'كسوة رخام',
      'تجديد واجهات',
      'رخام أصفر',
      'ديارنا الحديثة',
      'حجر طبيعي',
    ],
    usedBy: [''],
  },
  {
    slug: 's4-2026-10-22-equip-04',
    file: '/images/blog-ai/s4-2026-10-22-equip-04.jpg',
    scene:
      'مشهد تصويري لـسيزر لفت في موقع عمل بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'A scissor lift platform raised beside a building facade, professional industrial photography, real construction site, warm daylight, dust in the air, sharp focus, high detail, no text, no watermark',
    topics: [
      'سيزر لفت',
      'معدات ثقيلة',
      'تأجير معدات',
      'الرياض',
      'السعودية',
    ],
    usedBy: [''],
  },
  {
    slug: 'interior-staircase-marble',
    file: '/images/blog-ai/interior-staircase-marble.jpg',
    scene:
      'تفصيل قريب لدرج داخلي من الرخام يظهر درجة مصقولة بحافة مستديرة ورقاقة جانبية مطابقة، مع ضوء دافئ يلقي ظلالا ناعمة على الدرجات.',
    prompt:
      'Editorial photograph: close-up detail of an interior stone staircase showing a polished marble tread, rounded nosing edge and matching side cladding, warm sunlight casting soft shadows across the steps, architectural interior photography, no text or lettering.',
    topics: [
      'رخام الدرج',
      'درج داخلي',
      'حواف الدرج',
      'تركيب الدرج',
      'صقل الدرج',
    ],
    usedBy: [''],
  },
  {
    slug: 's5-2026-10-22-stone-dark-emperador-classic',
    file: '/images/blog-ai/s5-2026-10-22-stone-dark-emperador-classic.jpg',
    scene:
      'مشهد تصويري لـرخام إمبرادور الداكن بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Dark Emperador Marble marble, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'رخام إمبرادور الداكن',
      'رخام بني',
      'تأجير معدات الرياض',
      'ديارنا الحديثة',
    ],
    usedBy: [''],
  },
  {
    slug: 'cleaning-stone-sinks',
    file: '/images/blog-ai/cleaning-stone-sinks.jpg',
    scene:
      'عاملة نظافة تمسح حوض رخام مصقول بقطعة قماش ناعمة في حمام مشرق بإضاءة جانبية',
    prompt:
      'A housekeeper wiping a polished marble washbasin with a soft cloth in a bright bathroom, water droplets on the stone edge, daylight from the side, editorial photography',
    topics: [
      'تنظيف الحجر',
      'عناية المغاسل',
      'رخام الحمام',
      'المدينة المنورة',
      'صيانة الحجر',
    ],
    usedBy: [''],
  },
  {
    slug: 's6-2026-10-22-stone-silver-travertine-classic',
    file: '/images/blog-ai/s6-2026-10-22-stone-silver-travertine-classic.jpg',
    scene:
      'مشهد تصويري لـSilver Travertine Travertine بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Silver Travertine travertine, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'Silver Travertine',
      'ترافيرتين',
      'حجر طبيعي',
      'المدينة المنورة',
      'ديارنا الحديثة',
    ],
    usedBy: [''],
  },
  {
    slug: 's1-2026-10-23-stone-emperador-light-marble',
    file: '/images/blog-ai/s1-2026-10-23-stone-emperador-light-marble.jpg',
    scene:
      'مشهد تصويري لـرخام إمبرادور فاتح بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Emperador Light Marble marble, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'رخام إمبرادور',
      'حجر طبيعي',
      'واجهات',
      'أرضيات',
      'تشطيبات',
    ],
    usedBy: [''],
  },
  {
    slug: 'basin-sizes-heights',
    file: '/images/blog-ai/basin-sizes-heights.jpg',
    scene:
      'شريط قياس بجانب مغسلة حجرية على طاولة حمام يظهر الارتفاع والقطر',
    prompt:
      'A tape measure beside a stone basin on a bathroom counter showing height and diameter, editorial photography',
    topics: [
      'مغاسل حجر',
      'أحواض حمام',
      'رخام',
      'المدينة المنورة',
      'الحمامات',
    ],
    usedBy: [''],
  },
  {
    slug: 's2-2026-10-23-stone-roman-travertine-classic',
    file: '/images/blog-ai/s2-2026-10-23-stone-roman-travertine-classic.jpg',
    scene:
      'مشهد تصويري لـRoman Travertine بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Roman Travertine travertine, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'Roman Travertine',
      'travertine',
      'natural stone',
      'beige',
      'polished',
      'honed',
      'Madinah',
      'Medina',
      'حجر طبيعي',
      'ترافرتين',
      'واجهات',
      'أرضيات',
    ],
    usedBy: [''],
  },
  {
    slug: 's3-2026-10-23-stone-granite-silver-grey-1',
    file: '/images/blog-ai/s3-2026-10-23-stone-granite-silver-grey-1.jpg',
    scene:
      'مشهد تصويري لـجرانيت فضي رمادي بتصميم معماري أنيق',
    prompt:
      'Silver Grey Granite granite, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'جرانيت فضي',
      'رخام',
      'واجهات',
      'مغاسل',
      'مطابخ',
      'تشطيبات',
      'حجر طبيعي',
    ],
    usedBy: [''],
  },
  {
    slug: 'three-stones-comparison-table',
    file: '/images/blog-ai/three-stones-comparison-table.jpg',
    scene:
      'ثلاث عيّنات حجر في صف على طاولة ورشة: رخام وجرانيت وترافرتينو، وفني يقارن بينها',
    prompt:
      'Three stone sample tiles arranged in a row on a workshop table, marble granite and travertine, a technician comparing them, editorial photography',
    topics: [
      'مقارنة أحجار',
      'رخام',
      'جرانيت',
      'ترافرتينو',
      'أسطح مطبخ',
    ],
    usedBy: [''],
  },
  {
    slug: 's4-2026-10-23-stone-carrara-vessel-sink',
    file: '/images/blog-ai/s4-2026-10-23-stone-carrara-vessel-sink.jpg',
    scene:
      'مشهد تصويري لمغسلة حوض كارارا المستديرة بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Carrara Round Vessel Sink stone washbasin, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'مغاسل',
      'مغسلة رخام',
      'حوض كارارا',
      'مغسلة مستديرة',
      'رخام',
      'تشطيبات',
    ],
    usedBy: [''],
  },
  {
    slug: 'undermount-marble-sinks',
    file: '/images/blog-ai/undermount-marble-sinks.jpg',
    scene:
      'فنّي يثبّت مغسلاً رخامياً تحت سطح كونسول حجري سميك في حمام مضاء بإضاءة جانبية',
    prompt:
      'A fitter securing an undermount marble sink under a thick stone countertop in a bright bathroom, hands tightening a metal clamp, side daylight, editorial photography',
    topics: [
      'مغسل تحت السطح',
      'تركيب المغاسل',
      'رخام الكونسول',
      'المدينة المنورة',
      'حوض مدمج',
    ],
    usedBy: [''],
  },
  {
    slug: 's5-2026-10-23-stone-stone-finishes-guide',
    file: '/images/blog-ai/s5-2026-10-23-stone-stone-finishes-guide.jpg',
    scene:
      'ثلاث عيّنات حجر جنباً إلى جنب تُظهر تشطيباً مصقولاً وآخر مطفأً وثالثاً مجروشاً على طاولة ورشة',
    prompt:
      'Three stone sample tiles side by side showing polished, honed and textured finishes on a workshop table, soft daylight, editorial photography, macro detail',
    topics: [
      'تشطيبات_الحجر',
      'حجر_طبيعي',
      'رخام',
      'جرانيت',
      'تشطيب_مصقول',
      'تشطيب_مطفأ',
      'المدينة_المنورة',
      'ديارنا_الحديثة',
    ],
    usedBy: [''],
  },
  {
    slug: 's6-2026-10-23-stone-granite-exterior-facades',
    file: '/images/blog-ai/s6-2026-10-23-stone-granite-exterior-facades.jpg',
    scene:
      'عاملان يثبّتان ألواح جرانيت داكنة على واجهة فيلا حديثة بالمدينة المنورة، مع ضبط كلب معدني بميزان ماء وإضاءة عصر دافئة.',
    prompt:
      'Close-up of large natural dark granite stone cladding slabs being mounted on a modern villa exterior facade, dark grey granite panels with visible crystalline speckled stone texture, a construction worker in a safety helmet positioning a slab, stainless steel mechanical anchor brackets and metal frame, construction site, warm afternoon light, no text, no watermark',
    topics: [
      'واجهات',
      'جرانيت',
      'حجر طبيعي',
      'تشطيبات',
      'ديارنا الحديثة',
    ],
    usedBy: [''],
  },
  {
    slug: 's6-2026-10-23-stone-granite-exterior-facades-ig',
    file: '/images/blog-ai/s6-2026-10-23-stone-granite-exterior-facades-ig.jpg',
    scene:
      'ألواح جرانيت طبيعي داكن تُثبَّت على واجهة فيلا حديثة بالمدينة المنورة مع كلاليب معدنية وميزان ماء',
    prompt:
      'Close-up of large natural dark granite stone cladding slabs being mounted on a modern villa exterior facade, dark grey granite panels with visible crystalline speckled stone texture, a construction worker in a safety helmet positioning a slab, stainless steel mechanical anchor brackets and metal frame, construction site, warm afternoon light, no text, no watermark',
    topics: [
      'واجهات',
      'جرانيت',
      'حجر طبيعي',
      'تشطيبات',
      'ديارنا الحديثة',
    ],
    usedBy: [''],
  },
  {
    slug: 's1-2026-10-24-stone-portoro-classic',
    file: '/images/blog-ai/s1-2026-10-24-stone-portoro-classic.jpg',
    scene:
      'مشهد تصويري لـرخام بورتورو بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Portoro Marble marble, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'رخام بورتورو',
      'رخام أسود',
      'حجر طبيعي',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 's1-2026-10-24-stone-portoro-classic-v2',
    file: '/images/blog-ai/s1-2026-10-24-stone-portoro-classic-v2.jpg',
    scene:
      'مشهد تصويري لـرخام بورتورو الأسود بعروقه الذهبية المميزة، سطح مصقول لامع، بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Portoro Marble, black marble slab with distinctive gold and white veins, polished glossy surface, dark background stone, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'رخام بورتورو',
      'رخام أسود',
      'حجر طبيعي',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 's1-2026-10-24-stone-portoro-classic-ig',
    file: '/images/blog-ai/s1-2026-10-24-stone-portoro-classic-ig.jpg',
    scene:
      'مشهد تصويري لـرخام بورتورو الأسود بعروقه الذهبية المميزة، سطح مصقول لامع، بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Portoro Marble, black marble with distinctive gold and white veins, polished surface, high contrast dark background, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'رخام بورتورو',
      'رخام أسود',
      'حجر طبيعي',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 'narrow-bathroom-basins',
    file: '/images/blog-ai/narrow-bathroom-basins.jpg',
    scene:
      'حمام ضيق بمغسلة حجرية صغيرة وخلاط جداري',
    prompt:
      'Editorial photograph of a very narrow small bathroom, a compact natural stone washbasin fixed to the wall with an exposed chrome wall-mounted faucet mounted directly on the tiled wall above the basin, daylight from a small window, neutral cream and white tones, no people',
    topics: [
      'مغاسل حجر',
      'أحواض حمام',
      'رخام',
      'المدينة المنورة',
      'الحمامات',
    ],
    usedBy: [''],
  },
  {
    slug: 's2-2026-10-24-stone-silver-travertine-veined',
    file: '/images/blog-ai/s2-2026-10-24-stone-silver-travertine-veined.jpg',
    scene:
      'مشهد تصويري لحجر الترافنتينو الفضي المعرّق بتشطيب مصقول بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Veined Silver Travertine natural travertine stone slab, polished surface finish, soft grey base with clear white and pale grey linear veins running through the stone, visible natural pores and subtle crystalline texture, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'حجر ترافنتينو',
      'ترافنتينو فضي',
      'حجر طبيعي',
      'واجهات حجر',
      'ديارنا الحديثة',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 'basin-installation-steps',
    file: '/images/blog-ai/basin-installation-steps.jpg',
    scene:
      'يد تركّب مغسلة حجرية ثقيلة على الطاولة بمساند وسيليكون',
    prompt:
      'A plumber\'s hands fixing a heavy stone basin onto a bathroom counter with metal brackets and a bead of clear silicone sealant, level tool and tape measure nearby, daylight',
    topics: [
      'مغاسل حجر',
      'أحواض حمام',
      'رخام',
      'المدينة المنورة',
      'الحمامات',
    ],
    usedBy: [''],
  },
  {
    slug: 's3-2026-10-24-stone-granite-silver-grey-2',
    file: '/images/blog-ai/s3-2026-10-24-stone-granite-silver-grey-2.jpg',
    scene:
      'مشهد تصويري لـSilver Grey Granite 2 بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Silver Grey Granite 2 granite, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'جرانيت فضي',
      'حجر طبيعي',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 's4-2026-10-24-stone-calacatta-vessel-sink',
    file: '/images/blog-ai/s4-2026-10-24-stone-calacatta-vessel-sink.jpg',
    scene:
      'مغسلة مدمجة منحوتة في كتلة رخام كالاكاتا واحدة',
    prompt:
      'Bathroom vanity carved from one massive Calacatta marble block, integrated oval basin carved directly into the solid stone, gold and grey marble veins visible everywhere on the same continuous stone surface, polished marble, wall-mounted brushed gold faucet, soft daylight, architectural interior photography, sharp focus, high detail, no text, no watermark',
    topics: [
      'مغاسل',
      'رخام كالاكاتا',
      'مغسلة رخام',
      'ديارنا الحديثة',
    ],
    usedBy: [''],
  },
  {
    slug: 'basin-price-factors',
    file: '/images/blog-ai/basin-price-factors.jpg',
    scene:
      'عرض سعر مكتوب لمغاسل حجرية على مكتب بجانب عيّنات',
    prompt:
      'A written quotation for stone basins on a desk next to basin samples, editorial photography',
    topics: [
      'مغاسل حجر',
      'أحواض حمام',
      'رخام',
      'المدينة المنورة',
      'الحمامات',
    ],
    usedBy: [''],
  },
  {
    slug: 's5-2026-10-24-stone-sandstone-facades-cladding',
    file: '/images/blog-ai/s5-2026-10-24-stone-sandstone-facades-cladding.jpg',
    scene:
      'نجار حجر يثبّت لوح حجر رملي مشطوف على واجهة فيلا بيديه ومطرقة مطاطية، وعامل آخر يفحص الاستواء بخيط، وغبار القطع في الضوء.',
    prompt:
      'Editorial scene: a mason carefully setting a rough-hewn sandstone panel onto a villa facade with a rubber mallet, a second worker checking alignment with a string line, dust from cutting visible in daylight, close-up of stone texture and shadow, no text',
    topics: [
      'حجر رملي',
      'واجهات',
      'واجهات حجر رملي',
      'تكسية حجر',
      'واجهات فلل',
      'حجر طبيعي',
    ],
    usedBy: [''],
  },
  {
    slug: 'natural-stone-sealing',
    file: '/images/blog-ai/natural-stone-sealing.jpg',
    scene:
      'فني يطبّق مادة عازلة على أرضية رخام داخل فيلا مضاءة بنهار ناعم',
    prompt:
      'A technician applying penetrating stone sealer to a honed marble floor with a microfiber cloth inside a bright villa, soft daylight, sharp focus, high detail, 8k, professional photography, crisp, clear, well-defined, ultra realistic',
    topics: [
      'ختم الحجر',
      'عزل الرخام',
      'صيانة الحجر الطبيعي',
      'حماية الأسطح',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 'outdoor-stone-flooring',
    file: '/images/blog-ai/outdoor-stone-flooring.jpg',
    scene:
      'بلاطات حجر جيري بيج حديثة الرصف في فناء خارجي بفواصل رملية ظاهرة، ويد عامل بقفاز تمسك مطرقة مطاطية على بلاطة، وجزء من ميزان مستوٍ على الحجر',
    prompt:
      'Close-up detail of newly laid beige natural limestone paving slabs in an outdoor courtyard, visible sand joints between slabs, a worker\'s gloved hand holding a rubber mallet tapping one slab into place, part of a spirit level resting on the stone, hard shadows in warm late afternoon sunlight, shallow depth of field, macro editorial style, sharp focus, high detail, professional photography, crisp, clear',
    topics: [
      'أرضيات خارجية',
      'حجر ممشى',
      'فناء حجري',
      'حجر حدائق',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 'marble-countertops-buying-guide',
    file: '/images/blog-ai/marble-countertops-buying-guide.jpg',
    scene:
      'مطبخ بسطح عمل من الرخام ورب منزل يختار شكل الحافة من عيّنات',
    prompt:
      'A kitchen with a marble countertop and a homeowner choosing edge profile from samples, warm daylight, editorial photography',
    topics: [
      'مقارنة أحجار',
      'رخام',
      'جرانيت',
      'ترافرتينو',
      'أسطح مطبخ',
    ],
    usedBy: [''],
  },
  {
    slug: 's1-2026-10-25-stone-statuario-marble',
    file: '/images/blog-ai/s1-2026-10-25-stone-statuario-marble.jpg',
    scene:
      'مشهد تصويري لـرخام ستاتيواريو بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Statuario Marble marble, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'رخام ستاتيواريو',
      'رخام إيطالي',
      'رخام أبيض',
      'واجهات رخام',
    ],
    usedBy: [''],
  },
  {
    slug: 's2-2026-10-25-stone-roman-travertine-veincut',
    file: '/images/blog-ai/s2-2026-10-25-stone-roman-travertine-veincut.jpg',
    scene:
      'مشهد تصويري لـVein Cut Roman Travertine بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Vein Cut Roman Travertine travertine, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark, sharp focus, high detail, 4K resolution, ultra realistic, crisp, clear, professional photography, 2048x1024',
    topics: [
      'ترافينتين، حجر طبيعي، واجهات، تركيب، رصف',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-grout-joints-filling',
    file: '/images/blog-ai/stone-grout-joints-filling.jpg',
    scene:
      'يد فني بقفاز تملأ الفواصل بين ألواح حجر طبيعي كبيرة بمونة بيضاء باستخدام مسطرين مطاطي، وبجانبه دلو مونة وجاروف',
    prompt:
      'Photorealistic documentary photo of gloved hands holding a rubber grout float, pushing white cement grout into the joint between two large beige limestone tiles on a wall, fresh white grout line, construction site daylight',
    topics: [
      'ترويبات الحجر',
      'مونة فواصل',
      'شق الحجر',
      'ألواح حجر طبيعي',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 's3-2026-10-25-stone-granite-silver-cloud',
    file: '/images/blog-ai/s3-2026-10-25-stone-granite-silver-cloud.jpg',
    scene:
      'مشهد تصويري لـجرانيت فضي سحابي بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Silver Cloud Granite granite, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'جرانيت',
      'حجر طبيعي',
      'واجهات',
      'تشطيبات',
    ],
    usedBy: [''],
  },
  {
    slug: 'facade-leveling-flatness-guide',
    file: '/images/blog-ai/facade-leveling-flatness-guide.jpg',
    scene:
      'ميزان مياه معدني موضوع على لوح حجر جيري طبيعي بيج فوق طاولة عمل في ورشة، مع خلفية خشبية',
    prompt:
      'Macro photograph of a spirit level tool lying flat on a beige natural limestone slab on a workbench, workshop background, daylight, realistic, sharp focus',
    topics: [
      'استواء الواجهات',
      'تسوية الحجر',
      'ميزان مياه',
      'تثبيت الحجر',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 's4-2026-10-25-stone-nero-assalto-sink',
    file: '/images/blog-ai/s4-2026-10-25-stone-nero-assalto-sink.jpg',
    scene:
      'مشهد تصويري لـNero Assoluto Undermount Sink بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Nero Assoluto Undermount Sink stone washbasin, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark, sharp focus, high detail, 4K, professional photography',
    topics: [
      'رخام',
      'مغاسل',
      'نيرو أسسوتو',
      'حجر طبيعي',
      'واجهات',
      'تشطيبات',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-crack-repair-assessment',
    file: '/images/blog-ai/stone-crack-repair-assessment.jpg',
    scene:
      'مجرفة معدنية مسطّحة ملقاة على لوح حجر جيري بيج طبيعي فوق طاولة عمل في ورشة، بإضاءة نهارية وتركيز حاد',
    prompt:
      'Macro photograph of a metal trowel lying flat on a beige natural limestone slab on a workbench, workshop background, daylight, sharp focus, high detail, professional photography',
    topics: [
      'إصلاح تشققات الحجر',
      'ترميم الرخام',
      'تشقق الحجر الطبيعي',
      'صيانة الحجر',
      'معجون ترميم الحجر',
    ],
    usedBy: [''],
  },
  {
    slug: 'marble-vs-quartz-countertops',
    file: '/images/blog-ai/marble-vs-quartz-countertops.jpg',
    scene:
      'سطح مطبخ حجري أبيض بعروق رمادية مع ظهر حجري مطابق وخزائن داكنة وفتحة حوض فارغة',
    prompt:
      'Editorial photograph of a kitchen countertop with white veined natural marble backsplash and matching stone worktop, dark matte cabinets, empty sink cutout, daylight, sharp focus, no people',
    topics: [
      'أسطح المطبخ',
      'رخام',
      'كوارتز',
      'المقارنات',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 'limestone-facades-medina',
    file: '/images/blog-ai/limestone-facades-medina.jpg',
    scene:
      'إزميل معدني بطرف مسطح ملقى بشكل مائل على لوح حجر جيري بيج اللون فوق طاولة عمل، وخلفية ورشة عمل ضبابية',
    prompt:
      'Macro photograph of a small steel chisel lying diagonally on a beige natural limestone slab on a workbench, workshop background, daylight, sharp focus, high detail, professional photography, crisp, clear',
    topics: [
      'حجر جيري',
      'واجهات حجرية',
      'تشطيبات واجهات',
      'عزل الحجر',
      'أدوات تركيب الحجر',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 's3-2026-10-26-stone-negro-black-classic',
    file: '/images/blog-ai/s3-2026-10-26-stone-negro-black-classic.jpg',
    scene:
      'مشهد تصويري لـNegro Black Granite بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Negro Black Granite granite, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'negro-black-granite',
      'granite',
      'رخام',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-compound-mortar-materials',
    file: '/images/blog-ai/stone-compound-mortar-materials.jpg',
    scene:
      'مسطرين معدني بمقبض معدني ملقى بشكل مائل على لوح حجر طبيعي رمادي مرقط فوق طاولة عمل، وخلفية ورشة عمل ضبابية',
    prompt:
      'Macro photograph of a metal trowel with a metal handle lying diagonally on a grey speckled natural stone slab on a workbench, workshop background, daylight, sharp focus, high detail, professional photography, crisp, clear',
    topics: [
      'مونة تركيب الحجر',
      'تركيب الواجهات',
      'لصق الحجر الطبيعي',
      'مواد البناء',
      'أدوات التركيب',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 'natural-stone-curing-moisture',
    file: '/images/blog-ai/natural-stone-curing-moisture.jpg',
    scene:
      'فرشاة مسطّحة بمقبض خشبي ملقاة على لوح حجر طبيعي بيج فوق طاولة عمل، وخلفية ورشة عمل ضبابية',
    prompt:
      'Macro photograph of a stiff flat bristle brush with a wooden handle lying on a beige natural stone slab on a workbench, workshop background, daylight, sharp focus, high detail, professional photography, crisp, clear',
    topics: [
      'معالجة الحجر',
      'مونة تركيب الحجر',
      'رش الحجر بالماء',
      'تركيب الواجهات',
      'العناية بالحجر الطبيعي',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 'pool-stone-coping-guide',
    file: '/images/blog-ai/pool-stone-coping-guide.jpg',
    scene:
      'لوح جرانيت رمادي داكن مرقط بحافة أمامية مستديرة قطاعاً نصف دائرياً ملقى على طاولة عمل، وخلفية ورشة عمل ضبابية',
    prompt:
      'Macro photograph of a natural grey granite slab with a rounded bullnose edge lying on a workbench, workshop background, daylight, sharp focus, high detail, professional photography, crisp, clear',
    topics: [
      'حجر المسبح',
      'حواف المسبح',
      'جرانيت',
      'حافة مستديرة',
      'أرضيات خارجية',
      'المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 's3-2026-10-27-stone-kashmir-white-classic',
    file: '/images/blog-ai/s3-2026-10-27-stone-kashmir-white-classic.jpg',
    scene:
      'مشهد تصويري لـKashmir White Granite بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Kashmir White Granite granite, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'جرانيت',
      'حجر طبيعي',
      'واجهات',
      'مطابخ',
      'تشطيبات',
    ],
    usedBy: [''],
  },
  {
    slug: 's5-2026-10-29-stone-stone-facades-complete-selection-guide',
    file: '/images/blog-ai/s5-2026-10-29-stone-stone-facades-complete-selection-guide.jpg',
    scene:
      'واجهة فيلا حديثة مغشاة بألواح ترافرتينو فاتحة تحت شمس المدينة المنورة',
    prompt:
      'A row of modern villa exteriors with different natural stone cladding styles, granite travertine and limestone facades, soft morning sunlight, wide architectural photography, no people, no text',
    topics: [
      'واجهات',
      'حجر طبيعي',
      'جرانيت',
      'ترافرتينو',
    ],
    usedBy: [''],
  },
  {
    slug: 'interior-stone-wall-cladding-medina',
    file: '/images/blog-ai/interior-stone-wall-cladding-medina.jpg',
    scene:
      'أيدي عامل تركيب تكسية جدران حجرية داخلية بألوان ب، ألوان حجر جيري بيج، ملاط رقيق، إضاءة ورشة',
    prompt:
      'Editorial photograph of a stone cladding installation in progress on an interior wall, beige limestone slabs being fitted with stainless steel anchors, craftsman hands with trowel applying thin-set mortar, workshop lighting, sharp focus, high detail, professional photography',
    topics: [
      'تكسية جدران',
      'حجر طبيعي',
      'تكسية داخلية',
    ],
    usedBy: [''],
  },
  {
    slug: 's6-2026-10-29-stone-basin-sizes-heights',
    file: '/images/blog-ai/s6-2026-10-29-stone-basin-sizes-heights.jpg',
    scene:
      'شريط قياس بجانب مغسلة حجرية على طاولة حمام يظهر الارتفاع والقطر',
    prompt:
      'A tape measure beside a stone basin on a bathroom counter showing height and diameter, editorial photography',
    topics: [
      'مغاسل حجرية',
      'مقاسات مغسلة',
      'ارتفاعات',
      'حجر طبيعي',
      'رخام',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-polishing-grinding-guide',
    file: '/images/blog-ai/stone-polishing-grinding-guide.jpg',
    scene:
      'فانوس تلميع على لوح حجر جيري بيج على طاولة عمل',
    prompt:
      'Macro photograph of a polishing pad on a beige natural limestone slab, workshop background, daylight, sharp focus',
    topics: [
      'تلميع، تغطية، جلي، حجر طبيعي، المدينة المنورة',
    ],
    usedBy: [''],
  },
  {
    slug: 'outdoor-patio-terrace-stone-medina',
    file: '/images/blog-ai/outdoor-patio-terrace-stone-medina.jpg',
    scene:
      'ميزان مياه على لوح حجر بيج على طاولة عمل في ورشة',
    prompt:
      'Macro photograph of a beige natural limestone slab on a workbench with a spirit level tool lying flat on it, workshop background, daylight, sharp focus',
    topics: [
      'أحجار، فناء، تراس، المدينة المنورة، جرانيت، ترافرتينو',
    ],
    usedBy: [''],
  },
  {
    slug: 's2-2026-10-30-stone-cream-limestone-classic',
    file: '/images/blog-ai/s2-2026-10-30-stone-cream-limestone-classic.jpg',
    scene:
      'مشهد تصويري لـCream Limestone بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Cream Limestone limestone, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'limestone',
    ],
    usedBy: [''],
  },
  {
    slug: 's3-2026-10-30-stone-granite-nero-silver-veins',
    file: '/images/blog-ai/s3-2026-10-30-stone-granite-nero-silver-veins.jpg',
    scene:
      'مشهد تصويري مقسم لـNero Silver Veins Granite بتشطيب مصقول ومطفأ',
    prompt:
      'Nero Silver Veins Granite polished and honed finish split screen, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'granite',
      'nero silver veins',
      'architectural stone',
    ],
    usedBy: [''],
  },
  {
    slug: 'natural-stone-sinks-selection',
    file: '/images/blog-ai/natural-stone-sinks-selection.jpg',
    scene:
      'مغسلة جرانيت مصقول على سطح ترافرتينو مصقول في حمام حديث، إضاءة طبيعية ناعمة، تركيز واضح على نسيج الحجر وقطرات الماء',
    prompt:
      'Macro photograph of a polished granite vessel sink on a honed travertine countertop in a modern bathroom, soft natural light, sharp focus on stone texture and water droplets, professional interior photography',
    topics: [
      'مغاسل حجر، جرانيت، ترافرتينو، حمام، Medina',
    ],
    usedBy: [''],
  },
  {
    slug: 'bathroom-stone-flooring-medina',
    file: '/images/blog-ai/bathroom-stone-flooring-medina.jpg',
    scene:
      'أرضية حمام حديثة ببلاط ترافرتين بيج مصقول',
    prompt:
      'Editorial photograph of a modern bathroom floor with honed beige travertine tiles',
    topics: [
      'أرضيات حجر',
      'حمام',
      'ترافرتين',
      'رخام',
      'جرانيت',
    ],
    usedBy: [''],
  },
  {
    slug: 's5-2026-10-30-stone-facade-slab-thickness-20-30-50mm',
    file: '/images/blog-ai/s5-2026-10-30-stone-facade-slab-thickness-20-30-50mm.jpg',
    scene:
      'قياس سماكة لوح حجر بفركار على طاولة عمل قبل تجهيز واجهة',
    prompt:
      'Three natural stone wall panels of different thicknesses standing side by side in a stone workshop, a caliper measuring the panel edge, diffused daylight, editorial photography, no text',
    topics: [
      'سماكة ألواح',
      'واجهات',
      'حجر طبيعي',
      'تركيب واجهات',
      'دليل هندسي',
    ],
    usedBy: [''],
  },
  {
    slug: 's4-2026-10-30-stone-undermount-marble-sinks',
    file: '/images/blog-ai/s4-2026-10-30-stone-undermount-marble-sinks.jpg',
    scene:
      'مغسل رخام تحت السطح بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Professional product photography of marble undermount sink, sharp focus, high detail, 8k',
    topics: [
      'مغاسل',
      'رخام',
      'تحت السطح',
      'حمام',
      'تركيب مغاسل',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-polishing-restoration',
    file: '/images/blog-ai/stone-polishing-restoration.jpg',
    scene:
      '',
    prompt:
      'Macro photograph of a diamond polishing pad spinning on a white marble floor in a workshop, water spray, reflective surface, professional stone restoration, daylight, sharp focus',
    topics: [
    ],
    usedBy: [''],
  },
  {
    slug: 'natural-stone-gardens-walkways-medina',
    file: '/images/blog-ai/natural-stone-gardens-walkways-medina.jpg',
    scene:
      'ممر حجري من ترافرتينو على طاولة عمل في ورشة',
    prompt:
      'Macro photograph of a natural stone garden pathway with travertine pavers on a workbench, workshop background, daylight, sharp focus',
    topics: [
      'حجر طبيعي',
      'حدائق',
      'ممرات',
      'ترافرتينو',
      'جرانيت',
      'ليمنستون',
    ],
    usedBy: [''],
  },
  {
    slug: 's1-2026-10-31-stone-calacatta-gold-marble',
    file: '/images/blog-ai/s1-2026-10-31-stone-calacatta-gold-marble.jpg',
    scene:
      'مشهد تصويري لـCalacatta Gold Marble بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Calacatta Gold Marble marble, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'marble',
      'calacatta',
      'gold',
      'polished',
    ],
    usedBy: [''],
  },
  {
    slug: 's2-2026-10-31-stone-veined-travertine',
    file: '/images/blog-ai/s2-2026-10-31-stone-veined-travertine.jpg',
    scene:
      'مشهد تصويري لـBeige Veined Travertine بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Beige Veined Travertine travertine, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'stone',
      'travertine',
      'veined',
    ],
    usedBy: [''],
  },
  {
    slug: 's2-2026-10-31-stone-veined-travertine-ig',
    file: '/images/blog-ai/s2-2026-10-31-stone-veined-travertine-ig.jpg',
    scene:
      'مشهد تصويري لـBeige Veined Travertine بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Beige Veined Travertine travertine, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'stone',
      'travertine',
      'veined',
    ],
    usedBy: [''],
  },
  {
    slug: 'stone-surface-finishes-guide',
    file: '/images/blog-ai/stone-surface-finishes-guide.jpg',
    scene:
      'يد حرفى تحمل لوح حجر صغير يُظهر تشطيبين متباينين (مصقول لامع مقابل مطفي) على طاولة عمل مع أقراص صقل ماسية ورذاذ ماء، إضاءة ورشة دافئة',
    prompt:
      'Editorial close-up of a stone fabricator\'s hand holding a small sample slab showing two contrasting finishes side by side, polished glossy versus honed matte, on a workbench with diamond polishing pads and a water spray, warm workshop light, sharp focus, professional photography',
    topics: [
      'تشطيبات الحجر، مصقول، مطفي، مطرقة، مغاسل، واجهات',
    ],
    usedBy: [''],
  },
  {
    slug: 's3-2026-10-31-stone-granite-silver-pearl',
    file: '/images/blog-ai/s3-2026-10-31-stone-granite-silver-pearl.jpg',
    scene:
      'مشهد تصويري لـSilver Pearl Granite بإضاءة طبيعية وتفاصيل واضحة',
    prompt:
      'Silver Pearl Granite granite, polished surface finish, professional architectural photography, soft daylight, high detail, no text, no watermark',
    topics: [
      'granite',
    ],
    usedBy: [''],
  },
  {
    slug: 's4-2026-10-31-stone-facade-fixing-clips-mortar-joints',
    file: '/images/blog-ai/s4-2026-10-31-stone-facade-fixing-clips-mortar-joints.jpg',
    scene:
      'تثبيت قضبان معدنية وتعليق لوح حجر بالكلالات على واجهة مبنى',
    prompt:
      'A worker installing a stone facade panel with metal clips and anchors on a building wall, close-up of the fixing system and the joint, daylight, editorial photography, no text',
    topics: [
      'stone',
      'facade',
      'clips',
      'mortar',
      'joints',
    ],
    usedBy: [''],
  },
  {
    slug: 's6-2026-10-24-stone-marble-kitchen-acids',
    file: '/images/blog-ai/s6-2026-10-24-stone-marble-kitchen-acids.jpg',
    scene:
      'يد تمسح عصير حماض مسكوبا على سطح رخامي كريمي داخل مطبخ بإضاءة نافذة طبيعية، مع إظهار نسيج السطح ولمعته.',
    prompt:
      'Editorial photograph in a kitchen: a hand wiping spilled citrus juice from a creamy marble countertop with a soft cloth, close-up on surface texture and matte finish, natural window light, documentary style, no text or lettering.',
    topics: [
      'رخام المطبخ',
      'حمض الليمون على الرخام',
      'تأثير الحموض على الرخام',
      'صيانة رخام المطبخ',
      'حجر طبيعي',
      'تنظيف الرخام',
    ],
    usedBy: [''],
  },  {
    slug: 's6-2026-10-24-stone-marble-kitchen-acids-ig',
    file: '/images/blog-ai/s6-2026-10-24-stone-marble-kitchen-acids-ig.jpg',
    scene:
      'يد تمسح عصير حماض مسكوبا على سطح رخامي كريمي داخل مطبخ بإضاءة نافذة طبيعية، مع إظهار نسيج السطح ولمعته.',
    prompt:
      'Editorial photograph in a kitchen: a hand wiping spilled citrus juice from a creamy marble countertop with a soft cloth, close-up on surface texture and matte finish, natural window light, documentary style, no text or lettering.',
    topics: [
      'رخام المطبخ',
      'حمض الليمون على الرخام',
      'تأثير الحموض على الرخام',
      'صيانة رخام المطبخ',
      'حجر طبيعي',
      'تنظيف الرخام',
    ],
    usedBy: [''],
  },];

// Fallback only. A generated cover is always preferred; this exists so a
// post can never ship with no image at all.
export const BLOG_AI_FALLBACK = '/images/blog-ai/choosing-stone-countertop.jpg';
