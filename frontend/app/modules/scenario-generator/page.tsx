"use client";

import React, { useState, useEffect } from 'react';
import { Header } from "@/app/components/Header";
import { Footer } from "@/app/components/Footer";
import { 
    SettingsIcon,
    PlayIcon,
    Spinner,
    ExclamationTriangleIcon,
    TrashIcon,
    PlusIcon
} from '@/app/components/Icons';

// 型定義
interface MethodProfile {
  name: string;
  description: string;
}

interface Situation {
  name: string;
  description: string;
}

interface GenerationResult {
    scenarios_generated: number;
    scenario_ids: string[];
}

export default function LogGeneratorPage() {
  // --- State Management ---
  const [outputCount, setOutputCount] = useState<number>(5);
  const [methodPool, setMethodPool] = useState<MethodProfile[]>([
    { name: 'addToCart', description: 'Add product to the shopping cart' },
    { name: 'viewCart', description: 'View the contents of the shopping cart' },
  ]);
  const [situations, setSituations] = useState<Situation[]>([
    { name: 'On Product Page', description: 'User is viewing a product detail page' }
  ]);

  // UI State for adding new items
  const [newMethod, setNewMethod] = useState({ name: '', description: '' });
  const [newSituation, setNewSituation] = useState({ name: '', description: '' });

  // API State
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generationResult, setGenerationResult] = useState<GenerationResult | null>(null);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  // --- API Communication ---
  const handleGenerate = async () => {
    if (methodPool.length === 0 || situations.length === 0) {
        setToast({ message: '少なくとも1つのメソッドと状況が必要です。', type: 'error' });
        return;
    }
    setIsGenerating(true);
    setError(null);
    setGenerationResult(null);

    const payload = {
        output_count: Number(outputCount),
        method_pool: methodPool,
        situations: situations
    };

    console.log("Sending generation request with payload:", payload);

    try {
        const response = await fetch('http://localhost:8000/v1/scenarios/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTPエラー: ${response.status}`);
        }
        const result = await response.json();
        setGenerationResult(result);
        setToast({ message: 'シナリオの生成リクエストが成功しました。', type: 'success' });
    } catch (err) {
        const errorMessage = err instanceof Error ? err.message : '生成リクエストに失敗しました。';
        setError(errorMessage);
        setToast({ message: errorMessage, type: 'error' });
    } finally {
        setIsGenerating(false);
    }
  };
  
  useEffect(() => {
    if (toast) {
      const timer = setTimeout(() => setToast(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [toast]);

  // --- UI Handlers ---
  const addMethod = () => {
    if (newMethod.name.trim() && newMethod.description.trim()) {
        setMethodPool([...methodPool, newMethod]);
        setNewMethod({ name: '', description: '' });
    }
  };
  const removeMethod = (index: number) => {
    setMethodPool(methodPool.filter((_, i) => i !== index));
  };
  const addSituation = () => {
    if (newSituation.name.trim() && newSituation.description.trim()) {
        setSituations([...situations, newSituation]);
        setNewSituation({ name: '', description: '' });
    }
  };
  const removeSituation = (index: number) => {
    setSituations(situations.filter((_, i) => i !== index));
  };


  // --- Render Components ---
  const sidebarContent = (
    <>
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3 mb-4">
          <SettingsIcon className="h-6 w-6 text-gray-600 dark:text-gray-400" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">生成設定</h2>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-400">パラメータを入力してシナリオを生成します</p>
      </div>
      <div className="p-6 space-y-4 flex-1 overflow-y-auto">
        <div>
            <label htmlFor="outputCount" className="block text-sm font-medium text-gray-700 dark:text-gray-300">生成数 (output_count)</label>
            <input type="number" name="outputCount" id="outputCount" value={outputCount} onChange={(e) => setOutputCount(Number(e.target.value))} min="1" className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white dark:bg-gray-800"/>
        </div>
        
        <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
            <button onClick={handleGenerate} disabled={isGenerating} className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors">
                <PlayIcon className={`h-4 w-4 ${isGenerating ? 'animate-pulse' : ''}`} />
                {isGenerating ? '生成中...' : 'シナリオ生成開始'}
            </button>
        </div>
      </div>
    </>
  );

  const mainContent = (
    <div className="p-6 flex-1 overflow-y-auto flex flex-col gap-6">
        {/* Method Pool Section */}
        <div className="flex-1 flex flex-col">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">メソッドプール</h3>
            <div className="mt-4 p-4 rounded-lg bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 flex-1 flex flex-col">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <input type="text" value={newMethod.name} onChange={(e) => setNewMethod({...newMethod, name: e.target.value})} placeholder="メソッド名 (例: addToCart)" className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md sm:text-sm bg-white dark:bg-gray-800"/>
                    <input type="text" value={newMethod.description} onChange={(e) => setNewMethod({...newMethod, description: e.target.value})} placeholder="説明 (例: 商品をカートに追加)" className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md sm:text-sm bg-white dark:bg-gray-800"/>
                </div>
                <button onClick={addMethod} className="mb-4 w-full flex items-center justify-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-sm rounded-md"><PlusIcon className="h-4 w-4"/>メソッドを追加</button>
                <div className="flex-1 border rounded-md overflow-y-auto p-2 space-y-2 bg-gray-50 dark:bg-gray-800/50">
                    {methodPool.map((method, index) => (
                        <div key={index} className="p-2 rounded-md bg-white dark:bg-gray-900/50 flex justify-between items-center text-sm">
                            <div>
                                <div className="font-semibold">{method.name}</div>
                                <div className="text-xs text-gray-500 dark:text-gray-400">{method.description}</div>
                            </div>
                            <button onClick={() => removeMethod(index)} className="p-1 text-gray-400 hover:text-red-500 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"><TrashIcon className="h-4 w-4"/></button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
        {/* Situations Section */}
        <div className="flex-1 flex flex-col">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">状況 (Situations)</h3>
            <div className="mt-4 p-4 rounded-lg bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 flex-1 flex flex-col">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <input type="text" value={newSituation.name} onChange={(e) => setNewSituation({...newSituation, name: e.target.value})} placeholder="状況名 (例: On Product Page)" className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md sm:text-sm bg-white dark:bg-gray-800"/>
                    <input type="text" value={newSituation.description} onChange={(e) => setNewSituation({...newSituation, description: e.target.value})} placeholder="説明 (例: ユーザーが商品詳細ページを閲覧中)" className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md sm:text-sm bg-white dark:bg-gray-800"/>
                </div>
                <button onClick={addSituation} className="mb-4 w-full flex items-center justify-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-sm rounded-md"><PlusIcon className="h-4 w-4"/>状況を追加</button>
                <div className="flex-1 border rounded-md overflow-y-auto p-2 space-y-2 bg-gray-50 dark:bg-gray-800/50">
                    {situations.map((sit, index) => (
                        <div key={index} className="p-2 rounded-md bg-white dark:bg-gray-900/50 flex justify-between items-center text-sm">
                            <div>
                                <div className="font-semibold">{sit.name}</div>
                                <div className="text-xs text-gray-500 dark:text-gray-400">{sit.description}</div>
                            </div>
                            <button onClick={() => removeSituation(index)} className="p-1 text-gray-400 hover:text-red-500 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"><TrashIcon className="h-4 w-4"/></button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    </div>
  );

  return (
    <>
      <div className="flex h-screen flex-col bg-gray-50 dark:bg-gray-950">
        <Header />
        <div className="flex-1 flex overflow-hidden">
          <aside className="w-96 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 flex flex-col">{sidebarContent}</aside>
          <main className="flex-1 flex flex-col overflow-hidden">{mainContent}</main>
        </div>
        <Footer />
      </div>

      {toast && (<div className="fixed bottom-5 right-5 z-50"><div className={`px-4 py-3 rounded-lg shadow-lg text-sm font-medium ${toast.type === 'success' ? 'bg-green-100 dark:bg-green-800/90 text-green-800 dark:text-green-100' : 'bg-red-100 dark:bg-red-800/90 text-red-800 dark:text-red-100'}`}>{toast.message}</div></div>)}
    </>
  );
}
