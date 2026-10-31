# Иллюстрации блога

Серия создана 31 октября 2026 года встроенным инструментом imagegen. Стиль - графичное тёмное фэнтези: крупные цветовые плоскости, угловатые силуэты, рваные края, мантии и образованные герои. Визуальный ориентир пользователя - «умные герои Diablo». Персонажи придуманы для блога; изображения не служат портретами автора. Сторонние иллюстрации не использовались.

| Файл в `docs/assets/images/` | Сюжет | Размещение |
| --- | --- | --- |
| `evangi-raven-emblem.webp` | Ворон-учёный с гримуаром и компасом-шестерёнкой | Общая шапка, 80/64/48/40 px |
| `bull-bear-study.webp` | Бык и медведь над общим учебником | Главная, до 180 px по высоте |
| `developer-study-desk.webp` | Учёный-программист за столом, со спины | Вступление «Обо мне», справа |
| `about-learning-route.webp` | Героиня-картограф с картой и компасом | Учебный план, слева |
| `about-investment-workbench.webp` | Мастер-аналитик собирает механизм | Система инвестирования, справа |
| `about-research-journal.webp` | Летописец с журналом и вороном | Зачем нужен блог, слева |

В «Обо мне» изображения отображаются размером до 315×210 px, не более 45% ширины текста, с зазором 24 px. Первая картинка стала примерно на 30% меньше прежних 450×300 px. На узком экране обтекание выключается, текст идёт полной строкой; изображения занимают до 70% ширины и сохраняют чередование сторон. Разметка - `docs/about.md`, стили - классы `about-illustration` в `docs/stylesheets/site.css`.

Веб-версии экспортированы установленным `cwebp` с параметрами `-q 88 -alpha_q 100 -m 6 -metadata all`, без изменения размеров. Альфа-канал сохранён. Исходные PNG остаются в каталоге генератора, а страницы используют только локальные WebP из репозитория. Подписи находятся в HTML `figcaption` и набраны шрифтом сайта; в изображениях нет имён или логинов.

Эмблема шапки создана тем же встроенным инструментом imagegen по визуальному образцу основной серии. Название «Evangi · Гримуар капитала» и девиз «Магия начинается с матчасти.» набраны живым текстом сайта; они не встроены в рисунок.

## Финальные промпты

Первый рисунок создаёт образец стиля. Остальные используют его только как визуальный ориентир и показывают самостоятельные сцены.

### `bull-bear-study.webp`

```text
Use case: illustration-story.
Asset type: small horizontal illustration for a personal blog about learning finance, mathematics and code.
Scene: a bull and a bear as two ORIGINAL learned dark-fantasy adventurers, leaning over ONE shared open textbook. The bull holds a little chart rising, the bear a little chart falling; both are silently trying to understand the same geometric problem in the book. A tiny old calculator beside the book gives a dry anachronistic joke. Adult, clever, slightly stern characters rather than cute mascots.
Art direction: FLAT, ROUGH, ANGULAR 2D DARK FANTASY GAME ILLUSTRATION, like scholarly heroes from a grim action RPG. Build forms from large clearly separated flat color shapes, sharp planes, torn-paper-like silhouettes, ragged cloak hems and broken dry-brush edges. Strong rough ink contours, a few scratchy strokes. Limited colors: charcoal, bone ivory, desaturated steel blue, rusty ochre and a small ember-red accent. Stylized dark leather/armor and hooded scholar's cloth. Fur is suggested by a few jagged graphic masses, NOT individual realistic hairs.
This must be much flatter and more graphic than cinematic concept art: no photorealism, no smooth 3D rendering, no realistic fur texture, no soft airbrushed gradients, no cuddly rounded children's-book look. Distinct angular faces, restrained expressions and readable silhouettes at 180 pixels high. Original characters, no existing game logos or named characters.
Composition: compact low and WIDE approximately 3:1, both heads and the book clearly visible, modest clean margins. One single scene, no panel borders. Keep the textbook the shared focus.
Background: TRUE TRANSPARENT ALPHA outside the subjects, table and ragged graphic edges. No black rectangle, scenery, gradient vignette, opaque parchment background or checkerboard. It must look clean on a white webpage.
Text: no readable words, captions, letters, names or watermark; only simple chart and geometric marks.
```

### `developer-study-desk.webp`

