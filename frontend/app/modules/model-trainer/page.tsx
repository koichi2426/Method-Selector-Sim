"use client";

import React, { useState, useEffect, useMemo } from 'react';
import { Header } from "@/app/components/Header";
import { Footer } from "@/app/components/Footer";
import { 
    SettingsIcon,
    PlayIcon,
    Spinner,
    ExclamationTriangleIcon,
    RotateCcwIcon
} from '@/app/components/Icons';

// データセットの型定義をAPIレスポンスに合わせて修正
interface Dataset {
  ID: string;
  name: string;
  description: string;
  type: string;
  Triplet_ids: string[];
  created_at: string;
}

// トレーニング設定の型定義
interface TrainingConfig {
    dataset_id: string;
    epochs: number;
    batch_size: number;
    learning_rate: number;
    name: string;
    description: string;
}

export default function FinetunerPage() {
  // --- State Management ---
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [config, setConfig] = useState<TrainingConfig>({
    dataset_id: '',
    epochs: 10,
    batch_size: 32,
    learning_rate: 0.001,
    name: 'My New Training Run',
    description: 'Training a custom model with updated parameters.'
  });

  const [loadingDatasets, setLoadingDatasets] = useState(true);
  const [isTraining, setIsTraining] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [trainingResult, setTrainingResult] = useState<any>(null);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  // --- API Communication ---
  const fetchDatasets = async () => {
    setLoadingDatasets(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/v1/datasets');
      if (!response.ok) throw new Error(`HTTPエラー: ${response.status}`);
      const data = await response.json();
      const validDatasets = Array.isArray(data) ? data : [];
      setDatasets(validDatasets);
      // 最初のデータセットをデフォルトで選択
      if (validDatasets.length > 0 && !config.dataset_id) {
        setConfig(prev => ({ ...prev, dataset_id: validDatasets[0].ID }));
      }
    } catch (err) {
      setError(`データセットの取得に失敗しました: ${err instanceof Error ? err.message : String(err)}`);
      setDatasets([]);
    } finally {
      setLoadingDatasets(false);
    }
  };

  const handleStartTraining = async () => {
    // --- 送信前データ検証 ---
    if (!config.dataset_id) {
        setToast({ message: 'データセットを選択してください。', type: 'error' });
        return;
    }
    if (!config.name.trim()) {
        setToast({ message: 'モデル名を入力してください。', type: 'error' });
        return;
    }
    
    // 文字列の可能性があるため、送信直前に数値に変換
    const epochs = parseInt(String(config.epochs), 10);
    const batch_size = parseInt(String(config.batch_size), 10);
    const learning_rate = parseFloat(String(config.learning_rate));

    if (isNaN(epochs) || epochs <= 0 || isNaN(batch_size) || batch_size <= 0 || isNaN(learning_rate) || learning_rate <= 0) {
        setToast({ message: 'エポック数、バッチサイズ、学習率は0より大きい有効な数値を設定してください。', type: 'error' });
        return;
    }

    setIsTraining(true);
    setError(null);
    setTrainingResult(null);

    // --- 送信するデータ(ペイロード)を明示的に作成 ---
    const payload = {
        dataset_id: config.dataset_id,
        epochs: epochs,
        batch_size: batch_size,
        learning_rate: learning_rate,
        name: config.name,
        description: config.description,
    };

    // --- コンソールログにペイロードを出力 ---
    console.log("Sending training request with payload:", payload);

    try {
        const response = await fetch('http://localhost:8000/v1/models/train', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTPエラー: ${response.status}`);
        }
        const result = await response.json();
        setTrainingResult(result);
        setToast({ message: 'モデルのトレーニングを開始しました。', type: 'success' });
    } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'トレーニング開始リクエストに失敗しました。';
        setError(errorMessage);
        setToast({ message: errorMessage, type: 'error' });
    } finally {
        setIsTraining(false);
    }
  };

  useEffect(() => {
    fetchDatasets();
  }, []);

  useEffect(() => {
    if (toast) {
      const timer = setTimeout(() => setToast(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [toast]);

  const handleConfigChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setConfig(prev => ({
        ...prev,
        [name]: value
    }));
  };

  // --- Render Components ---
  const sidebarContent = (
    <>
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3 mb-4">
          <SettingsIcon className="h-6 w-6 text-gray-600 dark:text-gray-400" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">トレーニング設定</h2>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-400">パラメータを入力して学習を開始します</p>
      </div>
      <div className="p-6 space-y-4 flex-1 overflow-y-auto">
        <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 dark:text-gray-300">モデル名</label>
            <input type="text" name="name" id="name" value={config.name} onChange={handleConfigChange} className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white dark:bg-gray-800"/>
        </div>
        <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300">説明</label>
            <textarea name="description" id="description" value={config.description} onChange={handleConfigChange} rows={3} className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white dark:bg-gray-800"/>
        </div>
        <div>
            <label htmlFor="dataset_id" className="block text-sm font-medium text-gray-700 dark:text-gray-300">データセット</label>
            <select id="dataset_id" name="dataset_id" value={config.dataset_id} onChange={handleConfigChange} disabled={loadingDatasets} className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md bg-white dark:bg-gray-800 disabled:opacity-50">
                {loadingDatasets ? <option>読み込み中...</option> : datasets.map(d => <option key={d.ID} value={d.ID}>{d.name}</option>)}
            </select>
        </div>
        <div className="grid grid-cols-2 gap-4">
            <div>
                <label htmlFor="epochs" className="block text-sm font-medium text-gray-700 dark:text-gray-300">エポック数</label>
                <input type="number" name="epochs" id="epochs" value={config.epochs} onChange={handleConfigChange} min="1" className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white dark:bg-gray-800"/>
            </div>
            <div>
                <label htmlFor="batch_size" className="block text-sm font-medium text-gray-700 dark:text-gray-300">バッチサイズ</label>
                <input type="number" name="batch_size" id="batch_size" value={config.batch_size} onChange={handleConfigChange} min="1" className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white dark:bg-gray-800"/>
            </div>
        </div>
        <div>
            <label htmlFor="learning_rate" className="block text-sm font-medium text-gray-700 dark:text-gray-300">学習率</label>
            <input type="number" name="learning_rate" id="learning_rate" value={config.learning_rate} onChange={handleConfigChange} step="0.0001" min="0.00001" className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white dark:bg-gray-800"/>
        </div>
        <div className="pt-4 border-t border-gray-200 dark:border-gray-600">
            <button onClick={handleStartTraining} disabled={isTraining || loadingDatasets} className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors">
                <PlayIcon className={`h-4 w-4 ${isTraining ? 'animate-pulse' : ''}`} />
                {isTraining ? 'トレーニング中...' : 'トレーニング開始'}
            </button>
        </div>
      </div>
    </>
  );

  const mainContent = (
    <div className="p-6 flex-1 overflow-y-auto">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">トレーニングステータス</h3>
        <div className="mt-4 p-4 rounded-lg bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 min-h-[200px]">
            {error && (
                <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                    <h4 className="font-medium text-red-700 dark:text-red-300">エラー</h4>
                    <p className="text-xs text-red-700 dark:text-red-300 mt-1">{error}</p>
                </div>
            )}
            {trainingResult && (
                <div className="p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
                    <h4 className="font-medium text-green-700 dark:text-green-300">リクエスト成功</h4>
                    <p className="text-xs text-green-600 dark:text-green-400 mt-1">モデルのトレーニングが正常に開始されました。</p>
                    <pre className="mt-2 text-xs text-green-600 dark:text-green-400 whitespace-pre-wrap break-all max-h-64 overflow-y-auto">{JSON.stringify(trainingResult, null, 2)}</pre>
                </div>
            )}
            {!error && !trainingResult && (
                <div className="flex items-center justify-center h-full text-gray-500 dark:text-gray-400">
                    <p>トレーニングを開始すると、ここにステータスが表示されます。</p>
                </div>
            )}
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
