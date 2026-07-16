import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Produce a self-contained build (.next/standalone) for a minimal
  // production Docker image.
  output: "standalone",
};

export default nextConfig;
