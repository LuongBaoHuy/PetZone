import React from 'react';
import { Cloud, CloudRain, Droplets } from 'lucide-react';
import { motion } from 'framer-motion';

export const TemperatureCard = ({ temperature = 28, humidity = 65, loading = false }) => {
  const isHot = temperature > 30;
  const isCold = temperature < 18;
  
  const getTempColor = () => {
    if (isHot) return 'from-red-600 to-orange-500';
    if (isCold) return 'from-blue-600 to-cyan-500';
    return 'from-green-600 to-emerald-500';
  };

  const getTempStatus = () => {
    if (isHot) return { text: 'Nóng! Bật quạt', color: 'text-red-400' };
    if (isCold) return { text: 'Lạnh', color: 'text-blue-400' };
    return { text: 'Bình thường', color: 'text-green-400' };
  };

  const status = getTempStatus();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`relative overflow-hidden rounded-2xl p-8 backdrop-blur-sm border border-white/10 shadow-2xl
        bg-gradient-to-br ${getTempColor()} bg-opacity-10 hover:bg-opacity-20 transition-all duration-300
        ${isHot ? 'ring-2 ring-red-500/50' : ''}
      `}
    >
      {/* Background animation */}
      <div className="absolute inset-0 opacity-30">
        {isHot && (
          <motion.div
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ duration: 3, repeat: Infinity }}
            className="absolute inset-0 bg-gradient-to-br from-red-500 to-transparent opacity-20"
          />
        )}
      </div>

      <div className="relative z-10">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-bold text-white/80">Môi Trường</h3>
          <div className="p-3 bg-white/10 rounded-full">
            {isHot ? (
              <Cloud className="w-6 h-6 text-orange-400" />
            ) : (
              <CloudRain className="w-6 h-6 text-blue-400" />
            )}
          </div>
        </div>

        {/* Temperature Display */}
        <div className="space-y-6">
          {/* Temp */}
          <div>
            <div className="flex items-baseline justify-between mb-2">
              <span className="text-sm text-white/60">Nhiệt độ</span>
              <span className={`text-sm font-semibold ${status.color}`}>{status.text}</span>
            </div>
            <motion.div
              animate={{ opacity: isHot ? [1, 0.8, 1] : 1 }}
              transition={{ duration: 2, repeat: isHot ? Infinity : 0 }}
              className="text-5xl font-bold text-white mb-2"
            >
              {loading ? '...' : temperature.toFixed(1)}°C
            </motion.div>
            <div className="h-2 bg-white/10 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${Math.min(temperature / 40 * 100, 100)}%` }}
                transition={{ duration: 0.5 }}
                className={`h-full rounded-full bg-gradient-to-r ${getTempColor()}`}
              />
            </div>
          </div>

          {/* Humidity */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-white/60 flex items-center gap-2">
                <Droplets className="w-4 h-4" />
                Độ ẩm
              </span>
              <span className="text-sm font-semibold text-cyan-400">{humidity.toFixed(1)}%</span>
            </div>
            <div className="h-2 bg-white/10 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${humidity}%` }}
                transition={{ duration: 0.5 }}
                className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-blue-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Loading skeleton */}
      {loading && (
        <div className="absolute inset-0 bg-black/20 backdrop-blur-sm rounded-2xl flex items-center justify-center">
          <div className="w-8 h-8 border-2 border-white/30 border-t-white rounded-full animate-spin" />
        </div>
      )}
    </motion.div>
  );
};

export default TemperatureCard;
