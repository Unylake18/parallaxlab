import React from 'react';
import { Composition } from 'remotion';
import TL from '../../timeline.json';
import { Vid0030 } from './Vid0030';

// Uma fonte de tempo: a duração vem do timeline.json (o mesmo do Three.js e do Manim).
const FPS = 15;
export const Root: React.FC = () => (
  <>
    <Composition id="Vid0030" component={Vid0030} width={540} height={960} fps={FPS}
      durationInFrames={Math.round(TL.duracao_s * FPS)} />
    {/* master: 1080×1920 / 30 fps (3D, âncoras e Manim renderizados em 30 fps) */}
    <Composition id="Vid0030Final" component={Vid0030} width={1080} height={1920} fps={30}
      durationInFrames={Math.round(TL.duracao_s * 30)} />
  </>
);
