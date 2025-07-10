import Link from 'next/link';
import { CpuChipIcon } from '@heroicons/react/24/outline';

export const Header = () => (
  <header className="sticky top-0 z-50 w-full border-b border-gray-200/50 dark:border-gray-700/50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
    <div className="container mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
      <Link href="/" className="flex items-center gap-2">
        <CpuChipIcon className="h-7 w-7 text-blue-500" />
        <span className="text-xl font-bold text-gray-800 dark:text-white">Method-Selector-Sim</span>
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