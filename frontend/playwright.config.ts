import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  use: {
    baseURL: "http://127.0.0.1:5173",
    trace: "retain-on-failure",
  },
  webServer: [
    {
      command: "cd ../django && python manage.py runserver 127.0.0.1:8000 --noreload",
      url: "http://127.0.0.1:8000/api/auth/csrf",
      reuseExistingServer: !process.env.CI,
      timeout: 60_000,
    },
    {
      command: "npm run dev -- --host 127.0.0.1 --port 5173 --strictPort",
      url: "http://127.0.0.1:5173",
      reuseExistingServer: !process.env.CI,
      timeout: 60_000,
    },
  ],
});