```text
Use case: illustration-story.
Input image 1: STYLE REFERENCE ONLY. Create a NEW companion scene matching the bull-and-bear image's FLAT, ROUGH, ANGULAR 2D DARK FANTASY GAME ILLUSTRATION. Think intelligent scholar-adventurers from a grim action RPG: original learned heroes, tattered cloaks, graphic shapes and dry wit.
Match the reference's large flat color masses, sharp planar shading, rough broken ink contours, ragged brush edges and torn-paper-like silhouettes. Limited charcoal, bone ivory, dark desaturated steel blue, rusty ochre and muted ember-red accents. Fine detail is subordinate to a strong readable silhouette. NO photorealism, realistic fine texture, glossy 3D rendering, soft cinematic gradients, cute rounded children's-book characters or smooth corporate vector art.
Composition: one compact landscape 3:2 vignette, readable around 300 pixels wide, modest margins. The scene should feel different from the other illustrations rather than repeating the same desk and books.
Background: genuine TRANSPARENT ALPHA outside the jagged character and prop silhouettes. No rectangle, scene backdrop, external gradient glow, opaque parchment panel or checkerboard. The drawing goes on a WHITE webpage.
Text and privacy: no captions, readable words, names, usernames, logos or watermark. Only geometric marks, abstract code strokes, question marks or simple charts as relevant. No named existing game characters.
Scene: an anonymous scholarly MAGE-PROGRAMMER at a compact work desk, seen from behind and a little to the side so his face remains hidden. He wears a ragged dark blue hooded mantle with angular worn leather trim, studying an open geometric textbook while holding a pencil. A modern laptop with abstract code strokes and a small green checkmark sits beside it, plus a mug with a question-mark sticky note. The modern laptop in an old scholar's setting supplies quiet anachronistic humor. Keep this scene intimate and thoughtful, not a combat pose. It is the introductory illustration about a developer learning finance, not a real person's portrait.
```

### `about-learning-route.webp`

```text
Use case: illustration-story.
Input image 1: STYLE REFERENCE ONLY. Create a NEW companion scene matching the bull-and-bear image's FLAT, ROUGH, ANGULAR 2D DARK FANTASY GAME ILLUSTRATION. Think intelligent scholar-adventurers from a grim action RPG: original learned heroes, tattered cloaks, graphic shapes and dry wit.
Match the reference's large flat color masses, sharp planar shading, rough broken ink contours, ragged brush edges and torn-paper-like silhouettes. Limited charcoal, bone ivory, dark desaturated steel blue, rusty ochre and muted ember-red accents. Fine detail is subordinate to a strong readable silhouette. NO photorealism, realistic fine texture, glossy 3D rendering, soft cinematic gradients, cute rounded children's-book characters or smooth corporate vector art.
Composition: one compact landscape 3:2 vignette, readable around 300 pixels wide, modest margins. The scene should feel different from the other illustrations rather than repeating the same desk and books.
Background: genuine TRANSPARENT ALPHA outside the jagged character and prop silhouettes. No rectangle, scene backdrop, external gradient glow, opaque parchment panel or checkerboard. The drawing goes on a WHITE webpage.
Text and privacy: no captions, readable words, names, usernames, logos or watermark. Only geometric marks, abstract code strokes, question marks or simple charts as relevant. No named existing game characters.
Scene: a female hooded CARTOGRAPHER-SCHOLAR on a journey, shown from the thighs up in three-quarter view, facing toward the RIGHT. She studies an unfurled parchment with a large clear SPIRAL learning route and a few geometric checkpoints. A brass compass is in her gloved hand; her tattered mantle and travel satchel make a distinctive angular silhouette. The map and compass communicate planning, revisiting topics and learning. No table, laptop or stacks of books in this scene. Her expression is focused and inquisitive. No battle or treasure map labels.
```

### `about-investment-workbench.webp`

```text
Use case: illustration-story.
Input image 1: STYLE REFERENCE ONLY. Create a NEW companion scene matching the bull-and-bear image's FLAT, ROUGH, ANGULAR 2D DARK FANTASY GAME ILLUSTRATION. Think intelligent scholar-adventurers from a grim action RPG: original learned heroes, tattered cloaks, graphic shapes and dry wit.
Match the reference's large flat color masses, sharp planar shading, rough broken ink contours, ragged brush edges and torn-paper-like silhouettes. Limited charcoal, bone ivory, dark desaturated steel blue, rusty ochre and muted ember-red accents. Fine detail is subordinate to a strong readable silhouette. NO photorealism, realistic fine texture, glossy 3D rendering, soft cinematic gradients, cute rounded children's-book characters or smooth corporate vector art.
Composition: one compact landscape 3:2 vignette, readable around 300 pixels wide, modest margins. The scene should feel different from the other illustrations rather than repeating the same desk and books.
Background: genuine TRANSPARENT ALPHA outside the jagged character and prop silhouettes. No rectangle, scene backdrop, external gradient glow, opaque parchment panel or checkerboard. The drawing goes on a WHITE webpage.
Text and privacy: no captions, readable words, names, usernames, logos or watermark. Only geometric marks, abstract code strokes, question marks or simple charts as relevant. No named existing game characters.
Scene: a broad-shouldered dark-fantasy SCHOLAR-ARTIFICER in a worn ember-red cowl, shown at three-quarter profile facing LEFT, carefully assembling a compact analytical mechanism. One gauntleted hand holds a toothed brass component; the other steadies an angular astrolabe-like construction with coherent interlocking gears. Beside the mechanism hang two small parchment chart panels with zigzags that rise AND fall, like an experiment to test rather than predict a guaranteed result. A half-open design ledger at the base has simple diagrams. The character's posture is methodical and absorbed, not triumphant. Do not repeat the laptop desk scene. No coins, treasure, money printer or weapon.
```

