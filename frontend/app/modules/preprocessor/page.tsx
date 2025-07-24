"use client";

import { Header } from "@/app/components/Header";
import { Footer } from "@/app/components/Footer";
import Link from "next/link";
import React, { useState, useEffect, useMemo } from 'react';

// SVG Icon components
const ArrowLeft = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 12H5m0 0l7 7m-7-7l7-7" />
  </svg>
);

const Play = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const RotateCcw = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M1 4v6h6M3.51 15a9 9 0 1013.58-8.51" />
  </svg>
);

const Search = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
  </svg>
);

const Filter = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
  </svg>
);

const ChevronLeft = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
  </svg>
);

const ChevronRight = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
  </svg>
);

const Settings = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);

interface Scenario {
  ID: string;
  state: string;
  method_group: string[];
  target_method: string;
  negative_method_group: string[];
}

export default function CollectorPage() {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [selectedScenarios, setSelectedScenarios] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [processResult, setProcessResult] = useState<any>(null);
  
  // Search and filter states
  const [searchTerm, setSearchTerm] = useState('');
  const [methodFilter, setMethodFilter] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(50);
  const [sortBy, setSortBy] = useState<'state' | 'target_method' | 'id'>('state');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  // Fetch scenarios from API
  const fetchScenarios = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/v1/scenarios');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setScenarios(data);
    } catch (err) {
      setError(`シナリオの取得に失敗しました: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setLoading(false);
    }
  };

  // Process selected scenarios
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
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setProcessResult(result);
      setSelectedScenarios([]); // Clear selection after successful processing
    } catch (err) {
      setError(`処理に失敗しました: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setProcessing(false);
    }
  };

  // Filter and sort scenarios
  const filteredAndSortedScenarios = useMemo(() => {
    let filtered = scenarios.filter(scenario => {
      const matchesSearch = searchTerm === '' || 
        scenario.state.toLowerCase().includes(searchTerm.toLowerCase()) ||
        scenario.target_method.toLowerCase().includes(searchTerm.toLowerCase()) ||
        scenario.ID.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesMethod = methodFilter === '' ||
        scenario.method_group.some(method => method.toLowerCase().includes(methodFilter.toLowerCase())) ||
        scenario.negative_method_group.some(method => method.toLowerCase().includes(methodFilter.toLowerCase()));
      
      return matchesSearch && matchesMethod;
    });

    // Sort
    filtered.sort((a, b) => {
      let aValue = '';
      let bValue = '';
      
      switch (sortBy) {
        case 'state':
          aValue = a.state;
          bValue = b.state;
          break;
        case 'target_method':
          aValue = a.target_method;
          bValue = b.target_method;
          break;
        case 'id':
          aValue = a.ID;
          bValue = b.ID;
          break;
      }
      
      if (sortOrder === 'asc') {
        return aValue.localeCompare(bValue);
      } else {
        return bValue.localeCompare(aValue);
      }
    });

    return filtered;
  }, [scenarios, searchTerm, methodFilter, sortBy, sortOrder]);

  // Pagination
  const totalPages = Math.ceil(filteredAndSortedScenarios.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentScenarios = filteredAndSortedScenarios.slice(startIndex, endIndex);

  // Get unique methods for filter dropdown
  const uniqueMethods = useMemo(() => {
    const methods = new Set<string>();
    scenarios.forEach(scenario => {
      scenario.method_group.forEach(method => methods.add(method));
      scenario.negative_method_group.forEach(method => methods.add(method));
    });
    return Array.from(methods).sort();
  }, [scenarios]);

  // Toggle scenario selection
  const toggleScenario = (scenarioId: string) => {
    setSelectedScenarios(prev => 
      prev.includes(scenarioId)
        ? prev.filter(id => id !== scenarioId)
        : [...prev, scenarioId]
    );
  };

  // Select all on current page
  const selectAllCurrentPage = () => {
    const currentIds = currentScenarios.map(s => s.ID);
    setSelectedScenarios(prev => {
      const newSelection = new Set([...prev, ...currentIds]);
      return Array.from(newSelection);
    });
  };

  // Select all filtered results
  const selectAllFiltered = () => {
    const allFilteredIds = filteredAndSortedScenarios.map(s => s.ID);
    setSelectedScenarios(prev => {
      const newSelection = new Set([...prev, ...allFilteredIds]);
      return Array.from(newSelection);
    });
  };

  // Clear all selections
  const clearAll = () => {
    setSelectedScenarios([]);
  };

  // Load scenarios on component mount
  useEffect(() => {
    fetchScenarios();
  }, []);

  // Reset to first page when filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, methodFilter, sortBy, sortOrder]);

  return (
    <div className="flex min-h-screen flex-col bg-gray-50 dark:bg-gray-950">
      <Header />
      
      <div className="flex-1 flex overflow-hidden">
        {/* Control Panel Sidebar */}
        <div className="w-80 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 flex flex-col">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-3 mb-4">
              <Settings className="h-6 w-6 text-gray-600 dark:text-gray-400" />
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">操作パネル</h2>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              シナリオを選択して収集処理を実行します
            </p>
          </div>

          <div className="p-6 space-y-6 flex-1 overflow-y-auto">
            {/* Statistics */}
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

            {/* Selection controls */}
            <div className="space-y-3">
              <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">選択操作</h3>
              <div className="grid grid-cols-1 gap-2">
                <button
                  onClick={selectAllCurrentPage}
                  disabled={currentScenarios.length === 0}
                  className="px-3 py-2 text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-md hover:bg-blue-200 dark:hover:bg-blue-900/50 disabled:opacity-50 transition-colors"
                >
                  現在ページ全選択 ({currentScenarios.length})
                </button>
                <button
                  onClick={selectAllFiltered}
                  disabled={filteredAndSortedScenarios.length === 0}
                  className="px-3 py-2 text-xs bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-md hover:bg-green-200 dark:hover:bg-green-900/50 disabled:opacity-50 transition-colors"
                >
                  フィルタ結果全選択 ({filteredAndSortedScenarios.length})
                </button>
                <button
                  onClick={clearAll}
                  disabled={selectedScenarios.length === 0}
                  className="px-3 py-2 text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 disabled:opacity-50 transition-colors"
                >
                  選択解除
                </button>
              </div>
            </div>

            {/* Page size selector */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">表示件数</label>
              <select
                value={itemsPerPage}
                onChange={(e) => setItemsPerPage(Number(e.target.value))}
                className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
              >
                <option value={25}>25件</option>
                <option value={50}>50件</option>
                <option value={100}>100件</option>
                <option value={200}>200件</option>
                <option value={500}>500件</option>
              </select>
            </div>

            {/* Action buttons */}
            <div className="space-y-3 pt-4 border-t border-gray-200 dark:border-gray-600">
              <button
                onClick={fetchScenarios}
                disabled={loading}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 disabled:opacity-50 transition-colors"
              >
                <RotateCcw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                {loading ? '更新中...' : 'シナリオ更新'}
              </button>

              <button
                onClick={processScenarios}
                disabled={processing || selectedScenarios.length === 0}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors"
              >
                <Play className={`h-4 w-4 ${processing ? 'animate-pulse' : ''}`} />
                {processing ? '処理中...' : `収集処理実行 (${selectedScenarios.length})`}
              </button>
            </div>

            {/* Status messages */}
            {error && (
              <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                <p className="text-xs text-red-700 dark:text-red-300">{error}</p>
              </div>
            )}

            {processResult && (
              <div className="p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
                <p className="text-xs text-green-700 dark:text-green-300 font-medium mb-1">
                  処理完了
                </p>
                <pre className="text-xs text-green-600 dark:text-green-400 whitespace-pre-wrap max-h-32 overflow-y-auto">
                  {JSON.stringify(processResult, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Search and Filter Bar */}
          <div className="p-6 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  シナリオ一覧
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  機械学習用学習データの収集対象を選択
                </p>
              </div>
            </div>

            <div className="flex flex-col lg:flex-row gap-4">
              {/* Search */}
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="状態、メソッド、IDで検索..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              {/* Method Filter */}
              <div className="lg:w-64 relative">
                <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <select
                  value={methodFilter}
                  onChange={(e) => setMethodFilter(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">全メソッド</option>
                  {uniqueMethods.map(method => (
                    <option key={method} value={method}>{method}</option>
                  ))}
                </select>
              </div>

              {/* Sort */}
              <div className="lg:w-48">
                <select
                  value={`${sortBy}-${sortOrder}`}
                  onChange={(e) => {
                    const [field, order] = e.target.value.split('-');
                    setSortBy(field as 'state' | 'target_method' | 'id');
                    setSortOrder(order as 'asc' | 'desc');
                  }}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="state-asc">状態 (昇順)</option>
                  <option value="state-desc">状態 (降順)</option>
                  <option value="target_method-asc">メソッド (昇順)</option>
                  <option value="target_method-desc">メソッド (降順)</option>
                  <option value="id-asc">ID (昇順)</option>
                  <option value="id-desc">ID (降順)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Results Info and Pagination */}
          <div className="px-6 py-3 bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
            <div className="text-sm text-gray-600 dark:text-gray-400">
              {filteredAndSortedScenarios.length > 0 ? (
                <>
                  {startIndex + 1}-{Math.min(endIndex, filteredAndSortedScenarios.length)} / {filteredAndSortedScenarios.length.toLocaleString()} 件
                  {searchTerm || methodFilter ? ` (${scenarios.length.toLocaleString()}件から絞り込み)` : ''}
                </>
              ) : (
                'データがありません'
              )}
            </div>

            {totalPages > 1 && (
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                  className="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <ChevronLeft className="h-4 w-4" />
                </button>
                <span className="text-sm font-medium min-w-0 px-2">
                  {currentPage} / {totalPages}
                </span>
                <button
                  onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                  className="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <ChevronRight className="h-4 w-4" />
                </button>
              </div>
            )}
          </div>

          {/* Scenario List */}
          <div className="flex-1 overflow-auto bg-gray-50 dark:bg-gray-950">
            {loading ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <RotateCcw className="h-8 w-8 animate-spin text-gray-400 mx-auto mb-3" />
                  <div className="text-gray-500 dark:text-gray-400">シナリオを読み込み中...</div>
                </div>
              </div>
            ) : currentScenarios.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <div className="text-gray-500 dark:text-gray-400 mb-2">
                    {filteredAndSortedScenarios.length === 0 ? '条件に一致するシナリオが見つかりません' : 'このページにはデータがありません'}
                  </div>
                  {(searchTerm || methodFilter) && (
                    <button
                      onClick={() => {
                        setSearchTerm('');
                        setMethodFilter('');
                      }}
                      className="text-blue-600 dark:text-blue-400 hover:underline text-sm"
                    >
                      検索条件をクリア
                    </button>
                  )}
                </div>
              </div>
            ) : (
              <div className="bg-white dark:bg-gray-900">
                <div className="divide-y divide-gray-200 dark:divide-gray-700">
                  {currentScenarios.map((scenario) => (
                    <div
                      key={scenario.ID}
                      className={`px-6 py-4 cursor-pointer transition-colors ${
                        selectedScenarios.includes(scenario.ID)
                          ? 'bg-blue-50 dark:bg-blue-900/10 border-l-4 border-l-blue-500'
                          : 'hover:bg-gray-50 dark:hover:bg-gray-800/50'
                      }`}
                      onClick={() => toggleScenario(scenario.ID)}
                    >
                      <div className="flex items-start gap-4">
                        <div className="flex-shrink-0 pt-1">
                          <input
                            type="checkbox"
                            checked={selectedScenarios.includes(scenario.ID)}
                            onChange={() => toggleScenario(scenario.ID)}
                            className="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
                          />
                        </div>
                        
                        <div className="flex-1 min-w-0">
                          {/* メイン情報 */}
                          <div className="flex items-start justify-between mb-3">
                            <div className="flex-1">
                              <h4 className="text-sm font-medium text-gray-900 dark:text-white leading-5">
                                {scenario.state}
                              </h4>
                              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                                {scenario.target_method}
                              </p>
                            </div>
                            <div className="text-xs text-gray-400 dark:text-gray-500 font-mono ml-4">
                              {scenario.ID.substring(0, 8)}...
                            </div>
                          </div>

                          {/* メソッドタグ */}
                          <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2">
                              <span className="text-xs text-gray-500 dark:text-gray-400">メソッド:</span>
                              <div className="flex flex-wrap gap-1">
                                {scenario.method_group.map((method, index) => (
                                  <span
                                    key={index}
                                    className="inline-block px-2 py-0.5 text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded"
                                  >
                                    {method}
                                  </span>
                                ))}
                              </div>
                            </div>
                            
                            {scenario.negative_method_group.length > 0 && (
                              <div className="flex items-center gap-2">
                                <span className="text-xs text-gray-500 dark:text-gray-400">除外:</span>
                                <div className="flex flex-wrap gap-1">
                                  {scenario.negative_method_group.map((method, index) => (
                                    <span
                                      key={index}
                                      className="inline-block px-2 py-0.5 text-xs bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded"
                                    >
                                      {method}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  );
}