import React from 'react';
import { Heart, Moon, AlertCircle, Eye } from 'lucide-react';
import { motion } from 'framer-motion';

export const PetStatusCard = ({ isPresent = true, activityState = 'awake', loading = false }) => {
  const getStatusDisplay = () => {
    if (!isPresent) {
      return {
        title: 'Chuồng Trống',
        description: 'Thú cưng vắng mặt',
        color: 'from-gray-600 to-slate-600',
        icon: AlertCircle,
        pulse: false,
        textColor: 'text-gray-300',
      };
    }

    switch (activityState) {
      case 'sleeping':
        return {
          title: 'Đang Ngủ',
          description: 'Thú cưng đang nghỉ ngơi',
          color: 'from-indigo-600 to-purple-600',
          icon: Moon,
          pulse: true,
          textColor: 'text-indigo-300',
        };
      case 'awake':
        return {
          title: 'Đang Thức',
          description: 'Thú cưng năng động',
          color: 'from-green-600 to-teal-600',
          icon: Eye,
          pulse: true,
          textColor: 'text-green-300',
        };
      default:
        return {
          title: 'Không rõ',
          description: 'Không xác định trạng thái',
          color: 'from-yellow-600 to-orange-600',
          icon: AlertCircle,
          pulse: false,
          textColor: 'text-yellow-300',
        };
    }
  };

  const status = getStatusDisplay();
  const Icon = status.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.1 }}
      className={`relative overflow-hidden rounded-2xl p-8 backdrop-blur-sm border border-white/10 shadow-2xl
        bg-gradient-to-br ${status.color} bg-opacity-10 hover:bg-opacity-20 transition-all duration-300
      `}
    >
      {/* Animated background */}
      {status.pulse && (
        <motion.div
          animate={{ scale: [1, 1.1, 1], opacity: [0.5, 0.8, 0.5] }}
          transition={{ duration: 2, repeat: Infinity }}
          className={`absolute inset-0 bg-gradient-to-br ${status.color} opacity-10`}
        />
      )}

      <div className="relative z-10">
        <div className="flex items-start justify-between mb-8">
          <div>
            <h3 className="text-lg font-bold text-white/80 mb-1">Trạng Thái Thú Cưng</h3>
            <p className="text-sm text-white/50">Giám sát sự sống & Hoạt động</p>
          </div>
          <motion.div
            animate={status.pulse ? { scale: [1, 1.2, 1] } : {}}
            transition={{ duration: 2, repeat: Infinity }}
            className={`p-4 bg-white/10 rounded-full ${status.pulse ? 'ring-2 ring-white/30' : ''}`}
          >
            <Icon className={`w-8 h-8 ${status.textColor}`} />
          </motion.div>
        </div>

        {/* Status display */}
        <div className="space-y-6">
          {/* Main status */}
          <div>
            <div className="flex items-center gap-3 mb-3">
              <motion.div
                animate={status.pulse ? { scale: [1, 1.3, 1] } : {}}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="flex items-center"
              >
                <Heart className={`w-6 h-6 ${status.textColor} fill-current`} />
              </motion.div>
              <div>
                <h4 className="text-2xl font-bold text-white">{status.title}</h4>
                <p className="text-sm text-white/60">{status.description}</p>
              </div>
            </div>
          </div>

          {/* Activity indicator */}
          <div className="flex items-center gap-3 p-4 bg-white/5 rounded-xl border border-white/10">
            <div className={`w-3 h-3 rounded-full ${status.pulse ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`} />
            <span className="text-sm text-white/70">
              {loading ? 'Đang cập nhật...' : isPresent ? 'Thú cưng có mặt' : 'Chuồng trống'}
            </span>
          </div>

          {/* Energy indicators (if pet is present) */}
          {isPresent && (
            <div className="grid grid-cols-2 gap-3 pt-2">
              <div className="p-3 bg-white/5 rounded-lg">
                <p className="text-xs text-white/60 mb-1">Năng lượng tĩnh</p>
                <div className="h-1.5 bg-white/20 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-purple-500 rounded-full"
                    style={{ width: '70%' }}
                  />
                </div>
              </div>
              <div className="p-3 bg-white/5 rounded-lg">
                <p className="text-xs text-white/60 mb-1">Năng lượng động</p>
                <div className="h-1.5 bg-white/20 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-cyan-500 rounded-full"
                    style={{ width: '55%' }}
                  />
                </div>
              </div>
            </div>
          )}
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

export default PetStatusCard;
