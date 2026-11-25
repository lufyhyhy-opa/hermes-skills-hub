import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { STEPS } from "../data/script";
import { C, FONT, FPS } from "../theme";
import { EASE } from "../anim";

const OUT = 8;

/**
 * Bảng 4 mục dựng dần theo lời nói: mục mới sáng, mục cũ lùi về 50% —
 * đổi nhịp so với subtitle 3 tầng để đoạn liệt kê không đọc như slide.
 */
export const StepList: React.FC = () => {
  const frame = useCurrentFrame();
  if (!STEPS) return null;
  const { in: IN_AT, out: OUT_AT, items, title } = STEPS;
  if (frame < IN_AT * FPS || frame > OUT_AT * FPS + OUT) return null;

  const enter = EASE.outCubic(Math.min(1, (frame - IN_AT * FPS) / 10));
  const q = Math.min(1, Math.max(0, (frame - OUT_AT * FPS) / OUT));
  const last = items.reduce((acc, s, i) => (frame >= s.start * FPS ? i : acc), -1);

  return (
    <AbsoluteFill
      style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 300 }}
    >
      <div
        style={{
          width: 900,
          padding: "34px 40px 40px",
          borderRadius: 34,
          background: "rgba(10,10,16,0.56)",
          border: "1px solid rgba(255,255,255,0.14)",
          backdropFilter: "blur(22px)",
          boxShadow: "0 30px 90px rgba(0,0,0,.5)",
          opacity: enter * (1 - q),
          transform: `translateY(${(1 - enter) * 36 - 26 * q}px) scale(${0.97 + enter * 0.03})`,
          filter: `blur(${(1 - enter) * 8 + q * 8}px)`,
        }}
      >
        <div
          style={{
            fontFamily: FONT.bebas,
            fontSize: 34,
            letterSpacing: "0.16em",
            color: C.gold,
            marginBottom: 22,
          }}
        >
          {title}
        </div>

        {items.map((s, i) => {
          const p = EASE.outCubic(
            Math.min(1, Math.max(0, (frame - s.start * FPS + 2) / 9))
          );
          const active = i === last;
          return (
            <div
              key={i}
              style={{
                display: "flex",
                alignItems: "baseline",
                gap: 22,
                padding: "12px 0",
                opacity: p * (active ? 1 : 0.46),
                transform: `translateX(${(1 - p) * 46}px)`,
                filter: `blur(${(1 - p) * 9}px)`,
                transition: "none",
              }}
            >
              <span
                style={{
                  fontFamily: FONT.bebas,
                  fontSize: 54,
                  color: active ? C.gold : "rgba(255,255,255,.6)",
                  minWidth: 62,
                }}
              >
                0{i + 1}
              </span>
              <span
                style={{
                  fontFamily: FONT.display,
                  fontWeight: 700,
                  fontSize: 58,
                  color: "#fff",
                  lineHeight: 1.1,
                  textShadow: "0 4px 20px rgba(0,0,0,.6)",
                }}
              >
                {s.label}
              </span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
