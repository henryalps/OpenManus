# Nafas — Product Plan

## Goal
Build an original Arabic-first social voice-room Android app with a consistent, production-oriented design system.

## Planned modules
- Brand identity and exportable visual assets (SVG/PNG/WebP/Lottie as appropriate)
- Home and room discovery
- Live voice rooms, speaker seats, listener view, mute and moderator controls
- Authentication and user profiles
- Friend list, direct messages and notifications
- Room ownership, moderators, reporting, blocking and audit logs
- Gifts and animations
- VIP entitlements and purchase verification
- Backend API, database, rate limiting and authorization checks
- Admin dashboard, moderation tools, analytics and operational monitoring
- Accessibility, Arabic RTL, device-size support, automated tests and release signing

## Current implementation status
The first commit on this branch is only a starter Android shell with a sample Arabic home screen and a CI build workflow. It is not a complete product: authentication, real-time audio, backend, moderation, payments, full asset library, tests and production release configuration remain to be implemented and verified.

## Production acceptance criteria
- No secret keys committed to source control
- Server-authoritative role and VIP checks
- Verified payment receipts and entitlement handling
- Privacy policy, terms, data deletion and user-report flows
- Automated unit/UI tests and successful CI builds
- Load, network interruption and audio-device testing
- Signed release build and Play Console compliance review
