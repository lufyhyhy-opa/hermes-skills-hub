import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { CTA } from "../data/script";
import { C, FONT, FPS } from "../theme";
import { EASE } from "../anim";

export const Cta: React.FC = () => {
  const frame = useCurrentFrame();
  if (!CTA || frame < CTA.start * FPS) return null;

  const p = EASE.outBack(Math.min(1, (frame - CTA.start * FPS) / 12));
  const pulse = 1 + Math.sin((frame / FPS) * 6) * 0.015;

  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 190 }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 18,
          padding: "20px 40px",
          borderRadius: 999,
          background: "rgba(255,207,107,0.14)",
          border: `2px solid ${C.gold}`,
          backdropFilter: "blur(16px)",
          opacity: Math.min(1, p),
          transform: `translateY(${(1 - p) * 40}px) scale(${p * pulse})`,
          boxShadow: "0 18px 60px rgba(0,0,0,.45)",
        }}
      >
        <span style={{ fontSize: 44 }}>👇</span>
        <span style={{ fontFamily: FONT.body, fontWeight: 500, fontSize: 40, color: "#fff" }}>
          {CTA.label}
        </span>
        <span
          style={{
            fontFamily: FONT.bebas,
            fontSize: 52,
            letterSpacing: "0.1em",
            color: C.gold,
          }}
        >
          {CTA.keyword}
        </span>
      </div>
    </AbsoluteFill>
  );
};
