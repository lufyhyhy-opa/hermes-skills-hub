import React from "react";
import { Audio, Sequence, staticFile } from "remotion";
import { SFX } from "../data/script";

/** Bảng SFX do scripts/build.py sinh — mỗi cue đã trừ sẵn độ trễ đỉnh âm + độ trễ AAC. */
export const Sfx: React.FC = () => (
  <>
    {SFX.map((c, i) => (
      <Sequence key={i} from={c.from} layout="none" name={c.note}>
        <Audio src={staticFile(c.src)} volume={c.volume} />
      </Sequence>
    ))}
  </>
);
