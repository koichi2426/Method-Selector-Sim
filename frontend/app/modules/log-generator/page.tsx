import { Header } from "@/app/components/Header"; // Headerをインポート
import { Footer } from "@/app/components/Footer"; // Footerをインポート
import Link from "next/link";
import { ArrowUturnLeftIcon } from "@heroicons/react/24/outline";

export default function LogGeneratorPage() {
  return (
    <div className="flex min-h-screen flex-col bg-gray-50 dark:bg-gray-950">
      <Header />
      <main className="flex-1">
        <div className="container mx-auto max-w-5xl px-4 py-16 sm:py-24">
          {/* --- ページタイトル --- */}
          <div className="mb-12">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-5xl">
              状態・行動ログ生成モジュール
            </h1>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
              ここでログの生成をシミュレート・操作します。
            </p>
          </div>

          {/* --- このページ固有のコンテンツ --- */}
          <div className="rounded-xl bg-white dark:bg-gray-800/50 p-8 shadow-lg">
            <h2 className="text-2xl font-semibold text-gray-800 dark:text-white">操作パネル</h2>
            <div className="mt-6 h-64 flex items-center justify-center rounded-lg border-2 border-dashed border-gray-300 dark:border-gray-600">
              <p className="text-gray-400">（ここにログ生成用のUIを実装します）</p>
            </div>
          </div>

          {/* --- ホームへ戻るリンク --- */}
          <div className="mt-12">
            <Link href="/" className="inline-flex items-center gap-2 text-blue-500 hover:text-blue-600 dark:text-blue-400 dark:hover:text-blue-300">
              <ArrowUturnLeftIcon className="h-5 w-5" />
              <span>パイプラインのホームへ戻る</span>
            </Link>
          </div>

        </div>
      </main>
      <Footer />
    </div>
  );
}