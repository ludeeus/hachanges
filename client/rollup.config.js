import json from '@rollup/plugin-json';
import { terser } from 'rollup-plugin-terser';
import commonjs from 'rollup-plugin-commonjs';
import nodeResolve from 'rollup-plugin-node-resolve';
import progress from 'rollup-plugin-progress';
import typescript from 'rollup-plugin-typescript2';

const isdev = process.env.ROLLUP_WATCH;

const opts_terser = {};

const AwesomePlugins = [
  progress(),
  json(),
  nodeResolve(),
  commonjs(),
  typescript(),
  !isdev && terser(opts_terser),
];

export default [
  {
    input: ['src/main.ts'],
    output: {
      file: `build/main.js`,
      format: 'iife',
    },
    plugins: [...AwesomePlugins],
  },
];
