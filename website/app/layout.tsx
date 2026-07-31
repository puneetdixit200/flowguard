import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FlowGuard | AI-Assisted Network Intrusion Detection",
  description:
    "FlowGuard is a research-grade intrusion detection platform combining eBPF/XDP packet capture, C++ flow processing, multi-model machine learning, FastAPI, PostgreSQL, Redis, and a live security dashboard.",
  keywords: [
    "network intrusion detection",
    "eBPF",
    "XDP",
    "cybersecurity",
    "machine learning",
    "FastAPI",
    "C++",
    "network monitoring",
  ],
  authors: [{ name: "Puneet Dixit" }],
  creator: "Puneet Dixit",
  metadataBase: new URL("https://flowguard.vercel.app"),
  openGraph: {
    title: "FlowGuard | See threats before they become incidents",
    description:
      "An end-to-end IDS framework from kernel packet capture to explainable, multi-model threat detection.",
    type: "website",
    siteName: "FlowGuard",
  },
  twitter: {
    card: "summary_large_image",
    title: "FlowGuard | AI-Assisted Network Intrusion Detection",
    description:
      "eBPF/XDP capture, C++ flow aggregation, four ML models, FastAPI, and a real-time dashboard.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#07100f",
  colorScheme: "dark",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
