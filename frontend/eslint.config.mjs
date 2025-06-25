import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
];

module.exports = {
  rules: {
    "@typescript-eslint/no-explicit-any": "off", // どうしても必要な場合に any を許可
    "no-console": "warn", // 開発中は console 使用可
  },
};

export default eslintConfig;

