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
    topics: ['اختيار', 'مقارنة', 'رخام', 'جرانيت', 'سطح العمل', 'المطبخ'],
    usedBy: '',
  },
  {
    slug: 'travertine-facade-install',
    file: '/images/blog-ai/travertine-facade-install.jpg',
    scene:
      'رافعة تركّب ألواح ترافرتينو كبيرة على واجهة مبنى حديث، وعامل بمعدات سلامة، عند الغروب',
    prompt:
      'A construction crane installing large travertine facade panels on a modern building, worker in safety gear, golden hour, documentary photography',
    topics: [
      'واجهات',
      'ترافرتينو',
      'تركيب',
      'خارجي',
      'مبنى',
      'رافعة',
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
      'مواصفات',
      'قياس',
      'سماكة',
      'فحص',
      'ورشة',
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
      'سعر الحجر',
      'عرض سعر رخام',
      'مقارنة عروض',
      'المدينة المنورة',
      'تكلفة الحجر',
    ],
    usedBy: [''],
  },
  {
    slug: 'buying-natural-stone-checklist',
    file: '/images/blog-ai/buying-natural-stone-checklist.jpg',
    scene:
      'يد تقدم عيّنة حجر طبيعي كبيرة لعميل داخل معرض حجر في المدينة المنورة',
    prompt:
      'A shop assistant's hands presenting a large natural stone sample tile to a client inside a stone showroom, warm daylight from the side, editorial photography, shallow depth of field',
    topics: [
      'شراء الحجر',
      'عيّنة رخام',
      'معرض حجر',
      'المدينة المنورة',
      'سماكة الألواح',
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
      'كالاكاتا',
      'رخام إيطالي',
      'عروق الرخام',
      'الرخام الأبيض',
      'مستودع حجر',
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
      'تشطيبات الحجر',
      'مصقول',
      'مطفأ',
      'ساندبلاست',
      'عيّنات تشطيب',
    ],
    usedBy: [''],
  },
  {
    slug: 'medina-stone-facade-home-designs',
    file: '/images/blog-ai/medina-stone-facade-home-designs.jpg',
    scene:
      'منظر لواجهات منازل مغشاة بالحجر الطبيعي في حي سكني',
    prompt:
      'منظر لواجهات منازل متجاورة مغشاة بالحجر الطبيعي في حي سكني هادئ، تصاميم مختلفة لكل منزل، ضوء الشمس الصباحية، تصوير معماري واسع',
    topics: [
      'تصاميم واجهات',
      'منازل',
      'حجر طبيعي',
      'حي سكني',
      'إلهام',
    ],
    usedBy: [''],
  },
];

// Fallback only. A generated cover is always preferred; this exists so a
// post can never ship with no image at all.
export const BLOG_AI_FALLBACK = '/images/blog-ai/choosing-stone-countertop.jpg';
