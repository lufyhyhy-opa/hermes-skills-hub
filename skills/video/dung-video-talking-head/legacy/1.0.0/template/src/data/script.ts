// GIỮ CHỖ — chạy `python scripts/build.py` để sinh bản thật từ edit.json.
export type Word = { t: string; s: number; e: number };
export type Block = {
  id: string; start: number; end: number;
  style: "script" | "stomp" | "quote";
  color: "warn" | "gold" | "ink" | null;
  accent: number | null;
  top: Word[]; hero: Word[]; bottom: Word[];
};
export type Steps = { title: string; in: number; out: number; items: { label: string; start: number; end: number }[] };
export type Shot = { t: number; s0: number; s1: number; x?: number; y?: number };
export type Hook = { text: string; color: "warn" | "gold" | "ink"; land: number; out: number; end: number };
export type Cta = { label: string; keyword: string; start: number };
export type Cue = { from: number; target: number; src: string; volume: number; note: string };

export const DURATION_S = 10;
export const DURATION_F = 300;
export const HOOK: Hook | null = null;
export const BLOCKS: Block[] = [];
export const STEPS: Steps | null = null;
export const SHOTS: Shot[] = [{ t: 0, s0: 1, s1: 1.04 }];
export const CTA: Cta | null = null;
export const SFX: Cue[] = [];
