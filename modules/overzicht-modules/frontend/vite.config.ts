import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
export default defineConfig({
  plugins: [react()],
  server: { host: true, port: 20162 },
  preview: { port: 20162 }
});
