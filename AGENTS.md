# Content design LMS

Repository: Pythonidaer/content-design-lms, main. GitHub Pages is the deployment target. graphql-lms is the learner-shell reference, not the content source or destination.

Read DESIGN_DECISIONS.md before design changes. Preserve course-source mapping, original examples, the Start / Explore / Tone order, and the explicit scope limits. Edit build_course.py and regenerate embedded data. All sections start collapsed and all lessons are available by default.

No emojis or text-character icon substitutes. Use the existing SVG control family or clear text. Keep visible numbering unpadded, action targets usable, keyboard focus visible, and inputs at least 16px. Preserve the GOV.UK-inspired palette without suggesting government affiliation. Keep the frosted header and the existing learner features.

Permanent OpenAI keys must never enter public source, persistent browser storage, exports or logs. Only the localhost helper accepts a session-only permanent key; hosted pages accept ephemeral tokens. Keep voice optional, current-slide-only, time bounded, and explicit about cost estimates. Do not make billable calls in automated tests. No paid key was supplied for live testing.

Run npm test and npm run build, verify embedded parity, and inspect the diff before publishing. DOM checks and mocked WebRTC are not device/browser verification. Report real voice and mobile-layout limitations honestly.
