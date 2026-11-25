import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { BLOCKS, Block, Word } from "../data/script";
import { C, FONT, FPS, HERO_SCRIPT_FONT, NAMED } from "../theme";
import { EASE, fitSize } from "../anim";

const REVEAL = 9;    // frame để một từ hiện xong
const LEAD = 0.05;   // hiện sớm hơn tiếng nói (s)
const HOLD = 0.22;   // giữ lại sau khi nói xong (s)
const OUT = 6;       // frame thoát

const hex = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
const mix = (a: string, b: string, t: number) => {
  const [r1, g1, b1] = hex(a);
  const [r2, g2, b2] = hex(b);
  const f = (x: number, y: number) => Math.round(x + (y - x) * t);
  return `rgb(${f(r1, r2)},${f(g1, g2)},${f(b1, b2)})`;
};

// Dải màu chạy suốt cả dòng: mỗi từ lấy một lát của cùng một gradient,
// nên các từ nối lại vẫn đọc ra một chuyển màu liên tục (không cần đo chữ).
const RAMP = ["#fbf9ff", "#d7ccff", "#b3a4ff"];
const rampAt = (t: number) => {
  const k = Math.min(0.999, Math.max(0, t)) * (RAMP.length - 1);
  const i = Math.floor(k);
  return mix(RAMP[i], RAMP[i + 1], k - i);
};

const wordP = (frame: number, w: Word) =>
  EASE.outCubic(Math.min(1, Math.max(0, (frame - (w.s - LEAD) * FPS) / REVEAL)));

type LineKind = "small" | "hero";

const Line: React.FC<{
  words: Word[];
  frame: number;
  size: number;
  kind: LineKind;
  block: Block;
}> = ({ words, frame, size, kind, block }) => {
  const hero = kind === "hero";
  const dy = hero ? 40 : 24;
  const n = words.length;

  const font =
    !hero
      ? FONT.body
      : block.style === "script"
      ? HERO_SCRIPT_FONT
      : FONT.displayBlack;

  const stomp = hero && block.style !== "script";
  const solid = stomp ? NAMED[block.color ?? "ink"] : null;

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        alignItems: "baseline",
        columnGap: hero ? "0.24em" : "0.3em",
        rowGap: hero ? "0.02em" : "0.06em",
        maxWidth: 940,
        fontFamily: font,
        fontSize: size,
        lineHeight: hero ? 1.02 : 1.24,
        fontWeight: hero ? 900 : 500,
        fontStyle: hero && block.style === "script" ? "italic" : "normal",
        textTransform: stomp ? "uppercase" : "none",
        letterSpacing: hero ? "-0.015em" : "0",
      }}
    >
      {words.map((w, i) => {
        const p = wordP(frame, w);
        if (p <= 0) return <span key={i} style={{ opacity: 0 }}>{w.t}</span>;

        const accent = hero && block.accent === i;
        const color = solid
          ? solid
          : accent
          ? C.heroC
          : hero
          ? undefined
          : C.ink;

        const grad =
          hero && !solid && !accent
            ? `linear-gradient(100deg, ${rampAt(i / Math.max(n, 1))}, ${rampAt(
                (i + 1) / Math.max(n, 1)
              )})`
            : undefined;

        const common: React.CSSProperties = {
          display: "inline-block",
          opacity: p,
          transform: `translateY(${(1 - p) * dy}px)`,
          filter: `blur(${(1 - p) * (hero ? 12 : 8)}px)${
            hero ? " drop-shadow(0 8px 22px rgba(0,0,0,.8))" : ""
          }`,
        };

        return (
          <span key={i} style={{ position: "relative", ...common }}>
            {/* quầng sáng phía sau — bản sao nhoè của chính chữ đó */}
            {hero ? (
              <span
                aria-hidden
                style={{
                  position: "absolute",
                  inset: 0,
                  color: solid ?? "#8f7dff",
                  filter: "blur(22px)",
                  opacity: 0.7 * p,
                  pointerEvents: "none",
                }}
              >
                {w.t}
              </span>
            ) : null}
            <span
              style={{
                position: "relative",
                color: grad ? "transparent" : color,
                backgroundImage: grad,
                WebkitBackgroundClip: grad ? "text" : undefined,
                backgroundClip: grad ? ("text" as const) : undefined,
                textShadow: grad
                  ? "none"
                  : hero
                  ? "0 8px 34px rgba(0,0,0,.6), 0 2px 6px rgba(0,0,0,.5)"
                  : "0 3px 16px rgba(0,0,0,.75), 0 1px 3px rgba(0,0,0,.6)",
              }}
            >
              {w.t}
            </span>
          </span>
        );
      })}
    </div>
  );
};

const text = (ws: Word[]) => ws.map((w) => w.t).join(" ");

export const Subtitle: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 400,
        textAlign: "center",
      }}
    >
      {BLOCKS.map((b, bi) => {
        const nextStart = BLOCKS[bi + 1]?.start ?? b.end + 1.2;
        const outAt = Math.min(b.end + HOLD, nextStart - 0.22);
        const inAt = b.top.concat(b.hero, b.bottom)[0].s - LEAD;

        if (frame < inAt * FPS - 2 || frame > outAt * FPS + OUT) return null;

        const q = Math.min(1, Math.max(0, (frame - outAt * FPS) / OUT));
        const heroTxt = text(b.hero);
        const heroSize =
          b.style === "script"
            ? fitSize(heroTxt, 150, 15, 88)
            : fitSize(heroTxt, 176, 12, 98);

        return (
          <div
            key={b.id}
            style={{
              position: "absolute",
              bottom: 400,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 10,
              opacity: 1 - q,
              transform: `translateY(${-20 * EASE.inCubic(q)}px)`,
              filter: `blur(${6 * q}px)`,
            }}
          >
            {b.top.length ? (
              <Line
                words={b.top}
                frame={frame}
                size={fitSize(text(b.top), 54, 24, 38)}
                kind="small"
                block={b}
              />
            ) : null}

            <Line
              words={
                b.style === "quote"
                  ? b.hero.map((w, i) => ({
                      ...w,
                      t:
                        (i === 0 ? "“" : "") +
                        w.t +
                        (i === b.hero.length - 1 ? "”" : ""),
                    }))
                  : b.hero
              }
              frame={frame}
              size={heroSize}
              kind="hero"
              block={b}
            />

            {b.bottom.length ? (
              <Line
                words={b.bottom}
                frame={frame}
                size={fitSize(text(b.bottom), 54, 24, 38)}
                kind="small"
                block={b}
              />
            ) : null}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
