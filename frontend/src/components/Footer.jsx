import React from 'react';
import { Heart, Github } from 'lucide-react';
import { motion } from 'framer-motion';

export const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <motion.footer
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      transition={{ duration: 0.8 }}
      className="mt-16 border-t border-white/10 bg-gradient-to-b from-transparent to-slate-900/50 backdrop-blur-sm"
    >
      <div className="w-full flex justify-center">
        <div className="max-w-7xl w-full px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          {/* About */}
          <div>
            <h3 className="text-lg font-bold text-white mb-3">PetZone</h3>
            <p className="text-sm text-white/60 leading-relaxed">
              Hệ thống giám sát chuồng nuôi thông minh kết hợp IoT, AI và Automation để chăm sóc thú cưng tốt hơn.
            </p>
          </div>

          {/* Tech Stack */}
          <div>
            <h3 className="text-lg font-bold text-white mb-3">Tech Stack</h3>
            <ul className="space-y-2 text-sm text-white/60">
              <li>⚛️ React + Vite (Frontend)</li>
              <li>🔧 .NET Core (Backend)</li>
              <li>📡 ESP32 (IoT)</li>
              <li>🐍 Python AI (OpenCV)</li>
              <li>🗄️ PostgreSQL (Database)</li>
            </ul>
          </div>

          {/* Links */}
          <div>
            <h3 className="text-lg font-bold text-white mb-3">Links</h3>
            <div className="space-y-2 text-sm">
              <motion.a
                whileHover={{ x: 5 }}
                href="#"
                className="text-white/60 hover:text-white transition-colors flex items-center gap-2"
              >
                <Github className="w-4 h-4" />
                Repository
              </motion.a>
              <motion.a
                whileHover={{ x: 5 }}
                href="#"
                className="text-white/60 hover:text-white transition-colors block"
              >
                📖 Documentation
              </motion.a>
              <motion.a
                whileHover={{ x: 5 }}
                href="#"
                className="text-white/60 hover:text-white transition-colors block"
              >
                📞 Contact
              </motion.a>
            </div>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-white/10 pt-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm text-white/50">
              © {currentYear} PetZone. Developed with{' '}
              <motion.span
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
                className="inline-block mx-1"
              >
                <Heart className="w-4 h-4 text-red-500 inline" />
              </motion.span>
              for pet lovers.
            </p>
            <p className="text-sm text-white/50">
              Made for <span className="font-semibold text-white">Chuyển Đổi Số</span> Course
            </p>
          </div>
        </div>
        </div>
      </div>
    </motion.footer>
  );
};

export default Footer;
