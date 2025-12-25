import React, { useState, useEffect } from 'react';
import { Wifi, AlertTriangle, CheckCircle, Sun, Moon } from 'lucide-react';
import { motion } from 'framer-motion';

export const Header = ({ isConnected = true, lastUpdate = null, onThemeToggle }) => {
  const [isDark, setIsDark] = useState(true);

  const formatTime = (date) => {
    if (!date) return 'Chưa cập nhật';
    return new Date(date).toLocaleTimeString('vi-VN');
  };

  const handleThemeToggle = () => {
    setIsDark(!isDark);
    onThemeToggle?.(!isDark);
  };

  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="sticky top-0 z-50 bg-gradient-to-b from-slate-900/95 to-slate-900/50 backdrop-blur-xl border-b border-white/10"
    >
      <div className="w-full flex justify-center">
        <div className="max-w-7xl w-full px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            {/* Logo & Title */}
          <motion.div whileHover={{ scale: 1.05 }} className="flex items-center gap-3 cursor-pointer">
            <div className="relative">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 4, repeat: Infinity, repeatType: 'loop' }}
                className="text-3xl"
              >
                🐾
              </motion.div>
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute -inset-2 bg-gradient-to-r from-orange-500/20 to-pink-500/20 rounded-full blur-lg -z-10"
              />
            </div>
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-orange-400 to-pink-400 bg-clip-text text-transparent">
                PetZone
              </h1>
              <p className="text-xs text-white/50">Smart Pet Cage Monitoring System</p>
            </div>
          </motion.div>

          {/* Status indicators */}
          <div className="flex items-center gap-3 sm:gap-6">
            {/* Theme Toggle */}
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleThemeToggle}
              className="p-2.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 transition-all duration-300"
              title={isDark ? 'Chuyển sang sáng' : 'Chuyển sang tối'}
            >
              {isDark ? (
                <Sun className="w-5 h-5 text-yellow-400" />
              ) : (
                <Moon className="w-5 h-5 text-slate-400" />
              )}
            </motion.button>

            {/* Connection status */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="flex items-center gap-3 px-4 py-2 rounded-lg bg-white/5 border border-white/10"
            >
              <motion.div
                animate={isConnected ? { scale: [1, 1.2, 1] } : {}}
                transition={{ duration: 1.5, repeat: Infinity }}
              >
                {isConnected ? (
                  <CheckCircle className="w-5 h-5 text-green-400" />
                ) : (
                  <AlertTriangle className="w-5 h-5 text-red-400" />
                )}
              </motion.div>
              <span className="text-sm font-medium">
                {isConnected ? (
                  <span className="text-green-400">Kết nối • Bình thường</span>
                ) : (
                  <span className="text-red-400">Mất kết nối • Lỗi</span>
                )}
              </span>
            </motion.div>

            {/* Last update */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="hidden sm:flex items-center gap-2 text-sm text-white/60"
            >
              <Wifi className="w-4 h-4" />
              <span>Cập nhật: {formatTime(lastUpdate)}</span>
            </motion.div>
          </div>
        </div>
      </div>
      </div>
    </motion.header>
  );
};

export default Header;
