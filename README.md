# CSE6242 Team 5

## Description

This system is an interactive, scalable visualization search engine which supports image generation through search capabilities paired with image aesthetic assessment. Users can easily use this interface to quickly find high-quality, relevant images that were generated using text-to-image generative models such as Stable Diffusion.

The corresponding research paper and poster can be found in the `doc` directory.

## Installation

First, navigate to the CODE directory:

```bash
cd CODE
```

You need to have Node.js installed (prefereably the latest version) in order to run this locally.
Next, install all necessary dependencies with `npm install` (or `pnpm install` or `yarn`).

## Execution

Once you've installed dependencies, you can execute the code by starting a development server (note: make sure you are on the latest version of Node to avoid any config errors):

```bash
# Start the server and open the app in a new browser tab
npm run dev -- --open
```

If not automatically opened, navigate to `localhost:5173` in a web browser (currently only Google Chrome is supported) and the demo will be live. You use the interactive visualization system to search for images generated from particular prompts, filter based on image aesthetic assessment scores, and explore similar related images through the embedding-based clusterings.

Note: We recommend using Google Chrome for the best experience.

## Building

You can also create a production version of the app with

```bash
npm run build
```

You can preview the production build with `npm run preview`.

## Reproduction

For an overview of the data processing steps and algorithmic computation that can be used to reproduce our results, see [this file](https://github.com/CSE6242-Team5/CSE6242/blob/master/CODE/scripts/DATA_PROCESSING.md).
