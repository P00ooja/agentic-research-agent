# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.





#day 2
# Research Agent Frontend

React + Vite + Tailwind CSS frontend for the Research Agent application.

## Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Update `VITE_API_BASE_URL` if backend is on different port.

### 3. Start Development Server
```bash
npm run dev
```

Open `http://localhost:5173` in your browser.

## Features

- 🔍 Search for research topics
- ⏳ Real-time progress tracking
- 📊 Formatted research results
- 📚 Source citations and links
- 🎨 Beautiful responsive UI with Tailwind CSS

## Build for Production

```bash
npm run build
```

Output goes to `dist/` folder.

## Tech Stack

- React 19.2.8
- Vite 8.2.2
- Tailwind CSS 4.3.3
- Axios 1.20.0
- Lucide React 1.40.0
