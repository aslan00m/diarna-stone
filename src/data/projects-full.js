// مشاريع ديارنا الحديثة — كل مشروع صفحته الخاصة.
// `stages` مرتّبة زمنياً: قبل (هيكل/تجهيز) ← أثناء ← بعد (تشطيب وتسليم).
// الصور كلها من مشاريع حقيقية رفعتها الشركة، وطُمست منها أرقام
// هواتف المقاولين الآخرين قبل النشر.
export const PROJECTS_FULL = [
  {
    slug: 'villa-evening',
    title: 'فيلا حديثة — إضاءة مسائية',
    category: 'فلل ومبانٍ سكنية',
    summary:
      'فيلا حديثة بواجهة داكنة وزجاج واسع، أنجزنا فيها توريد وتركيب الحجر على الواجهات الخارجية مع تنسيق الحديقة والمسبح المفتوح على الواجهة الخلفية.',
    scope: ['توريد الحجر', 'تركيب الواجهات', 'أعمال أرضيات', 'تشطيب خارجي'],
    duration: 'غير محدد',
    cover: '/images/heroes/hero-1-villa-evening.jpg',
    coverAlt: 'فيلا حديثة بواجهة داكنة وإضاءة داخلية دافئة عند الغروب',
    stages: [
      { label: 'قبل', note: 'مرحلة الأساس والهيكل', images: [] },
      { label: 'بعد', note: 'التسليم النهائي', images: [
        { src: '/images/heroes/hero-1-villa-evening.jpg', alt: 'الفيلا بعد التسليم عند الغروب' },
        { src: '/images/heroes/hero-2-villa-pool.jpg', alt: 'المسبح والواجهة الخلفية بعد التشطيب' },
      ] },
    ],
  },
  {
    slug: 'villa-pool-modern',
    title: 'فيلا بمسبح خارجي',
    category: 'فلل ومبانٍ سكنية',
    summary:
      'فيلا بيضاء حديثة بمسبح خارجي وحدائق نخيل. ركبنا فيها ألواح حجرية على الواجهة، ووزّعنا نفس الخامة على أرضيات الشرفة الخارجية.',
    scope: ['تركيب الواجهات', 'أرضيات خارجية', 'حواجز وزجاج'],
    duration: 'غير محدد',
    cover: '/images/heroes/hero-2-villa-pool.jpg',
    coverAlt: 'فيلا بيضاء حديثة بمسبح خارجي وحدائق نخيل',
    stages: [
      { label: 'بعد', note: 'التسليم النهائي', images: [
        { src: '/images/heroes/hero-2-villa-pool.jpg', alt: 'الفيلا والمسبح بعد التشطيب' },
        { src: '/images/heroes/hero-3-villa-pool-2.jpg', alt: 'مسبح فيروزي وشرفات زجاجية' },
      ] },
    ],
  },
  {
    slug: 'villa-minimal',
    title: 'فيلا بمسبح وشرفات',
    category: 'فلل ومبانٍ سكنية',
    summary:
      'فيلا من مستويين بمسبح فيروزي، بواجهة بيضاء وأسقف خشبية داخلية. عملنا على الواجهة والأرضياتochlor مع الحرص على تناسب الخامة مع لون المسبح.',
    scope: ['تركيب الواجهات', 'أرضيات', 'تشطيب داخلي'],
    duration: 'غير محدد',
    cover: '/images/heroes/hero-3-villa-pool-2.jpg',
    coverAlt: 'فيلا من مستويين بمسبح فيروزي وشرفات زجاجية',
    stages: [
      { label: 'بعد', note: 'التسليم النهائي', images: [
        { src: '/images/heroes/hero-3-villa-pool-2.jpg', alt: 'الفيلا بعد التسليم' },
        { src: '/images/heroes/hero-4-villa-modern.jpg', alt: 'واجهة بيضاء وأسقف خشبية ومسبح طويل' },
      ] },
    ],
  },
  {
    slug: 'villa-white-minimal',
    title: 'فيلا بأسلوب مينمال',
    category: 'فلل ومبانٍ سكنية',
    summary:
      'فيلا بيضاء بواجهة نظيفة ومسبح طويل، مع تظليل خشبي يخفف من صرامة الخط Architects. ركبنا فيه أرضيات حجرية بلون محايد يترك الزجاج يبرز.',
    scope: ['أرضيات داخلية', 'واجهات', 'تشطيب'],
    duration: 'غير محدد',
    cover: '/images/heroes/hero-4-villa-modern.jpg',
    coverAlt: 'فيلا بواجهة بيضاء وأسقف خشبية ومسبح طويل',
    stages: [
      { label: 'بعد', note: 'التسليم النهائي', images: [
        { src: '/images/heroes/hero-4-villa-modern.jpg', alt: 'الفيلا بأسلوب مينمال بعد التسليم' },
      ] },
    ],
  },
  {
    slug: 'facade-beige-residence',
    title: 'واجهة فيلا بتشطيب حجري',
    category: 'واجهات خارجية',
    summary:
      'واجهة فيلا بتشطيب حجري بلون بيج مع زخارف هندسية حول الشبابيك الزرقاء. هذه صورة توضيحية لنوع التشطيب الذي ننفّذه على الواجهات.',
    scope: ['تركيب الواجهات', 'زخارف وكورنيش'],
    duration: 'غير محدد',
    cover: '/images/projects/p01-facade-beige.jpg',
    coverAlt: 'واجهة فيلا بيج بتشطيب حجري وزخارف هندسية حول الشبابيك الزرقاء',
    stages: [
      { label: 'بعد', note: 'واجهة مكتملة', images: [
        { src: '/images/projects/p01-facade-beige.jpg', alt: 'واجهة الفيلا البيج بعد التشطيب' },
        { src: '/images/projects/p02-facade-blue-glass.jpg', alt: 'واجهة مبنى سكني بنوافذ زجاجية زرقاء' },
      ] },
    ],
  },
  {
    slug: 'residence-blue-glass',
    title: 'واجهة مبنى سكني زجاج',
    category: 'واجهات خارجية',
    summary:
      'واجهة مبنى متعدد الطوابق تجمع بين النوافذ الزجاجية الزرقاء والعمود الخرساني الأمامي. ركبنا فيها Limestone حول الأعمدة وحافظنا على نظافة خط الزجاج.',
    scope: ['تركيب الواجهات', 'تشطيب الأعمدة'],
    duration: 'غير محدد',
    cover: '/images/projects/p02-facade-blue-glass.jpg',
    coverAlt: 'واجهة مبنى متعدد الطوابق بنوافذ زجاجية زرقاء وعمود خرساني أمامي',
    stages: [
      { label: 'بعد', note: 'واجهة مكتملة', images: [
        { src: '/images/projects/p02-facade-blue-glass.jpg', alt: 'الواجهة الزجاجية بعد التشطيب' },
      ] },
    ],
  },
  {
    slug: 'residence-stone-glass',
    title: 'واجهة سكنية حجرية وزجاج',
    category: 'واجهات خارجية',
    summary:
      'مبنى سكني حديث يجمع بين حجر فاتح في الحواف وزجاج داكن في الوسط. هذا المزيج يحتاج دقة في قصّ Stone حتى تتطابق الفواصل بينRISTO الزجاجي والحجري.',
    scope: ['تركيب الواجهات', 'قص دقيق', 'تنسيق مع الزجاج'],
    duration: 'غير محدد',
    cover: '/images/projects/p13-residence-stone-glass.jpg',
    coverAlt: 'مبنى سكني حديث بواجهة حجرية فاتحة وزجاج داكن وشرفات',
    stages: [
      { label: 'قبل', note: 'الهيكل والواجهة الأولية', images: [
        { src: '/images/projects/p32-wip-grey-3story.jpg', alt: 'الهيكل Grey الخرساني قبل تركيب الحجر' },
        { src: '/images/projects/p34-wip-light-facade.jpg', alt: 'الواجهة الفاتحة أثناء التركيب' },
      ] },
      { label: 'بعد', note: 'واجهة مكتملة', images: [
        { src: '/images/projects/p13-residence-stone-glass.jpg', alt: 'الواجهة الحجرية والزجاجية بعد التشطيب' },
      ] },
    ],
  },
  {
    slug: 'dark-facade-wip',
    title: 'واجهة حجرية داكنة',
    category: 'واجهات خارجية',
    summary:
      'مشروع واجهة حجرية داكنة مع أعمدة خرسانية بارزة. التزمّينا في التركيب بزوايا حادة على الكورنيش لأن الحجر الداكن ين إبراز خطّ الكورنيش أكثر من الفاتح.',
    scope: ['توريد الحجر', 'تركيب الواجهة', 'كورنيش وزوايا'],
    duration: 'غير محدد',
    cover: '/images/projects/p03-wip-dark-facade.jpg',
    coverAlt: 'مبنى تحت الإنشاء بواجهة حجرية داكنة وأعمدة خرسانية بارزة',
    stages: [
      { label: 'أثناء', note: 'مرحلة التركيب', images: [
        { src: '/images/projects/p03-wip-dark-facade.jpg', alt: 'الواجهة الحجرية الداكنة أثناء التركيب' },
        { src: '/images/projects/p04-wip-stone-beam.jpg', alt: 'تركيب الحجر مع الكمرات الخرسانية' },
      ] },
    ],
  },
  {
    slug: 'stone-beam-work',
    title: 'تركيب حجر مع كمرات',
    category: 'واجهات خارجية',
    summary:
      'صورة قريبة لتركيب الحجر الرمادي فوق الكمرات البيضاء بين الطوابق. هذه المرحلة هي الأدق في المشروع كله، لأن أي خطأ في استقامة الكمر يظهر في كامل الواجهة.',
    scope: ['تركيب حجر', 'معايرة الاستقامة'],
    duration: 'غير محدد',
    cover: '/images/projects/p04-wip-stone-beam.jpg',
    coverAlt: 'مبنى قيد الإنشاء بحجر رمادي على الواجهة وكمرات بيضاء بين الطوابق',
    stages: [
      { label: 'أثناء', note: 'مرحلة التركيب الدقيقة', images: [
        { src: '/images/projects/p04-wip-stone-beam.jpg', alt: 'الحجر الرمادي فوق الكمرات البيضاء' },
        { src: '/images/projects/p07-scaffolding-panels.jpg', alt: 'عمال على سقلات يركّبون ألواح الواجهة' },
      ] },
    ],
  },
  {
    slug: 'panel-installation',
    title: 'تركيب ألواح الواجهة',
    category: 'واجهات خارجية',
    summary:
      'عمال على سقلات يركّبون ألواح الواجهة الفاتحة على مبنى طابقين. نلتقط هذه الصور توثيقاً لمراحل العمل ولتسجيل الحالة مع العميل.',
    scope: ['تركيب ألواح', 'أعمال سقلات'],
    duration: 'غير محدد',
    cover: '/images/projects/p07-scaffolding-panels.jpg',
    coverAlt: 'عمال على سقلات يركّبون ألواح واجهة فاتحة على مبنى من طابقين',
    stages: [
      { label: 'أثناء', note: 'مرحلة التركيب', images: [
        { src: '/images/projects/p07-scaffolding-panels.jpg', alt: 'تركيب ألواح الواجهة من السقالات' },
      ] },
    ],
  },
  {
    slug: 'ornate-classic-facade',
    title: 'تشطيب واجهات بأسلوب كلاسيكي',
    category: 'واجهات خارجية',
    summary:
      'مبنى أبيض مزخرف بأقواس وأعمدة وشرفات وتيجان أسفلية. كل تفصيلة هنا منحوتة ومركّبة يدوياً، وهذا النوع يحتاج وقتاً أطول في التنفيذ من الواجهات الحديثة.',
    scope: ['تشطيب كلاسيكي', 'أعمال النحت', 'تركيب التفاصيل'],
    duration: 'غير محدد',
    cover: '/images/projects/p09-ornate-white.jpg',
    coverAlt: 'مبنى أبيض مزخرف بأقواس وأعمدة وشرفات وتيجان أسفلية',
    stages: [
      { label: 'قبل', note: 'الهيكل', images: [
        { src: '/images/projects/p23-wip-grey-arch.jpg', alt: 'الهيكل Grey مع الأقواس قبل التشطيب' },
        { src: '/images/projects/p10-neoclassical-facade.jpg', alt: 'واجهة نيوكلاسيكية أثناء التشطيب' },
      ] },
      { label: 'بعد', note: 'الواجهة مكتملة', images: [
        { src: '/images/projects/p09-ornate-white.jpg', alt: 'المبنى الكلاسيكي بعد التشطيب الكامل' },
      ] },
    ],
  },
  {
    slug: 'neoclassical-facade',
    title: 'واجهة نيوكلاسيكية',
    category: 'واجهات خارجية',
    summary:
      'واجهة نيوكلاسيكية بيضاء طويلة بزخارف كلاسيكية ونوافذ مقوسة. التزمّمنا بتناسق التاج والدرجات مع الحفاظ على بساطة الخط راضي التصميم الحديث.',
    scope: ['واجهات كلاسيكية', 'زخارف', 'تشطيب'],
    duration: 'غير محدد',
    cover: '/images/projects/p10-neoclassical-facade.jpg',
    coverAlt: 'مبنى أبيض طويل بزخارف كلاسيكية ونوافذ مقوسة يحيط به حواجز معدنية',
    stages: [
      { label: 'بعد', note: 'واجهة مكتملة', images: [
        { src: '/images/projects/p10-neoclassical-facade.jpg', alt: 'الواجهة النيوكلاسيكية بعد التشطيب' },
        { src: '/images/projects/p17-classic-facade-work.jpg', alt: 'واجهة كلاسيكية أثناء أعمال الإنهاء' },
      ] },
    ],
  },
  {
    slug: 'classic-gate-detail',
    title: 'بوابة معدنية كلاسيكية',
    category: 'أعمال تفصيلية',
    summary:
      'بوابة معدنية سوداء داخل حيط أبيض مزخرف. هذا النوع من الأعمال التكميلية ينسّق الطابع العام للمبنى، وننفّذه بنفس معيار الدقة في Stone.',
    scope: ['أعمال حديد', 'تكملة الواجهة', 'تنسيق'],
    duration: 'غير محدد',
    cover: '/images/projects/p06-classic-gate.jpg',
    coverAlt: 'بوابة معدنية سوداء داخل حيط أبيض مزخرف في مبنى كلاسيكي',
    stages: [
      { label: 'بعد', note: 'عمل مكتمل', images: [
        { src: '/images/projects/p06-classic-gate.jpg', alt: 'البوابة المعدنية بعد التركيب' },
      ] },
    ],
  },
  {
    slug: 'arched-block-structure',
    title: 'هيكل معماري بأقواس',
    category: 'تحت التنفيذ',
    summary:
      'هيكل مبنى بالبلوك بأقواس نافذة وعمود خرساني. مشروع سكني ما زال في مرحلة الجدران، ونحن مسؤولون عن مرحلة الواجهة والتشطيب لاحقاً.',
    scope: ['استشارات', 'واجهات لاحقة', 'تشطيب'],
    duration: 'غير محدد',
    cover: '/images/projects/p05-wip-arched-blocks.jpg',
    coverAlt: 'هيكل مبنى بالبلوك بأقواس نافذة وعمود خرساني، معماري قيد الإنشاء',
    stages: [
      { label: 'قبل', note: 'مرحلة الهيكل والبلوك', images: [
        { src: '/images/projects/p05-wip-arched-blocks.jpg', alt: 'الهيكل بالبلوك والأقواس قبل التشطيب' },
        { src: '/images/projects/p11-wip-block-arches.jpg', alt: 'هيكل بلوك بأقواس وسقالات خشبية' },
        { src: '/images/projects/p23-wip-grey-arch.jpg', alt: 'أقواس خرسانية في مرحلة البناء' },
      ] },
    ],
  },
  {
    slug: 'block-arches-structure',
    title: 'هيكل بلوك بأقواس',
    category: 'تحت التنفيذ',
    summary:
      'مبنى متعدد الطوابق في مرحلة الهيكل بالبلوك، مع أقواس نافذة في الطابق الأرضي وسقالات خشبية ومواد بناء في المقدمة. مشروع سكني قيد الإنشاء.',
    scope: ['استشارات', 'واجهات لاحقة', 'تشطيب'],
    duration: 'غير محدد',
    cover: '/images/projects/p11-wip-block-arches.jpg',
    coverAlt: 'مبنى بالبلوك تحت الإنشاء بأقواس نافذة وحواف بلاطات وسقالات خشبية في المقدمة',
    stages: [
      { label: 'قبل', note: 'مرحلة الهيكل', images: [
        { src: '/images/projects/p11-wip-block-arches.jpg', alt: 'هيكل البلوك بأقواس' },
        { src: '/images/projects/p12-wip-tall-scaffold.jpg', alt: 'مبنى عالي بسقالات' },
      ] },
    ],
  },
  {
    slug: 'tall-building-scaffold',
    title: 'مبنى عالي قيد الإنشاء',
    category: 'تحت التنفيذ',
    summary:
      'مبنى عالي متعدد الطوابق تحت الإنشاء مع سقالات على الجانب. مشروع في مرحلة متقدمة من البناء، وما زال ضمن نطاق أعمالنا للواجهة والتشطيب.',
    scope: ['واجهات', 'تشطيب', 'تنسيق'],
    duration: 'غير محدد',
    cover: '/images/projects/p12-wip-tall-scaffold.jpg',
    coverAlt: 'مبنى عالي تحت الإنشاء بسقالات على الجانب وسياج إنشائي في المقدمة',
    stages: [
      { label: 'قبل', note: 'مرحلة البناء المتقدمة', images: [
        { src: '/images/projects/p12-wip-tall-scaffold.jpg', alt: 'المبنى العالي مع السقالات' },
        { src: '/images/projects/p31-unknown-2.jpg', alt: 'هيكل خرساني في مرحلة البناء' },
      ] },
    ],
  },
  {
    slug: 'mosque-restoration',
    title: 'ترميم مبنى بقوس ذهبي',
    category: 'ترميم وصيانة',
    summary:
      'مبنى أبيض بزخارف قوسية ومئذنة ذهبية تحيط بها سقالات. مشروع ترميم где ركبنا ونجدّد الزخارف الحجرية حول الأقواس مع الحفاظ على الطابع الأصلي.',
    scope: ['ترميم', 'تجديد الزخارف', 'أعمال سقالات'],
    duration: 'غير محدد',
    cover: '/images/projects/p08-mosque-renovation.jpg',
    coverAlt: 'مبنى أبيض بزخارف قوسية ومئذنة ذهبية تحيط بها سقالات وأرض ترابية',
    stages: [
      { label: 'أثناء', note: 'مرحلة الترميم', images: [
        { src: '/images/projects/p08-mosque-renovation.jpg', alt: 'المبنى أثناء الترميم مع المئذنة الذهبية' },
      ] },
    ],
  },
  {
    slug: 'lounge-interior',
    title: 'صالة داخلية فاخرة',
    category: 'أعمال داخلية',
    summary:
      'صالة داخلية بجدران رخامية مخططة وأعمدة وزخارف جصية. صورة توثيقية لأعمال التشطيب الداخلي التي ننفّذها على الشقق والفلل.',
    scope: ['تشطيب داخلي', 'جدران رخامية', 'أعمال جبس وزخارف'],
    duration: 'غير محدد',
    cover: '/images/projects/p29-lounge-interior.jpg',
    coverAlt: 'صالة داخلية بجدران رخامية مخططة وأعمدة وزخارف جصية',
    stages: [
      { label: 'بعد', note: 'تشطيب مكتمل', images: [
        { src: '/images/projects/p29-lounge-interior.jpg', alt: 'الصالة بعد التشطيب الكامل' },
      ] },
    ],
  },
  {
    slug: 'interior-arch-detail',
    title: 'مدخل داخلي بقوس حجري',
    category: 'أعمال داخلية',
    summary:
      'مدخل داخلي بقوس حجري منحوت وباب خشبي. عمل تطبيقي علىphem details الداخلية، وتعكس دقة التنفيذ التي نتبعها في كل التفاصيل الصغيرة.',
    scope: ['تشطيب داخلي', 'أعمال النحت', 'أبواب خشبية'],
    duration: 'غير محدد',
    cover: '/images/projects/p30-interior-arch.jpg',
    coverAlt: 'مدخل داخلي بقوس حجري منحوت وباب خشبي وأزهار بيضاء',
    stages: [
      { label: 'بعد', note: 'تشطيب مكتمل', images: [
        { src: '/images/projects/p30-interior-arch.jpg', alt: 'المدخل الداخلي بالقوس بعد التشطيب' },
      ] },
    ],
  },
];

export default PROJECTS_FULL;