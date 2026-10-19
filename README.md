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

## Private voice on Vercel

The course stays public. Voice is private and its microphone icon is hidden until server-verified login. No database is needed. A signed HttpOnly/Secure/SameSite=Strict cookie remembers login for 12 hours. The shortcut is a UI convenience, not an access control: direct API requests require the signed cookie too.

1. Import `Pythonidaer/content-design-lms` at https://vercel.com/new . Use **Other**, repository root, and Node 22. `vercel.json` supplies the build command and `site-dist` output. Source API functions live in `api/`; only the public allowlist is copied to the static output. The Vercel build uses committed/generated curriculum files; run `npm run build` locally when editing the course.
2. Add these server-only environment variables in Vercel, then deploy:

| Variable | Value |
| --- | --- |
| `OPENAI_API_KEY` | Your OpenAI `sk-` API key |
| `VOICE_PASSWORD` | A unique password, at least 16 characters |
| `VOICE_SESSION_SECRET` | A random signing secret, at least 32 characters |

Generate a signing secret on your computer with `node -e "console.log(require('node:crypto').randomBytes(32).toString('hex'))"`. Never prefix these variables with `NEXT_PUBLIC_` or `VITE_`, commit them, or paste them into chat. Use Vercel's Secret option if available. Environment changes require redeployment. Optional `APP_ORIGIN` pins POST requests to one exact origin, such as `https://your-course.vercel.app` without a trailing slash; omit it to use the request's origin and allow Vercel preview deployments.

3. Visit the deployed site. Press **Ctrl+Shift+L** (Windows/Linux) or **Cmd+Shift+L** (Mac). If the browser intercepts that shortcut, or you are on mobile, open `https://YOUR-VERCEL-DOMAIN/#voice-login` instead.
4. Enter `VOICE_PASSWORD` (use Show password to check typing). The microphone icon appears. Click it and Start conversation; no API-key entry or local process is needed. Sign out is in the voice modal. Login expiry is verified whenever a new voice token is requested. Signing out clears this browser's cookie and stops its active call; it does not revoke a copied cookie or another browser's active call. Rotating either the password or signing secret invalidates existing cookies for future requests.
5. Test: anonymous visitors see no voice icon; wrong password fails; correct password reveals the icon; refresh remembers login; start/read/end works; sign out hides the icon and stops audio. Do not infer the audio cutoff is resolved just because deployment succeeds.

The browser gets only a short-lived OpenAI token. Vercel handles login and token creation; established WebRTC audio flows directly between the browser and OpenAI. Same-origin POST checks, bounded JSON input, timing-safe password comparison and instance-local throttles are included. Serverless instances do not share those throttles: use Vercel Firewall rate limiting for durable brute-force protection and OpenAI project spend controls. No shared anonymous token endpoint is deployed.

GitHub Pages remains a static alternative, using the local helper described below. Existing progress/notes are per-origin: moving from GitHub Pages or localhost to Vercel does not automatically transfer them.

## Voice setup


The header microphone icon opens voice setup. The tutor receives current visible slide text, not notes, hidden slides or ChatGPT history. Setup closes once connected so the slide stays visible. The active bar contains microphone, read-aloud and end controls; the header icon reopens setup and session usage. No duplicate Start again/Details button is shown. An ended call hides the bar.

### Save a key once on this computer

Requires Node 22+ on the same computer as the browser:

```sh
npm start
```

Open either http://127.0.0.1:8787 or https://pythonidaer.github.io/content-design-lms/ . Click the microphone icon, paste your `sk-` key, select **Save on this computer**, and start a conversation. Later, leave the key blank to reuse it. Use **Remove saved key** in the same modal to delete the saved configuration. Saving is opt-in; leaving it unchecked uses the entered key only for that connection. No key is prefilled or returned to the page.

The helper stores plaintext JSON at `~/.config/content-design-lms/voice.json`, outside this repository, with owner-only file permissions on macOS/Linux. This is a simple local file, not encrypted storage or Keychain; protect your user account and backups. No permanent key enters localStorage, exports, logs, Git or the Pages artifact. `OPENAI_API_KEY` in the helper environment is also supported. Explicitly entered keys take priority, then environment, then the saved file.

