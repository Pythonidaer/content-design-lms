# Content design LMS decisions

- Reuse graphql-lms's shared learner runtime, Markdown safety, collapsible outline, slide controls, notes, quizzes, reports and course-copy workflow. Replace the GraphQL curriculum and use a unique content-design progress key.
- Start, Explore, then Tone in practice follows the user's requested learning order. Source directory is a reference stage. Core planning/writing pages are adapted; complete A to Z guides are linked rather than squeezed into slides. This is not a complete-site mirror.
- One short idea or activity per slide, with a 110-word automated ceiling. Lessons use a principle, original example, practice, self-check and source links. Ten tone qualities form an authored reference deck with one quality per slide. All sections begin collapsed; every lesson stays available.
- Use GOV.UK-inspired black, white, blue, green and yellow. No government logo, crown or implied endorsement. Keep system sans-serif typography and the shared frosted header. No emoji or character-icon substitutes. Keep actual SVG controls, visible focus, and readable input sizes.
- Optional voice control is placed in the header and its dialog survives learner-shell rerenders. It uses WebRTC for browser audio, not SIP telephony. The assistant receives current slide text through session instructions; it does not automatically see the screen or access ChatGPT memory. Notes and other slides are excluded.
- GitHub Pages accepts ephemeral credentials only. A localhost-only helper accepts an unsaved key or server environment key, verifies same-origin requests, and mints tokens. No shared public secret or unauthenticated hosted token service is deployed.
- Default to a mini model, one-minute sessions, brief replies, manual microphone activation, an inactivity timeout and no automatic reconnection. Estimated costs are conservative usage feedback, not a guaranteed spending cap. Stop audio on close, backgrounding and navigation.
- Verification: course/schema/source tests and DOM integration with all 139 slides; token helper and voice lifecycle tested with mocks. Real model calls, AirPods routing and mobile layout remain unverified. No billable calls were made.


## Voice without an obstructing modal — 2026-10-18

User reported that the active voice dialog covered the slide being discussed. The dialog now handles credentials and connection setup only. Once connected, it closes and a compact nonmodal voice bar is inserted after the learner header in normal document flow. It displays the current slide title, microphone state/session status, read-aloud action, Details, and End conversation. The persistent bar and audio element live outside the modal and remount after learner-shell rerenders.

Closing setup during an established call hides setup without ending the call. Ending the conversation, leaving/backgrounding the page, or reaching the existing limits still stops tracks and closes WebRTC. Closing setup while connection is pending cancels setup. Slide changes update the current supplied text; no notes or hidden slides are added. The existing theme, course data and learner features are unchanged.

Mocked tests verify auto-closing setup, continued connection after hiding, bar remounting, updated context, delegated microphone/read controls, and explicit End cleanup. No paid API call or rendered device verification was performed.
