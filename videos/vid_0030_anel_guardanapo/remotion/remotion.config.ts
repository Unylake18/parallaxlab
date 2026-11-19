// Saída no padrão do canal (AGENTS.md): H.264, yuv420p, CRF 14. Chrome: o do sistema (CHROMIUM_PATH) se existir.
import { Config } from '@remotion/cli/config';

Config.setVideoImageFormat('png');
Config.setCodec('h264');
Config.setCrf(14);
Config.setPixelFormat('yuv420p');
Config.setOverwriteOutput(true);
if (process.env.CHROMIUM_PATH) Config.setBrowserExecutable(process.env.CHROMIUM_PATH);
