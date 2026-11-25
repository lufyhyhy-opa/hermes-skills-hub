import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { BLOCKS, Block, SAFE, Word } from "../data/script";
import { C, FONT, FPS, HERO_SCRIPT_FONT, NAMED } from "../theme";
import { EASE, fitSize, wordCap } from "../anim";

// Mốc hiện (show), mốc tắt (out) và số frame thoát (exit_f: 6 thường, 2 khi chuyển
// nhanh để từ cuối kịp đọc — R30) do picture_lock tính sẵn (lead, giữ, đồng bộ đỉnh
// tiếng) — ở đây chỉ còn độ dài animation hiện chữ.
const REVEAL = 9;    // frame để một từ hiện xong (đạt 90 % ở frame 5 = sync_frame.block)

// Block đặt đáy ở SAFE.sub_bottom_px; dòng cuối chừa thêm phần nét chữ thò dưới
// đáy dòng (em của dòng) để đáy nét chữ nằm ở y 1436 mà không ra ngoài hộp — B14
// đo nét chữ, không đo hiệu ứng (Ruling R26). Đo trên font hiện tại với dấu nặng
// và g j p q y ỵ, mọi cỡ fitSize cho ra: hero script (BeVietnamPro Black Italic,
// lineHeight 1,02) thò tới 0,121 em; dòng nhỏ (BeVietnamPro, 1,24) chạm đáy dòng;
// hero stomp/quote (DTPhudu hoa) còn cách đáy ≥ 0,05 em. Phần dư ~0,02–0,04 em
// cho làm tròn điểm ảnh. Đổi font thì đo lại (check_text_safe sẽ báo).
const DESC = { small: 0.04, script: 0.14, stomp: 0 } as const;

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
  EASE.outCubic(Math.min(1, Math.max(0, (frame - w.show * FPS) / REVEAL)));

type LineKind = "small" | "hero";

const Line: React.FC<{
  words: Word[];
  frame: number;
  size: number;
  kind: LineKind;
  block: Block;
  last: boolean;
  probe: boolean;
}> = ({ words, frame, size, kind, block, last, probe }) => {
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
  const face = !hero ? "small" : stomp ? "stomp" : "script";

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        alignItems: "baseline",
        columnGap: hero ? "0.24em" : "0.3em",
        rowGap: hero ? "0.02em" : "0.06em",
        maxWidth: SAFE.sub_max_w,
        paddingBottom: last ? `${DESC[face]}em` : 0,
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

        // probe bỏ drop-shadow (R26); blur hiện chữ vẫn đo — chữ lên hình đúng như vậy (R29)
        const common: React.CSSProperties = {
          display: "inline-block",
          opacity: p,
          transform: `translateY(${(1 - p) * dy}px)`,
          filter: `blur(${(1 - p) * (hero ? 12 : 8)}px)${
            hero && !probe ? " drop-shadow(0 8px 22px rgba(0,0,0,.8))" : ""
          }`,
        };

        return (
          <span key={i} style={{ position: "relative", ...common }}>
            {/* quầng sáng phía sau — bản sao nhoè của chính chữ đó */}
            {hero && !probe ? (
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
                textShadow: grad || probe
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

// B2: dòng chỉ xuống dòng giữa các từ, nên cỡ còn bị chặn bởi từ dài nhất (anim.wordCap): trần
// em mỗi ký tự = em/ký tự lớn nhất trên mọi từ của 60 kịch bản kênh, advance đo bằng fontTools
// (dòng nhỏ BeVietnamPro 500: "mâm" 0,815; hero script BeVietnamPro Black Italic: "mâm" 0,828,
// "WORKFLOW" 0,818; hero stomp/quote DTPhudu Black in hoa: "MỞ" 0,655) — nét chữ nghiêng vẫn hẹp
// hơn advance; test_picture render kiểm các từ xấu nhất. Đổi font thì đo lại.
const WORD_EM = { small: 0.82, script: 0.83, stomp: 0.66 } as const;
const capped = (ws: Word[], face: keyof typeof WORD_EM, size: number) =>
  wordCap(ws.map((w) => w.t), size, WORD_EM[face], SAFE.sub_max_w);
const smallSize = (ws: Word[]) => capped(ws, "small", fitSize(text(ws), 54, 24, 38));

export const Subtitle: React.FC<{ probe?: boolean }> = ({ probe = false }) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: SAFE.sub_bottom_px,
        textAlign: "center",
      }}
    >
      {BLOCKS.map((b) => {
        const outAt = b.out;
        const inAt = Math.min(...b.top.concat(b.hero, b.bottom).map((w) => w.show));

        if (frame < inAt * FPS - 2 || frame > outAt * FPS + b.exit_f) return null;

        const q = Math.min(1, Math.max(0, (frame - outAt * FPS) / b.exit_f));
        const heroTxt = text(b.hero);
        const heroWords =
          b.style === "quote"
            ? b.hero.map((w, i) => ({
                ...w,
                t: (i === 0 ? "“" : "") + w.t + (i === b.hero.length - 1 ? "”" : ""),
              }))
            : b.hero;
        const heroSize =
          b.style === "script"
            ? capped(heroWords, "script", fitSize(heroTxt, 150, 15, 88))
            : capped(heroWords, "stomp", fitSize(heroTxt, 176, 12, 98));

        return (
          <div
            key={b.id}
            style={{
              position: "absolute",
              bottom: SAFE.sub_bottom_px,
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
                size={smallSize(b.top)}
                kind="small"
                block={b}
                last={false}
                probe={probe}
              />
            ) : null}

            <Line
              words={heroWords}
              frame={frame}
              size={heroSize}
              kind="hero"
              block={b}
              last={!b.bottom.length}
              probe={probe}
            />

            {b.bottom.length ? (
              <Line
                words={b.bottom}
                frame={frame}
                size={smallSize(b.bottom)}
                kind="small"
                block={b}
                last
                probe={probe}
              />
            ) : null}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
