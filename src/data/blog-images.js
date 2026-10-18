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

// Fallback only. A generated cover is always preferred; this exists so a
// post can never ship with no image at all.
export const BLOG_AI_FALLBACK = '/images/blog-ai/choosing-stone-countertop.jpg';
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
];
