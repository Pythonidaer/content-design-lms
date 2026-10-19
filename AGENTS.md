# Content design LMS

Repository: Pythonidaer/content-design-lms, main. Vercel is the private hosted-voice target; GitHub Pages remains a static alternative. graphql-lms is the learner-shell reference, not the content source or destination.

Read DESIGN_DECISIONS.md before design changes. Preserve course-source mapping, original examples, the Start / Explore / Tone order, and the explicit scope limits. Edit build_course.py and regenerate embedded data. All sections start collapsed and all lessons are available by default.

No emojis or text-character icon substitutes. Use the existing SVG control family or clear text. Keep visible numbering unpadded, action targets usable, keyboard focus visible, and inputs at least 16px. Preserve the GOV.UK-inspired palette without suggesting government affiliation. Keep the frosted header and the existing learner features.

Permanent OpenAI keys must never enter public source, persistent browser storage, exports or logs. The localhost helper may save a key only when the user opts in, in ~/.config/content-design-lms/voice.json outside the repository. Hosted pages may forward a user-entered key only to that helper; OpenAI browser sessions use ephemeral tokens. The helper trusts only localhost and the exact production origin; never serve or return the saved key. Keep voice optional, current-slide-only, time bounded, and explicit about cost estimates. Do not make billable calls in automated tests. No paid key was supplied for live testing.

Run npm test and npm run build, verify embedded parity, and inspect the diff before publishing. DOM checks and mocked WebRTC are not device/browser verification. Report real voice and mobile-layout limitations honestly.

Hosted voice uses api/voice.mjs and lib/hosted-voice.cjs. Enforce server-side password verification, signed HttpOnly cookies and same-origin JSON POST for voice tokens; hiding the login or icon is not authorization. Secrets are Vercel server environment variables only. Keep the public learner course accessible. No database is required. Do not claim instance-local rate limits are globally enforced or that the unresolved audio cutoff is fixed. Diagnostic logs must never include credentials, transcripts, slide text, SDP or raw audio.
