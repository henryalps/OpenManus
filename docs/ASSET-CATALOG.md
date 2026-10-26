# Nafas visual asset catalog

## Source formats
- Brand marks and static interface icons: SVG master + Android VectorDrawable where appropriate.
- Raster artwork: PNG for transparency, WebP for delivery where suitable; preserve editable originals.
- Motion: Lottie JSON for lightweight vector motion; short WebM/MP4 only when appropriate and tested on target devices.
- Audio: licensed/owned OGG or AAC, normalized and size-budgeted.

## Initial source assets
- Brand: `assets/brand/nafas-mark.svg`
- Microphone: `assets/icons/microphone.svg`
- Speaker seat: `assets/icons/room-seat.svg`
- Gift: `assets/icons/gift.svg`
- VIP badge: `assets/icons/vip.svg`
- Profile frame: `assets/icons/profile-frame.svg`
- Android vector icon: `app/src/main/res/drawable/nafas_app_icon.xml`

## Remaining production asset work
Room themes and backgrounds, complete seat states (available/speaking/muted/owner/moderator), gift animation set, VIP levels, profile frames by tier, badges, empty/error/loading states, store screenshots, app icon adaptive layers, and Arabic typography QA. Every asset must be tested in RTL layouts, at multiple densities, and on low-memory devices. Do not ship placeholder or unlicensed content.