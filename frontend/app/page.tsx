import Link from 'next/link';
import React from 'react';
import { Header } from '@/app/components/Header'; // 共通Headerをインポート
import { Footer } from '@/app/components/Footer'; // 共通Footerをインポート
import {
  PencilSquareIcon, InboxArrowDownIcon, CircleStackIcon,
  ArrowsRightLeftIcon, ShieldCheckIcon, Cog6ToothIcon,
  ArrowLongRightIcon, ArrowLongLeftIcon // DownArrowのインポートを削除
} from '@heroicons/react/24/outline';

// --- このページだけで使うコンポーネント ---

// ModuleCard Component
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

// FlowArrow Components
const RightArrow: React.FC = () => (
  <div className="hidden text-gray-300 dark:text-gray-600 md:block">
    <ArrowLongRightIcon className="h-10 w-10" />
  </div>
);

const LeftArrow: React.FC = () => (
  <div className="hidden text-gray-300 dark:text-gray-600 md:block">
    <ArrowLongLeftIcon className="h-10 w-10" />
  </div>
);


// --- Main Page Component ---
export default function Home() {
  const row1Modules = [
    { href: "/modules/log-generator", title: "状態・行動ログ生成", icon: <PencilSquareIcon /> },
    { href: "/modules/collector", title: "収集モジュール", icon: <InboxArrowDownIcon /> },
    { href: "/database/logs", title: "状態・行動ログ保管", icon: <CircleStackIcon /> },
    { href: "/modules/triplet-converter", title: "Triplet変換", icon: <ArrowsRightLeftIcon /> },
  ];

  const row2Modules = [
    { href: "/modules/validator", title: "モデル検証", icon: <ShieldCheckIcon /> },
    { href: "/database/models", title: "モデル保管", icon: <CircleStackIcon /> },
    { href: "/modules/finetuner", title: "ファインチューナー", icon: <Cog6ToothIcon /> },
    { href: "/database/triplets", title: "Triplet保管", icon: <CircleStackIcon /> },
  ];

  return (
    <div className="flex min-h-screen flex-col bg-gray-50 dark:bg-gray-950">
      <Header />
      <main className="flex-1">
        <div className="container mx-auto max-w-7xl px-4 py-16 sm:py-24">
          <div className="mb-16 text-center">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl">
              推論エンジン パイプライン
            </h1>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
              各モジュールをクリックして、パイプラインの各ステップを操作・確認できます。
            </p>
          </div>
          
          <div className="relative rounded-2xl bg-gray-200/30 dark:bg-gray-800/30 p-8 md:p-12 border border-gray-200/50 dark:border-gray-700/50">
            
            <div className="flex flex-col items-center justify-center gap-8">
              {/* --- 1行目 --- */}
              <div className="flex flex-wrap items-center justify-center gap-x-4 gap-y-6">
                {row1Modules.map((module, i) => (
                  <React.Fragment key={module.href}>
                    <ModuleCard {...module} />
                    {i < row1Modules.length - 1 && <RightArrow />}
                  </React.Fragment>
                ))}
              </div>

              {/* --- 2行目（逆順） --- */}
              <div className="flex flex-wrap-reverse items-center justify-center gap-x-4 gap-y-6">
                 {row2Modules.map((module, i) => (
                  <React.Fragment key={module.href}>
                    <ModuleCard {...module} />
                    {i < row2Modules.length - 1 && <LeftArrow />}
                  </React.Fragment>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}