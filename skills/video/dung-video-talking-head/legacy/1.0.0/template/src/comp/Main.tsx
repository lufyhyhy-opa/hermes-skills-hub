import React from "react";
import { AbsoluteFill } from "remotion";
import { Fonts } from "../fonts";
import { Footage } from "./Footage";
import { Grade } from "./Grade";
import { StepList } from "./StepList";
import { Subtitle } from "./Subtitle";
import { Cta } from "./Cta";
import { Hook } from "./Hook";
import { Sfx } from "./Sfx";

export const Main: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#000" }}>
    <Fonts />
    <Footage />
    <Grade />
    <StepList />
    <Subtitle />
    <Hook />
    <Cta />
    <Sfx />
  </AbsoluteFill>
);
