import Link from 'next/link';
import React from 'react';
// Heroiconsから必要なアイコンをインポートします
import {
  PencilSquareIcon,
  InboxArrowDownIcon,
  CircleStackIcon,
  ArrowsRightLeftIcon,
  ShieldCheckIcon,
  DocumentTextIcon,
  Cog6ToothIcon,
  ArrowLongRightIcon, // 矢印アイコンもHeroiconsに変更
} from '@heroicons/react/24/outline'; // 線画スタイルのアイコンをインポート

// モジュールカードの型定義を更新
type ModuleCardProps = {
  href: string;
  title: string;
  icon: React.ReactNode; // アイコンをReactコンポーネントとして受け取る
  className?: string;
};

// モジュールカードコンポーネント
const ModuleCard: React.FC<ModuleCardProps> = ({ href, title, icon, className }) => (
  <Link href={href}>
    <div className={`
      flex flex-col items-center justify-center text-center group
      p-4 w-40 h-32 bg-white dark:bg-gray-800 
      border border-gray-200 dark:border-gray-700 rounded-lg 
      shadow-md hover:shadow-xl hover:-translate-y-1 transition-all cursor-pointer
      ${className}
    `}>
      {/* アイコンの色やサイズを調整 */}
      <div className="w-10 h-10 text-gray-500 dark:text-gray-400 group-hover:text-blue-500 transition-colors">
        {icon}
      </div>
      <span className="mt-3 font-semibold text-sm text-gray-700 dark:text-gray-200">{title}</span>
    </div>
  </Link>
);

// フローを示す矢印コンポーネント
const FlowArrow: React.FC = () => (
  <div className="text-gray-300 dark:text-gray-600 mx-2 hidden md:block">
    <ArrowLongRightIcon className="w-10 h-10" />
  </div>
);

// メインのホームページ
export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 dark:bg-gray-900 p-4 md:p-8">
      <div className="mb-12 text-center">
        <h1 className="text-4xl font-bold text-gray-800 dark:text-white">
          推論エンジン パイプライン
        </h1>
        <p className="text-gray-600 dark:text-gray-300 mt-2">
          各モジュールをクリックして操作してください。
        </p>
      </div>

      <div className="flex flex-col items-center gap-8">
        {/* 上段のフロー */}
        <div className="flex items-center justify-center flex-wrap gap-4 md:gap-0">
          <ModuleCard href="/modules/log-generator" title="状態・行動ログ生成" icon={<PencilSquareIcon />} />
          <FlowArrow />
          <ModuleCard href="/modules/collector" title="収集モジュール" icon={<InboxArrowDownIcon />} />
          <FlowArrow />
          <ModuleCard href="/database/logs" title="ログ保管" icon={<CircleStackIcon />} />
          <FlowArrow />
          <ModuleCard href="/modules/triplet-converter" title="Triplet変換" icon={<ArrowsRightLeftIcon />} />
          <FlowArrow />
          <ModuleCard href="/database/triplets" title="Triplet保管" icon={<CircleStackIcon />} />
        </div>

        {/* 下段のフロー (逆順) */}
        <div className="flex items-center justify-center flex-wrap-reverse gap-4 md:gap-0">
          <ModuleCard href="/modules/validator" title="モデル検証" icon={<ShieldCheckIcon />} />
          <FlowArrow />
          <ModuleCard href="/database/models" title="モデル保管" icon={<CircleStackIcon />} />
          <FlowArrow />
          <ModuleCard href="/models/trained" title="トレーニング済モデル" icon={<DocumentTextIcon />} />
          <FlowArrow />
          <ModuleCard href="/modules/finetuner" title="ファインチューナー" icon={<Cog6ToothIcon />} />
          <FlowArrow />
          <ModuleCard href="/models/decoder" title="デコーダモデル" icon={<DocumentTextIcon />} />
        </div>
      </div>
    </main>
  );
}