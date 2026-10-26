# NAFAS Premium Visual System

## Core art direction
- Product: NAFAS — voice chat rooms, speakers, gifts, profile identity, agencies and moderation.
- Base palette: midnight navy and indigo; accent aqua/sapphire; metallic gold for VIP/host; magenta for social gifts.
- Icon style: bold silhouette, controlled layered gradients, edge highlights, subtle shadows and consistent 256 × 256 viewBox.
- Full-room backgrounds may use a portrait canvas; UI icons should remain transparent.

## Added in this batch
- nafas-gift-diamond-premium.svg
- nafas-gift-rose-premium.svg
- nafas-mic-muted.svg
- nafas-host-badge.svg
- nafas-level-badge.svg
- nafas-coin.svg
- nafas-notification-bell.svg
- nafas-follow-heart.svg
- nafas-empty-room.svg

## Quality gates before production
1. Preview SVGs on both light and dark surfaces and check clipping at common Android icon sizes.
2. Add accessibility labels in UI code; decorative art should be marked decorative.
3. Convert to Android VectorDrawable or rasterize at density-specific sizes only where runtime SVG support is unavailable.
4. Run Android build and screen-level tests after integration.
5. Do not treat vector artwork as real 3D models or animated files.
