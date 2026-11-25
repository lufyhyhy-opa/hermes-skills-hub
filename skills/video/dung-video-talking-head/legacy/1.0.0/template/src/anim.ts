import { interpolate } from "remotion";
import { FPS } from "./theme";

export const EASE = {
  outCubic: (t: number) => 1 - Math.pow(1 - t, 3),
  inCubic: (t: number) => t * t * t,
  inOut: (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
  outBack: (t: number) => 1 + 2.2 * Math.pow(t - 1, 3) + 1.4 * Math.pow(t - 1, 2),
};

/** Tiến độ 0→1 giữa hai mốc giây, kèm easing. */
export const seg = (
  frame: number,
  fromSec: number,
  toSec: number,
  ease: (t: number) => number = EASE.outCubic
) => {
  const raw = interpolate(frame, [fromSec * FPS, toSec * FPS], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return ease(raw);
};

export const lerp = (p: number, a: number, b: number) => a + (p - 0) * (b - a);

/** Cỡ chữ co lại theo độ dài chuỗi để không tràn khung. */
export const fitSize = (text: string, base: number, idealChars: number, min: number) =>
  Math.max(min, Math.min(base, (base * idealChars) / Math.max(text.length, 1)));

/** Nhiễu tất định (mulberry32) – dùng cho grain/jitter, không đổi giữa các lần render. */
export const rand = (seed: number) => {
  let t = (seed + 0x6d2b79f5) >>> 0;
  t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
