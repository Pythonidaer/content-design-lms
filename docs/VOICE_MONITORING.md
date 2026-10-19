# Voice monitoring: first investigation

The reported bug is still open: audio stops mid-word with AirPods and microphone muted while the session timer continues. The first hosted trace confirms a response limit: `response.done` was `incomplete` with `max_output_tokens` at 03:23:07.623 UTC, audio drained at 03:23:13.820, and the user ended the still-connected call at 03:23:26.260. This identifies the cause in that session. The output budget is now 2,048; verify with a fresh session before declaring the symptom resolved on the device. Moving to Vercel alone was not the fix.

## Establish the hosted workflow

Verify password login, icon visibility after refresh, anonymous API rejection, token creation, and sign out first. Keep the one-minute default session and existing usage thresholds. No billable model calls were made by automated tests. Device audio routing and real Vercel delivery require manual review.

## Monitoring versus observability

Monitoring tells us whether requests succeeded and how long they took. Observability helps explain a failure by correlating response events, connection state and audio playback behavior.

| Signal | Where to look | What it can tell us |
| --- | --- | --- |
| Login/token request status and duration | Vercel project → Logs | Backend startup, configuration, authentication or upstream failures |
| Request ID | API response header/body and `api.session` diagnostic | Match a successful token request to its server log |
| `response.done` status/reason | Modal → Connection diagnostics | Complete, incomplete or cancelled generation; output-limit reason if supplied |
| `audio.pause`, `audio.waiting`, `audio.stalled`, `audio.error` | Connection diagnostics | Playback interruption signals; events alone do not prove a cause |
| `remote.track.mute`, `peer.state`, `channel.closed` | Connection diagnostics | Track/transport interruptions |
| `session.stopped` reason | Connection diagnostics | Application timeout, explicit End, cost threshold or backgrounding |
| Dollar spend | OpenAI usage dashboard | Actual billed API usage; app usage is an estimate |

## Reproduce without guessing

1. Start a one-minute hosted session on a known slide. Keep the microphone muted and select Read this slide. Stay on the page.
2. If audio cuts off, note approximately when and whether text keeps growing. Before ending, open the microphone setup and copy Connection diagnostics.
3. Record browser/version, AirPods versus computer speaker, and whether the microphone was muted. Repeat once using computer speakers to compare. Do not repeatedly incur charges if one trace already isolates a cause.
4. Match the response completion reason and media/connection events. An incomplete generation is different from complete text whose audio playback was interrupted. No event is proof without the reproduction timing.
5. Change the implicated behavior and rerun the same case. Avoid changing output budgets, timers and playback routing simultaneously.

Diagnostics are held in memory, reset at session start and capped at 160 events. They exclude transcripts, slide text, notes, keys, tokens, cookies, IP addresses, SDP and audio recordings. Copying diagnostics does not automatically upload them. Vercel server logs include only event name, request ID, status and duration. They do not receive browser audio/playback logs; share a copied trace explicitly to correlate it. Vercel logs cover token creation, not the ongoing peer-to-peer audio stream.

Instance-local login/token throttling is not a durable global quota. Configure Vercel Firewall rules for login/API abuse protection and keep OpenAI project spending controls. No external analytics or monitoring subscription is added.

## What this trace taught us

The session remained connected after the response ended. Response generation finished at the configured token ceiling, then already-buffered audio played for about six more seconds. There was no track, peer or playback failure event before that cutoff. That is stronger evidence for generation truncation than an AirPods routing failure in this trace. Text and audio generation have output budgets; a short text-sized ceiling can be too small for speech. Raising the ceiling allows more generation and can increase actual spend, while brief-response instructions and existing session/spend controls remain in place.
