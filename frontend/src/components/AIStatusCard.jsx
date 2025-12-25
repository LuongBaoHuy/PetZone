import React from 'react';
import { Camera, CheckCircle, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';

export const AIStatusCard = ({ hasPet = true, confidence = 0.95, loading = false }) => {
  const getDetectionStatus = () => {
    if (!hasPet) {
      return {
        title: 'Chuồng Trống',
        description: 'Không phát hiện thú cưng',
        color: 'from-slate-600 to-gray-600',
        icon: AlertCircle,
        textColor: 'text-slate-300',
        bgColor: 'bg-slate-500/20',
      };
    }

    return {
      title: 'Phát Hiện Thú Cưng',
      description: 'AI nhận diện có thú cưng trong chuồng',
      color: 'from-pink-600 to-rose-600',
      icon: CheckCircle,
      textColor: 'text-pink-300',
      bgColor: 'bg-pink-500/20',
    };
  };

  const status = getDetectionStatus();
  const Icon = status.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className={`relative overflow-hidden rounded-2xl p-8 backdrop-blur-sm border border-white/10 shadow-2xl
        bg-gradient-to-br ${status.color} bg-opacity-10 hover:bg-opacity-20 transition-all duration-300
      `}
    >
      {/* Background glow effect */}
      {hasPet && (
        <motion.div
          animate={{ opacity: [0.4, 0.8, 0.4] }}
          transition={{ duration: 3, repeat: Infinity }}
          className="absolute inset-0 bg-gradient-to-t from-pink-500/20 to-transparent"
        />
      )}

      <div className="relative z-10">
        <div className="flex items-start justify-between mb-8">
          <div>
            <h3 className="text-lg font-bold text-white/80 mb-1">Nhận Diện AI</h3>
            <p className="text-sm text-white/50">Camera & Phân tích hình ảnh</p>
          </div>
          <motion.div
            whileHover={{ scale: 1.1 }}
            className={`p-4 ${status.bgColor} rounded-full border border-white/20`}
          >
            <Camera className={`w-8 h-8 ${status.textColor}`} />
          </motion.div>
        </div>

        {/* Detection status */}
        <div className="space-y-6">
          {/* Main detection indicator */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <motion.div
                animate={hasPet ? { scale: [1, 1.2, 1] } : {}}
                transition={{ duration: 1, repeat: Infinity }}
              >
                <Icon className={`w-7 h-7 ${status.textColor}`} />
              </motion.div>
              <h4 className="text-2xl font-bold text-white">{status.title}</h4>
            </div>
            <p className="text-sm text-white/70 ml-10">{status.description}</p>
          </div>

          {/* Confidence bar */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-white/60">Độ tin cây</span>
              <motion.span
                animate={{ opacity: [0.7, 1, 0.7] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="text-sm font-bold text-pink-400"
              >
                {(confidence * 100).toFixed(1)}%
              </motion.span>
            </div>
            <div className="h-2 bg-white/10 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${confidence * 100}%` }}
                transition={{ duration: 0.8 }}
                className="h-full rounded-full bg-gradient-to-r from-pink-500 to-rose-500"
              />
            </div>
          </div>

          {/* Camera status */}
          <div className="p-4 bg-white/5 rounded-xl border border-white/10 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-white/70">Tình trạng Camera</span>
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
                className="w-3 h-3 bg-green-500 rounded-full"
              />
            </div>
            <p className="text-xs text-white/50">Hoạt động bình thường</p>
          </div>

          {/* Detection mode badge */}
          <div className="flex gap-2">
            <span className="px-3 py-1 text-xs font-semibold bg-gradient-to-r from-cyan-500/30 to-blue-500/30 border border-cyan-500/50 rounded-full text-cyan-300">
              🎯 Motion Detection
            </span>
            <span className="px-3 py-1 text-xs font-semibold bg-gradient-to-r from-purple-500/30 to-pink-500/30 border border-purple-500/50 rounded-full text-purple-300">
              ✨ Real-time
            </span>
          </div>
        </div>
      </div>

      {/* Loading state */}
      {loading && (
        <div className="absolute inset-0 bg-black/20 backdrop-blur-sm rounded-2xl flex items-center justify-center">
          <div className="w-8 h-8 border-2 border-white/30 border-t-white rounded-full animate-spin" />
        </div>
      )}
    </motion.div>
  );
};

export default AIStatusCard;
