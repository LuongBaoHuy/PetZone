using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PetZone.Models;

namespace PetZone.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class SensorController : ControllerBase
    {
        private readonly PetZoneDbContext _context;

        public SensorController(PetZoneDbContext context)
        {
            _context = context;
        }

        // 1. API NHẬN DỮ LIỆU TỪ ESP32 (POST: api/sensor)
        [HttpPost]
        public async Task<IActionResult> PostSensorData([FromBody] SensorReading data)
        {
            Console.WriteLine("\n========== ESP32 DATA RECEIVED ==========");
            
            if (data == null)
            {
                Console.WriteLine("[ERROR] Data is NULL!");
                return BadRequest("Dữ liệu trống!");
            }

            // Log chi tiết dữ liệu nhận được
            Console.WriteLine($"[SENSOR] Temperature: {data.Temperature}°C");
            Console.WriteLine($"[SENSOR] Humidity: {data.Humidity}%");
            Console.WriteLine($"[SENSOR] Presence Energy: {data.PresenceEnergy}");
            Console.WriteLine($"[SENSOR] Movement Energy: {data.MovementEnergy}");
            Console.WriteLine($"[SENSOR] Distance: {data.Distance}");

            // Nếu ESP32 không gửi thời gian, server tự điền giờ hiện tại
            if (data.CreatedAt == null || data.CreatedAt == DateTime.MinValue)
            {
                data.CreatedAt = DateTime.UtcNow;
                Console.WriteLine($"[INFO] Auto-set CreatedAt: {data.CreatedAt}");
            }

            try
            {
                _context.SensorReadings.Add(data);
                await _context.SaveChangesAsync();
                Console.WriteLine($"[SUCCESS] Saved to DB with ID: {data.Id}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[ERROR] Database save failed: {ex.Message}");
                return StatusCode(500, "Lỗi lưu database");
            }

            Console.WriteLine("========================================\n");
            return Ok(new { message = "Server đã nhận OK", id = data.Id });
        }

        // 2. API LẤY DỮ LIỆU MỚI NHẤT (GET: api/sensor/latest)
        [HttpGet("latest")]
        public async Task<IActionResult> GetLatestData()
        {
            var latest = await _context.SensorReadings
                                .OrderByDescending(x => x.CreatedAt)
                                .FirstOrDefaultAsync();

            if (latest == null) return NotFound("Chưa có dữ liệu nào");
            return Ok(latest);
        }
    }
}