### `about-research-journal.webp`

```text
Use case: illustration-story.
Input image 1: STYLE REFERENCE ONLY. Create a NEW companion scene matching the bull-and-bear image's FLAT, ROUGH, ANGULAR 2D DARK FANTASY GAME ILLUSTRATION. Think intelligent scholar-adventurers from a grim action RPG: original learned heroes, tattered cloaks, graphic shapes and dry wit.
Match the reference's large flat color masses, sharp planar shading, rough broken ink contours, ragged brush edges and torn-paper-like silhouettes. Limited charcoal, bone ivory, dark desaturated steel blue, rusty ochre and muted ember-red accents. Fine detail is subordinate to a strong readable silhouette. NO photorealism, realistic fine texture, glossy 3D rendering, soft cinematic gradients, cute rounded children's-book characters or smooth corporate vector art.
Composition: one compact landscape 3:2 vignette, readable around 300 pixels wide, modest margins. The scene should feel different from the other illustrations rather than repeating the same desk and books.
Background: genuine TRANSPARENT ALPHA outside the jagged character and prop silhouettes. No rectangle, scene backdrop, external gradient glow, opaque parchment panel or checkerboard. The drawing goes on a WHITE webpage.
Text and privacy: no captions, readable words, names, usernames, logos or watermark. Only geometric marks, abstract code strokes, question marks or simple charts as relevant. No named existing game characters.
Scene: a lean hooded CHRONICLER-SCHOLAR in a dark charcoal mantle, shown from the waist up in three-quarter view facing RIGHT. He writes with a large ivory quill in an oversized open research journal supported on his lap. A small angular raven familiar on the book's edge holds a loose paper bookmark in its beak, as if helpfully stealing it. Both look attentively at the page. The journal has only abstract handwriting strokes and small simple diagrams, not readable words. Make the silhouette and pose clearly distinct from the cartographer and artificer. No large table or laptop; dry, gentle visual humor rather than horror.
```

### `evangi-raven-emblem.webp`

```text
Use case: logo-brand.
Asset type: compact square header emblem for a personal Russian blog named Evangi · Гримуар капитала, whose motto means "Magic starts with the fundamentals".
Input image 1: STYLE REFERENCE ONLY. Match this series' flat angular dark-fantasy game illustration, strong broken ink contours, large separated color shapes, ragged/torn cloak edges and restrained dry-brush marks.
Subject: one clever, slightly stern RAVEN-SCHOLAR in a tattered dark blue hood, perched closely on and protectively holding ONE closed old grimoire. On the book's visible cover is a single large simple brass medallion combining a gear outline and a compass needle. The joke is how seriously this scholar guards a textbook. Clear raven beak and alert eye, original character.
Composition: a centered compact SQUARE emblem with very small safe outer margins, no frame or shield border. The bird, hood and book form one strong recognizable silhouette. It must stay readable at 64–80 pixels high: few large shapes, minimal small detail. Book and medallion large enough to remain distinct.
Palette: charcoal, desaturated steel blue, aged ivory pages, rusty ochre/brass and one small muted ember-red ribbon. Flat graphic shadows and angular feather masses. No individual realistic feathers, photorealistic rendering, glossy 3D, smooth gradients or cute pastel mascot treatment.
Background: GENUINE TRANSPARENT ALPHA outside the raven and book's ragged edges. No black rectangle, backdrop, glow, paper texture, scenery, vignette or checkerboard. The emblem will sit on a white website header.
Text: no letters, words, initials, name, motto, labels or watermark embedded in the artwork; the website renders all typography separately. No extra characters or props, no recognizable existing game logos or characters.
```
