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
    ClipboardDocumentIcon
} from '@/app/components/Icons';

// モデルデータの型定義をAPIレスポンスに合わせて修正
interface Model {
  ID: string;
  name: string;
  Dataset_ID: string;
  description: string;
  file_path: string;
  created_at: string; // ISO 8601 format string
}

export default function DatabaseModelsPage() {
  // --- State Management ---
  const [models, setModels] = useState<Model[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Filtering, Sorting, Pagination States
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'name' | 'created_at'>('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(50);

  // Selection & Deletion States
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [showBulkConfirmModal, setShowBulkConfirmModal] = useState(false);

  // Toast Notification State
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  // --- Data Fetching & Deletion ---
  const fetchModels = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/v1/models');
      if (!response.ok) throw new Error(`HTTPエラー: ${response.status}`);
      const data = await response.json();
      setModels(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(`モデルデータの取得に失敗しました: ${err instanceof Error ? err.message : String(err)}`);
      setModels([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchModels();
  }, []);
  
  useEffect(() => {
    setCurrentPage(1);
    setSelectedIds([]);
  }, [searchTerm, sortBy, sortOrder, itemsPerPage]);

  useEffect(() => {
    if (toast) {
      const timer = setTimeout(() => setToast(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [toast]);

  const confirmBulkDelete = async () => {
    setError(null);
    const deletionPromises = selectedIds.map(id => 
        fetch(`http://localhost:8000/v1/models/${id}`, { method: 'DELETE' })
    );
    try {
        const results = await Promise.allSettled(deletionPromises);
        const successfulDeletes = results.filter(r => r.status === 'fulfilled' && r.value.ok).length;
        
        if (successfulDeletes > 0) {
            setModels(prev => prev.filter(s => !selectedIds.includes(s.ID)));
            setToast({ message: `${successfulDeletes}件のモデルを削除しました。`, type: 'success' });
        }

        const failedDeletes = results.length - successfulDeletes;
        if (failedDeletes > 0) {
            throw new Error(`${failedDeletes}件のモデル削除に失敗しました。`);
        }
    } catch (err) {
        setError(err instanceof Error ? err.message : '一括削除中にエラーが発生しました。');
    } finally {
        setSelectedIds([]);
        setShowBulkConfirmModal(false);
    }
  };
  
  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text).then(() => {
        setToast({ message: `${label} をコピーしました！`, type: 'success' });
    }, () => {
        setToast({ message: 'コピーに失敗しました。', type: 'error' });
    });
  };

  // --- Selection Logic ---
  const toggleSelection = (id: string) => {
    setSelectedIds(prev => prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]);
  };

  const selectAllCurrentPage = () => {
    const currentIds = currentModels.map(s => s.ID);
    setSelectedIds(prev => Array.from(new Set([...prev, ...currentIds])));
  };

  const selectAllFiltered = () => {
    setSelectedIds(filteredAndSortedModels.map(s => s.ID));
  };

  // --- Filtering & Sorting ---
  const filteredAndSortedModels = useMemo(() => {
    if (!models) return [];
    
    let processed = [...models];

    if (searchTerm) {
        processed = processed.filter(model => {
            const searchLower = searchTerm.toLowerCase();
            return (
                model.name.toLowerCase().includes(searchLower) ||
                model.description.toLowerCase().includes(searchLower) ||
                model.Dataset_ID.toLowerCase().includes(searchLower) ||
                model.ID.toLowerCase().includes(searchLower)
            );
        });
    }

    processed.sort((a, b) => {
        const fieldA = a[sortBy]?.toString().toLowerCase() || '';
        const fieldB = b[sortBy]?.toString().toLowerCase() || '';
        return sortOrder === 'asc' ? fieldA.localeCompare(fieldB) : fieldB.localeCompare(fieldA);
    });

    return processed;
  }, [models, searchTerm, sortBy, sortOrder]);

  // --- Pagination ---
  const totalPages = Math.ceil(filteredAndSortedModels.length / itemsPerPage);
  const currentModels = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    return filteredAndSortedModels.slice(startIndex, startIndex + itemsPerPage);
  }, [filteredAndSortedModels, currentPage, itemsPerPage]);


  // --- Render Components ---
  const sidebarContent = (
    <>
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3 mb-4">
          <SettingsIcon className="h-6 w-6 text-gray-600 dark:text-gray-400" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">操作パネル</h2>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-400">学習済みモデルの閲覧と管理</p>
      </div>
      <div className="p-6 space-y-6 flex-1 overflow-y-auto">
        <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 space-y-2">
          <div className="flex justify-between text-sm"><span className="text-gray-600 dark:text-gray-400">総モデル数:</span><span className="font-medium text-gray-900 dark:text-white">{models.length.toLocaleString()}</span></div>
          <div className="flex justify-between text-sm"><span className="text-gray-600 dark:text-gray-400">フィルタ後:</span><span className="font-medium text-gray-900 dark:text-white">{filteredAndSortedModels.length.toLocaleString()}</span></div>
          <div className="flex justify-between text-sm"><span className="text-gray-600 dark:text-gray-400">選択済み:</span><span className="font-medium text-blue-600 dark:text-blue-400">{selectedIds.length.toLocaleString()}</span></div>
        </div>

        <div className="space-y-3">
            <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">選択操作</h3>
            <div className="grid grid-cols-1 gap-2">
                <button onClick={selectAllCurrentPage} disabled={currentModels.length === 0} className="px-3 py-2 text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-md hover:bg-blue-200 dark:hover:bg-blue-900/50 disabled:opacity-50 transition-colors">現在ページ全選択 ({currentModels.length})</button>
                <button onClick={selectAllFiltered} disabled={filteredAndSortedModels.length === 0} className="px-3 py-2 text-xs bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-md hover:bg-green-200 dark:hover:bg-green-900/50 disabled:opacity-50 transition-colors">フィルタ結果全選択 ({filteredAndSortedModels.length})</button>
                <button onClick={() => setSelectedIds([])} disabled={selectedIds.length === 0} className="px-3 py-2 text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 disabled:opacity-50 transition-colors">選択解除</button>
            </div>
        </div>

        <div className="space-y-2">
            <label htmlFor="items-per-page" className="text-sm font-medium text-gray-700 dark:text-gray-300">表示件数</label>
            <select id="items-per-page" value={itemsPerPage} onChange={(e) => setItemsPerPage(Number(e.target.value))} className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"><option value={25}>25件</option><option value={50}>50件</option><option value={100}>100件</option><option value={200}>200件</option></select>
        </div>

        <div className="space-y-3 pt-4 border-t border-gray-200 dark:border-gray-600">
          <button onClick={fetchModels} disabled={loading} className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 disabled:opacity-50 transition-colors"><RotateCcwIcon className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />{loading ? '更新中...' : 'サーバーから再取得'}</button>
          <button onClick={() => setShowBulkConfirmModal(true)} disabled={selectedIds.length === 0} className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors"><TrashIcon className="h-4 w-4" />選択したモデルを削除 ({selectedIds.length})</button>
        </div>
        {error && (<div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"><p className="text-xs text-red-700 dark:text-red-300">{error}</p></div>)}
      </div>
    </>
  );

  const mainContent = (
    <>
      <div className="p-6 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 space-y-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">学習済みモデル一覧</h3>
        <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1 relative"><SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" /><input type="text" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} placeholder="モデル名, 説明, IDなどで検索..." className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent" /></div>
            <div className="lg:w-48"><select value={`${sortBy}-${sortOrder}`} onChange={(e) => { const [field, order] = e.target.value.split('-'); setSortBy(field as 'name' | 'created_at'); setSortOrder(order as 'asc' | 'desc'); }} className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"><option value="created_at-desc">作成日時 (新しい順)</option><option value="created_at-asc">作成日時 (古い順)</option><option value="name-asc">名前 (昇順)</option><option value="name-desc">名前 (降順)</option></select></div>
        </div>
      </div>

      <div className="px-6 py-3 bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <div className="text-sm text-gray-600 dark:text-gray-400">{filteredAndSortedModels.length > 0 ? (<>{(currentPage - 1) * itemsPerPage + 1}-{Math.min(currentPage * itemsPerPage, filteredAndSortedModels.length)} / {filteredAndSortedModels.length.toLocaleString()} 件</>) : 'データがありません'}</div>
        {totalPages > 1 && (<div className="flex items-center gap-2"><button onClick={() => setCurrentPage(p => Math.max(1, p - 1))} disabled={currentPage === 1} className="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50"><ChevronLeftIcon className="h-4 w-4" /></button><span className="text-sm font-medium">{currentPage} / {totalPages}</span><button onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))} disabled={currentPage === totalPages} className="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50"><ChevronRightIcon className="h-4 w-4" /></button></div>)}
      </div>

      <div className="flex-1 overflow-auto bg-gray-50 dark:bg-gray-950">
        {loading ? (<div className="flex items-center justify-center h-full"><Spinner className="h-8 w-8 text-blue-500" /></div>) : currentModels.length === 0 ? (<div className="flex items-center justify-center h-full text-center text-gray-500 dark:text-gray-400"><p>{models.length > 0 ? '条件に一致するモデルがありません。' : '表示するモデルがありません。'}</p>{searchTerm && <button onClick={() => setSearchTerm('')} className="text-sm text-blue-500 hover:underline mt-2">検索をクリア</button>}</div>) : (
          <div className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
            {currentModels.map((model) => (
              <div key={model.ID} className={`transition-colors duration-150 ${selectedIds.includes(model.ID) ? 'bg-blue-100 dark:bg-blue-900/30' : 'even:bg-gray-50 dark:even:bg-gray-800/50 hover:bg-blue-50 dark:hover:bg-blue-900/20'}`} onClick={() => toggleSelection(model.ID)}>
                <div className="px-6 py-4 flex items-start justify-between gap-4 cursor-pointer">
                  <div className="flex-shrink-0 pt-1"><input type="checkbox" checked={selectedIds.includes(model.ID)} onChange={(e) => { e.stopPropagation(); toggleSelection(model.ID); }} className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"/></div>
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-semibold text-gray-900 dark:text-white truncate">{model.name}</h4>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{model.description}</p>
                    <div className="font-mono text-xs text-gray-500 dark:text-gray-400 mt-2 space-y-1">
                        <div className="flex items-center gap-2">
                            <span className="flex-shrink-0">ID:</span>
                            <span className="text-gray-700 dark:text-gray-300 truncate">{model.ID}</span>
                            <button onClick={(e) => { e.stopPropagation(); copyToClipboard(model.ID, 'ID'); }} className="p-1 text-gray-400 hover:text-gray-700 dark:hover:text-white rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 flex-shrink-0"><ClipboardDocumentIcon className="h-4 w-4" /></button>
                        </div>
                        <div className="flex items-center gap-2">
                            <span className="flex-shrink-0">Dataset ID:</span>
                            <span className="text-gray-700 dark:text-gray-300 truncate">{model.Dataset_ID}</span>
                            <button onClick={(e) => { e.stopPropagation(); copyToClipboard(model.Dataset_ID, 'Dataset ID'); }} className="p-1 text-gray-400 hover:text-gray-700 dark:hover:text-white rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 flex-shrink-0"><ClipboardDocumentIcon className="h-4 w-4" /></button>
                        </div>
                    </div>
                    <div className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                        Created: {new Date(model.created_at).toLocaleString('ja-JP')}
                    </div>
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
      <div className="flex h-screen flex-col bg-gray-50 dark:bg-gray-950">
        <Header />
        <div className="flex-1 flex overflow-hidden">
          <aside className="w-80 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 flex flex-col">{sidebarContent}</aside>
          <main className="flex-1 flex flex-col overflow-hidden">{mainContent}</main>
        </div>
        <Footer />
      </div>

      {toast && (<div className="fixed bottom-5 right-5 z-50"><div className={`px-4 py-3 rounded-lg shadow-lg text-sm font-medium ${toast.type === 'success' ? 'bg-green-100 dark:bg-green-800/90 text-green-800 dark:text-green-100' : 'bg-red-100 dark:bg-red-800/90 text-red-800 dark:text-red-100'}`}>{toast.message}</div></div>)}
      
      {showBulkConfirmModal && (<div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60"><div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 w-full max-w-md"><h3 className="text-lg font-medium text-gray-900 dark:text-white">一括削除の確認</h3><div className="mt-4"><p className="text-sm text-gray-600 dark:text-gray-300">{selectedIds.length}件のモデルを本当に削除しますか？この操作は元に戻せません。</p></div><div className="mt-6 flex justify-end gap-3"><button type="button" onClick={() => setShowBulkConfirmModal(false)} className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm hover:bg-gray-50 dark:hover:bg-gray-600">キャンセル</button><button type="button" onClick={confirmBulkDelete} className="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md shadow-sm hover:bg-red-700">削除する</button></div></div></div>)}
    </>
  );
}