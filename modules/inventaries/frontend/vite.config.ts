import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
export default defineConfig({
  plugins: [react()],
  server: { host: true, port: 20080 },
  preview: { port: 20080 }
});