Keep `npm start` running while using the published site. Chrome may ask for permission to access devices on your local network; allow it for this site to reach the localhost helper. If the browser blocks this connection, use the local URL instead. The helper binds only to 127.0.0.1 and allows CORS only for its own local origin and `https://pythonidaer.github.io` (browser origins cannot distinguish different repository paths on the same GitHub Pages account). Other websites cannot mint tokens through it. A compromised trusted origin, local malware or extensions can still misuse access.

Without the helper, the published site still accepts short-lived `ek_` tokens generated with `node token.cjs`. The helper exchanges a permanent key for a token with a 60-second connection window; expiry does not terminate an established call. AirPods follow the selected system/browser audio route. Leaving/backgrounding the page or reaching the limits ends the call; closing setup during connection cancels it, while closing setup after connection preserves it. Slide changes update the supplied text, but past conversation turns may refer to earlier slides.

### Costs and limits

Default model: `gpt-realtime-2.1-mini`, verified in official OpenAI documentation on 2026-10-18. Default session: one minute; selectable maximum three minutes. Conversation and read-aloud replies allow up to 2,048 output tokens, including audio. The prompt still requests two or three short sentences. This is a maximum, not a fixed charge or requested answer length. The session stops after 30 seconds without activity or after approximately $0.10 in reported usage. Estimates are computed from response usage at the documented text/audio rates and conservatively do not apply cached discounts. Other fees or billing adjustments are not included. Usage arrives after turns, so the threshold can be exceeded. Client timers and estimates are convenience controls, **not a guaranteed billing cap**. No automatic reconnection or session restart occurs.

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

## Voice rollout and monitoring

Phase 1: deploy to Vercel and test login, hidden voice access, refresh, sign out and real session startup. Phase 2: investigate the reported audio cutoff while the session remains connected, including with microphone muted. The first supplied hosted trace identified `response.done` → `incomplete` → `max_output_tokens`. The response budget has since been raised from 256 (768 for read-aloud) to 2,048 across helper, hosted session, browser updates and explicit readings. The fix needs a fresh real-device test; other audio/transport causes are not ruled out. No timeout behavior changed.

The voice modal includes **Usage and diagnostics → Copy diagnostics**. These in-memory events record response completion/reason, connection state and audio playback/track events, never slide text, notes, transcript, API keys, cookies, SDP or recordings. Vercel function logs contain event, status, duration and a request ID. See [voice monitoring guide](docs/VOICE_MONITORING.md) for the first debugging exercise.

### Login setup errors

A server-setup error is not an incorrect-password result: configuration is checked before password verification. The login now names missing variables or password/signing-secret minimum lengths, without displaying their values. If all three variables were added, check that they are assigned to Production in the same Vercel project and redeploy after changing them. Verify that the browser is on the latest Production deployment, rather than an older preview URL. The Show password button changes only the input display and resets to hidden on submit/close.

### Voice dialog design

The modal follows the three AI design reset files in [llm-instruction-toolkit](https://github.com/Pythonidaer/llm-instruction-toolkit/tree/main/design/ai-design-reset), reviewed at 8fcbf905152c911f2350b9bb6105a1ca3a3de5ab. Show the duration, a short privacy/cost notice and the Start action first. Transcript, usage and diagnostic detail are collapsed, while Sign out is a quiet footer action. Voice CSS has a single component section instead of accumulated overrides. Audio configuration and lifecycle are unchanged by this design pass.

### Current-slide voice context

The tutor receives an explicitly labelled heading and body. Navigation updates the session instructions and adds a reference item without requesting an answer. Read this slide captures the current slide again and includes that exact text in the read request. The tutor is instructed to use the supplied text without claiming to see screen pixels or asking for text that is already supplied. Prior slide conversation remains in session history; notes are excluded.

### Voice selection

The default API voice is `cedar`, with a natural British English accent requested in the session instructions. This is an approximation rather than an exact match to a ChatGPT app voice; accent adherence and sound need listening review. Changes take effect in a new voice session after deployment and refresh.

The voice modal includes all ten Realtime voices. Cedar is selected initially; choose another voice before starting a conversation. The selection is locked during connection and playback. End the conversation to select another. The British English accent instruction applies to every choice, so these are not neutral voice previews. No automatic paid preview calls are made.
