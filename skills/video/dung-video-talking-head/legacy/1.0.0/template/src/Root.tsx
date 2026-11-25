import React from "react";
import { Composition } from "remotion";
import { Main } from "./comp/Main";
import { DUR, FPS, H, W } from "./theme";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Main"
    component={Main}
    durationInFrames={DUR}
    fps={FPS}
    width={W}
    height={H}
  />
);
