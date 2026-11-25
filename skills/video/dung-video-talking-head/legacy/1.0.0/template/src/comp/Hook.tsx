import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { FONT, FPS, NAMED } from "../theme";
import { HOOK } from "../data/script";
import { EASE } from "../anim";


/**
 * Cú mở: con số chiếm gần hết khung, giữ một nhịp rồi thu nhỏ + nhoè
 * rơi xuống chỗ dòng phụ — bàn giao cho subtitle thay vì cắt phụt.
 */
export const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  if (!HOOK || t > HOOK.end) return null;
  const { land: HOLD, out: OUT, end: END, text } = HOOK;
  const IN = 0;
  const color = NAMED[HOOK.color];

  const enter = EASE.outCubic(Math.min(1, (t - IN) / (HOLD - IN)));
  const push = EASE.inOut(Math.min(1, Math.max(0, (t - HOLD) / (OUT - HOLD))));
  const exit = EASE.inCubic(Math.min(1, Math.max(0, (t - OUT) / (END - OUT))));

  const scale = (1.34 - 0.34 * enter) * (1 + push * 0.05) * (1 - exit * 0.42);

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", paddingBottom: 240 }}>
      <div
        style={{
          position: "relative",
          fontFamily: FONT.bebas,
          fontSize: 460,
          lineHeight: 0.86,
          color,
          opacity: enter * (1 - exit),
          transform: `translateY(${(1 - enter) * 60 + exit * 420}px) scale(${scale})`,
          filter: `blur(${(1 - enter) * 26 + exit * 16}px)`,
          textShadow: "0 20px 90px rgba(0,0,0,.7)",
        }}
      >
        <span
          aria-hidden
          style={{
            position: "absolute",
            inset: 0,
            color,
            filter: "blur(52px)",
            opacity: 0.75,
          }}
        >
          {text}
        </span>
        <span style={{ position: "relative" }}>{text}</span>
      </div>
    </AbsoluteFill>
  );
};
