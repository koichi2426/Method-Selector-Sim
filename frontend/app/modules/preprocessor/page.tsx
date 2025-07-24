"use client";

import { Header } from "@/app/components/Header";
import { Footer } from "@/app/components/Footer";
import React, { useState, useEffect, useMemo } from 'react';
// 外部ファイルからアイコンコンポーネントをインポート
import {
  SettingsIcon,
  RotateCcwIcon,
  PlayIcon,
  SearchIcon,
  FilterIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  Spinner
} from "@/app/components/Icons";

// シナリオデータの型定義
interface Scenario {
  ID: string;
  state: string;
  method_group: string[];
  target_method: string;
  negative_method_group: string[];
}

export default function PreprocessorPage() {
  // --- State Management ---
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [selectedScenarios, setSelectedScenarios] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [processResult, setProcessResult] = useState<any>(null);
  
  // 検索とフィルタリング用のState
  const [searchTerm, setSearchTerm] = useState('');
  const [methodFilter, setMethodFilter] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(50);
  // エラーを修正: 'id' を 'ID' に変更
  const [sortBy, setSortBy] = useState<'state' | 'target_method' | 'ID'>('state');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  // --- API Communication ---

  // APIからシナリオを取得する関数
  const fetchScenarios = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/v1/scenarios');
      if (!response.ok) {
        throw new Error(`HTTPエラー: ${response.status}`);
      }
      const data = await response.json();
      setScenarios(data);
    } catch (err) {
      setError(`シナリオの取得に失敗しました: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setLoading(false);
    }
  };

  // 選択されたシナリオを処理する関数
  const processScenarios = async () => {
    if (selectedScenarios.length === 0) {
      setError('処理するシナリオを選択してください');
      return;
    }

    setProcessing(true);
    setError(null);
    setProcessResult(null);

    try {
      const response = await fetch('http://localhost:8000/v1/scenarios/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          scenario_ids: selectedScenarios
        }),
      });

      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(`HTTPエラー: ${response.status} - ${errorData}`);
      }

      const result = await response.json();
      setProcessResult(result);
      setSelectedScenarios([]); // 処理成功後、選択をクリア
      await fetchScenarios(); // シナリオ一覧を再読み込み
    } catch (err) {
      setError(`処理に失敗しました: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setProcessing(false);
    }
  };

  // --- Memos and Effects ---

  // フィルタリングとソートをメモ化
  const filteredAndSortedScenarios = useMemo(() => {
    let filtered = scenarios.filter(scenario => {
      const searchLower = searchTerm.toLowerCase();
      const matchesSearch = searchTerm === '' || 
        scenario.state.toLowerCase().includes(searchLower) ||
        scenario.target_method.toLowerCase().includes(searchLower) ||
        scenario.ID.toLowerCase().includes(searchLower);
      
      const methodLower = methodFilter.toLowerCase();
      const matchesMethod = methodFilter === '' ||
        scenario.method_group.some(method => method.toLowerCase().includes(methodLower)) ||
        scenario.negative_method_group.some(method => method.toLowerCase().includes(methodLower));
      
      return matchesSearch && matchesMethod;
    });

    // ソート処理
    filtered.sort((a, b) => {
      const fieldA = a[sortBy]?.toString().toLowerCase() || '';
      const fieldB = b[sortBy]?.toString().toLowerCase() || '';
      
      if (sortOrder === 'asc') {
        return fieldA.localeCompare(fieldB);
      } else {
        return fieldB.localeCompare(fieldA);
      }
    });

    return filtered;
  }, [scenarios, searchTerm, methodFilter, sortBy, sortOrder]);

  // ページネーション関連の計算
  const totalPages = Math.ceil(filteredAndSortedScenarios.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentScenarios = filteredAndSortedScenarios.slice(startIndex, endIndex);

  // フィルタ用ドロップダウンのメソッド一覧をメモ化
  const uniqueMethods = useMemo(() => {
    const methods = new Set<string>();
    scenarios.forEach(scenario => {
      scenario.method_group.forEach(method => methods.add(method));
      scenario.negative_method_group.forEach(method => methods.add(method));
    });
    return Array.from(methods).sort();
  }, [scenarios]);

  // 初回マウント時にシナリオを読み込む
  useEffect(() => {
    fetchScenarios();
  }, []);

  // フィルタ条件が変更されたら1ページ目に戻る
  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, methodFilter, sortBy, sortOrder, itemsPerPage]);


  // --- Event Handlers ---

  const toggleScenario = (scenarioId: string) => {
    setSelectedScenarios(prev => 
      prev.includes(scenarioId)
        ? prev.filter(id => id !== scenarioId)
        : [...prev, scenarioId]
    );
  };

  const selectAllCurrentPage = () => {
    const currentIds = currentScenarios.map(s => s.ID);
    const newSelection = new Set([...selectedScenarios, ...currentIds]);
    setSelectedScenarios(Array.from(newSelection));
  };

  const selectAllFiltered = () => {
    const allFilteredIds = filteredAndSortedScenarios.map(s => s.ID);
    setSelectedScenarios(allFilteredIds);
  };

  const clearAll = () => {
    setSelectedScenarios([]);
  };

  // --- Render ---

  return (
    <div className="flex min-h-screen flex-col bg-gray-50 dark:bg-gray-950">
      <Header />
      
      <div className="flex-1 flex overflow-hidden">
        {/* 操作パネル (左サイドバー) */}
        <aside className="w-80 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 flex flex-col">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-3 mb-4">
              <SettingsIcon className="h-6 w-6 text-gray-600 dark:text-gray-400" />
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">操作パネル</h2>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              シナリオを選択して収集処理を実行します
            </p>
          </div>

          <div className="p-6 space-y-6 flex-1 overflow-y-auto">
            {/* 統計情報 */}
            <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">総データ数:</span>
                <span className="font-medium text-gray-900 dark:text-white">{scenarios.length.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">フィルタ後:</span>
                <span className="font-medium text-gray-900 dark:text-white">{filteredAndSortedScenarios.length.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">選択済み:</span>
                <span className="font-medium text-blue-600 dark:text-blue-400">{selectedScenarios.length.toLocaleString()}</span>
              </div>
            </div>

            {/* 選択操作 */}
            <div className="space-y-3">
              <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">選択操作</h3>
              <div className="grid grid-cols-1 gap-2">
                <button onClick={selectAllCurrentPage} disabled={currentScenarios.length === 0} className="px-3 py-2 text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-md hover:bg-blue-200 dark:hover:bg-blue-900/50 disabled:opacity-50 transition-colors">
                  現在ページ全選択 ({currentScenarios.length})
                </button>
                <button onClick={selectAllFiltered} disabled={filteredAndSortedScenarios.length === 0} className="px-3 py-2 text-xs bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-md hover:bg-green-200 dark:hover:bg-green-900/50 disabled:opacity-50 transition-colors">
                  フィルタ結果全選択 ({filteredAndSortedScenarios.length})
                </button>
                <button onClick={clearAll} disabled={selectedScenarios.length === 0} className="px-3 py-2 text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 disabled:opacity-50 transition-colors">
                  選択解除
                </button>
              </div>
            </div>

            {/* 表示件数 */}
            <div className="space-y-2">
              <label htmlFor="items-per-page" className="text-sm font-medium text-gray-700 dark:text-gray-300">表示件数</label>
              <select id="items-per-page" value={itemsPerPage} onChange={(e) => setItemsPerPage(Number(e.target.value))} className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500">
                <option value={25}>25件</option>
                <option value={50}>50件</option>
                <option value={100}>100件</option>
                <option value={200}>200件</option>
                <option value={500}>500件</option>
              </select>
            </div>

            {/* アクションボタン */}
            <div className="space-y-3 pt-4 border-t border-gray-200 dark:border-gray-600">
              <button onClick={fetchScenarios} disabled={loading} className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 disabled:opacity-50 transition-colors">
                <RotateCcwIcon className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                {loading ? '更新中...' : 'シナリオ更新'}
              </button>
              <button onClick={processScenarios} disabled={processing || selectedScenarios.length === 0} className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors">
                <PlayIcon className={`h-4 w-4 ${processing ? 'animate-pulse' : ''}`} />
                {processing ? '処理中...' : `収集処理実行 (${selectedScenarios.length})`}
              </button>
            </div>

            {/* ステータスメッセージ */}
            {error && (
              <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                <p className="text-xs text-red-700 dark:text-red-300">{error}</p>
              </div>
            )}
            {processResult && (
              <div className="p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
                <p className="text-xs text-green-700 dark:text-green-300 font-medium mb-1">処理完了</p>
                <pre className="text-xs text-green-600 dark:text-green-400 whitespace-pre-wrap break-all max-h-32 overflow-y-auto">{JSON.stringify(processResult, null, 2)}</pre>
              </div>
            )}
          </div>
        </aside>

        {/* メインコンテンツ */}
        <main className="flex-1 flex flex-col overflow-hidden">
          {/* 検索・フィルターバー */}
          <div className="p-6 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">シナリオ一覧</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">機械学習用学習データの収集対象を選択</p>
            </div>
            <div className="flex flex-col lg:flex-row gap-4">
              <div className="flex-1 relative">
                <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input type="text" placeholder="状態、メソッド、IDで検索..." value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
              </div>
              <div className="lg:w-64 relative">
                <FilterIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <select value={methodFilter} onChange={(e) => setMethodFilter(e.target.value)} className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                  <option value="">全メソッド</option>
                  {uniqueMethods.map(method => (<option key={method} value={method}>{method}</option>))}
                </select>
              </div>
              <div className="lg:w-48">
                {/* エラーを修正: 'id' を 'ID' に変更 */}
                <select value={`${sortBy}-${sortOrder}`} onChange={(e) => { const [field, order] = e.target.value.split('-'); setSortBy(field as 'state' | 'target_method' | 'ID'); setSortOrder(order as 'asc' | 'desc'); }} className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                  <option value="state-asc">状態 (昇順)</option>
                  <option value="state-desc">状態 (降順)</option>
                  <option value="target_method-asc">メソッド (昇順)</option>
                  <option value="target_method-desc">メソッド (降順)</option>
                  <option value="ID-asc">ID (昇順)</option>
                  <option value="ID-desc">ID (降順)</option>
                </select>
              </div>
            </div>
          </div>

          {/* 結果件数とページネーション */}
          <div className="px-6 py-3 bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
            <div className="text-sm text-gray-600 dark:text-gray-400">
              {filteredAndSortedScenarios.length > 0 ? (
                <>{startIndex + 1}-{Math.min(endIndex, filteredAndSortedScenarios.length)} / {filteredAndSortedScenarios.length.toLocaleString()} 件</>
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

          {/* シナリオ一覧 */}
          <div className="flex-1 overflow-auto bg-gray-50 dark:bg-gray-950">
            {loading ? (
              <div className="flex items-center justify-center h-full"><Spinner className="h-8 w-8 text-blue-500" /></div>
            ) : currentScenarios.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center text-gray-500 dark:text-gray-400">
                  <p>条件に一致するシナリオが見つかりません。</p>
                  {(searchTerm || methodFilter) && (
                    <button onClick={() => { setSearchTerm(''); setMethodFilter(''); }} className="text-blue-600 dark:text-blue-400 hover:underline text-sm mt-2">検索条件をクリア</button>
                  )}
                </div>
              </div>
            ) : (
              <div className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                {currentScenarios.map((scenario) => (
                  <div key={scenario.ID} className={`px-6 py-4 cursor-pointer transition-colors ${selectedScenarios.includes(scenario.ID) ? 'bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500' : 'hover:bg-gray-50 dark:hover:bg-gray-800/50'}`} onClick={() => toggleScenario(scenario.ID)}>
                    <div className="flex items-start gap-4">
                      <div className="flex-shrink-0 pt-1">
                        <input type="checkbox" checked={selectedScenarios.includes(scenario.ID)} onChange={(e) => { e.stopPropagation(); toggleScenario(scenario.ID); }} className="h-4 w-4 text-blue-600 rounded border-gray-300 dark:border-gray-600 focus:ring-blue-500" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex-1">
                            <h4 className="text-sm font-medium text-gray-900 dark:text-white leading-5">{scenario.state}</h4>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{scenario.target_method}</p>
                          </div>
                          <div className="text-xs text-gray-400 dark:text-gray-500 font-mono ml-4 flex-shrink-0">{scenario.ID.substring(0, 8)}</div>
                        </div>
                        <div className="flex flex-wrap items-center gap-x-4 gap-y-1">
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-gray-500 dark:text-gray-400">メソッド:</span>
                            <div className="flex flex-wrap gap-1">
                              {scenario.method_group.map((method, index) => (<span key={index} className="inline-block px-2 py-0.5 text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded">{method}</span>))}
                            </div>
                          </div>
                          {scenario.negative_method_group.length > 0 && (
                            <div className="flex items-center gap-2">
                              <span className="text-xs text-gray-500 dark:text-gray-400">除外:</span>
                              <div className="flex flex-wrap gap-1">
                                {scenario.negative_method_group.map((method, index) => (<span key={index} className="inline-block px-2 py-0.5 text-xs bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded">{method}</span>))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </main>
      </div>
      
      <Footer />
    </div>
  );
}