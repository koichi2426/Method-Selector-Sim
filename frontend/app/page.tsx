import Link from 'next/link';
import React from 'react';
// Heroiconsから必要なアイコンをインポート
import {
  PencilSquareIcon, InboxArrowDownIcon, CircleStackIcon,
  ArrowsRightLeftIcon, ShieldCheckIcon, DocumentTextIcon,
  Cog6ToothIcon, ArrowLongRightIcon, CpuChipIcon
} from '@heroicons/react/24/outline';

// --- Header Component ---
const Header = () => (
  <header className="sticky top-0 z-50 w-full border-b border-gray-200/50 dark:border-gray-700/50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
    <div className="container mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
      <Link href="/" className="flex items-center gap-2">
        <CpuChipIcon className="h-7 w-7 text-blue-500" />
        <span className="text-xl font-bold text-gray-800 dark:text-white">Inference Engine</span>
      </Link>
      <nav>
        <a 
          href="https://github.com/koichi2426/Method-Selector-Sim"
          target="_blank" 
          rel="noopener noreferrer" 
          className="text-gray-600 hover:text-blue-500 dark:text-gray-300 dark:hover:text-blue-400 transition-colors"
        >
          GitHub
        </a>
      </nav>
    </div>
  </header>
);

// --- ModuleCard Component ---
type ModuleCardProps = { href: string; title: string; icon: React.ReactNode; };
const ModuleCard: React.FC<ModuleCardProps> = ({ href, title, icon }) => (
  <Link href={href}>
    <div className="
      group flex h-36 w-44 flex-col items-center justify-center gap-3 rounded-xl 
      border border-gray-200/80 dark:border-gray-700/80 
      bg-white/70 dark:bg-gray-800/70 
      p-4 text-center shadow-lg shadow-gray-200/50 dark:shadow-black/20
      transition-all duration-300 hover:!bg-white hover:dark:!bg-gray-800 hover:shadow-xl hover:-translate-y-1.5
    ">
      <div className="h-10 w-10 text-gray-500 transition-colors group-hover:text-blue-500 dark:text-gray-400">
        {icon}
      </div>
      <span className="font-semibold text-sm text-gray-800 dark:text-gray-100">{title}</span>
    </div>
  </Link>
);

// --- FlowArrow Component ---
const FlowArrow: React.FC = () => (
  <div className="hidden text-gray-300 dark:text-gray-600 md:block">
    <ArrowLongRightIcon className="h-10 w-10" />
  </div>
);

// --- Footer Component ---
const Footer = () => (
  <footer className="w-full border-t border-gray-200/50 dark:border-gray-700/50 py-6">
    <div className="container mx-auto max-w-7xl px-4 text-center text-sm text-gray-500">
      <p>&copy; {new Date().getFullYear()} Lightweight Inference Engine Project. All Rights Reserved.</p>
    </div>
  </footer>
);

// --- Main Page Component ---
export default function Home() {
  // 指定された順番でパイプラインのデータを定義
  const pipelineModules = [
    { href: "/modules/log-generator", title: "状態・行動ログ生成", icon: <PencilSquareIcon /> },
    { href: "/modules/collector", title: "収集モジュール", icon: <InboxArrowDownIcon /> },
    { href: "/database/logs", title: "状態・行動ログ保管", icon: <CircleStackIcon /> },
    { href: "/modules/triplet-converter", title: "Triplet変換", icon: <ArrowsRightLeftIcon /> },
    { href: "/database/triplets", title: "Triplet保管", icon: <CircleStackIcon /> },
    { href: "/modules/finetuner", title: "ファインチューナー", icon: <Cog6ToothIcon /> },
    { href: "/database/models", title: "モデル保管", icon: <CircleStackIcon /> },
    { href: "/modules/validator", title: "モデル検証", icon: <ShieldCheckIcon /> },
  ];

  return (
    <div className="flex min-h-screen flex-col bg-gray-50 dark:bg-gray-950">
      <Header />
      <main className="flex-1">
        <div className="container mx-auto max-w-7xl px-4 py-16 sm:py-24">
          {/* --- ページタイトル --- */}
          <div className="mb-16 text-center">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl">
              推論エンジン パイプライン
            </h1>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
              各モジュールをクリックして、パイプラインの各ステップを操作・確認できます。
            </p>
          </div>

          {/* --- パイプラインのコンテナ --- */}
          <div className="rounded-2xl bg-gray-200/30 dark:bg-gray-800/30 p-8 md:p-12 border border-gray-200/50 dark:border-gray-700/50">
            {/* 1直線に並べ、画面幅に応じて折り返す */}
            <div className="flex flex-wrap items-center justify-center gap-x-4 gap-y-6">
              {pipelineModules.map((module, i) => (
                <React.Fragment key={module.href}>
                  <ModuleCard {...module} />
                  {i < pipelineModules.length - 1 && <FlowArrow />}
                </React.Fragment>
              ))}
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}