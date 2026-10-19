# Voice monitoring

## Test the hosted workflow

Verify password login, microphone icon visibility after refresh, session startup, read-aloud, End and Sign out. Automated tests use mocks; device audio and production delivery require manual review.

## Monitoring and observability

Monitoring tells us whether a request succeeded and how long it took. Observability helps explain a failure using response, connection and playback signals together.

| Signal | Location | Purpose |
| --- | --- | --- |
| Request status and duration | Vercel project logs | Find configuration, authentication or upstream failures |
| Request ID | API response and diagnostics | Correlate token creation with backend logs |
| Response status and completion reason | Usage and diagnostics | Distinguish completed, incomplete, cancelled and failed responses |
| Playback and track events | Usage and diagnostics | Identify playback or transport changes |
| Session stop reason | Usage and diagnostics | Identify a timer, explicit End or other application stop |
| Actual API spend | OpenAI usage dashboard | Compare billing with the app's estimated cost |

## Investigate a cutoff

1. Use one slide and a repeatable question. Keep the page open during the test.
2. If speech stops unexpectedly, open Usage and diagnostics and copy diagnostics before starting another session.
3. Compare generation completion with playback and connection events. An incomplete response differs from completed generation whose playback was interrupted.
4. Change one implicated behavior, then repeat the same case.

The response ceiling is 2,048 tokens per reply. A higher ceiling can permit more generation and spending; brief-answer instructions and existing session/usage controls remain in place. Diagnostics include the configured ceiling so the tested version can be checked.

## Privacy and limits

Browser diagnostics stay in memory, reset at session start and are capped at 160 events. They exclude transcripts, slide text, notes, credentials, SDP, recordings and IP addresses. Copying does not upload them automatically. Backend logs include only event name, request ID, HTTP status and duration. Backend logs cover token creation, not the ongoing audio stream. Review copied logs before sharing them; detailed session traces do not belong in a public repository without explicit permission.

Instance-local throttling is not a global quota. Use Vercel Firewall controls for durable API abuse protection and OpenAI project spending controls. No external monitoring subscription is required for these initial checks.
