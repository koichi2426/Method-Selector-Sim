"use client";

import React, { useState, useEffect, useMemo } from 'react';
import { Header } from "@/app/components/Header";
import { Footer } from "@/app/components/Footer";
import { 
    SearchIcon, 
    TrashIcon, 
    Spinner, 
    ExclamationTriangleIcon,
    RotateCcwIcon,
    SettingsIcon,
    ChevronLeftIcon,
    ChevronRightIcon,
    ClipboardDocumentIcon // コピーアイコンを追加
} from '@/app/components/Icons';

// データ構造の型定義
interface ProcessedScenario {
  ID: string;
  Scenario_ID: string;
  state: string;
  method_group: string[];
  negative_method_group: string[];
}

// 検索キーワードをハイライト表示するためのヘルパーコンポーネント
const Highlight = ({ text, highlight }: { text: string; highlight: string }) => {
  if (!highlight.trim()) {
    return <span>{text}</span>;
  }
  const regex = new RegExp(`(${highlight.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
  const parts = text.split(regex);
  return (
    <span>
      {parts.map((part, i) =>
        regex.test(part) ? (
          <mark key={i} className="bg-yellow-200 dark:bg-yellow-700/50 rounded-sm px-0.5 py-0.5">
            {part}
          </mark>
        ) : (
          <span key={i}>{part}</span>
        )
      )}
    </span>
  );
};


export default function ProcessedDataStorePage() {
  // --- State Management ---
  const [scenarios, setScenarios] = useState<ProcessedScenario[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Filtering, Sorting, Pagination States
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'state' | 'ID'>('state');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(50);

  // Deletion States
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [itemToDelete, setItemToDelete] = useState<ProcessedScenario | null>(null);

  // Toast Notification State
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  // --- Data Fetching & Deletion ---
  const fetchScenarios = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/v1/processed-scenarios');
      if (!response.ok) throw new Error(`HTTPエラー: ${response.status}`);
      const data = await response.json();
      setScenarios(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(`ログの取得に失敗しました: ${err instanceof Error ? err.message : String(err)}`);
      setScenarios([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchScenarios();
  }, []);
  
  // Reset page on filter/sort change
  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, sortBy, sortOrder, itemsPerPage]);

  // Toast timeout effect
  useEffect(() => {
    if (toast) {
      const timer = setTimeout(() => setToast(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [toast]);

  const handleDeleteClick = (scenario: ProcessedScenario) => {
    setItemToDelete(scenario);
    setShowConfirmModal(true);
  };

  const confirmDelete = async () => {
    if (!itemToDelete) return;
    setDeletingId(itemToDelete.ID);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8000/v1/processed-scenarios/${itemToDelete.ID}`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error(`HTTPエラー: ${response.status}`);
      setScenarios(prev => prev.filter(s => s.ID !== itemToDelete.ID));
      setToast({ message: 'ログを正常に削除しました。', type: 'success' });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : String(err);
      setError(`削除に失敗しました: ${errorMessage}`);
      setToast({ message: '削除に失敗しました。', type: 'error' });
    } finally {
      setShowConfirmModal(false);
      setItemToDelete(null);
      setDeletingId(null);
    }
  };
  
  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text).then(() => {
        setToast({ message: `${label} をコピーしました！`, type: 'success' });
    }, (err) => {
        console.error('Copy failed', err);
        setToast({ message: 'コピーに失敗しました。', type: 'error' });
    });
  };

  // --- Filtering & Sorting ---
  const filteredAndSortedScenarios = useMemo(() => {
    if (!scenarios) return [];
    
    let processed = [...scenarios];

    // Filtering
    if (searchTerm) {
        processed = processed.filter(scenario => {
            const searchLower = searchTerm.toLowerCase();
            return (
                scenario.state.toLowerCase().includes(searchLower) ||
                scenario.ID.toLowerCase().includes(searchLower) ||
                scenario.Scenario_ID.toLowerCase().includes(searchLower) ||
                [...scenario.method_group, ...scenario.negative_method_group].some(m => m.toLowerCase().includes(searchLower))
            );
        });
    }

    // Sorting
    processed.sort((a, b) => {
        const fieldA = a[sortBy]?.toString().toLowerCase() || '';
        const fieldB = b[sortBy]?.toString().toLowerCase() || '';
        
        if (sortOrder === 'asc') {
            return fieldA.localeCompare(fieldB);
        } else {
            return fieldB.localeCompare(fieldA);
        }
    });

    return processed;
  }, [scenarios, searchTerm, sortBy, sortOrder]);

  // --- Pagination ---
  const totalPages = Math.ceil(filteredAndSortedScenarios.length / itemsPerPage);
  const currentScenarios = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    return filteredAndSortedScenarios.slice(startIndex, endIndex);
  }, [filteredAndSortedScenarios, currentPage, itemsPerPage]);


  // --- Render Components ---
  const sidebarContent = (
    <>
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3 mb-4">
          <SettingsIcon className="h-6 w-6 text-gray-600 dark:text-gray-400" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">操作パネル</h2>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          保管されたログの閲覧と管理
        </p>
      </div>
      <div className="p-6 space-y-6 flex-1 overflow-y-auto">
        <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-600 dark:text-gray-400">総ログ数:</span>
            <span className="font-medium text-gray-900 dark:text-white">{scenarios.length.toLocaleString()}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-600 dark:text-gray-400">フィルタ後:</span>
            <span className="font-medium text-gray-900 dark:text-white">{filteredAndSortedScenarios.length.toLocaleString()}</span>
          </div>
        </div>

        <div className="space-y-2">
            <label htmlFor="items-per-page" className="text-sm font-medium text-gray-700 dark:text-gray-300">表示件数</label>
            <select id="items-per-page" value={itemsPerPage} onChange={(e) => setItemsPerPage(Number(e.target.value))} className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500">
            <option value={25}>25件</option>
            <option value={50}>50件</option>
            <option value={100}>100件</option>
            <option value={200}>200件</option>
            </select>
        </div>

        <div className="space-y-3 pt-4 border-t border-gray-200 dark:border-gray-600">
          <button onClick={fetchScenarios} disabled={loading} className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 disabled:opacity-50 transition-colors">
            <RotateCcwIcon className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            {loading ? '更新中...' : 'ログを再取得'}
          </button>
        </div>
        {error && (
          <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p className="text-xs text-red-700 dark:text-red-300">{error}</p>
          </div>
        )}
      </div>
    </>
  );

  const mainContent = (
    <>
      <div className="p-6 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 space-y-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">ログデータ一覧</h3>
        <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1 relative">
                <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input type="text" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} placeholder="状態、メソッド、IDで検索..." className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </div>
            <div className="lg:w-48">
                <select value={`${sortBy}-${sortOrder}`} onChange={(e) => { const [field, order] = e.target.value.split('-'); setSortBy(field as 'state' | 'ID'); setSortOrder(order as 'asc' | 'desc'); }} className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="state-asc">状態 (昇順)</option>
                    <option value="state-desc">状態 (降順)</option>
                    <option value="ID-asc">ID (昇順)</option>
                    <option value="ID-desc">ID (降順)</option>
                </select>
            </div>
        </div>
      </div>

      <div className="px-6 py-3 bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <div className="text-sm text-gray-600 dark:text-gray-400">
            {filteredAndSortedScenarios.length > 0 ? (
            <>{(currentPage - 1) * itemsPerPage + 1}-{Math.min(currentPage * itemsPerPage, filteredAndSortedScenarios.length)} / {filteredAndSortedScenarios.length.toLocaleString()} 件</>
            ) : 'データがありません'}
        </div>
        {totalPages > 1 && (
            <div className="flex items-center gap-2">
            <button onClick={() => setCurrentPage(p => Math.max(1, p - 1))} disabled={currentPage === 1} className="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50">
                <ChevronLeftIcon className="h-4 w-4" />
            </button>
            <span className="text-sm font-medium">{currentPage} / {totalPages}</span>
            <button onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))} disabled={currentPage === totalPages} className="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50">
                <ChevronRightIcon className="h-4 w-4" />
            </button>
            </div>
        )}
      </div>

      <div className="flex-1 overflow-auto bg-gray-50 dark:bg-gray-950">
        {loading ? (
          <div className="flex items-center justify-center h-full"><Spinner className="h-8 w-8 text-blue-500" /></div>
        ) : currentScenarios.length === 0 ? (
          <div className="flex items-center justify-center h-full text-center text-gray-500 dark:text-gray-400">
            <p>{scenarios.length > 0 ? '条件に一致するログがありません。' : '表示するログデータがありません。'}</p>
            {searchTerm && <button onClick={() => setSearchTerm('')} className="text-sm text-blue-500 hover:underline mt-2">検索をクリア</button>}
          </div>
        ) : (
          <div className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
            {currentScenarios.map((scenario) => (
              <div key={scenario.ID} className="px-6 py-4 even:bg-gray-50 dark:even:bg-gray-800/50 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors duration-150">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-medium text-gray-900 dark:text-white leading-5">
                      <Highlight text={scenario.state} highlight={searchTerm} />
                    </h4>
                    <div className="flex flex-wrap items-center gap-x-4 gap-y-1 mt-2">
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-gray-500 dark:text-gray-400">メソッド:</span>
                        <div className="flex flex-wrap gap-1">
                          {scenario.method_group.map((m, i) => <span key={i} className="px-2 py-0.5 text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded">{m}</span>)}
                        </div>
                      </div>
                      {scenario.negative_method_group.length > 0 && (
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-gray-500 dark:text-gray-400">除外:</span>
                          <div className="flex flex-wrap gap-1">
                            {scenario.negative_method_group.map((m, i) => <span key={i} className="px-2 py-0.5 text-xs bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded">{m}</span>)}
                          </div>
                        </div>
                      )}
                    </div>
                    <div className="font-mono text-xs text-gray-500 dark:text-gray-400 mt-3 space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="flex-shrink-0">ID:</span>
                        <span className="text-gray-700 dark:text-gray-300 truncate">{scenario.ID}</span>
                        <button onClick={() => copyToClipboard(scenario.ID, 'ID')} className="p-1 text-gray-400 hover:text-gray-700 dark:hover:text-white rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 flex-shrink-0">
                          <ClipboardDocumentIcon className="h-4 w-4" />
                        </button>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="flex-shrink-0">Scenario ID:</span>
                        <span className="text-gray-700 dark:text-gray-300 truncate">{scenario.Scenario_ID}</span>
                        <button onClick={() => copyToClipboard(scenario.Scenario_ID, 'Scenario ID')} className="p-1 text-gray-400 hover:text-gray-700 dark:hover:text-white rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 flex-shrink-0">
                           <ClipboardDocumentIcon className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                  <div className="flex-shrink-0">
                    <button onClick={() => handleDeleteClick(scenario)} disabled={deletingId === scenario.ID} className="p-2 text-gray-500 hover:text-red-600 dark:hover:text-red-400 rounded-md hover:bg-red-50 dark:hover:bg-red-900/20 disabled:opacity-50">
                      {deletingId === scenario.ID ? <Spinner className="h-5 w-5" /> : <TrashIcon className="h-5 w-5" />}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );

  return (
    <>
      <div className="flex min-h-screen flex-col bg-gray-50 dark:bg-gray-950">
        <Header />
        <div className="flex-1 flex overflow-hidden">
          <aside className="w-80 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 flex flex-col">
            {sidebarContent}
          </aside>
          <main className="flex-1 flex flex-col overflow-hidden">
            {mainContent}
          </main>
        </div>
        <Footer />
      </div>

      {/* Toast Notification */}
      {toast && (
        <div className="fixed bottom-5 right-5 z-50">
            <div className={`px-4 py-3 rounded-lg shadow-lg text-sm font-medium ${toast.type === 'success' ? 'bg-green-100 dark:bg-green-800/90 text-green-800 dark:text-green-100' : 'bg-red-100 dark:bg-red-800/90 text-red-800 dark:text-red-100'}`}>
                {toast.message}
            </div>
        </div>
      )}

      {/* Deletion Confirmation Modal */}
      {showConfirmModal && itemToDelete && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 w-full max-w-md">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">ログの削除確認</h3>
            <div className="mt-4">
              <p className="text-sm text-gray-600 dark:text-gray-300">本当にこのログを削除しますか？この操作は元に戻せません。</p>
              <div className="mt-4 bg-gray-100 dark:bg-gray-700/50 p-3 rounded-md space-y-1">
                <p className="text-sm font-mono text-gray-700 dark:text-gray-400 truncate" title={itemToDelete.ID}>ID: {itemToDelete.ID}</p>
                <p className="text-sm text-gray-800 dark:text-gray-200">State: {itemToDelete.state}</p>
              </div>
            </div>
            <div className="mt-6 flex justify-end gap-3">
              <button type="button" onClick={() => setShowConfirmModal(false)} className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm hover:bg-gray-50 dark:hover:bg-gray-600">キャンセル</button>
              <button type="button" onClick={confirmDelete} className="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md shadow-sm hover:bg-red-700">削除する</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
