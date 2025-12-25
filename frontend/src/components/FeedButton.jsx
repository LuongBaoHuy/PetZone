import React, { useState } from 'react';
import { Send, Loader, AlertCircle, CheckCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const FeedButton = ({ onClick, loading = false, disabled = false }) => {
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedbackType, setFeedbackType] = useState('success'); // success, error

  const handleClick = async () => {
    try {
      setFeedbackType('success');
      setShowFeedback(true);
      await onClick?.();
      setTimeout(() => setShowFeedback(false), 3000);
    } catch (error) {
      setFeedbackType('error');
      setShowFeedback(true);
      setTimeout(() => setShowFeedback(false), 3000);
    }
  };

  return (
    <>
      <motion.div
        className="relative"
        whileHover={{ scale: disabled ? 1 : 1.05 }}
        whileTap={{ scale: disabled ? 1 : 0.95 }}
      >
        {/* Main button */}
        <button
          onClick={handleClick}
          disabled={disabled || loading}
          className={`relative overflow-hidden w-full py-6 px-8 rounded-2xl font-bold text-xl
            flex items-center justify-center gap-3 transition-all duration-300
            ${
              disabled || loading
                ? 'opacity-50 cursor-not-allowed bg-gray-600'
                : 'bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 active:shadow-inner shadow-xl'
            }
            text-white border-2 border-white/20
          `}
        >
          {/* Button shine effect */}
          <motion.div
            className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/30 to-white/0"
            initial={{ x: '-100%' }}
            animate={!disabled && !loading ? { x: '100%' } : {}}
            transition={{ duration: 2, repeat: Infinity }}
          />

          {/* Content */}
          <div className="relative z-10 flex items-center justify-center gap-3">
            <motion.div
              animate={loading ? { rotate: 360 } : {}}
              transition={{ duration: 1, repeat: Infinity, repeatType: 'loop' }}
            >
              {loading ? (
                <Loader className="w-6 h-6" />
              ) : (
                <motion.div
                  animate={{ y: [0, -4, 0] }}
                  transition={{ duration: 1, repeat: Infinity }}
                >
                  <Send className="w-6 h-6" />
                </motion.div>
              )}
            </motion.div>
            <span className="font-bold text-lg">
              {loading ? 'Đang Gửi...' : 'Cho Ăn Ngay'}
            </span>
          </div>

          {/* Pulse ring */}
          {!disabled && !loading && (
            <motion.div
              className="absolute inset-0 border-2 border-white/40 rounded-2xl"
              animate={{ scale: [1, 1.1], opacity: [1, 0] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            />
          )}
        </button>

        {/* Heat effect when active */}
        {!disabled && !loading && (
          <motion.div
            className="absolute -inset-2 bg-gradient-to-r from-orange-500 to-red-500 rounded-2xl blur-xl opacity-0 -z-10"
            animate={{ opacity: [0.2, 0.5, 0.2] }}
            transition={{ duration: 3, repeat: Infinity }}
          />
        )}
      </motion.div>

      {/* Feedback toast */}
      <AnimatePresence>
        {showFeedback && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.8 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.8 }}
            transition={{ type: 'spring', damping: 15 }}
            className={`mt-4 p-4 rounded-xl flex items-center gap-3 border-2
              ${
                feedbackType === 'success'
                  ? 'bg-green-500/20 border-green-500/50 text-green-300'
                  : 'bg-red-500/20 border-red-500/50 text-red-300'
              }
            `}
          >
            {feedbackType === 'success' ? (
              <CheckCircle className="w-6 h-6 flex-shrink-0" />
            ) : (
              <AlertCircle className="w-6 h-6 flex-shrink-0" />
            )}
            <span className="font-semibold">
              {feedbackType === 'success'
                ? '✅ Đã gửi lệnh cho ăn! Servo đang quay...'
                : '❌ Lỗi khi gửi lệnh. Vui lòng thử lại.'}
            </span>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default FeedButton;
