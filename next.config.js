/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  experimental: {
    outputFileTracingRoot: undefined
  },
  webpack: (config) => {
    // Konva's node entry references the optional native `canvas` package, which
    // we never use (the studio runs in the browser). Stub it so the bundle builds.
    config.resolve.alias = { ...config.resolve.alias, canvas: false };
    return config;
  },
}

module.exports = nextConfig
