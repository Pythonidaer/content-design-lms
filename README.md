# Content design LMS

A slide-based content-design course using the learner setup from [graphql-lms](https://github.com/Pythonidaer/graphql-lms). This is an independent learning project, not a GOV.UK service or an official government course.

Live course: https://pythonidaer.github.io/content-design-lms/

## Learning path

1. **Start:** content design, user needs, scope/format, and drafting with prototypes.
2. **Explore:** planning, organisation, structure, language, titles, summaries, links, accessibility, translation, URLs, maintenance, retirement, change communication, style guides, and evaluation.
3. **Tone in practice:** voice versus tone, NN/g's dimensions, GOV.UK's approach, comparing and testing tone, ten authored tone qualities, and a capstone.
4. **Sources:** an annotated scope slide and the complete source directory.

Includes **26 lesson decks, 139 slides, three knowledge checks, and a 12-question final review**. The final reuses the knowledge-check questions with explanations; it is review, not an independent examination. Practice tasks and capstone drafts are self-assessed. Each short lesson has a principle, original example, practice task, worked self-check, and source links. Tone qualities are an authored reference, not an official taxonomy.

The content-design subject is broader than the LMS delivery medium: examples include public services, forms, websites, and communications. Learners can use their own content as a practice project.

## GOV.UK source scope

Start with [Understand content design](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/understand-content-design/), then explore [Writing to GOV.UK standards](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/).

`source-manifest.json` inventories 27 sources and maps them to lessons. The course contains original concise summaries of the core planning/writing topics directly linked from the writing-standards section. The A to Z and technical A to Z guides are linked lookup references, not exhaustively reproduced. It does not claim to include every GOV.UK publication, publishing-tool instruction, specialist style entry, or linked research paper. See THIRD_PARTY_NOTICES.md.

## Learner setup

Borrowed from GraphQL LMS: collapsible outline, slide player, notes, completion, quizzes and retakes, skill reports/CSV, learner preferences, and Copy entire course. Sections start collapsed; all lessons and assessments are available by default. Turn off Unlock all in Learner settings for the inherited final-review gate. Progress is local to this course and browser; clearing browser data removes it. No account or cross-device sync is provided.

The white/black/blue/green/yellow palette is inspired by the GOV.UK Design System. No crown, government wordmark, or proprietary government typeface is used. The existing shared frosted header, SVG controls, readable mobile inputs, plain numbering, and no-emoji rules are preserved.

## Voice setup

The top **Talk about this slide** button opens an OpenAI Realtime WebRTC tutor. It receives only the current visible slide, not your notes, hidden slides, complete course, or ChatGPT history. It can discuss the slide or read it aloud. A transcript is available during the session. Voice is optional; all course content works without it.

**GitHub Pages cannot run the secret-key helper. Never put a permanent OpenAI key into public source or browser storage.**

### Simplest private setup: run locally

Requires Node 22+.

```sh
npm install
npm start
```

Open http://127.0.0.1:8787. Select a slide, press Talk about this slide, and enter your API key into the local panel. The key is forwarded only to the helper on this computer to mint a short-lived token, then the field is cleared. It is not saved or logged. Alternatively set `OPENAI_API_KEY` in the helper's environment and leave the field blank. Credentials stay out of localStorage, course exports, and GitHub.

### Using the hosted GitHub Pages course

Create an ephemeral token on a trusted computer with `OPENAI_API_KEY` set in its environment:

```sh
node token.cjs
```

Paste the printed `ek_` token into the hosted voice panel promptly; it has a 60-second connection window. Token expiry does not end a connected session. A permanent `sk-` key is rejected by the hosted page. An authenticated hosted token helper would remove this manual step and is a future deployment task; none is currently deployed.

After connecting, use Enable microphone to talk or Read this slide to hear it. AirPods follow the browser/device's selected audio route; the site cannot force iOS output selection. Closing the panel, ending the session, hiding the page, or leaving stops tracks and closes the connection. Slide changes replace the supplied slide context; previous conversation turns may still refer to an earlier slide.

### Costs and limits

Default model: `gpt-realtime-2.1-mini`, verified in official OpenAI documentation on 2026-10-18. Default session: one minute; selectable maximum three minutes. Conversation replies are limited to 256 output tokens; an explicitly requested slide reading can use up to 768. The session stops after 30 seconds without activity or after approximately $0.10 in reported usage. Estimates are computed from response usage at the documented text/audio rates and conservatively do not apply cached discounts. Other fees or billing adjustments are not included. Usage arrives after turns, so the threshold can be exceeded. Client timers and estimates are convenience controls, **not a guaranteed billing cap**. No automatic reconnection or session restart occurs.

API access and billing are separate from a ChatGPT subscription. Use project-level spending controls where available and review actual API usage. Live API calls, real audio quality, model availability for your project, and AirPods routing have not been tested with a paid key in this environment. No billable model calls were made during development.

Official references:
- https://developers.openai.com/api/docs/guides/voice-webrtc
- https://developers.openai.com/api/reference/resources/realtime/subresources/client_secrets/methods/create
- https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini
- https://developers.openai.com/api/reference/overview

## Development and deployment

```sh
npm ci
npm test
npm run build
```

Edit `build_course.py` and run it to regenerate `course.json`, embedded index data, and the source manifest. Keep IDs stable; changing a lesson's fingerprint resets that lesson's saved progress. The learner runtime and theme are separate from the curriculum. `voice-config.js` owns the model, prompt and cost estimate.

GitHub Actions runs tests and publishes only public learner files through Pages. The server, token script, tests, source generator, package dependencies, and credentials are not uploaded as the Pages artifact. Enable Pages with GitHub Actions if the repository settings have not already enabled it.

Tests verify course readiness, embedded parity, bounded slides, source mapping, quiz answers, all 139 rendered slides through a DOM environment, completion, reports, and mocked voice/token behavior. They do not establish rendered layout, real WebRTC transport, or actual microphone playback. Mobile Safari, larger displays, voice interruption, and AirPods need device review.
